#!/opt/anaconda3/envs/DA/bin python
import requests
import pymongo
client=pymongo.MongoClient("mongodb://localhost:27017")
db=client['bilibili']
collection=db['trending']
r=requests.get("http://localhost:8000")
data=r.json()
collection.insert_one(data)
client.close()
r.close()
