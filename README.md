# NGA 自动搬饼机器人

设计旨在通过 github 的 action 功能，实现定时拉取 bilibili 特定帐号动态、处理格式后作为帖子转发到 NGA。

## 通过 github action 部署

1. fork 本仓库
2. 在 src/data.json 中填入所需的信息（例如，对应平台的 cookie、需要转到的板块 id。）
3. 调整 .github/workflows/python-app.yml 中的 schedule

## 本地部署

运行 run.sh 即可。

或者安装 requirements.txt，然后运行 run.py。