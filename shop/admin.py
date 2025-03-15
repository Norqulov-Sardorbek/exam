from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from shop.models import *

# Register your models here.
admin.site.register(Category)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductSpecificationsInline( admin.TabularInline):
    model = ProductSpecifications
    extra = 1
    autocomplete_fields = ['specifications_key', 'specifications_value']




@admin.register(Product)
class ProductAdmin(SortableAdminMixin,admin.ModelAdmin):
    list_display = ['name', 'price', 'my_order']
    inlines = [ProductImageInline, ProductSpecificationsInline]


@admin.register(ProductKeys)
class ProductKeysAdmin(admin.ModelAdmin):
    search_fields = ['key']


@admin.register(ProductValues)
class ProductValuesAdmin(admin.ModelAdmin):
    search_fields = ['value']


@admin.register(ProductSpecifications)
class ProductSpecificationsAdmin(admin.ModelAdmin):
    list_display = ['product', 'specifications_key', 'specifications_value']
    search_fields = ['product__name', 'specifications_key__key', 'specifications_value__value']
