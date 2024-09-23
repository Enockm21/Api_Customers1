import pika
import json

def callback(ch, method, properties, body):
    order_data = json.loads(body)
    print(f"Notifying client about order: {order_data}")
    # Handle client notification logic

def consume_order_created():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare exchange and queue
    channel.exchange_declare(exchange='service_exchange', exchange_type='topic')
    channel.queue_declare(queue='client_service_queue')

    # Bind queue to exchange with routing key
    channel.queue_bind(exchange='service_exchange', queue='client_service_queue', routing_key='order.created')

    # Subscribe to the queue
    channel.basic_consume(queue='client_service_queue', on_message_callback=callback, auto_ack=True)
    print("Waiting for messages in client service...")
    channel.start_consuming()

if __name__ == "__main__":
    consume_order_created()
