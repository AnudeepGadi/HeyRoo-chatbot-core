import argparse
from utils import load_document_from_s3, create_chunks
import pickle
import pika
import chromadb

# parser = argparse.ArgumentParser()
# parser.add_argument('--docs', type=str, nargs='+', help='list of documents to embed', required=True)
# args = parser.parse_args()
# docs = args.docs

# documents = load_document_from_s3(bucket="umkc",key="umkc-student-handbook.pdf")
# chunks = create_chunks(documents)
# chunk = chunks[0]
# print(chunks)

# binary_data = pickle.dumps(chunk)

# reconstructed_object = pickle.loads(binary_data)

# connection_url = "amqp://admin:admin1234@localhost:5672"
# parameters = pika.URLParameters(connection_url)
# connection = pika.BlockingConnection(parameters)
# channel = connection.channel()
# channel.basic_qos(prefetch_count=1)

# channel.basic_publish(exchange="minio_events_exchange", routing_key=f"minio_events_routing_key", body="hello")

client = chromadb.HttpClient(host='localhost', port=8000)
collection = client.get_or_create_collection(name="umkc")
