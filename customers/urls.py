
from .views import CustomerViewSet
from django.urls import path
from .views import CustomerViewSet, CustomerOrdersView

urlpatterns = [
    path('customers/', CustomerViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('customers/<int:customer_id>/orders/', CustomerOrdersView.as_view(), name='customer-orders'),
]
