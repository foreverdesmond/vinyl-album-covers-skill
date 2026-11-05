#!/bin/zsh
# 准备交给 GPT 的参考图:最多 5 张,每张都小于 1,000,000 字节,缺图或超限时失败退出。
# 不传样片时用 2 张 B 站构图图;传入样片时用样片替代 B 站构图图。
# 用法:prepare_gpt_inputs.sh <已通过的简笔画封面> <输出目录> [已通过的样片...]
set -u
LIMIT=1000000
RAW=https://raw.githubusercontent.com/foreverdesmond/vinyl-album-covers-skill/main/assets/gpt-inputs
LOCAL=/Users/richy/Projects/CodexImages/vinyl-album-covers-skill/assets/gpt-inputs
HERE=${0:A:h}/../assets/gpt-inputs
MAX_IMAGES=5
FIXED=(02-bilibili-layout-1.jpg 03-bilibili-layout-2.jpg 04-style-eason-wo-bu-hao-ai.jpg 05-channel-logo.png)

[[ $# -ge 2 ]] || { print -u2 "用法:$0 <简笔画封面> <输出目录> [样片...]"; exit 2; }
sketch=$1; out=$2; shift 2
[[ $# -le 2 ]] || { print -u2 "【输入图超限】样片最多 2 张"; exit 1; }
[[ $# -eq 0 ]] || FIXED=(04-style-eason-wo-bu-hao-ai.jpg 05-channel-logo.png)
[[ -s $sketch ]] || { print -u2 "【输入图缺失】简笔画封面:$sketch"; exit 1; }
mkdir -p "$out" || exit 1
rm -f "$out"/*(N)

size() { stat -f %z "$1"; }
readable() { sips -g pixelWidth "$1" 2>/dev/null | grep -q pixelWidth; }

# 压缩到限额内;PNG 保留透明通道,只缩尺寸。
shrink() {
  local src=$1 dst=$2 q px
  if [[ $dst == *.png ]]; then
    cp "$src" "$dst"
    for px in 1024 900 768 640 512; do
      [[ $(size "$dst") -lt $LIMIT ]] && return 0
      sips -Z $px "$src" --out "$dst" >/dev/null 2>&1
    done
  else
    if [[ $src == *.jpg && $(size "$src") -lt $LIMIT ]]; then cp "$src" "$dst"; return 0; fi
    for px in 2048 1600 1280 1024; do
      for q in 90 80 70 60; do
        sips -s format jpeg -s formatOptions $q -Z $px "$src" --out "$dst" >/dev/null 2>&1
        [[ -s $dst && $(size "$dst") -lt $LIMIT ]] && return 0
      done
    done
  fi
  [[ -s $dst && $(size "$dst") -lt $LIMIT ]]
}

fetch_fixed() {
  local name=$1 dst=$2 dir
  for dir in "$HERE" "$LOCAL"; do
    [[ -s $dir/$name ]] && { cp "$dir/$name" "$dst"; return 0; }
  done
  curl -fsSL --max-time 60 "$RAW/$name" -o "$dst"
}

shrink "$sketch" "$out/01-album-sketch.jpg" || { print -u2 "【输入图超限】简笔画封面"; exit 1; }
for name in $FIXED; do
  tmp=$out/.tmp-$name
  fetch_fixed "$name" "$tmp" || { print -u2 "【输入图缺失】$name"; exit 1; }
  shrink "$tmp" "$out/$name" || { print -u2 "【输入图超限】$name"; exit 1; }
  rm -f "$tmp"
done
n=6
for s in "$@"; do
  [[ -s $s ]] || { print -u2 "【输入图缺失】样片:$s"; exit 1; }
  shrink "$s" "$out/0$n-approved-sample-$((n-5)).jpg" || { print -u2 "【输入图超限】样片:$s"; exit 1; }
  n=$((n+1))
done

count=$(print -l "$out"/*.(jpg|png) | wc -l | tr -d " ")
[[ $count -le $MAX_IMAGES ]] || { print -u2 "【输入图超限】共 $count 张,最多 $MAX_IMAGES 张"; exit 1; }

{
  print '['
  first=1
  for f in "$out"/*.(jpg|png); do
    readable "$f" || { print -u2 "【输入图损坏】$f"; exit 1; }
    b=$(size "$f")
    [[ $b -lt $LIMIT ]] || { print -u2 "【输入图超限】$f"; exit 1; }
    [[ $first -eq 1 ]] || print ','
    first=0
    print -n "  {\"path\": \"$f\", \"bytes\": $b}"
  done
  print '\n]'
} > "$out/manifest.json" || exit 1
print "参考图已就绪:$out"
cat "$out/manifest.json"
