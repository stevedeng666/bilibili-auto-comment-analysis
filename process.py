import scrape
import asyncio
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
        try:
            comments=scrape.bilibiliComment(result['id'])
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
        except:
            pass
    return commentSet

