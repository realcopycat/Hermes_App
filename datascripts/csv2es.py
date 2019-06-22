# 处理案例 放入es

from elasticsearch import Elasticsearch as ES
from elasticsearch.helpers import bulk
import csv

es=ES([{"host":"localhost","port":9200}])
data_mapping={
    "mappings":{
        #指定文档类型 #注意！据说是官方已不再建议使用的一种特性
        #self.doc_type:{
        "properties":{
            "caseinfo":{

                #type indicates the type of this field
                #不能使用string，这是版本问题，text似乎表示可以索引的意思
                "type":"text",

                #ik是一个需要另外安装的中文分词器
                "analyzer":"ik_max_word",

                #指定搜索时可用在可分词字段的分词器
                "search_analyzer":"ik_smart",

                #决定字段是否可以被用户搜索
                "index":True

                },#注意此处的逗号！

            "casedetail":{

                #同上
                "type":"text",

                "analyzer":"ik_max_word",

                "search_analyzer":"ik_smart",

                "index":True

                },
            
            "casesummary":{

                #同上
                "type":"text",

                "analyzer":"ik_max_word",

                "search_analyzer":"ik_smart",

                "index":True

                },

            }
        }
    }

#如果不存在该名称的索引则进行下一步
if not es.indices.exists(index="democase"):
    #如果不存在则建立索引
    es.indices.create(index="democase",body=data_mapping)
    print("create {} mapping successfully!".format("democase"))
else:
    #如果已存在，则打印相关的消息
    print("index: {} has already create!".format("democase"))

path = "/home/procedureData/caseimport.csv"

csv_file= open(path,'r', encoding='UTF-8')
csvReader = csv.reader(csv_file)
dataInRow = []
count = 0
for eachLine in csvReader:
    print(eachLine)
    if count == 0:
        count = count + 1
        continue
    else:
        count = count + 1 
        action = {
            "_index":"democase",
            "_source":{
                "caseinfo":eachLine[1],
                "casedetail":eachLine[2],
                "casesummary":eachLine[3]
                }
        }
        dataInRow.append(action)

try:
    success,_=bulk(es,dataInRow,index="democase",raise_on_error=True)
except Exception as e:
    print(e)
    input()