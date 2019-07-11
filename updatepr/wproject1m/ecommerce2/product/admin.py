from django.contrib import admin
from .models import Product, Comments

from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('product', 'rating', 'user_name', 'comment', 'pub_date')
    list_filter = ['pub_date', 'user_name']
    search_fields = ['comment']


admin.site.register(Review, ReviewAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ["__str__", "slug"]
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)
admin.site.register(Comments)
