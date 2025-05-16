import scrape
#import asyncio
import plotly.express as px
from snownlp import SnowNLP
import pandas as pd
'''
#异步版，容易封IP，我已经被封了好几次了555
def parse(keyword):
    results=scrape.bilibiliSearch(keyword)
    commentSet={"keyword":keyword,"data":[]}
    tasks=[]
    async def handle(oid,title):
        try:
            comments=await scrape.bilibiliComment(oid)
            commentSet['data'].append(
                {
                    "id":oid,
                    'title':title,
                    'comments':[{"时间戳":comment['ctime'], 
                                    '内容':comment['content']['message'],
                                    '点赞数':comment['like'], 
                                    '回复':[{"时间戳":reply['ctime'], 
                                            '内容':reply['content']['message'],
                                            '点赞数':reply['like']} for reply in comment['replies']]} for comment in comments]
                }
            )
        except:
            pass
        
    
    for result in results:
        tasks.append(asyncio.ensure_future(handle(result['id'],result['title'])))
    
    loop=asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    return commentSet
'''



#同步版
def parse(keyword):
    results=scrape.bilibiliSearch(keyword)
    commentSet={"keyword":keyword,"data":[]}
    for result in results:
        comments=scrape.bilibiliComment(result['id'])
        if comments is None:
            continue
        commentSet['data'].append(
            {
                "id":result["id"],
                'title':result['title'],
                'comments':[{"时间戳":comment['ctime'], 
                            '内容':comment['content']['message'],
                            '点赞数':comment['like'], 
                            '回复':[{"时间戳":reply['ctime'], 
                                    '内容':reply['content']['message'],
                                    '点赞数':reply['like']} for reply in comment['replies']]} for comment in comments]
            }
        )
    return commentSet

def comment2list(data:dict):
    commentList=[]
    for i in data['data']:
        for j in i['comments']:
            text=j['内容'].replace("\n","")
            commentList.append(j['内容'])
    return commentList,data['keyword']
def sentimentPlot(commentList,title):
    attrs=['Positive' if SnowNLP(comment).sentiments>0.5 else 'Negative' for comment in commentList]
    data=pd.Series(attrs).value_counts().reset_index(name="count")
    fig=px.pie((data),names="index",values='count',title=f'关键词:{title} 情感分析',color="index",color_discrete_map={"Negative":"red","Positive":"green"})
    return fig