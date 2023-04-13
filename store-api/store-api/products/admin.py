from django.contrib import admin
from .models import Products


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

    class Meta:
        model = Products
