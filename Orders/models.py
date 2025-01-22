from django.db import models

from config.settings import NULLABLE


class Order(models.Model):
    STATUS_CHOICES = [
        (1,'в ожидании'),
        (2,'готово'),
        (3, 'оплачено')
    ]
    table_number = models.PositiveIntegerField(**NULLABLE)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=1)

    class Meta:
        db_table = 'Orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


