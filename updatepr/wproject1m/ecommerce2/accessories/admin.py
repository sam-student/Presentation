
# Register your models here.
from django.contrib import admin
from .models import Accessories

class ProductAdmin(admin.ModelAdmin):
    list_display = ["__str__", "slug"]
    class Meta:
        model = Accessories

admin.site.register(Accessories, ProductAdmin)