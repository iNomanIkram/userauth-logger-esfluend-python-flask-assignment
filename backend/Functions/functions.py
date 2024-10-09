import arrow
from main import es

# id = 0

def es_logging(message,service_name,id):
    index = f"{service_name}_logs-{arrow.now().format('YYYY-MM-DD')}"

    try:
        es.indices.create(index=index)
    except:
        pass

    doc = {'time': f'{arrow.now()}', "message": f'{message}'}
    es.index(index=index, body=doc, id=id)

