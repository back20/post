import requests
import json
import os
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def get_env_variable(var_name):
    """安全获取环境变量"""
    value = os.getenv(var_name)
    if not value:
        logger.error(f"环境变量 {var_name} 未设置")
        raise EnvironmentError(f"环境变量 {var_name} 未设置")
    return value

def build_request_data(session3rd):
    """构建请求数据"""
    return {
        "scene": "0",
        "version": "1.1.11",
        "session3rd": session3rd,
        "adUnitId": "adunit-d744d39589885989",
        "type": "100"
    }

def build_headers():
    """构建请求头"""
    return {
        "sign": "b73548fc0fa46d64a9e5810bcdadcf5f",
        "user-agent": "Mozilla/5.0 (Linux; Android 14; M2102K1C Build/UKQ1.240624.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.168 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/39.142857)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "api.planet.shenxu.net.cn",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }

def send_post_request(url, headers, data):
    """发送POST请求并返回响应"""
    try:
        logger.info(f"发送POST请求到: {url}")
        logger.debug(f"请求头: {headers}")
        logger.debug(f"请求数据: {data}")
        
        response = requests.post(
            url,
            headers=headers,
            data=data,
            timeout=10  # 设置超时时间
        )
        
        # 检查HTTP状态码
        response.raise_for_status()
        logger.info(f"请求成功，状态码: {response.status_code}")
        
        return response
    
    except requests.exceptions.Timeout:
        logger.error("请求超时")
        raise
    except requests.exceptions.ConnectionError:
        logger.error("连接错误")
        raise
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP错误: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"请求发生未知错误: {str(e)}")
        raise

def main():
    try:
        logger.info("开始执行POST请求任务")
        
        # 配置参数
        api_url = "https://api.planet.shenxu.net.cn/planet/api/client/reward/done"
        
        # 获取环境变量
        session3rd = get_env_variable('AZID')
        
        # 构建请求
        headers = build_headers()
        data = build_request_data(session3rd)
        
        # 发送请求
        response = send_post_request(api_url, headers, data)
        
        # 解析响应
        try:
            response_data = response.json()
            logger.info(f"响应message: {response_data.get('message', '未找到message字段')}")
            logger.debug(f"完整响应: {json.dumps(response_data, indent=2)}")
        except json.JSONDecodeError:
            logger.error(f"响应不是有效的JSON格式: {response.text}")
        
        logger.info("POST请求任务执行完成")
        
    except Exception as e:
        logger.error(f"任务执行失败: {str(e)}", exc_info=True)
        # 非零退出码表示失败
        exit(1)

if __name__ == "__main__":
    main()
    
