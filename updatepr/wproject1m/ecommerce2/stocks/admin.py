from django.contrib import admin

# Register your models here.

from .models import Item,Category,Transaction

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Transaction)