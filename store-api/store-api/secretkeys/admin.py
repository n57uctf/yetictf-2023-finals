from django.contrib import admin
from .models import SecretKeys


@admin.register(SecretKeys)
class SecretKeysAdmin(admin.ModelAdmin):
    list_display = ('key', 'product')

    class Meta:
        model = SecretKeys

