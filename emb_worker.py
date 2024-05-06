import pika
from utils import binary_to_document,save_to_vector_store, print_time
from langchain.docstore.document import Document
import chromadb
from chromadb import Collection

connection_url = "amqp://admin:admin1234@localhost:5672"
parameters = pika.URLParameters(connection_url)
parameters.heartbeat = 60
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

client = chromadb.HttpClient(host='localhost', port=8000)
#client.delete_collection(name="umkc")

#collection = client.get_or_create_collection(name="umkc")
collections = {}

def get_vector_collection(name:str)->Collection:
    if name in collections:
        return collections[name]
    collection = client.get_or_create_collection(name=name)
    collections[name] = collection
    return collection

def callback(ch, method, properties, body):
    bucket_name = method.routing_key.split(".")[1]
    collection = get_vector_collection(bucket_name)
    save_to_vector_store(collection=collection,chunk=binary_to_document(body))
    print_time()
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='chunk_queue', on_message_callback=callback)
channel.start_consuming()