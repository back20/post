import requests
import os

def punch_in(session3rd):
    url = "https://api.planet.shenxu.net.cn/planet/api/client/punch/dates"
    headers = {
        "Host": "api.planet.shenxu.net.cn",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_8_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0 (Immersed/20) uni-app",
        "sign": "7a796d6acf30993cadd4c0ebb7c117be",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9"
    }
    
    data = f"""scene=0&version=1.2.3&session3rd={session3rd}"""
    
    try:
        res = requests.post(url, headers=headers, data=data)
        print(f"Session3rd: {session3rd[:10]}... 签到结果: {res.text}")
        return True
    except Exception as e:
        print(f"Session3rd: {session3rd[:10]}... 签到失败: {str(e)}")
        return False

if __name__ == "__main__":
    # 从环境变量获取多个session3rd，用逗号分隔
    sessions = os.getenv("SESSION3RDS", "").split(",")
    
    if not sessions or sessions == [""]:
        print("未配置任何session3rd，请检查环境变量")
        exit(1)
    
    print(f"开始签到，共{len(sessions)}个账号")
    for session in sessions:
        if session.strip():  # 跳过空字符串
            punch_in(session.strip())
    
    print("所有账号签到完成")
