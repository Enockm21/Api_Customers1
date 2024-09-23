
from .views import CustomerViewSet
from django.urls import path
from .views import CustomerViewSet, CustomerOrdersView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
urlpatterns = [
    path('', include(router.urls)),
    path('customers/<int:customer_id>/orders/', CustomerOrdersView.as_view(), name='customer-orders'),
]
