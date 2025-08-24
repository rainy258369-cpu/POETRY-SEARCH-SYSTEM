# 古典诗歌知识图谱查询系统

一个基于知识图谱和SPARQL查询的古典诗歌智能问答系统，能够回答关于古诗词、作者、朝代和相关内容的自然语言问题。

[👉 在线演示（Render）](https://poetry-search-system.onrender.com)

---

## 功能特性
- 🔍 **智能问答**：支持自然语言查询，如"李白的作品有哪些？"、"静夜思的作者是谁？"
- 📚 **多维度查询**：可查询诗歌、作者、朝代、内容、译文和赏析等信息
- 🎨 **优雅界面**：采用中国传统美学设计的响应式Web界面
- 🤖 **AI增强**：集成DeepSeek AI提供智能分析和补充回答
- 📊 **知识图谱**：基于RDF知识图谱，包含丰富的诗歌语义关系
---

## 技术栈
### 后端
- Flask - Python Web框架
- RDFLib - RDF知识图谱处理
- SPARQL - 语义查询语言
- DeepSeek API - AI智能问答

### 前端
- HTML5/CSS3 - 页面结构和样式
- JavaScript - 交互逻辑
- 响应式设计 - 移动端适配

### 数据
- TTL格式知识图谱
- 结构化诗歌数据（标题、作者、朝代、内容、译文、赏析）

---

## 项目结构
.
├── SPARQL.py # Flask 主程序
├── wsgi.py # WSGI 启动文件
├── requirements.txt # Python 依赖
├── templates/         # HTML模板
│   ├── index.html
│   └── result.html
├── static/           # 静态资源
│   ├── style.css
│   └── result.css
├── data/              # 知识图谱数据文件
│   ├── out_poem_decoded.ttl
│   └── ctext.ttl
├── .env              # 环境配置
└── README.md

---

##查询示例
查询示例
"李白的作品有哪些？"
"静夜思的作者是谁？"
"春晓的内容是什么？"
"苏轼是哪个朝代的？"
"登鹳雀楼的赏析"
"唐代的诗歌有哪些？"
