from sparql import app

# Render / gunicorn 生产环境入口
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
