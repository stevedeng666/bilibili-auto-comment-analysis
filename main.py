from typing import Union

from fastapi import FastAPI
from scrape import *
import process
app = FastAPI()


@app.get("/")
def read_root():
    return bilibili()


@app.get("/getData")
def get():
    return bilibili()

@app.get("/search")
def search_items(keyword:str):
    return process.parse(keyword)