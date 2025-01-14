import re #正则表达式
import os #操作系统
import json #json格式
import requests #http请求
import pandas as pd
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed  # For multithreading


# API URL 获取代理 IP 列表
api_url = "http://api.tianqiip.com/getip?secret=6x9exujeu7dsvzhj&num=200&type=txt&port=1&time=3&mr=1&sign=d65b096e60c7812d5ba71ceaf13afbdb"
# secret 秘钥 secret：密钥，用于身份验证/num=500：请求 500 个代理 IP/type=json：期望的返回格式为 JSON/port=1：指定要获取的端口类型/mr=1：可能是其他定制参数。/sign：签名，用于安全验证。
# 获取代理 IP 列表
def get_proxy_list(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and len(data['data']) > 0: #检查解析后的json数据中是否有‘data'这个量
                for item in data['data']:
                    proxy_http = f"http://{item['ip']}:{item['port']}"
                    proxy_https = f"http://{item['ip']}:{item['port']}"
                    proxy_list.append({'http': proxy_http, 'http': proxy_https}) #将每个代理 IP 和端口组合成 http://ip:port 的格式
                
                print("Fetched proxies:", proxy_list)  # 打印获取到的所有代理
                return proxy_list
            else:
                print("No proxies available from the API")
                return []
        else:
            print(f"Failed to fetch proxies, status code: {response.status_code}")
            return []
    except requests.RequestException as e: #检查异常情况
        print(f"Error fetching proxies: {e}")
        return []

# 构建代理池，获取 500 个 IP
proxy_list = get_proxy_list(api_url)

# 如果代理池为空，使用本地 IP 或者给出一个空的代理，直接进行请求
if not proxy_list:
    print("Proxy list is empty, using local IP as fallback.")
    proxy_list = [""]

# 设置一个指针，记录当前使用的代理 IP
proxy_index = 0  #记录当前ip位置

def get_next_proxy(proxy_list):
    global proxy_index
    proxy = proxy_list[proxy_index]  # 获取当前代理ip
    print(f"Current proxy pool: {proxy_list}")  # 打印当前的代理池
    proxy_index = (proxy_index + 1) % len(proxy_list)  # 轮询代理列表
    return proxy