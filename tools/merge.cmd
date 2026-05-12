@REM 封面第1页插入到最前面 (after 0)
@REM python tools/merge.py thesis.pdf --after 0 cover.pdf:1

@REM 声明插入到封面之后 (after 1)
@REM python tools/merge.py thesis.pdf --after 0 cover.pdf:1 --after 1 declaration.pdf

@REM 授权书插入到第2页后
@REM python tools/merge.py thesis.pdf --after 0 cover.pdf:1 --after 1 declaration.pdf --after 2 authorization.pdf

@REM 正文删掉第3页、第7页
@REM python tools/merge.py thesis.pdf --drop 3,7

@REM 正文只要第10-60页
@REM python tools/merge.py thesis.pdf --body-pages 10-60

@REM 组合使用
@REM python tools/merge.py thesis.pdf \
@REM   --after 0 cover.pdf:1 \
@REM   --after 1 declaration.pdf \
@REM   --after 2 authorization.pdf \
@REM   --drop 1,3 \
@REM   --body-pages 1-80 \
@REM   -o final.pdf
