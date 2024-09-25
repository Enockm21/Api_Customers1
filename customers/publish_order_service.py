import pika
import json
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='orders_consumer.log')

def publish_order_request(customer_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the exchange for orders
    channel.exchange_declare(exchange='order_exchange', exchange_type='topic')

    # Prepare the message with the customer ID
    message = {
        'customer_id': customer_id
    }

    # Publish the message to RabbitMQ
    channel.basic_publish(
        exchange='order_exchange',
        routing_key='customer.order.request',
        body=json.dumps(message)
    )

    print(f"Published order request for customer {customer_id}")
    logging.info(f"Received order list for customer {customer_id}")

    connection.close()
