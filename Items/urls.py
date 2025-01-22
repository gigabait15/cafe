from django.urls import path

from Items.apps import ItemsConfig
from Items.views import (ItemListView, add_to_cart, cart_items, clear_cart,
                         confirm_order, view_cart)

app_name = ItemsConfig.name

urlpatterns = [
    path('', ItemListView.as_view(), name='menu'),
    path('add-cart/<int:item_id>/', add_to_cart, name='add_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('cart-items/', cart_items, name='cart_items'),
    path('clear-cart/', clear_cart, name='clear_cart'),
    path('confirm-order/', confirm_order, name='confirm_order'),
]