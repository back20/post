name: 定时执行POST请求

on:
  workflow_dispatch:
  schedule:
    - cron: '*/5 * * * *'

permissions:
  contents: read

jobs:
  post-request:
    runs-on: ubuntu-latest
    name: 发送POST请求
    timeout-minutes: 5
    
    steps:
      - name: 检出代码
        uses: actions/checkout@v4
        with:
          fetch-depth: 1
      
      - name: 设置Python环境
        uses: actions/setup-python@v5
        with:
          python-version: '3.9'
          # 移除了cache配置，避免查找requirements.txt
      
      - name: 安装依赖
        run: |
          python -m pip install --upgrade pip
          pip install requests
        id: install-deps
      
      - name: 运行POST请求脚本
        env:
          AZID: ${{ secrets.AZID }}
          PYTHONUNBUFFERED: 1
        run: |
          echo "开始执行POST请求脚本..."
          python post_request.py
        id: run-script
      
      - name: 任务执行结果
        if: always()
        run: |
          if [ "${{ steps.run-script.outcome }}" = "success" ]; then
            echo "任务执行成功"
          else
            echo "任务执行失败"
            exit 1
          fi
    
