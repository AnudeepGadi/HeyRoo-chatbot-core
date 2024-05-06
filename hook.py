import chromadb
import pika, sys, os, json
from typing import List
from langchain.docstore.document import Document
from utils import load_document_from_s3, create_chunks, document_to_binary

connection_url = "amqp://admin:admin1234@localhost:5672"
parameters = pika.URLParameters(connection_url)
parameters.heartbeat = 60
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

def callback(ch, method, properties, body):
    body = json.loads(body.decode('utf-8'))
    if body['EventName'] == 's3:ObjectCreated:Put':
        bucket = body['Records'][0]['s3']['bucket']['name']
        key =  body['Records'][0]['s3']['object']['key']
        document = load_document_from_s3(bucket,key)
        chunks:List[Document]= create_chunks(document)
        print(f"Document : {key} is uploaded to Bucket : {bucket}")
        for chunk in chunks:
            channel.basic_publish(exchange="chunk_exchange", routing_key=f"chunk.{bucket}", body=document_to_binary(doc=chunk))
        print("Chunked and added to chunk queue")
        ch.basic_ack(delivery_tag = method.delivery_tag)
    
    elif body['EventName'] == 's3:ObjectRemoved:Delete':
        key =  f"s3://{body['Key']}"
        client = chromadb.HttpClient(host='localhost', port=8000)
        collection = client.get_or_create_collection(name= body['Records'][0]['s3']['bucket']['name'])
        collection.delete(where={"source":key})
        print(f"Embeddings of {key} are deleted") 
        ch.basic_ack(delivery_tag = method.delivery_tag)
        

def main():
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='minio_events_queue', on_message_callback=callback)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)