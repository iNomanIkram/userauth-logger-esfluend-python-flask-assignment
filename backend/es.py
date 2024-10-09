from elasticsearch import Elasticsearch
es = Elasticsearch(HOST='http://localhost',PORT=9200)
# try:
#     es.indices.create(index="logs")
#     print('created')
# except:
#     print(es.indices.exists(index="first_index"))
#
# doc = {
#     "time":"2021-22-21",
#     "message":"backend_serviced5"
# }
#
# es.index(index="logs",body=doc,id=6)

body = {
    "from":0,
    "size":5,
    "query": {
        "match": {
            "message":"backend"
        }
    }
}

print(es.search(index='register_frontend_service_call_logs_logs-2021-03-18'))

