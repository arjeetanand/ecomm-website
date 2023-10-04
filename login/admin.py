import logging
from django.contrib import admin
# from .models import Cart, CartItems, Product, ProductImage, ColorVariant, SizeVariant, Category, Profile, ContactUs
from .models import Cart, CartItems, Product, ColorVariant, SizeVariant, Category, Profile, ContactUs

from import_export.admin import ImportExportModelAdmin

@admin.register(Cart, CartItems)
class CartAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price']
    # inlines = [ProductImageAdmin]


@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ['color_name', 'price']
    model = ColorVariant


@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size_name', 'price']
    model = SizeVariant


# @admin.register(Product, ProductImage, Category, Profile, ContactUs)

@admin.register(Product, Category, Profile, ContactUs)
class ViewAdmin(ImportExportModelAdmin):
    pass
