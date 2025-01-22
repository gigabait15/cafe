from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        db_table = 'Items'
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

