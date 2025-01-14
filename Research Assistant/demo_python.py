import requests
import time

if __name__ == '__main__':
    # 客户ip提取链接,每次提取1个，提取链接可以换成自己购买的 #按量提取 100个
    url = 'http://api.tianqiip.com/getip?secret=jol9ec6lqovxtc38&type=txt&num=1&time=3&port=1&sign=820f3eb1681d6e1290ba4a38251a2c4c'
    # 访问的目标地址
    targeturl = 'http://myip.ipip.net'  
    response = requests.get(url)
    content =response.content.decode("utf-8").strip()
    print('提取IP：' + content)  #获取ip
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print('提取IP时间：' + nowtime)
    sj = content.strip().split(":", 1)
    sj1 = sj[0]
    print("IP：", sj1)
    sj2 = sj[1]
    print("端口：", sj2)   #拆分ip形式


    try:
        proxyMeta = "http://nfd0p2:bHQAp5iW@%(host)s:%(port)s" % {  # 账密验证,需要购买的代理套餐开通才可使用账密验证，此种情况无需加白名单
        # proxyMeta = "http://%(host)s:%(port)s" % {#白名单验证
            "host": sj1,
            "port": sj2,
        }
        print("代理1：", proxyMeta)
        proxysdata = {
            'http': proxyMeta,
            'https': proxyMeta
        }
        headers = {
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.'
        }
        start = int(round(time.time() * 1000))
        resp = requests.get(targeturl, proxies=proxysdata, headers=headers, timeout=20)
        costTime = int(round(time.time() * 1000)) - start
        print("耗时：" + str(costTime) + "ms")
        print("返回:",resp.text)
        s = requests.session()
        s.keep_alive = False
    except Exception as e:
        print(e)




