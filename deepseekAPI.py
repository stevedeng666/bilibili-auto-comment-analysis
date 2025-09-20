from openai import OpenAI
import json
import process
def analyze(data):
    data=str(process.comment2list(data))
    client = OpenAI(api_key="自己设置", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "对收到的bilibili评论数据进行至少以下三个维度的分析：舆论倾向，热门话题，情绪分布，可以自己补充更有价值的分析，只返回分析结果的纯html代码形式以便直接加载进javafx webview展示，无需其他任何内容，因为纯html返回结果易于解析"},
            {"role": "user", "content": data},
        ],
        stream=False
    )
    with open("aicontents.txt",'w') as f:
        f.write(response.choices[0].message.content)
    return response.choices[0].message.content
