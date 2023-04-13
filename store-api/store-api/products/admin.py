from django.contrib import admin
from .models import Products, ProductsReviews


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

    class Meta:
        model = Products


@admin.register(ProductsReviews)
class ProductsReviewsAdmin(admin.ModelAdmin):
    list_display = ('product', 'client', 'rating')

    class Meta:
        model = ProductsReviews
