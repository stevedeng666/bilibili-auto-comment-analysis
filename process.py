import scrape
#import asyncio
import plotly.express as px
from snownlp import SnowNLP
import pandas as pd
import jieba
from wordcloud import WordCloud
import json
import re
import time
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
    #有时候爬取到的评论数不多的原因：bilibili风控；该视频下面本来就没什么评论...
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
    time.sleep(0.05)
    return commentSet

def parse_json(json_data):
    #将json字符串转换成字典对象
    if isinstance(json_data, str):
        try:
            return json.loads(json_data)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON string provided")
    elif isinstance(json_data, dict):
        return json_data
    else:
        raise TypeError("Input must be either JSON string or dictionary")

def comment2list(data:dict):
    #将parse函数返回的原始数据解析成 ([评论1，评论2,...] , "搜素关键词")
    comments = []
    for document in data.get("data", []):
        for comment in document.get("comments", []):
            comments.append(comment.get("内容", ""))
            for reply in comment.get("回复", []):
                comments.append(reply.get("内容", ""))
    return comments,data['keyword']


#已被comment2tkdocs和tkdocs2merged代替
def clean_text(text):
    #清洗中文文本，若接收str则直接清洗，若接收list则用join拼接成str
    if isinstance(text,str):
        #删除无意义符号
        text = text.replace("&#34", "").replace("回复 @", "")
        #删除一些标点
        text = re.sub(r"[^\u4e00-\u9fa5，。！？；]", "", text)
        #分句
        sentences = re.split(r"[，。！？；]+", text)
        return [s.strip() for s in sentences if s.strip()]
    elif isinstance(text,list):
        return clean_text(" ".join(text))
    else:
        raise TypeError("Input must be either JSON string or dictionary")
#已被comment2tkdocs和tkdocs2merged代替
def tokenize_and_filter(sentences):
    #接收clean_text返回的分句list，进行分词和停用词筛选，返回词汇list(不区分视频)
    stopwords=[]
    with open("stopwords.txt","r") as f:
        for stopword in f.readlines():
            stopwords.append(stopword.strip())
    '''
    #stopwords.append([
    "的", "了", "是", "在", "我", "有", "和", "就", "不", "人",
    "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去",
    "你", "会", "着", "没有", "看", "好", "自己", "这", "那", "我们",
    "他们", "她", "它", "被", "对", "为", "你们", "什么", "能", "而",
    "不是", "现在", "怎么", "因为", "所以", "如果", "但是", "还是", "就是",
    "还有", "又", "然后", "而且", "呢", "吧", "吗", "啊", "哇", "哦",
    "哎", "啦", "嘿", "嗯", "a呀", "呗", "着呢", "过", "得", "将",
    "让", "把", "每", "每个", "与", "之", "及", "其", "此", "已",
    "并", "等", "再", "从", "或", "由", "向", "给", "关于", "根据",
    "比如", "例如", "比如说", "其中", "某", "某个", "以及", "之一", "虽然",
    "由于", "不过", "即使", "即便", "尽管", "而是", "甚至", "同时", "总之",
    "首先", "其次","说明","觉得","证明","可以","以为","真的","这个","已经","一下","那个","应该","不能","这样","可能","这种","知道","而已"])
    '''
    all_words = []
    jieba.load_userdict("userdict.txt")
    for sent in sentences:
        words = jieba.lcut(sent.replace("[]","-").replace("]","-"))
        filtered = [w for w in words if w not in stopwords and len(w) > 1]
        all_words.extend(filtered)
    return all_words

def comment2tokenized(json_data):
    #comment2list方法到tokenize方法的顺序调用
    data = parse_json(json_data)
    raw_comments = comment2list(data)[0]
    cleaned_sentences = clean_text(raw_comments)
    return tokenize_and_filter(cleaned_sentences)

def comment2tkdocs(data:dict):
    #parse返回的dict to 
    #清洗并分词后的分文档（一个文档就是一条评论）词列表，即
    '''[
        ["word1","word2",...], #文档一
        ... #文档n
    ]
    '''
    jieba.load_userdict("userdict.txt")
    data=comment2list(data)[0]
    documents=[jieba.lcut(sts.replace("[","-").replace("]","-").replace("&#34", "").replace("回复 @", ""),cut_all=False) for sts in data]
    stopwords=[]
    with open("stopwords.txt","r") as f:
        for line in f.readlines():
            stopwords.append(line.strip())
    return [[word for word in document if word not in stopwords and len(word)>1] for document in documents]

def tkdocs2merged(data:list):
    #将comment2tkdocs返回的分文档分词list合并为不分文档的纯分词list
    return [word for doc in data for word in doc]







def sentimentPlot(commentList,title):
    #接收comment2list返回的对象，绘制情感分析饼状图
    attrs=[]
    for comment in commentList:
        score=SnowNLP(comment).sentiments
        if score>0.6:
            attrs.append("Positive")
        elif score<=0.6 and score>=0.4:
            attrs.append("Neutral")
        elif score<0.4:
            attrs.append("Negative")
    #attrs=['Positive' if SnowNLP(comment).sentiments>0.5 else 'Negative' for comment in commentList]
    data=pd.Series(attrs).value_counts().reset_index(name="count")
    #fig=px.pie((data),names="index",values='count',title=f'关键词:{title} 情感分析',color="index",color_discrete_map={"Negative":"red","Positive":"green"})
    fig=px.pie((data),names="index",values='count',title=f'关键词:{title} 情感分析',color="index",color_discrete_map={"Negative":"red","Positive":"green","Neutral":"blue"})
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def wordcloudPlot(wordList):
    #接收tokenize_and_filter返回的分词后list
    import matplotlib.pyplot as plt
    import io
    wc = WordCloud(
        font_path="/System/Library/Fonts/STHeiti Light.ttc",  # 确保你有这个字体文件（或替换为其他支持中文的字体）
        background_color='white',
        width=800,
        height=600,
        max_words=100
    ).generate(" ".join(wordList))
    img_bytes = io.BytesIO()  # 创建空字节流，指针在位置0
    wc.to_image().save(img_bytes, format='PNG')
    return img_bytes
