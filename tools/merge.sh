# 封面第1页插入到最前面 (after 0)
python tools/merge.py thesis.pdf --after 0 cover.pdf:1

# 声明插入到封面之后 (after 1)
python tools/merge.py thesis.pdf --after 0 cover.pdf:1 --after 1 declaration.pdf

# 授权书插入到第2页后
python tools/merge.py thesis.pdf --after 0 cover.pdf:1 --after 1 declaration.pdf --after 2 authorization.pdf

# 正文删掉第3页、第7页
python tools/merge.py thesis.pdf --drop 3,7

# 正文只要第10-60页
python tools/merge.py thesis.pdf --body-pages 10-60

# 组合使用
python tools/merge.py thesis.pdf \
  --after 0 cover.pdf:1 \
  --after 1 declaration.pdf \
  --after 2 authorization.pdf \
  --drop 1,3 \
  --body-pages 1-80 \
  -o final.pdf
