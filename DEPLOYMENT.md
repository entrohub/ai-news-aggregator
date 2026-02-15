# AI 信息聚合器 - 部署信息

## 线上地址
- **网站**: https://ai-news-aggregator-dir2.onrender.com/
- **中文版**: https://ai-news-aggregator-dir2.onrender.com/?lang=zh
- **英文版**: https://ai-news-aggregator-dir2.onrender.com/?lang=en

## GitHub 仓库
- **地址**: https://github.com/entrohub/ai-news-aggregator
- **分支**: main

## 部署平台: Render
- **服务类型**: Web Service
- **运行时**: Python
- **构建命令**: `pip install -r requirements.txt`
- **启动命令**: `gunicorn app:app`
- **自动部署**: 推送到 main 分支后 Render 自动重新部署

## 环境变量 (Render 控制台设置)
| 变量名 | 说明 |
|--------|------|
| `OPENAI_API_KEY` | OpenAI API 密钥，用于 GPT-4o-mini 翻译 |
| `PYTHON_VERSION` | `3.11` (render.yaml 中配置) |

## 技术栈
- **后端**: Flask + Gunicorn
- **数据库**: SQLite (本地文件)
- **翻译**: OpenAI GPT-4o-mini
- **定时任务**: APScheduler (每 2 天自动抓取)
- **前端**: Jinja2 + Bootstrap 5 (CDN)

## 数据源
| 来源 | 类型 | 说明 |
|------|------|------|
| ArXiv CS.AI | RSS | 人工智能论文 |
| MIT Tech Review | RSS | 科技新闻 |
| OpenAI Blog | RSS | OpenAI 官方博客 |
| The Verge AI | RSS | AI 科技报道 |
| HackerNews | API | AI 相关热门帖子 |
| Reddit r/artificial | API | AI 讨论社区 |

## 本地运行
```bash
cd ai-news-aggregator
pip install -r requirements.txt
export OPENAI_API_KEY="你的key"
python app.py
# 访问 http://localhost:5000
```

## 费用估算
- **Render**: 免费 tier
- **OpenAI 翻译**: ~$0.01-0.02 / 次刷新 (200 篇文章), 每 2 天一次, 月费用约 $0.15-0.30
