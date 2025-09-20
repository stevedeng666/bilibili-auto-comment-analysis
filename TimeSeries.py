import pymongo
import plotly.express as px
import pandas as pd
import time
def getTrendingPlot(speed:int):
    client=pymongo.MongoClient("mongodb://localhost:27017")
    db=client["bilibili"]
    collection=db["trending"]
    cols=[i for i in range(1,31)]
    cols.append("timestamp")
    df=pd.DataFrame(columns=cols)
    for n,i in enumerate(collection.find()):
        row=i["data"]
        row.append(i["时间戳"])
        df.loc[n]=row
    df['timestamp']=pd.to_datetime(df.timestamp.map(time.ctime))
    df=pd.melt(df,id_vars=["timestamp"],value_vars=df.columns[:-1],var_name="排名",value_name="热搜内容")
    df["排名"]=df['排名'].astype(int)
    df["排名+热搜"]=df.排名.astype(str)+" : "+df.热搜内容
    fig=px.bar(
    df,
    y='热搜内容',
    x=[0.5]*len(df),
    animation_frame='timestamp',
    animation_group="热搜内容",
    text="排名+热搜",
    title="bilibili热搜变化",
    height=1200,
    width=800
    )
    fig.update_yaxes(autorange="reversed",title_text=None)
    fig.update_xaxes(
        visible=False,  # 隐藏整个X轴
        showticklabels=False  # 隐藏刻度标签（双重保险）
    )
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = speed
    fig.update_layout(
    autosize=False,  # 禁用自动调整大小
    height=1200,     # 明确设置高度
    width=800        # 明确设置宽度
    )
    return fig
