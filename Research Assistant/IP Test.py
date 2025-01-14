import re
import os
import requests
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# 代理IP API地址
api_url = "http://api.xiequ.cn/VAD/GetIp.aspx?act=getall&uid=150876&vkey=A67F3E026FC80A80D168E729668B9D53&num=200&time=6&plat=1&re=0&type=6&so=1&group=101&ow=1&spl=1&addr=&db=1"

proxy_list = []

# 从API获取并构建代理池
def fetch_and_build_proxy_list(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            proxies = response.text.strip().splitlines()
            for proxy in proxies:
                proxyHost, proxyPort = proxy.split(":")
                proxyMeta = f"http://{proxyHost}:{proxyPort}"
                proxy_list.append({
                    "http": proxyMeta,
                    # "https": proxyMeta
                })
            print("Proxy pool constructed.")
        else:
            print(f"Failed to fetch proxies, status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error fetching proxies: {e}")

# 获取下一个代理的函数，轮询代理池
proxy_index = 0
def get_next_proxy():
    global proxy_index
    if proxy_list:  # 检查代理池不为空
        proxy = proxy_list[proxy_index]
        proxy_index = (proxy_index + 1) % len(proxy_list)
        return proxy
    else:
        return None

cookies = {'_ga': 'GA1.2.1644231359.1718892969', 'gdId': '54f449bf-7407-42a3-b477-9f7463f059f5', 'rl_page_init_referrer': 'RudderEncrypt%3AU2FsdGVkX19K7%2F5S%2BEAG9hpY0lOYo79XpC9uYqlFwGKMsJUCU6FzBNcQ2FQS7jQSkaZWcBHsd8d3KZNHUxHDbBSrNbASZgFBK9V2rJ9WbIOr5bUE9Vr%2FGah2Pyv25TjdSkpzH4c%2F%2F0wBjjqCbXxQpj8IVSiScBJQdYetvHHkJGG%2BcK2KNIu%2FSKVzx6KYHR8iaa6w5LkciAmbKFb%2F5FCvbG4ll0aqIk4DZXXRdfSLFVk%3D', 'rl_page_init_referring_domain': 'RudderEncrypt%3AU2FsdGVkX1%2BNblCkwLEk9oiqUuVZHFvn3UffpLausXrWy5Icp4AOAa3UY54OE2Cv', '_optionalConsent': 'true', 'indeedCtk': '1i0r08vnai03u801', '_fbp': 'fb.1.1718931757639.725498665831171696', 'rttdf': 'true', '_pin_unauth': 'dWlkPU5URmlOVGsyWVRVdE5EWmpNUzAwTmpKa0xXSXdaakl0T1RFM1pUWTVOMlV6T1RFMg', 'uc': '8013A8318C98C51765F313E41297D44CDFF1078FDFEC6FBAAA984A83A0F9D286B291AAC3BBC4F729239AD69F96E339F0C2723F79396CEC0CD2BA584834E6C35F5EF1A6478862C5AC0AC5F880BBFC1BF6CA0411B3BBB33D4F5E896363F60472CE3F3EF8084074D3C5BB913D4A0BDAC8D1EAE7D90A7D06210399915FFBED58EDBC335EB7A7EA01D52287D35BF42FBC7E61', '_gcl_au': '1.1.189131620.1727236020', 'GSESSIONID': 'undefined', 'cass': '1', 'at': 'kk8fSbqdc-FOLAuqvGHgGIKE7Du66M6IqWY1f_m_vQr7T-TEeIWRKidwd8IBcMG55B221UdmX3-1FLbaqv_WxQlUg0joVOvbUBU8RiJHF2-Qx_2LuuDfakPp81Dmj8nENYUtWM9LF_Y3ZzbsyY6NTT4hEmHkp1EPAFxxHELy3nPL6Nf0WfZRqCj6kLcj6zWClulKsPK8Hcr1vtKQSpIg2cLRuINxABLWa5jCmo8RbIDXeKpQswYtdaNInfU-QJx0yZf44tkvuX9osCtfPBi2HOIUYrwEYy6_-ds57XqU2WW0n308vVQogxQaYLGu22al3wlYUZHAktGd1wgyoaqgwj94qHIq5hrLpBK6RtCS0K-AZqh4vojkmn0vMjH47wt602R7HvhcLB227iUH6eiW6HaiyNEnLa5yxHzauOyklwVtGBRGr0-MJ8olNQyuzt3kf_L_6nb9MJvz7fGfTT3Uq4Lk-BziuNvHKlyqycT3e2BnGQCTulutzOUgi33cJz3wJAZLEptkMRtkV-869u1NHxEaaa8_vLPeJNd07rZwWkirm7w5_qQA2zdILCK9a4OvrljP_mJ9mrYxxge4Fi-91FhBND9K1zrglqvWSkHR5HiXH4sgqg-4KgSq0MVOifXt4wP-L-Qo3axiJGbFFssQnT69Kn9aP_VTrJM5Nw7i03QbB9D9F8Pgm9HhFA4D8IQHXBI0_EfRpvoyxoJVG15U64LMw177lbVyWcDgKaIClpt7ri40cgL90iEYgi9Yd0foVa1JzV_rCrIQJTkw5EmWgJeqE5IEST4kVUnbTsHAqtXiAkQ-EcjgVxAj85LqAf56kKUIJmpmksc_xGvOMedgQg4ZGBv1k-ulvFwi3185P02_OgBtNSzyYvp-MQ', 'asst': '1731039142.0', 'gdsid': '1731035192572:1731039143872:4C7890C52FD881EC760F7A5B1F592461', 'rsSessionId': '1731039143310', 'cdArr': '', '_rdt_uuid': '1721526794704.9753d317-1c0e-4052-81e6-802a24a6d994', 'AWSALB': 'dRE55Iv10PGAvVHlOzcw/nHRbqtziHZXeMG27fkNFmLS0AyH0gY8QybOP8d+HwHweidafwzJJ5ujvDdY0IwXGqKdY4ViBcgjNb4CnILdWeFWMjFBZ8Vq4SvEH7cJ', 'AWSALBCORS': 'dRE55Iv10PGAvVHlOzcw/nHRbqtziHZXeMG27fkNFmLS0AyH0gY8QybOP8d+HwHweidafwzJJ5ujvDdY0IwXGqKdY4ViBcgjNb4CnILdWeFWMjFBZ8Vq4SvEH7cJ', 'JSESSIONID': '4B726B9B562862473208B808CC3B2A38', '__cf_bm': 'TfIKS6EW5YwJya.ZRgYyT868KSEPn.Et_UmoXD6816U-1731039236-1.0.1.1-9selPOek4Hn8GfPBkUOX2S_sXdeLTf6MFsjSyBEHHu42SPjOREuby8rdVQevThyXYzBrip_IFQ1MuPzPM_rFmw', '_gid': 'GA1.2.822333134.1731039240', '_gat': '1', 'cf_chl_rc_m': '1', '_ga_500H17GZ8D': 'GS1.2.1731039240.30.1.1731039253.47.0.0', 'cf_clearance': 'orr3wkfvXREVsPzO0jhjWqQGGIvJlFdLJ9Atvvt_kGI-1731039253-1.2.1.1-L0cV8vhePyEd1IFZobZdFYnvZ_GMk1_8RK_MjpRFQ6ixjQk9YYcR1WIrtJbMChHCsTGrie_kL9HLBO9c0Xp.0Sf2g5qx9G847ugY7bQ51HK0FHZ4RVpFrQ0j8.ewXF57xyM26XVbP2AWGJpOTp1d3e2UQs4eQLZd2uaRjtjkNpWkgMERVU3jJSgOTdOKAOO6_H4LNikDxKTfB3_5AcQ69hvgKQ436Gb0hx.vKhoW.hpJiPc.2BUydb9O1_iYLATCBzyZCuZEznrfGc3l77DsSOlwehxTcjf3x16.FW2VFZyiBjbYagD1XL9au_uMSxcIJPhT4AHsxDzPRAcEwbIPseeW.NxS_xyybVM5KI73FbFlMBknPQjB4eS6NCAteoKkR.KhwE36e7ceIAcHnWFoGqcoDwA60tndYCXx_sJI.qJo9j.ZYJHjauf_OPE3y2co', 'bs': 'e_cqJCSYxGiO-CK5rYj_iQ:N8isNnOvQQ7txgyUfnoTuZx_ZSeZxR9azkQuQ0Wj9daWudkpiz0cLxRKXED20xWYjDn5drEKfnuiG83O5VseHrHcGFKZshc2iE2xmfjd0JI:1dmEyVmBj9OZgm--m4X_T5jigqORcTBUY1dW18r1FN4', '_cfuvid': '9fKHWKT2xJBfR5HDN_ASbKsYxlg4vQAKpIoCYSTOAZA-1731039262461-0.0.1.1-604800000', 'rl_user_id': 'RudderEncrypt%3AU2FsdGVkX1%2Bzqkng2SMH1ZrIaTlp4u8lc9TeH6hJLJ0%3D', 'rl_trait': 'RudderEncrypt%3AU2FsdGVkX18u8fUwjwRhd7fUX5MEHjwSSMGm5%2BBxfAdESGJe659mFzHeCltlbkWzJtR2dRgGZAe2e%2F7%2FQilVFFvsFoZSMetUV3q4YSjhbshbwo0kTQoH5ph00Z0LQeyNflpyJSaDD445AKwyQposPtjtO9zGnFoJOftNQDRKYJ8E3GK69nhAQIobkfKzZD2y%2BCvhwMsu7tbs83%2FZ1VqBn1R2N%2FqLCgPx4kUZY%2BVSK60%3D', 'rl_group_id': 'RudderEncrypt%3AU2FsdGVkX19sbP6vWQtsdMWaEyWENVN7COt9mfgKv04%3D', 'rl_group_trait': 'RudderEncrypt%3AU2FsdGVkX18dl5VgvdI4BDCOWrsCfcuOG5OO67DI5Ak%3D', 'rl_anonymous_id': 'RudderEncrypt%3AU2FsdGVkX1%2BqVyMyeH391lpERQSZMKBE9IVLXGiCZh1rYcBRH5g3dCgXkJjgP2IvrNgFovC%2BX9RilUmWFxIoGw%3D%3D', 'rsReferrerData': '%7B%22currentPageRollup%22%3A%22%2Freviews%2Findex%22%2C%22previousPageRollup%22%3A%22%2Freviews%2Findex%22%2C%22currentPageAbstract%22%3A%22%2FReviews%2Findex.htm%22%2C%22previousPageAbstract%22%3A%22%2FReviews%2Findex.htm%22%2C%22currentPageFull%22%3A%22https%3A%2F%2Fwww.glassdoor.sg%2FReviews%2Findex.htm%3Foverall_rating_low%3D1%26page%3D1%26locName%3DAmerica%26filterType%3DRATING_OVERALL%22%2C%22previousPageFull%22%3A%22https%3A%2F%2Fwww.glassdoor.sg%2FReviews%2Findex.htm%3Foverall_rating_low%3D1%26page%3D1%26locName%3DAmerica%26filterType%3DRATING_OVERALL%22%7D', 'rl_session': 'RudderEncrypt%3AU2FsdGVkX188o2B1DRtFT2T63FLHMM64TS4FAOKHoEeiM1oRSA22nA9fmw%2FryLpNJhn4fVrRnjEAB9J7KJ21NLEMdaWTK2qC58uLUI0rwCabzgnJn9f0sjxCfo45HxUvWAaewDEccjKNVv%2BLxnH5Aw%3D%3D', 'OptanonConsent': 'isGpcEnabled=0&datestamp=Fri+Nov+08+2024+12%3A14%3A24+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202407.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=63f8ac6f-a2fc-4006-b5f9-73045f09d172&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0017%3A1&AwaitingReconsent=false'}


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',   ####务必要注意latin
    # 'cookie': '_ga=GA1.2.632463846.1722317374; _gid=GA1.2.30809110.1722317374; _ga_500H17GZ8D=GS1.2.1722317374.1.1.1722317387.47.0.0; cf_clearance=mf035C48r0Gci4WtD0KIGkAqWX7xqiBm_l5gw7putdg-1722317386-1.0.1.1-RJv8yQxuFKgPu7hCcTotjYEA6e67f9TIW2YRsFbVtE1CBlwqQxPrNF.VrReAOAMYcDiBqKwVsGiv4Z8kdRDZmw; gdId=35387e46-48ee-45d9-aaa8-f63489bf6af2; _cfuvid=oPTrtzsZpRPk.pW4pqRrjQ0_AINIwKH8QdlOHUmNJJI-1722317398260-0.0.1.1-604800000; rl_page_init_referrer=RudderEncrypt%3AU2FsdGVkX1%2F7BtDjI%2FlZULQXsLUSKA7vBpoxGgbM2rxPXHaIMG1WPhoPe4rHS80UwnwEQhpGeq4vEQT08I0Gt6%2FZaah2aXz7BIFvuv6lhJNqYeIqlVVJa6HK6q%2FAHMHJFPfczpmF1xfx%2Bq051qfzgWSc8uUGgT1iQ49tP01pdBCrhLjtGEHghFsSYfsMreAO8FONd3CVVRHCn5vpW1VrRZuRKqhDuLpNPzGEND4Ol0tn1QbC00zeJQdgo17TdS0y; rl_page_init_referring_domain=RudderEncrypt%3AU2FsdGVkX1%2FIrE5FjzLSrbUcZRYRMJjR%2F49ny7trnPq9G%2FeF%2FxRiJdmZs39abcGy; GSESSIONID=undefined; _optionalConsent=true; _gcl_au=1.1.1599511814.1722317415; JSESSIONID=1201A0B80CE525010529EB92CB242E2C; cass=0; AWSALB=u/XJyi1hjcA7kU7ZXgk+ChjeaM65oJV0ok6mb6dbjrXfMccWq6f2byqO2lcAjy7KqCcH92JDBL3qB2N6m4LScMyK9d2aHfSuzThg9686v7ccq+4rnfe6mVN9/Dy6; AWSALBCORS=u/XJyi1hjcA7kU7ZXgk+ChjeaM65oJV0ok6mb6dbjrXfMccWq6f2byqO2lcAjy7KqCcH92JDBL3qB2N6m4LScMyK9d2aHfSuzThg9686v7ccq+4rnfe6mVN9/Dy6; AFSID=ZjlkMzZiMDAtMTNiOS00OGEwLWI2YWItNTJmZTQ2NTljNDgx; rl_user_id=RudderEncrypt%3AU2FsdGVkX1%2Fp0P%2FIbY86wxcm81rTImgzcx9QCS6NKs8%3D; rl_trait=RudderEncrypt%3AU2FsdGVkX1%2FeG6V0J3cEpNwN7L8gvqWjD8pUNEfqC8WcKlXmIzTLorszgYixGdOqOjcX7gHlq1HOZdef1q%2Bgw%2BDuMqD5pVegi4VZGAV3aW4GrDTCI0xgNv%2FlliHhQy1JFQ2ScAogaWI7hY9TKL8Ed1qZzaaChNTM30vkCqsFXH2YAxZffOW8g9yNBIX5AQgf1Tho5OROr42I6l8PqmqubQ%3D%3D; rl_group_id=RudderEncrypt%3AU2FsdGVkX1%2FnXWNKB84h%2FIACyocyy4ObX4z7qaj38VM%3D; rl_group_trait=RudderEncrypt%3AU2FsdGVkX1%2BMt2ELHDCQyzzqWGf0hzymXfy5Yvcv37Y%3D; rl_anonymous_id=RudderEncrypt%3AU2FsdGVkX1%2B8egg0Ow5I%2F3IQz%2BSYMzC0q5hrhVmP4ci4jQ9vHK7CgpJFTosOwvY0LlUTF6LlUKbrg5vSAh9OFQ%3D%3D; rl_session=RudderEncrypt%3AU2FsdGVkX18fURfiCU0H2IjFbOsh3j8o1ox1A33%2BM9142S1Z%2B3WnNZG1yBjDO9JdN18UW%2Bk%2BIYvCf6YcXIZoJoE0O5RLzKj%2Fw7uLeRjpeJwbZqFAZC5jDlDdCjp1bxPNYXi%2Ba%2B59KLU6SqsrLaHuzw%3D%3D; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jul+30+2024+14%3A45%3A58+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202405.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=30bc6539-3a74-4b73-9a09-ce6f26b1eef8&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0017%3A1&AwaitingReconsent=false; gdsid=1722317398188:1722326490792:149F4541423C718024F4044CD446037D; at=BH-O62XD9oq9p-RqyBGJwBZZdZnKf7US-H3fQcVO-njtPC5e4B_6gcAnWqptT7rf3X8YHCzSo_dxMAMibi0IAv5ICmJC6_VmyjGvnDnuJLgzlM1tMQIJedW_vdlbT0zVWifSIztmgxPT-NKTXaR4O8J-ov03-9XbjEqRO-G0LB8gUXIGP9MhXHTgMzbI03lmbMa-ZHy4jy18V5yQQAjap_Rln2wP-iPJ4Vf80kIpVdmIAmqs2xP1-h7PR65PsqaCfn4hKZQK3ZZtNcP1_p2m6S6-12n7PJbtRDhrZioA-b1fEXxV42bP-Z3OE2cAu_avUevGZB64NYynRmKr3gy11XeWqK4771g79dnfiLI7EeIQhqqwaoED9JCV0FjeVnothlXM_1nI3CKx75SGnmaNBBVfNMqlvkfFFAaUeaxP5lpYDIex-cD7-s7i_ZTT61ZLbU5Yb3bk28u0OqA4naO41BEpmidF0g0ZSb5RCJoa3q4_5pdlyGFUzMPxCTD0vYBQOQ0FijZ1MB2cd8zfUubV7NJLbagCU67v0QuvnJpfSInfAEeQoPzLEb55vMztaHY_x8on-ASG4USmhBViy2QevWra5y01LH2LDpPx1GphJCg9f5TJV0o1-1OcUZMDYJS1UDeGd7oYPZ61qCHgLqi2vSKQH3L21a25e4leQ5oxv2o-Z9rwVzYMhzJVnhvhwVuvwbEis2hZVP1XvnlKnf4DF1-6p-Fyu_VJb6UgkjzsFpot-SMA_zQqtbAxYCquoux1ZCm8I0aMjZ2OxOOjVW_uVLn97zQ4UBAkCMBApq7DmvGjM2jfsMnPOryDa3t8le_IV84w9F2D15bszHy7EgS1ax7bArdO53fd-FTf9dq16NEJVt46MvvKV4qsELTv4g; asst=1722326490.0; bs=dIRNR6tdbTBjYayWkDUrHQ:zYvT6dtjND_TDqyaDJDRi0QqclfteQ6WpGD7zdRjAHgAYRWkaolosahjRpQWw_J2WaWxTBLwZAeaWkTdUl_cIyIEUfJhi5zdwCUuBEk2jy0:aoSwpm-eu7GpZejByj6inhobRlp2LJWQayk8YgRTlyM; __cf_bm=wTQ3KHcEe2m6s.wxa6mkjj8QsyEsn15LoKwCpglhb1Q-1722326490-1.0.1.1-jlw2Q06MTnqN8vTdfH_V4OvGp1WE3yS3MJvaq1jBrNEV_SacTeD_3O8A_IaNteQ1b27P_yuFCZ_FEKUgjsKEmA; cdArr=76%2C1547%2C686%2C64%2C242%2C1048%2C52%2C52%2C73%2C71',
    'priority': 'u=0, i',
    'referer': 'https://www.glassdoor.sg/',
    'sec-ch-ua':'"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"128.0.6613.120"',
    'sec-ch-ua-full-version-list': '"Chromium";v="128.0.6613.120", "Not;A=Brand";v="24.0.0.0", "Google Chrome";v="128.0.6613.120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
,
}

resultList = []

# 保存数据到 CSV
def save_data(resultList):
    df = pd.DataFrame(resultList)
    if os.path.exists('./usname9.csv'):
        existing_df = pd.read_csv("./usname9.csv")
        new_df = pd.concat([existing_df, df])
        new_df.to_csv("./usname9.csv", index=False)
    else:
        df.to_csv("./usname9.csv", index=False)

# 清理数据
def clear_data(response):
    pattern = r'"id":\s*(\d+),\s*"__typename":\s*"Employer".*?"shortName":\s*"(.*?)"'
    employers = re.findall(pattern, response, re.DOTALL)
    if not employers:  
        return False

    temp_data = [{'id': emp[0], 'shortName': emp[1]} for emp in employers]
    resultList.extend(temp_data)
    return True

# 发出请求函数
def make_request(url):
    max_retries = 5
    retry_delay = 1.5

    for _ in range(max_retries):
        proxy = get_next_proxy()
        try:
            print(f"Using proxy: {proxy}")
            response = requests.get(url, cookies=cookies, headers=headers, proxies=proxy, timeout=10)
            print(f"Status code: {response.status_code} for URL: {url}")
            if response.status_code == 200 and response.text.strip():
                return response.text
            elif response.status_code == 429:
                print(f"Received 429 Too Many Requests. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 1.2
            else:
                print(f"Received unexpected status code {response.status_code}.")
                break
        except requests.RequestException as e:
            print(f"Request error with proxy {proxy}: {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_delay *= 2
    return None

# 爬取特定位置和行业的页面
def scrape_state_industry(locId, industry_id):
    for page in range(1, 500):
        url = f'https://www.glassdoor.sg/Reviews/index.htm?overall_rating_low=1&page={page}&locId={locId}&locType=S&locName=United%20States&industry={industry_id}&filterType=RATING_OVERALL'
        print(f"Scraping LocID {locId}, Industry {industry_id}, Page {page}")
        response_text = make_request(url)
        if response_text is None:
            print(f"Failed to retrieve data for LocID {locId}, Industry {industry_id} at page {page}. Stopping.")
            break

        has_data = clear_data(response=response_text)
        if has_data:
            print(f"Successfully got data from page {page} for LocID {locId}, Industry {industry_id}.")
        else:
            print(f"No more data found for LocID {locId}, Industry {industry_id} after page {page}. Stopping.")
            break

# 主程序
if __name__ == '__main__':
    # 初始化代理池
    fetch_and_build_proxy_list(api_url)

    locid_df = pd.read_excel('D:/dataset for RA/2024 RA/Labor Amenity/数据处理/公司名字爬取/locid.xlsx')
    locIds = locid_df['locid'].tolist()
    industry_ids = list(range(200001, 200003))

    max_workers = 100
    futures = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for locId in locIds:
            for industry_id in industry_ids:
                print(f"Queueing scrape for LocID: {locId}, Industry: {industry_id}")
                future = executor.submit(scrape_state_industry, locId, industry_id)
                futures.append(future)

        for future in as_completed(futures):
            future.result()

    save_data(resultList)