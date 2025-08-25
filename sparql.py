from flask import Flask, request, render_template, jsonify
from rdflib import Graph
from pathlib import Path
import pandas as pd
import re
import requests
import json

app = Flask(__name__)

# 1. 加载 TTL 数据文件

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

g = Graph()
g.parse(DATA_DIR / "out_poem_decoded.ttl", format="turtle")
print(f"知识图谱已加载，共 {len(g)} 条三元组")

import os

DEEPSEEK_API_URL = os.environ.get("DEEPSEEK_API_URL", "")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")


class SPARQLPoetryProcessor:
    def __init__(self):
        self.graph = g
        self.PATTERNS = {
            "poems_by_author": r"(.+)的(诗|作品|诗歌|词|文章|著作)",
            "author_by_poem": r"(.*)的作者(是谁|是)?",
            "dynasty_by_poem": r"(.*)是.*朝代(的|所作的)?",
            "content_by_poem": r"(.*)的内容",
            "translation_by_poem": r"(.*)的翻译",
            "appreciation_by_poem": r"(.*)的赏析",
            "poems_by_dynasty": r"(.*)朝代的(诗|作品|诗歌|词)"
        }

    def execute_query(self, query):
        """在内存图谱上执行 SPARQL 查询"""
        try:
            results = self.graph.query(query)
            bindings = []
            for row in results:
                binding = {}
                for var, val in row.asdict().items():
                    binding[var] = {'value': str(val)}
                bindings.append(binding)
            return {"results": {"bindings": bindings}}
        except Exception as e:
            print(f"查询失败: {e}")
            return None

    def process_results(self, results):
        """把查询结果转成 DataFrame"""
        if not results or 'results' not in results or 'bindings' not in results['results']:
            return pd.DataFrame()
        rows = []
        for binding in results['results']['bindings']:
            row = {var: binding[var]['value'] for var in binding}
            rows.append(row)
        return pd.DataFrame(rows)

    def get_full_poem_info(self, poem_title):
        """获取完整诗词信息"""
        query = f"""
        PREFIX : <http://www.semanticweb.org/ontologies/poetry#>
        SELECT ?title ?author ?dynasty ?content ?translation ?appreciation
        WHERE {{
            ?poem a :Poem ;
                  :title "{poem_title}" ;
                  :author ?author ;
                  :dynasty ?dynasty ;
                  :content ?content .
            OPTIONAL {{ ?poem :translation ?translation }}
            OPTIONAL {{ ?poem :appreciation ?appreciation }}
            BIND("{poem_title}" AS ?title)
        }}
        """
        results = self.execute_query(query)
        df = self.process_results(results)
        return df

    def search(self, question):
        """根据问题选择查询策略"""
        for key, pattern in self.PATTERNS.items():
            match = re.search(pattern, question)
            if match:
                if key == "poems_by_author":
                    author = match.group(1)
                    query = f"""
                    PREFIX : <http://www.semanticweb.org/ontologies/poetry#>
                    SELECT ?title
                    WHERE {{
                        ?poem a :Poem ;
                              :author "{author}" ;
                              :title ?title .
                    }}
                    """
                    return self.process_results(self.execute_query(query))

                elif key == "author_by_poem":
                    title = match.group(1)
                    query = f"""
                    PREFIX : <http://www.semanticweb.org/ontologies/poetry#>
                    SELECT ?author
                    WHERE {{
                        ?poem a :Poem ;
                              :title "{title}" ;
                              :author ?author .
                    }}
                    """
                    return self.process_results(self.execute_query(query))

                elif key == "dynasty_by_poem":
                    title = match.group(1)
                    query = f"""
                    PREFIX : <http://www.semanticweb.org/ontologies/poetry#>
                    SELECT ?dynasty
                    WHERE {{
                        ?poem a :Poem ;
                              :title "{title}" ;
                              :dynasty ?dynasty .
                    }}
                    """
                    return self.process_results(self.execute_query(query))

                elif key == "content_by_poem":
                    title = match.group(1)
                    query = f"""
                    PREFIX : <http://www.semanticweb.org/ontologies/poetry#>
                    SELECT ?content
                    WHERE {{
                        ?poem a :Poem ;
                              :title "{title}" ;
                              :content ?content .
                    }}
                    """
                    return self.process_results(self.execute_query(query))

                elif key == "translation_by_poem":
                    title = match.group(1)
                    query = f"""
                    PREFIX : <http://www.semanticweb.org/ontologies/poetry#>
                    SELECT ?translation
                    WHERE {{
                        ?poem a :Poem ;
                              :title "{title}" ;
                              :translation ?translation .
                    }}
                    """
                    return self.process_results(self.execute_query(query))

                elif key == "appreciation_by_poem":
                    title = match.group(1)
                    query = f"""
                    PREFIX : <http://www.semanticweb.org/ontologies/poetry#>
                    SELECT ?appreciation
                    WHERE {{
                        ?poem a :Poem ;
                              :title "{title}" ;
                              :appreciation ?appreciation .
                    }}
                    """
                    return self.process_results(self.execute_query(query))

                elif key == "poems_by_dynasty":
                    dynasty = match.group(1)
                    query = f"""
                    PREFIX : <http://www.semanticweb.org/ontologies/poetry#>
                    SELECT ?title
                    WHERE {{
                        ?poem a :Poem ;
                              :dynasty "{dynasty}" ;
                              :title ?title .
                    }}
                    """
                    return self.process_results(self.execute_query(query))
        return pd.DataFrame()


processor = SPARQLPoetryProcessor()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"error": "请输入查询内容"})
    df = processor.search(query)
    return render_template("result.html", query=query, results=df.to_dict(orient="records"))

@app.route("/result", methods=["GET"])
def result():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"error": "请输入查询内容"})
    df = processor.search(query)
    return render_template("result.html", query=query, results=df.to_dict(orient="records"))

@app.route("/query", methods=["GET"])
def query_api():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"error": "请输入查询内容"})
    df = processor.search(query)
    return jsonify({
        "result": df.to_dict(orient="records"),
        "status": "ok"
    })


if __name__ == "__main__":
    app.run(debug=True)
