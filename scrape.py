import requests
from bs4 import BeautifulSoup
import json
import time
#热搜api返回{序号:(热搜标题,内容,URL)}
bilibiliHeaders={
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'origin': 'https://www.bilibili.com',
    'priority': 'u=1, i',
    'referer': 'https://www.bilibili.com/blackboard/activity-trending-topic.html',
    'sec-ch-ua': '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0'
    }
bilibiliCookie="自己设置"
def baidu():
    url = "https://top.baidu.com/board?tab=realtime"
    payload = {}
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referer': 'https://top.baidu.com/board',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
    'sec-ch-ua': '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'Origin': 'https://top.baidu.com'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    listDict={}
    if response.ok:
        soup=BeautifulSoup(response.text,features="html.parser")
        tags=soup.find_all("div",class_="category-wrap_iQLoo horizontal_1eKyQ")
        for tag in tags:
            listDict[("0" if tag.select('div[class*="index"]')[0].text.strip()=="" else tag.select('div[class*="index"]')[0].text.strip())]=(tag.select('div[class*=single-text]')[0].text.strip(),
                                                                                                                                             tag.select('div[class*=large]')[0].text.rstrip(" 查看更多>").strip(),
                                                                                                                                             tag.select('a[class*=look-more]')[0].get("href"))
    return listDict

def weibo():
    url = "https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&luicode=20000061&lfid=5070140584495876"

    payload = {}
    headers = {
    'sec-ch-ua-platform': '"macOS"',
    'X-XSRF-TOKEN': '572ff6',
    'Referer': 'https://m.weibo.cn/p/index?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&luicode=20000061&lfid=5070140584495876',
    'sec-ch-ua': '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'MWeibo-Pwa': '1',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
    'Accept': 'application/json, text/plain, */*'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    tempDict=json.loads(response.text)["data"]["cards"][0]["card_group"]
    listDict={}
    for index,item in enumerate(tempDict):
        listDict[str(index)]=(item["desc"],"",item["scheme"])
    return listDict

def rednote():
    pass

def bilibili():
    url = "https://app.bilibili.com/x/v2/search/trending/ranking?limit=30"
    payload = {}
    headers = bilibiliHeaders

    response = requests.request("GET", url, headers=headers, data=payload)
    tempDict=json.loads(response.text)
    listDict={}
    listDict['时间戳']=round(time.time())
    listDict['data']=[item['show_name'] for item in tempDict['data']['list']]
    return listDict

def zhihu():#坏了!!!
    url = "https://www.zhihu.com/hot"
    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
    'Cookie': '自己设置'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    listDict={}
    if response.ok:
        soup=BeautifulSoup(response.text,features="html.parser")
        tags=soup.find_all("section",class_="HotItem")
        for tag in tags:
            try:
                listDict[str(tag.select('div[class*=rank]')[0].text)]=(tag.select('h2[class*=title]')[0].text,
                                                               tag.select('p[class*=excerpt]')[0].text,
                                                               "")
            except IndexError:
                print("IndexError，可能是没有excerpt")
    return listDict


def bilibiliSearch(keyword):
    #需要cookies
    url = f"https://api.bilibili.com/x/web-interface/wbi/search/type?keyword={keyword}&search_type=video"
    payload = {}
    headers = bilibiliHeaders
    headers["Cookie"]='自己设置'

    response = requests.request("GET", url, headers=headers, data=payload)
    '''
    返回格式举例：
    [{"author":aaa,
    "id":111,
    "arcurl":aaa,
    "title":aaa,
    "description":aaa} , ...]
    '''
    return response.json()['data']['result']

'''
async def bilibiliComment(oid):
    异步版，容易封IP，我已经被封了好几次了555
    url = f"https://api.bilibili.com/x/v2/reply?type=1&oid={oid}&sort=1"
    headers = bilibiliHeaders
    async with(aiohttp.ClientSession()) as session:
        async with(session.get(url, headers=bilibiliHeaders)) as response:
            print("Status Code: ", response.status)
            try:
                data=(await response.json())['data']['replies']
                return data
            except KeyError:
                return None
'''

'''
    返回结果举例：
    [{"ctime":时间戳,
    "like":点赞数,
    "member":{"uname":用户名},
    "sex":性别,
    "replies":回复，楼中楼,
    "content":{"message":正文}}]
'''

#我发现爬comment不带cookie的话就只返回三条结果，而且cookie要时不时更新，否则会失效
def bilibiliComment(oid):
    #url=f"https://api.bilibili.com/x/v2/reply/wbi/main?type=1&oid={oid}&sort=1"
    url = f"https://api.bilibili.com/x/v2/reply?type=1&oid={oid}&sort=1"
    headers = bilibiliHeaders
    headers["Cookie"]=bilibiliCookie
    response = requests.request("GET", url, headers=headers)
    try:
        data=response.json()['data']['replies']
        return data
    except KeyError:
        return None

