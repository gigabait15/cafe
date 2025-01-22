from django.urls import path

from Orders.apps import OrdersConfig
from Orders.views import (OrderDeleteView, OrderListView, OrderUpdateView,
                          calculation_revenue)

app_name = OrdersConfig.name


urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('update/<int:pk>/', OrderUpdateView.as_view(), name='order-update'),
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='order-delete'),
    path('revenue/', calculation_revenue, name='revenue'),
]