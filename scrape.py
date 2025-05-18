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
    'Cookie': '_xsrf=lFZKCQheTnXzAvPhgOGSNpDk9tIw1PZ5; _zap=cf9ea9f3-2f72-406d-804d-aed3c8679eab; d_c0=ADBSXHOQCRqPTpLnzT8AH4UfXIuYMJKShJw=|1740098445; __snaker__id=LJgMmPXUupQyZb3Y; q_c1=a03a879c9c5143cdb8f653afc3b123a3|1740475514000|1740475514000; z_c0=2|1:0|10:1743126328|4:z_c0|80:MS4xcHkyakVRQUFBQUFtQUFBQVlBSlZUUk9SMG1nQWZLUFlxNkpfWHlYRnlPaDJtWk54T0ViLVVnPT0=|4bad7277a17454bd920a6c783e288389924b29eb538ee533f9f09ace01fb066c; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1744182721,1744249473,1744417148,1744421715; __zse_ck=004_aT4hvFboisuinvy5uxVvIcgjV6PTdA89sReYG2q5C6AgPSzgaSdGioq5SM9G7WG0pLggvGKza1UsE69J31MKXdZ7TRNzSxULIod1uocDSm2UaqUZl/bhX730pMNpY6ay-77mo9UNu6D32Meu4cQKIaX2yXN7fOpRjIkJStdrhWua/cRWwgPe0F1rcmcrRfc69RY5bYN/vrk+j2qNxJgRVGmenJX0OzOW5wOuX2Vox9I+vjsSxoV9HQBXrp3p9y86VEAKohx/ZwLLzijzHREdUTfZFpgJMXLWr/c2/rHUEWU8=; tst=h; SESSIONID=lU0uBaVeEeji71npiBnFS54jUmUwbQw8NDS4j2lpKm6; JOID=UFkQB0pogNQa3b8nL26gwZWvKS4yB9HlapzddUsu5rpy741KW2ZY2HTduCIr_3usP907LkcbcUQkZyQXD0Iqm6E=; osd=Vl8RC0huhtUW37khLmKix5OuJSw0AdDpaJrbdEcs4Lxz449MXWdU2nLbuS4p-X2tM989KEYXc0IiZigVCUQrl6M=; BEC=684e706569bf16169217bb2a788786f3; BEC=04f80badde0b95441251f0ed57775ff7'
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
    headers["Cookie"]='buvid3=01A897BA-2F34-DFCE-129C-648F1E4AD73409021infoc; b_nut=1740098609; _uuid=4D4B2542-B7F10-B78F-101F3-38D8B5DAD6F110152infoc; enable_web_push=DISABLE; buvid4=FE795F54-3EB5-75FE-AF65-FBB69976D19109972-025022100-BcL%2FiGDjV6q1kavXA8cQUk1KYiI4uwIEJWlGMCcXJZmQWcrOypImXRHgYZ8QvCuO; DedeUserID=171638608; DedeUserID__ckMd5=fb7076ae2a9b560b; rpdid=0zbfAGOKCP|12KGp1eWD|3c|3w1TLhaB; header_theme_version=CLOSE; buvid_fp_plain=undefined; hit-dyn-v2=1; LIVE_BUVID=AUTO7917406176336900; blackside_state=0; CURRENT_BLACKGAP=0; is-2022-channel=1; enable_feed_channel=ENABLE; buvid_fp=e48a1e9c08e00442a3eafa326817254e; PVID=1; CURRENT_QUALITY=120; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2MTQ0MTcsImlhdCI6MTc0NjM1NTE1NywicGx0IjotMX0.CgoZ73-q0njAqPG7yPt8UTTEZackTOHBFRRV8uOC5Ww; bili_ticket_expires=1746614357; bp_t_offset_171638608=1063341968714629120; fingerprint=3f69fc24b0abd4a8c38d8e880b5978b8; SESSDATA=3a074703%2C1762060785%2C478f8%2A51CjCj7C7cEE3i4hvY2imQUz5VF4L26jbP6qrZ_AVIj9N97C9Xy_UilTVmoOxgnu2DFusSVkdhcFJVVDBzUk5ScFRYOUJBSTkwZkNoNFRKbzQ0OGZ4cUJrTDI1OUg0UWk1WUFVNWNXRVVjb3p3ZWZHZl9WZDZ4TEpyUHhDbGhlT3V2eWtsV28zRzBnIIEC; bili_jct=7bcd92c2933372f1454304c147004f8b; sid=8gp8bhn9; b_lsid=D89B6A10B_196A55DEB24; CURRENT_FNVAL=4048; home_feed_column=4; browser_resolution=816-756'

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

def bilibiliComment(oid):
    #url=f"https://api.bilibili.com/x/v2/reply/wbi/main?type=1&oid={oid}&sort=1"
    url = f"https://api.bilibili.com/x/v2/reply?type=1&oid={oid}&sort=1"
    headers = bilibiliHeaders
    response = requests.request("GET", url, headers=headers)
    try:
        data=response.json()['data']['replies']
        return data
    except KeyError:
        return None

