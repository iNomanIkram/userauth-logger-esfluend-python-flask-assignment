import logging

import arrow
from elasticsearch import Elasticsearch
es = Elasticsearch(HOST='http://elasticsearch',PORT=9200)

def es_logging(message,service_name,id):
    index = f"{service_name}_logs-{arrow.now().format('YYYY-MM-DD')}"

    # create index if not present
    try:
        es.indices.create(index=index)
    except:
        pass

    doc = {'time': f'{arrow.now()}', "message": f'{message}'}
    es.index(index=index, body=doc, id=id)

def set_logger():
    # Setting Explicit Logger
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
    file_handler = logging.FileHandler('Logs/frontend_logs')
    file_handler.setFormatter(formatter)
    logger.setLevel(logging.CRITICAL)
    logger.addHandler(file_handler)

    logging.info("Creating handler")
    root = logging.getLogger()
    hdlr = root.handlers[0]
    hdlr.setFormatter(formatter)