#!/bin/zsh
# 把待审图片压成适合上传评论和手机查看的小图:JPEG,长边不超过 1600 像素,每张小于 500,000 字节。
# 只读原图,不改动成品。输出文件名带上所在目录,避免 4x3/ 和 16x9/ 里的同名图互相覆盖。
# 用法:make_previews.sh <输出目录> <图片>...
# 输出:每行一张预览图的完整路径。
set -u
LIMIT=500000
[[ $# -ge 2 ]] || { print -u2 "用法:$0 <输出目录> <图片>..."; exit 2; }
out=$1; shift
mkdir -p "$out" || exit 1
rm -f "$out"/*.jpg(N)
for src in "$@"; do
  [[ -s $src ]] || { print -u2 "【预览图失败】找不到图片:$src"; exit 1; }
  dir=${src:h:t}
  if [[ $dir == _work ]]; then dst="$out/${src:t:r}.jpg"; else dst="$out/${dir}-${src:t:r}.jpg"; fi
  ok=0
  long=$(sips -g pixelWidth -g pixelHeight "$src" 2>/dev/null | awk '/pixel/{if($2>m)m=$2}END{print m+0}')
  [[ $long -gt 0 ]] || { print -u2 "【预览图失败】图片打不开:$src"; exit 1; }
  for px in 1600 1280 1024 800; do
    (( px > long )) && px=$long  # 只缩小,不放大
    for q in 82 70 60; do
      sips -s format jpeg -s formatOptions $q -Z $px "$src" --out "$dst" >/dev/null 2>&1
      if [[ -s $dst && $(stat -f %z "$dst") -lt $LIMIT ]]; then ok=1; break 2; fi
    done
  done
  [[ $ok -eq 1 ]] || { print -u2 "【预览图失败】压不到 $LIMIT 字节以下:$src"; exit 1; }
  print "$dst"
done
