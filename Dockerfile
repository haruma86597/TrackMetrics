# Use the Microsoft Dev Container image for Python 3.12
FROM mcr.microsoft.com/devcontainers/python:3.12

# Set environment variables
# Prevents Python from writing .pyc files and keeps stdout/stderr unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install Python dependencies
# 依存関係のインストールを先に定義してビルドキャッシュを有効化
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Use the 'vscode' user provided by the base image
# This ensures consistency with devcontainer features
RUN chown -R vscode:vscode /app
USER vscode

# Default command (adjust main.py to your entry point)
CMD ["python3", "main.py"]
