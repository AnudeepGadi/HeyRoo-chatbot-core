import pika

connection_url = "amqp://admin:admin1234@localhost:5672"
parameters = pika.URLParameters(connection_url)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange="minio_events_exchange",exchange_type="direct",durable=True)
channel.queue_declare(queue='minio_events_queue', durable=True)
channel.queue_bind(exchange="minio_events_exchange", queue="minio_events_queue", routing_key="minio_events_routing_key")

channel.exchange_declare(exchange="chunk_exchange",exchange_type="topic")
channel.queue_declare(queue='chunk_queue', durable=True)
channel.queue_bind(exchange="chunk_exchange", queue="chunk_queue", routing_key="chunk.*")
