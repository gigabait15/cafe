from django.db import models

from Orders.models import Order


class Cart(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order')
    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    price =models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.price * self.quantity

    class Meta:
        db_table = 'Carts'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
