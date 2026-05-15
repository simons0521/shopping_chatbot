FROM python:3.12-slim

WORKDIR /workspace

# 优化1：先只复制依赖文件（利用 Docker 缓存）
COPY requirements.txt .

# 优化2：先安装依赖（这一层会被缓存，除非 requirements.txt 改变）
RUN pip install --no-cache-dir -r requirements.txt

# 优化3：最后复制代码（代码改动不会导致依赖重装）
COPY . .

# 优化4：设置 Python 路径
ENV PYTHONPATH=/workspace

# 优化5：暴露端口
EXPOSE 8000

# 优化6：运行
ENTRYPOINT ["python", "app/main.py"]