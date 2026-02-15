# AI News Aggregator

## 项目概述
Python Flask Web 应用，聚合多个数据源的 AI 相关新闻，支持中英文双语。

## 项目结构
```
app.py              # Flask 主应用 + 路由 + 定时任务
fetcher.py          # 数据抓取 (RSS + HackerNews API + Reddit API)
database.py         # SQLite 数据库操作
translator.py       # OpenAI GPT-4o-mini 翻译
templates/index.html # Web 界面 (Jinja2 + Bootstrap 5)
requirements.txt    # 依赖: flask, feedparser, requests, gunicorn, openai, apscheduler
render.yaml         # Render 部署配置
DEPLOYMENT.md       # 部署详细文档
```

## 部署信息
- **线上地址**: https://ai-news-aggregator-dir2.onrender.com/
- **GitHub**: https://github.com/entrohub/ai-news-aggregator
- **平台**: Render (免费 tier), 推送 main 分支自动部署
- **启动命令**: `gunicorn app:app`

## 环境变量
- `OPENAI_API_KEY` — OpenAI API 密钥，用于 GPT-4o-mini 翻译文章标题和摘要

## 关键设计决策
- 翻译在抓取时执行，结果存入 `title_zh` / `summary_zh` 字段，不在页面加载时翻译
- APScheduler 每 2 天自动执行 `fetch_all()`
- 刷新请求在后台线程运行，避免 HTTP 请求超时
- 无 API key 时翻译静默跳过，不会崩溃

## 数据源
RSS: ArXiv CS.AI, MIT Tech Review, OpenAI Blog, The Verge AI
API: HackerNews (按 AI 关键词过滤), Reddit r/artificial

## 本地开发
```bash
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."
python app.py
# http://localhost:5000
```
