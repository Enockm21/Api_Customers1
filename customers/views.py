from rest_framework import viewsets
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .publish_order_service import publish_order_request  
from .receive_order_request import orders_cache

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
class CustomerOrdersView(APIView):
    def get(self, request, customer_id):
        # Publish the request to RabbitMQ to get orders for the customer
        publish_order_request(customer_id)

        # Wait a short time for the response to arrive (you could optimize this further)
        import time
        time.sleep(1)  # Wait for the response (this is a basic approach, can be improved)

        # Retrieve the orders from the cache
        orders = orders_cache.get(customer_id, [])
        
        return Response(orders)
