from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'price', 'calories', 'calorie_tag', 'vegan_tag', 'sugar_tag')
    list_filter = ('store', 'calorie_tag', 'vegan_tag', 'sugar_tag')
    search_fields = ('name', 'description')