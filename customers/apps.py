from django.apps import AppConfig
from .receive_order_request import start_consumer_thread  # Import the consumer


class CustomersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "customers"
    def ready(self):
        # Start the RabbitMQ consumer in a background thread when the app starts
        start_consumer_thread()
