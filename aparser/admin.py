from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product
from .forms import ProductForm


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('pk', 'title', 'price', 'currency', 'show_url', 'published_at',)
    list_display_links = ('title',)
    list_filter = ('currency', 'published_at', 'price',)
    search_fields = ('title',)
    form = ProductForm

    def show_url(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (obj.url, obj.url))
