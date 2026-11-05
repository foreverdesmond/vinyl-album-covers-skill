#!/bin/zsh
# 把待审核封面合成一张总览图,文件小于 1,000,000 字节。
# 用法:make_review_sheet.sh <专辑目录> <输出.jpg> [跳过的序号,如 01]
set -u
[[ $# -ge 2 ]] || { print -u2 "用法:$0 <专辑目录> <输出.jpg> [跳过的序号]"; exit 2; }
album=$1; out=$2; skip=${3:-}
FF=$(command -v ffmpeg || print /opt/homebrew/bin/ffmpeg)
[[ -x $FF ]] || { print -u2 "找不到 ffmpeg"; exit 1; }
tmp=$(mktemp -d) || exit 1
trap 'rm -rf "$tmp"' EXIT
i=0
for f in "$album"/16x9/*.png(N) "$album"/4x3/*.png(N); do
  [[ -n $skip && ${f:t} == ${skip}-* ]] && continue
  i=$((i+1)); ln -s "$f" "$tmp/$(printf %04d $i).png"
done
[[ $i -gt 0 ]] || { print -u2 "没有找到待审核图片"; exit 1; }
cols=6; (( i < cols )) && cols=$i
rows=$(( (i + cols - 1) / cols ))
mkdir -p "${out:h}"
for q in 3 5 8 12 18; do
  "$FF" -loglevel error -y -framerate 1 -i "$tmp/%04d.png" \
    -vf "scale=480:360:force_original_aspect_ratio=decrease,pad=480:360:(ow-iw)/2:(oh-ih)/2:color=black,tile=${cols}x${rows}:padding=6:color=white" \
    -frames:v 1 -q:v $q "$out" || exit 1
  [[ $(stat -f %z "$out") -lt 1000000 ]] && { print "总览图已生成:$out($i 张)"; exit 0; }
done
print -u2 "总览图超过 1,000,000 字节:$out"; exit 1
