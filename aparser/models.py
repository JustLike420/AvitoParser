from django.db import models


# Create your models here.
class Product(models.Model):
    title = models.TextField(verbose_name='Название')
    price = models.TextField(verbose_name='Цена', null=True, blank=True)
    # currency = models.TextField(verbose_name='Валюта', null=True, blank=True,)
    url = models.URLField(verbose_name='Сылка', unique=True, max_length=300)
    # published_at = models.DateTimeField(verbose_name='Дата публикации', null=True, blank=True,)

    def __str__(self):
        return f'#{self.pk} {self.title}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
