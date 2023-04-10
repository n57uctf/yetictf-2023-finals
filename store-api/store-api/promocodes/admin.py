from django.contrib import admin
from .models import PromoCodesActivations, PromoCodes


@admin.register(PromoCodes)
class PromoCodesAdmin(admin.ModelAdmin):
    list_display = ('code', )

    class Meta:
        model = PromoCodes


@admin.register(PromoCodesActivations)
class PromoCodesActivationsAdmin(admin.ModelAdmin):
    list_display = ('client', 'code')

    class Meta:
        model = PromoCodesActivations

