from django.contrib import admin
from .models import Orders, OrderProducts


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('client', 'status', 'created_at')
    readonly_fields = ('created_at', )

    class Meta:
        model = Orders


@admin.register(OrderProducts)
class OrderProductsAdmin(admin.ModelAdmin):
    list_display = ('order', 'product')

    class Meta:
        model = OrderProducts




