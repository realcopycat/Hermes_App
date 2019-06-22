# public function

from elasticsearch import Elasticsearch as ES

def searchInES(des, index, keyname, resNum):
    esDriver = ES([{"host":"localhost","port":9200}])
    #query body
    queryBody = {
        "query":{
            "term":{
                keyname:des
            }
        }
    }
    print(queryBody)
    #search
    result = esDriver.search(index = index, doc_type="_doc", body = queryBody, size = resNum)
    print(result)
    return result['hits']['hits']