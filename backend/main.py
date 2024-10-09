from flask import Flask
from elasticsearch import Elasticsearch

es = Elasticsearch(HOST='http://elasticsearch',PORT=9200)

app = Flask(__name__)