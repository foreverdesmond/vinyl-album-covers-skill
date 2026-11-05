#!/bin/zsh
# 准备交给 GPT 的参考图:每张都小于 1,000,000 字节,缺图或超限时失败退出。
# 用法:prepare_gpt_inputs.sh <已通过的简笔画封面> <输出目录> [已通过的样片...]
set -u
LIMIT=1000000
RAW=https://raw.githubusercontent.com/foreverdesmond/vinyl-album-covers-skill/main/assets/gpt-inputs
LOCAL=/Users/richy/Projects/CodexImages/vinyl-album-covers-skill/assets/gpt-inputs
HERE=${0:A:h}/../assets/gpt-inputs
FIXED=(02-bilibili-layout-1.jpg 03-bilibili-layout-2.jpg 04-bilibili-layout-3.jpg 05-style-eason-wo-bu-hao-ai.jpg 06-channel-logo.png)

[[ $# -ge 2 ]] || { print -u2 "用法:$0 <简笔画封面> <输出目录> [样片...]"; exit 2; }
sketch=$1; out=$2; shift 2
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
n=7
for s in "$@"; do
  [[ -s $s ]] || { print -u2 "【输入图缺失】样片:$s"; exit 1; }
  shrink "$s" "$out/0$n-approved-sample-$((n-6)).jpg" || { print -u2 "【输入图超限】样片:$s"; exit 1; }
  n=$((n+1))
done

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
