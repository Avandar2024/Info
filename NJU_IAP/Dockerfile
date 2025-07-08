# 使用官方 Python 镜像作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /flask_app
COPY . /flask_app

RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码到工作目录
WORKDIR /flask_app/backend

# Gunicorn 的配置 (可以根据需要调整 worker 数量等)
# 假设你的 Flask app 实例在 app/main.py 中，变量名为 app
CMD ["python","run.py"]
# CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app:app_instance"]
