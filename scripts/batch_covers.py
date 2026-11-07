#!/usr/bin/env python3
"""full 阶段批量出图:逐张生图、检查比例和文字,通过后才放进成品目录。

用法:batch_covers.py <专辑目录> [--max-seconds 420] [--redo 03 --redo 05-4x3 --note 意见] [--retry-failed]

输入:_work/tracklist.json、_work/batch-config.json、_work/album-cover-sketch.png、已通过的样片。
退出码:0 全部完成  2 输入错误  3 时间到,再运行一次继续  4 额度耗尽  5 有图未通过,见 _work/batch-status.json
"""
import argparse
import fcntl
import json
import os
import re
import shutil
import subprocess
import sys
import time
import unicodedata

DONE, MORE, BAD_INPUT, QUOTA, FAILED = 0, 3, 2, 4, 5
MAGPIE = os.environ.get("VINYL_MAGPIE", "/Applications/magpie.app/Contents/MacOS/magpie")
LOCAL_SKILL = "/Users/richy/Projects/CodexImages/vinyl-album-covers-skill"
IMAGE_MODEL = "codex/gpt-image-2"
RATIOS = {"4x3": ("4:3", 4 / 3), "16x9": ("16:9", 16 / 9)}
RATIO_TOLERANCE = 0.005
MAX_TRIES = 3  # 首次 + 重出 2 次
SECONDS_PER_IMAGE = 80
QUOTA_ERROR = re.compile(r"\b429\b|usage limit|rate.?limit|quota|resource.?exhausted", re.I)
ILLEGAL_NAME = re.compile(r'[/\\:*?"<>|]')
CHECK_PROMPT = (
    '只按图上实际看到的内容回答,输出 JSON,不要解释:{"texts":["逐条列出图上所有可读文字,保持原样"]}'
)


class QuotaExhausted(Exception):
    pass


class InputError(Exception):
    pass


def skill_file(*parts):
    here = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), *parts)
    return here if os.path.exists(here) else os.path.join(LOCAL_SKILL, *parts)


def read_json(path, default=None):
    if not os.path.exists(path):
        if default is not None:
            return default
        raise InputError(f"缺少文件:{path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def normalized(text):
    text = unicodedata.normalize("NFKC", text).casefold()
    return "".join(c for c in text if c.isalnum())


def load_templates():
    with open(skill_file("references", "prompts.md"), encoding="utf-8") as f:
        doc = f.read()
    blocks = re.findall(r"```text\n(.*?)```", doc, re.S)
    layouts = dict(re.findall(r"^\| ([A-D]) \| (.+?) \|$", doc, re.M))
    if len(blocks) < 3 or len(layouts) != 4:
        raise InputError("references/prompts.md 的结构不对,找不到封面提示词或版式表")
    return blocks[1], blocks[2], layouts


def build_prompt(templates, config, title, layout, ratio, note):
    cover, first_point, layouts = templates
    singer = (config.get("singer") or "").strip()
    first_point = first_point.replace("{版式 A、B、C 或 D 的说明}", layouts[layout]).strip()
    prompt = re.sub(r"第一,.*?\n\n", lambda _: first_point + "\n\n", cover, count=1, flags=re.S)
    if singer:
        prompt = prompt.replace("{歌手名}", singer)
    else:
        prompt = prompt.replace("歌手名:{歌手名}\n", "").replace(",歌手名再次之", "")
        prompt = prompt.replace(
            "歌曲名次之。", "歌曲名次之。画面上不要出现歌手名、主创姓名或‘无歌手’这类文字。"
        )
    prompt = prompt.replace("{歌曲名}", title)
    prompt = prompt.replace("{封面可包含的元素}", config["elements"])
    prompt = prompt.replace("{4:3 或 16:9}", ratio)
    prompt = prompt.replace("{退回重做时追加:审核意见:...}", f"审核意见:{note}" if note else "")
    if re.search(r"\{[^}]*\}", prompt):
        raise InputError(f"提示词还有未填写的内容:{prompt}")
    return prompt.strip() + "\n"


def plan_items(album, tracklist, config):
    """按实际出图的曲目连续编号,样片之外的曲目轮换 A、B、C、D。"""
    tracks = [t for t in tracklist["tracks"] if not t.get("excluded")]
    sample = int(config.get("sample_track") or 1)
    order = "ABCD"
    start = order.find(config.get("sample_layout") or "D") + 1
    items, turn = [], 0
    for number, track in enumerate(tracks, 1):
        if number == sample:
            continue
        layout = order[(start + turn) % 4]
        turn += 1
        name = ILLEGAL_NAME.sub("-", track["title"]).strip()
        for folder in RATIOS:
            items.append(
                {
                    "key": f"{number:02d}-{folder}",
                    "number": f"{number:02d}",
                    "title": track["title"],
                    "layout": layout,
                    "folder": folder,
                    "target": os.path.join(album, folder, f"{number:02d}-{name}.png"),
                }
            )
    return items, f"{sample:02d}"


def find_sample(album, sample, folder):
    directory = os.path.join(album, folder)
    names = sorted(os.listdir(directory)) if os.path.isdir(directory) else []
    for name in names:
        if name.startswith(sample + "-") and name.endswith(".png"):
            return os.path.join(directory, name)
    raise InputError(f"缺少样片:{folder}/{sample}-*.png")


def prepare_references(album, sample):
    work = os.path.join(album, "_work")
    inputs = os.path.join(work, "gpt-inputs")
    result = subprocess.run(
        [
            "zsh",
            skill_file("scripts", "prepare_gpt_inputs.sh"),
            os.path.join(work, "album-cover-sketch.png"),
            inputs,
            find_sample(album, sample, "16x9"),
            find_sample(album, sample, "4x3"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise InputError(result.stderr.strip() or "参考图准备失败")
    return [entry["path"] for entry in read_json(os.path.join(inputs, "manifest.json"))]


def run_magpie(args, timeout=280):
    try:
        result = subprocess.run([MAGPIE, *args], capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 1, "命令超时"
    return result.returncode, result.stdout + result.stderr


def generate(prompt, references, ratio, path):
    args = ["tool", "generate_image", "--prompt", prompt, "--size", ratio, "--model", IMAGE_MODEL]
    for reference in references:
        args += ["--reference_images", reference]
    last_error = ""
    for _ in range(2):  # 网络抖动或超时重试 1 次
        if os.path.exists(path):
            os.remove(path)
        code, output = run_magpie(args + ["-o", path])
        if code == 0 and os.path.exists(path) and os.path.getsize(path) > 0:
            return None
        if QUOTA_ERROR.search(output):
            raise QuotaExhausted(output.strip()[:300])
        last_error = output.strip()[:300]
    return last_error or "没有生成图片"


def ratio_problem(path, folder):
    result = subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", path], capture_output=True, text=True
    )
    sizes = re.findall(r"pixel(?:Width|Height): (\d+)", result.stdout)
    if len(sizes) != 2:
        return "图片打不开"
    width, height = int(sizes[0]), int(sizes[1])
    target = RATIOS[folder][1]
    if abs(width / height / target - 1) > RATIO_TOLERANCE:
        return f"比例不对:{width}×{height}"
    return None


def read_texts(path):
    last_error = ""
    for _ in range(2):
        code, output = run_magpie(["tool", "analyze_image", path, "--prompt", CHECK_PROMPT], 120)
        match = re.search(r"\{.*\}", output, re.S)
        if code == 0 and match:
            try:
                return [str(t) for t in json.loads(match.group(0))["texts"]]
            except (ValueError, KeyError, TypeError):
                last_error = "看图结果不是 JSON"
                continue
        if QUOTA_ERROR.search(output):
            raise QuotaExhausted(output.strip()[:300])
        last_error = output.strip()[:300]
    raise RuntimeError(last_error or "看图失败")


def text_problems(texts, title, config):
    """返回 (必须重出的问题, 交给人工看的多余文字)。"""
    seen = normalized("".join(texts))
    singer = (config.get("singer") or "").strip()
    required = ["黑胶试听", title] + ([singer] if singer else [])
    problems = [f"缺少文字:{t}" for t in required if normalized(t) not in seen]
    forbidden = ["无歌手"] + list(config.get("forbidden_texts") or [])
    problems += [f"出现禁止文字:{t}" for t in forbidden if normalized(t) in seen]
    allowed = required + list(config.get("allowed_texts") or []) + [
        "Vinyl Record Music Collection",
        "Vinyl Record",
        "Music",
        "Collection",
    ]
    allowed = [normalized(t) for t in allowed]
    extras = [t for t in texts if normalized(t) and not any(normalized(t) in a or a in normalized(t) for a in allowed)]
    return problems, extras


def make_one(item, config, templates, references, status, work):
    entry = status["items"].setdefault(item["key"], {"status": "pending", "tries": 0})
    tmp = os.path.join(work, "batch-tmp", item["key"] + ".png")
    ratio = RATIOS[item["folder"]][0]
    prompt = build_prompt(templates, config, item["title"], item["layout"], ratio, entry.get("note"))
    problems = []
    while entry["tries"] < MAX_TRIES:
        if not os.path.exists(tmp):  # 额度中断时图可能已出好,接续时不重出
            entry["tries"] += 1
            error = generate(prompt, references, ratio, tmp)
            if error:
                problems = [f"生图失败:{error}"]
                continue
        problems = [p for p in [ratio_problem(tmp, item["folder"])] if p]
        extras = []
        if not problems:
            try:
                texts = read_texts(tmp)
            except RuntimeError as error:
                problems = [f"看图失败:{error}"]
                break
            problems, extras = text_problems(texts, item["title"], config)
            entry["texts"] = texts
        if not problems:
            os.makedirs(os.path.dirname(item["target"]), exist_ok=True)
            os.replace(tmp, item["target"])
            entry.update(status="ok", problems=[], extras=extras)
            return
        if entry["tries"] < MAX_TRIES:
            os.remove(tmp)
    if os.path.exists(tmp):  # 留给人工判断,文字检查也可能读错
        failed_dir = os.path.join(work, "batch-failed")
        os.makedirs(failed_dir, exist_ok=True)
        os.replace(tmp, os.path.join(failed_dir, item["key"] + ".png"))
    entry.update(status="failed", problems=problems)


def finish(album, config, tracklist, sample):
    work = os.path.join(album, "_work")
    count = len([t for t in tracklist["tracks"] if not t.get("excluded")])
    for folder in RATIOS:
        found = [n for n in os.listdir(os.path.join(album, folder)) if n.endswith(".png")]
        if len(found) != count:
            raise InputError(f"{folder}/ 有 {len(found)} 张图,应为 {count} 张")
    sheet = ["zsh", skill_file("scripts", "make_review_sheet.sh"), album, os.path.join(work, "review-sheet.jpg")]
    if not config.get("skip_sample") and count > 1:  # 只有一首时总览图就是样片
        sheet.append(sample)
    subprocess.run(sheet, check=True, capture_output=True)
    name = os.path.basename(os.path.normpath(album)) + "-封面合集.zip"
    archive = os.path.join(album, name)
    if os.path.exists(archive):
        os.remove(archive)
    subprocess.run(["zip", "-qr", archive, "4x3", "16x9", "-i", "*.png"], cwd=album, check=True)
    return archive


def progress(items, status):
    states = [status["items"].get(i["key"], {}).get("status", "pending") for i in items]
    entries = status["items"].items()
    return {
        "total": len(items),
        "ok": states.count("ok"),
        "pending": states.count("pending"),
        "failed": {k: v["problems"] for k, v in entries if v["status"] == "failed"},
        "extras": {k: v["extras"] for k, v in entries if v.get("extras")},
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("album")
    parser.add_argument("--max-seconds", type=int, default=420)
    parser.add_argument("--redo", action="append", default=[], help="如 03 或 03-4x3")
    parser.add_argument("--note", default="", help="退回意见,写进重出图片的提示词")
    parser.add_argument("--retry-failed", action="store_true")
    options = parser.parse_args()

    album = os.path.abspath(options.album)
    work = os.path.join(album, "_work")
    report = {"album": album}
    code = DONE
    lock = None
    try:
        lock = open(os.path.join(work, ".batch.lock"), "w")
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise InputError("这张专辑已有一个批量任务在运行")

        tracklist = read_json(os.path.join(work, "tracklist.json"))
        config = read_json(os.path.join(work, "batch-config.json"))
        if not (config.get("elements") or "").strip():
            raise InputError("batch-config.json 缺少 elements")
        status_path = os.path.join(work, "batch-status.json")
        status = read_json(status_path, {"items": {}})
        items, sample = plan_items(album, tracklist, config)
        known = {item["key"] for item in items}
        for wanted in options.redo:
            keys = [k for k in known if k == wanted or k.startswith(wanted + "-")]
            if not keys:
                raise InputError(f"--redo 找不到:{wanted}")
            for key in keys:
                status["items"][key] = {"status": "pending", "tries": 0, "note": options.note}
        if options.retry_failed:
            for entry in status["items"].values():
                if entry["status"] == "failed":
                    entry.update(status="pending", tries=0)
        for item in items:  # 目录里已有的图算完成,不重出
            entry = status["items"].get(item["key"])
            if entry is None and os.path.exists(item["target"]):
                status["items"][item["key"]] = {"status": "ok", "tries": 0, "extras": []}

        todo = [i for i in items if status["items"].get(i["key"], {}).get("status", "pending") == "pending"]
        os.makedirs(os.path.join(work, "batch-tmp"), exist_ok=True)
        started = time.time()
        if todo:
            templates = load_templates()
            references = prepare_references(album, sample)
            if len(references) != 5:
                raise InputError(f"参考图应为 5 张,实际 {len(references)} 张")
            for item in todo:
                if time.time() - started + SECONDS_PER_IMAGE > options.max_seconds:
                    code = MORE
                    break
                try:
                    make_one(item, config, templates, references, status, work)
                finally:
                    write_json(status_path, status)

        report.update(progress(items, status))
        if code == DONE and report["failed"]:
            code = FAILED
        if code == DONE:
            report["zip"] = finish(album, config, tracklist, sample)
            report["review_sheet"] = os.path.join(work, "review-sheet.jpg")
            shutil.rmtree(os.path.join(work, "batch-tmp"), ignore_errors=True)
    except QuotaExhausted as error:
        code = QUOTA
        report.update(progress(items, status), error=str(error))
    except (InputError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        code = BAD_INPUT
        report["error"] = str(error)
    finally:
        if lock:
            lock.close()
    report["exit_code"] = code
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
