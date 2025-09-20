from typing import Union

from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from scrape import *
import process
import LDA
from fastapi import Body
import asyncio
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Any
import TimeSerise
import deepseekAPI
from bs4 import BeautifulSoup
app = FastAPI()
class plotData(BaseModel):
    keyword:str
    data:List[Any]

@app.get("/")
def read_root():
    return bilibili()


@app.get("/getData")
def get():
    return bilibili()

@app.get("/search")
def search_items(keyword:str):
    return process.parse(keyword)

@app.post("/plotPie")
def plot_pie(requestData:plotData):
    data=requestData.dict()
    fig = process.sentimentPlot(*process.comment2list(data))
    html = fig.to_html(full_html=True, include_plotlyjs=True)
    return HTMLResponse(content=html)

@app.post("/plotWordCloud")
def plot_wordCloud(requestData:plotData):
    data=requestData.dict()
    img_bytes=process.wordcloudPlot(process.tkdocs2merged(process.comment2tkdocs(data)))
    return Response(content=img_bytes.getvalue(), media_type="image/png")

#绘制LDA主题一致性和主题困惑度图
@app.post("/plotLDAp")
def plot_LDAp(requestData:plotData):
    data=requestData.dict()
    data=process.comment2tkdocs(data)
    img1,img2=LDA.LDAMetrics(data)
    #构造网页
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Matplotlib Plots</title>
        <style>
            body {{
                margin: 0;
                padding: 20px;
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
            }}
            .plot-container {{
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 30px;
                margin: 30px auto;
                max-width: 1200px;
            }}
            .plot {{
                flex: 1 1 45%;
                min-width: 400px;
                max-width: 500px;
                border: 1px solid #ddd;
                padding: 15px;
                background: white;
                box-shadow: 0 0 15px rgba(0,0,0,0.1);
                border-radius: 8px;
                box-sizing: border-box;
            }}
            .plot img {{
                width: 100%;
                height: auto;
                display: block;
                object-fit: contain;
            }}
            h1 {{
                text-align: center;
                color: #333;
                margin-bottom: 20px;
                font-size: 24px;
            }}
            @media (max-width: 900px) {{
                .plot {{
                    flex: 1 1 100%;
                    max-width: 100%;
                }}
            }}
        </style>
    </head>
    <body>
        <h1>LDA Model Evaluation Metrics</h1>
        <div class="plot-container">
            <div class="plot">
                <img src="data:image/png;base64,{img1}" alt="Coherence Score">
            </div>
            <div class="plot">
                <img src="data:image/png;base64,{img2}" alt="Perplexity">
            </div>
        </div>
    </body>
    </html>
"""
    return HTMLResponse(content=html_content)

@app.post("/plotLDA/{ntopics}")
def plot_LDA(requestData:plotData, ntopics:int):
    html_content=LDA.modelLDA(process.comment2tkdocs(requestData.dict()),ntopics)
    return HTMLResponse(content=html_content)

@app.get("/getTrendingPlot")
def plotTrending(speed:int=Query(1000, description="帧播放速度（毫秒/帧）", gt=400)):
    fig=TimeSerise.getTrendingPlot(speed)
    html = fig.to_html(full_html=True, include_plotlyjs=True)
    return HTMLResponse(content=html)

@app.post("/AITextAnalysis")
def aiTextAnalysis(requestData:plotData):
    data=requestData.dict()
    html=deepseekAPI.analyze(data)
    soup=BeautifulSoup(html,"html.parser")
    html=soup.find("html").prettify()
    return HTMLResponse(content=html)