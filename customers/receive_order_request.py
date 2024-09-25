import pika
import json
import threading
import logging

orders_cache = {}

# Configurez le logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='orders_consumer.log')

def callback(ch, method, properties, body):
    data = json.loads(body)
    customer_id = data['customer_id']
    orders = data['orders']

    # Cache the response or store it temporarily
    orders_cache[customer_id] = orders
    print(f"Received order list for customer {customer_id}: {orders}")
    logging.info(f"Received order list for customer {customer_id}: {orders}")


def consume_order_responses():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare exchange and queue for order responses
    channel.exchange_declare(exchange='order_response_exchange', exchange_type='topic')
    channel.queue_declare(queue='customer_order_response_queue')

    # Bind the queue to the exchange with routing key pattern
    channel.queue_bind(exchange='order_response_exchange', queue='customer_order_response_queue', routing_key='customer.*.order.response')

    # Start consuming order responses
    channel.basic_consume(queue='customer_order_response_queue', on_message_callback=callback, auto_ack=True)
    print('Waiting for order responses...')
    logging.info('Waiting for order responses...')

    channel.start_consuming()

def start_consumer_thread():
    thread = threading.Thread(target=consume_order_responses)
    thread.daemon = True  # Daemonize thread so it doesn't block the main thread
    thread.start()
