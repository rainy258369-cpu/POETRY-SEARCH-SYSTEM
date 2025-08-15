# 古典诗歌知识图谱查询系统

一个基于 Flask 的古典诗词查询网站，支持自然语言提问，结合 SPARQL 知识图谱与 AI（DeepSeek API）进行解析与展示。

[👉 在线演示（Render）](https://poetry-search-system.onrender.com)

---

## 功能特性
- 支持自然语言提问（如“李白的作品有哪些？”、“静夜思的作者是谁？”）
- 基于 SPARQL 查询 `.ttl` 格式古诗词数据
- 返回完整诗文、作者、朝代、译文、赏析等
- 前端古风美化，适配 PC 和移动端
- 可接入 DeepSeek API 补充 AI 分析

---

## 技术栈
- **后端**：Flask, SPARQLWrapper, pandas, rdflib, requests
- **前端**：HTML, CSS, JavaScript
- **部署**：Render（gunicorn + wsgi）

---

## 项目结构
.
├── SPARQL.py # Flask 主程序
├── wsgi.py # WSGI 启动文件
├── requirements.txt # Python 依赖
├── templates/ # HTML 模板
├── static/ # CSS 文件
├── data/ # .ttl 数据文件
└── README.md
