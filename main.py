from typing import Union

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from scrape import *
import process
from fastapi import Body
import asyncio
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Any
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
    img_bytes=process.wordcloudPlot(process.comment2tokenized(data))
    return Response(content=img_bytes.getvalue(), media_type="image/png")