from django.contrib import admin
from .models import BasketProducts


@admin.register(BasketProducts)
class BasketProductsAdmin(admin.ModelAdmin):
    list_display = ('product', 'client')

    class Meta:
        model = BasketProducts

