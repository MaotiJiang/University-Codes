import re #正则表达式
import os #操作系统
import json #json格式
import requests #http请求
import pandas as pd
import time  # 导入time模块以便使用sleep函数

cookies = {'gdId': '70bca716-9d25-4c26-a303-7fadbee018fb', 'rl_page_init_referrer': 'RudderEncrypt%3AU2FsdGVkX1%2F8Ne5lAKIAyp4yD93VBNje3GZHZ%2Byx85j3Y2WKYhs2VF49tRVinum7', 'rl_page_init_referring_domain': 'RudderEncrypt%3AU2FsdGVkX19iRPnkO3xyS%2F9QzVBfKMHjsOi10nBisu4%3D', '_ga': 'GA1.2.93092202.1717691783', '_optionalConsent': 'true', '_gcl_au': '1.1.1634886070.1717691791', '_fbp': 'fb.1.1717691794420.720966834758934798', 'optimizelyEndUserId': 'oeu1717691852988r0.5553837164174631', 'uc': '8013A8318C98C51765F313E41297D44CDFF1078FDFEC6FBADAEBE799372D3505909ECD5DC0E67143F9FB24FEFCCB1A8E7C1E788903E13C1A8C71DC1060431B7480231B116021B2ED4F790734795765D23E2325A5DF7426404D1D871141E37A59E2E84F5C007A514BF52021B9A26BFD0A9FCC2F95B8FCB46DA60AC2036E17B35C8911D6045864C63E015D3FD412669277', 'indeedCtk': '1hvn6p6cbih2s801', '_pin_unauth': 'dWlkPU56WmpOMlkzWXpRdE4yUXhaUzAwWW1ZM0xXRmpOMk10TVRVeU1USmlaVGRqWVRkaA', '_gid': 'GA1.2.1381709359.1724119896', '_ga_500H17GZ8D': 'GS1.2.1724119899.14.0.1724119899.60.0.0', 'cf_clearance': '4tlvuQm75BpjAQ7wS4zUIfs45pHvu6_AtEWzdPxspoI-1724119895-1.2.1.1-HID567LYVQ1.SZ8Yl_B4Pe1fhMJvcsrJu225xdSTe3vQkKa8Qu1ECRoRDcVatzVIrY2KgI2eO0n3snq.jjZ9bP3H00jz9DGvHuR0XmrHp1RlBw_aMqonzdiKHp4KODkIbn.a6T7r7JAIZ74pDh7SzxYFD_VCEQULnavk13Uz8hhqpjQLh2K9BfQcluODH63SH0TzL5LWFSQo.nbwxKOF5sOU8pAU2qx5NVJ6nTsKJDunry0fWdy8nQl6TQJ3FRxuUzmt4EAEJcymrFxM6EItf0eMXH_LHgooccqf9gKHFSHNCvScGkD1NlwMbpP2_IjLYPseqn53c.hOTGbupKeJCHw9703kuDqNoLI34NVHCAXNtWglxB5eiZXs5Yw0n5U1eJCHO.UDXf_YsjG03Iy7kbdXLHDgF98_VXp6JvH4m.AVfwExNNXgi58sPDKx9O6c', 'rsSessionId': '1724119921744', 'cdArr': '', 'JSESSIONID': '6E394C739A4CADE5D775FA86CFE2F5F0', 'cass': '0', 'asst': '1724120189.0', 'gdsid': '1724119921574:1724120621326:F5E1F459D36780CAD21C7B70BB7F8079', 'rsReferrerData': '%7B%22currentPageRollup%22%3A%22%2Freviews%2Findex%22%2C%22previousPageRollup%22%3A%22%2Freviews%2Findex%22%2C%22currentPageAbstract%22%3A%22%2FReviews%2Findex.htm%22%2C%22previousPageAbstract%22%3A%22%2FReviews%2Findex.htm%22%2C%22currentPageFull%22%3A%22https%3A%2F%2Fwww.glassdoor.sg%2FReviews%2Findex.htm%3Foverall_rating_low%3D1%26page%3D1%26locId%3D1%26locType%3DN%26locName%3DUnited%2520States%26filterType%3DRATING_OVERALL%22%2C%22previousPageFull%22%3A%22https%3A%2F%2Fwww.glassdoor.sg%2FReviews%2Findex.htm%3Foverall_rating_low%3D1%26page%3D1%26locId%3D1%26locType%3DN%26locName%3DUnited%2520States%26filterType%3DRATING_OVERALL%22%7D', '__cf_bm': 'jUX3h0vtAt7ybyg3VfqvGZiPnpNbV0Z8vD6g1A1_l8A-1724120771-1.0.1.1-MQuAJL8NELZFmShO72jXZq9J0NbsWUJN1SzFn63QMn_3aajRpZe88DVHyBFKYRzUiVniQnd4wrtNRYNCx9X_PA', '_cfuvid': 'FeXOkb356AtdNku45mm2_FLxz6Wbf4Qow2CrabVf1d0-1724120771954-0.0.1.1-604800000', 'at': '7mGZ3tBIU51KTfUmg76Ck-sJY-Eiy4VLmNNG_I8BVsMACoXS53jVtC3wpbPzFTO4zYySFp5628ZZuCfwBO3_UgyI4FX1vT41LnbVWVl8RvcdEiGCizzUgIrp6b2cZ05YEvHehOJzbZEJVGUFbWt-u8kPZnxC7UT1cvktxh8MnxFuSJxhi7h-6fg8uJC0nqOts_0A8-t8sgiEzMo3-pwpAMr_3lj08p9HS0HOEOKyzuPKRpsm3LPQBhow2eb9KTRHyO3CB56vjSByzx9DsKF9pZH3nLRW9ATWUluAtzeP3fjL0p76bcS7hQRwkHTJozYe2nqNVMZB0wueDrH14SZNPX7Btk9YksGbb0PervVcWQUL9KhnsUYJ9Z0LyrKcjzVlCyfnSOTmta765WsLu7zF7lWkFEqQdW9riLwk3bHZsa5rdqitFEW_5yPWwsYWL8VobwNbXy3XTfGEfVrhamf7h_Dw9jyauRcmdmSkjuMButVrnOrOQsRXAgTapz7PSLYnINQANOCglSi1t7aZHDyz-CGrHrNjDRH_13nJjKV3P9Z41L_HrA-XIonqJNAAVtNWf7Nv1a3lhRL3BfS2fveJPxlI1g-6iVQZxvNcwh-6Rc2E9KeamNQ39Y3ceB7O_qWpYrFE40e0VCFCOB_OZLv6ruKd8MjkreN8ZzyIrD7ST5rQE5tNeDh9F0wvOjzHrZp9MOEP_sdI7BVhI15-34Jk1z9ufESbe1soOxB55K3_d4V_Zj6Bvj6s3cEviz_4tn7D9vG1hF-OWlrWLrGl71YxwZqJ8MjV4juIgATiLo3LCsYeMatddzfFQnI5LNMNJhVl9n6WrsR_rp8uUld2jDmRwyLbQl9nZuoertFl_A2MorHQkFQ8H0yA6OW3mg', 'bs': 'w_IxM3yGGU_BpHegaTtNyg:p2etlQbG7AcYiHmlNZWPqaTm_r9BmzsbC0oR9-LjxJjwPXNL4uruukteAvMBq4ZB8eHeFbHeGeM2Tx83K-yWoaNB-LFJtPxwQKjLB0Jr2DI:liy3vJgr5qJi5bVuYRDMOid3BtF211o3svy9jzExhi0', 'rl_user_id': 'RudderEncrypt%3AU2FsdGVkX1%2FxDkhy0%2B5uT7HYPw0%2FDb1BgaFfnNHV0vg%3D', 'rl_trait': 'RudderEncrypt%3AU2FsdGVkX1%2Fy4JP6VPYLTRgX27TrAYMPpbpvmJ2jPM1qjJ%2FkqA%2B%2Bje1XRe9mozMENCF5%2BHG3qjkWzppJRT9VLabh8IYUJrg1nB1MmPw23rIMflGSQWN2zZPN8sOv5joTqMfo2bw8TZqJhd%2BC2ZAo33%2FAN4a8lKfMc8xyLf59VYijf1XeJXnaAdnyT2VMJi613MleJmrax054CwDlnIB8M7%2FhTPHTmKxn0VwB0WxaCHw%3D', 'rl_group_id': 'RudderEncrypt%3AU2FsdGVkX1%2F0JkHOrPucOKsXuNOZuLLGL%2FcP5Sw25M4%3D', 'rl_group_trait': 'RudderEncrypt%3AU2FsdGVkX1%2FtNvVji6f0Qt00gyUgSXdsbphVDSOzRgU%3D', 'GSESSIONID': 'undefined', 'rl_anonymous_id': 'RudderEncrypt%3AU2FsdGVkX19IDuvcN8ozRWhyj0Ghyiv3ktje7iiFlcE9u39aplpFqU6wGQhfZ87KH76sn%2FCHcNDd3aUkGsyxLQ%3D%3D', 'rl_session': 'RudderEncrypt%3AU2FsdGVkX1%2FKcWKlelaAWcaCJr3EMphUuB7%2BWQeQH7mwqSIrZ2FVeoe%2BHOfBZhhYPnhsEtov2PN4FASBYlvGyYte6hdVCQ6v9zAocHxruoMyfoDZYYVTwt6t%2BcmdaJhDZy%2FCBDZMSJ3aV8rdxWhxTA%3D%3D', 'AWSALB': 'dchgzcs71gjIqKjK8wb2vkPKck3iZo420Y0F080ayoQ3r0o1MZJZyYBqZp99HXbGHpqJBa3U8uSQXwtdtX1NrmbsJrCZiqSKBiY/6nojvh9XwvWE7Nv4V+fA2ba+', 'AWSALBCORS': 'dchgzcs71gjIqKjK8wb2vkPKck3iZo420Y0F080ayoQ3r0o1MZJZyYBqZp99HXbGHpqJBa3U8uSQXwtdtX1NrmbsJrCZiqSKBiY/6nojvh9XwvWE7Nv4V+fA2ba+', 'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+Aug+20+2024+10%3A27%3A04+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202407.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=7bebb18d-1540-4242-ab7e-1fc7316058ab&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A0%2CC0017%3A1&AwaitingReconsent=false', '_rdt_uuid': '1717692078109.e090bc15-5b4c-45c3-a12d-58cecff523e9'}




headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',   ####务必要注意latin
    # 'cookie': '_ga=GA1.2.632463846.1722317374; _gid=GA1.2.30809110.1722317374; _ga_500H17GZ8D=GS1.2.1722317374.1.1.1722317387.47.0.0; cf_clearance=mf035C48r0Gci4WtD0KIGkAqWX7xqiBm_l5gw7putdg-1722317386-1.0.1.1-RJv8yQxuFKgPu7hCcTotjYEA6e67f9TIW2YRsFbVtE1CBlwqQxPrNF.VrReAOAMYcDiBqKwVsGiv4Z8kdRDZmw; gdId=35387e46-48ee-45d9-aaa8-f63489bf6af2; _cfuvid=oPTrtzsZpRPk.pW4pqRrjQ0_AINIwKH8QdlOHUmNJJI-1722317398260-0.0.1.1-604800000; rl_page_init_referrer=RudderEncrypt%3AU2FsdGVkX1%2F7BtDjI%2FlZULQXsLUSKA7vBpoxGgbM2rxPXHaIMG1WPhoPe4rHS80UwnwEQhpGeq4vEQT08I0Gt6%2FZaah2aXz7BIFvuv6lhJNqYeIqlVVJa6HK6q%2FAHMHJFPfczpmF1xfx%2Bq051qfzgWSc8uUGgT1iQ49tP01pdBCrhLjtGEHghFsSYfsMreAO8FONd3CVVRHCn5vpW1VrRZuRKqhDuLpNPzGEND4Ol0tn1QbC00zeJQdgo17TdS0y; rl_page_init_referring_domain=RudderEncrypt%3AU2FsdGVkX1%2FIrE5FjzLSrbUcZRYRMJjR%2F49ny7trnPq9G%2FeF%2FxRiJdmZs39abcGy; GSESSIONID=undefined; _optionalConsent=true; _gcl_au=1.1.1599511814.1722317415; JSESSIONID=1201A0B80CE525010529EB92CB242E2C; cass=0; AWSALB=u/XJyi1hjcA7kU7ZXgk+ChjeaM65oJV0ok6mb6dbjrXfMccWq6f2byqO2lcAjy7KqCcH92JDBL3qB2N6m4LScMyK9d2aHfSuzThg9686v7ccq+4rnfe6mVN9/Dy6; AWSALBCORS=u/XJyi1hjcA7kU7ZXgk+ChjeaM65oJV0ok6mb6dbjrXfMccWq6f2byqO2lcAjy7KqCcH92JDBL3qB2N6m4LScMyK9d2aHfSuzThg9686v7ccq+4rnfe6mVN9/Dy6; AFSID=ZjlkMzZiMDAtMTNiOS00OGEwLWI2YWItNTJmZTQ2NTljNDgx; rl_user_id=RudderEncrypt%3AU2FsdGVkX1%2Fp0P%2FIbY86wxcm81rTImgzcx9QCS6NKs8%3D; rl_trait=RudderEncrypt%3AU2FsdGVkX1%2FeG6V0J3cEpNwN7L8gvqWjD8pUNEfqC8WcKlXmIzTLorszgYixGdOqOjcX7gHlq1HOZdef1q%2Bgw%2BDuMqD5pVegi4VZGAV3aW4GrDTCI0xgNv%2FlliHhQy1JFQ2ScAogaWI7hY9TKL8Ed1qZzaaChNTM30vkCqsFXH2YAxZffOW8g9yNBIX5AQgf1Tho5OROr42I6l8PqmqubQ%3D%3D; rl_group_id=RudderEncrypt%3AU2FsdGVkX1%2FnXWNKB84h%2FIACyocyy4ObX4z7qaj38VM%3D; rl_group_trait=RudderEncrypt%3AU2FsdGVkX1%2BMt2ELHDCQyzzqWGf0hzymXfy5Yvcv37Y%3D; rl_anonymous_id=RudderEncrypt%3AU2FsdGVkX1%2B8egg0Ow5I%2F3IQz%2BSYMzC0q5hrhVmP4ci4jQ9vHK7CgpJFTosOwvY0LlUTF6LlUKbrg5vSAh9OFQ%3D%3D; rl_session=RudderEncrypt%3AU2FsdGVkX18fURfiCU0H2IjFbOsh3j8o1ox1A33%2BM9142S1Z%2B3WnNZG1yBjDO9JdN18UW%2Bk%2BIYvCf6YcXIZoJoE0O5RLzKj%2Fw7uLeRjpeJwbZqFAZC5jDlDdCjp1bxPNYXi%2Ba%2B59KLU6SqsrLaHuzw%3D%3D; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jul+30+2024+14%3A45%3A58+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202405.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=30bc6539-3a74-4b73-9a09-ce6f26b1eef8&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0017%3A1&AwaitingReconsent=false; gdsid=1722317398188:1722326490792:149F4541423C718024F4044CD446037D; at=BH-O62XD9oq9p-RqyBGJwBZZdZnKf7US-H3fQcVO-njtPC5e4B_6gcAnWqptT7rf3X8YHCzSo_dxMAMibi0IAv5ICmJC6_VmyjGvnDnuJLgzlM1tMQIJedW_vdlbT0zVWifSIztmgxPT-NKTXaR4O8J-ov03-9XbjEqRO-G0LB8gUXIGP9MhXHTgMzbI03lmbMa-ZHy4jy18V5yQQAjap_Rln2wP-iPJ4Vf80kIpVdmIAmqs2xP1-h7PR65PsqaCfn4hKZQK3ZZtNcP1_p2m6S6-12n7PJbtRDhrZioA-b1fEXxV42bP-Z3OE2cAu_avUevGZB64NYynRmKr3gy11XeWqK4771g79dnfiLI7EeIQhqqwaoED9JCV0FjeVnothlXM_1nI3CKx75SGnmaNBBVfNMqlvkfFFAaUeaxP5lpYDIex-cD7-s7i_ZTT61ZLbU5Yb3bk28u0OqA4naO41BEpmidF0g0ZSb5RCJoa3q4_5pdlyGFUzMPxCTD0vYBQOQ0FijZ1MB2cd8zfUubV7NJLbagCU67v0QuvnJpfSInfAEeQoPzLEb55vMztaHY_x8on-ASG4USmhBViy2QevWra5y01LH2LDpPx1GphJCg9f5TJV0o1-1OcUZMDYJS1UDeGd7oYPZ61qCHgLqi2vSKQH3L21a25e4leQ5oxv2o-Z9rwVzYMhzJVnhvhwVuvwbEis2hZVP1XvnlKnf4DF1-6p-Fyu_VJb6UgkjzsFpot-SMA_zQqtbAxYCquoux1ZCm8I0aMjZ2OxOOjVW_uVLn97zQ4UBAkCMBApq7DmvGjM2jfsMnPOryDa3t8le_IV84w9F2D15bszHy7EgS1ax7bArdO53fd-FTf9dq16NEJVt46MvvKV4qsELTv4g; asst=1722326490.0; bs=dIRNR6tdbTBjYayWkDUrHQ:zYvT6dtjND_TDqyaDJDRi0QqclfteQ6WpGD7zdRjAHgAYRWkaolosahjRpQWw_J2WaWxTBLwZAeaWkTdUl_cIyIEUfJhi5zdwCUuBEk2jy0:aoSwpm-eu7GpZejByj6inhobRlp2LJWQayk8YgRTlyM; __cf_bm=wTQ3KHcEe2m6s.wxa6mkjj8QsyEsn15LoKwCpglhb1Q-1722326490-1.0.1.1-jlw2Q06MTnqN8vTdfH_V4OvGp1WE3yS3MJvaq1jBrNEV_SacTeD_3O8A_IaNteQ1b27P_yuFCZ_FEKUgjsKEmA; cdArr=76%2C1547%2C686%2C64%2C242%2C1048%2C52%2C52%2C73%2C71',
    'priority': 'u=0, i',
    'referer': 'https://www.glassdoor.sg',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"127.0.6533.89"',
    'sec-ch-ua-full-version-list': '"Not)A;Brand";v="99.0.0.0", "Google Chrome";v="127.0.6533.89", "Chromium";v="127.0.6533.89"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
,
}

resultList = []

def sava_data(resultList):
    # 将数据转换为DataFrame对象
    df = pd.DataFrame(resultList)
    # print(df)
    if os.path.exists('./cornameedge.xlsx'):
        # 读取现有的Excel文件，如果不存在则创建一个空的DataFrame
        existing_df = pd.read_excel("./cornameedge.xlsx")
        # 将新数据追加到现有数据的末尾
        new_df = pd.concat([existing_df, df])
        # 将合并后的数据保存到Excel文件中
        new_df.to_excel("./cornameedge.xlsx", index=False)
    else:
        df.to_excel("./cornameedge.xlsx", index=False)


def clear_data(response):
    # 匹配对应数据内容
    short_names = re.findall(r'\"shortName\":\"(.*?)\"', response)

    for short_name in short_names:
        dit = {
            'shortName': short_name
        }
        resultList.append(dit)


if __name__ == '__main__':

    for page in range(35, 101):  # 改为 range(1, 101) 以爬取100页
        if page == 1:
            url = f'https://www.glassdoor.sg/Reviews/index.htm?overall_rating_low=1&page=1&locId=1&locType=N&locName=United%20States&filterType=RATING_OVERALL'
        else:
            url = f'https://www.glassdoor.sg/Reviews/index.htm?overall_rating_low=1&page={page}&locId=1&locType=N&locName=United%20States&filterType=RATING_OVERALL'

        print(f"当前爬取第{page}页数据")
        
        try:
            response = requests.get(
                url=url,
                cookies=cookies,
                headers=cookies,  # 你原本有 `headers` 但没有定义，这里使用 `cookies` 作为 headers 传入
            )
            
            if response.status_code == 429:
                print(f"第{page}页请求过于频繁，等待一段时间后重试...")
                time.sleep(60)  # 如果遇到429错误，等待60秒再试
                response = requests.get(
                    url=url,
                    cookies=cookies,
                    headers=cookies,
                )
            
            if response.status_code == 200:
                clear_data(response=response.text)
                print(resultList)
            else:
                print(f"第{page}页请求失败，状态码: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"请求第{page}页时出现错误: {e}")
        
        # 在每个请求之间增加随机间隔
        time.sleep(5 + (page % 5))  # 每次请求后随机等待5-9秒之间

    sava_data(resultList)


