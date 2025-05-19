from django.contrib import admin
from .models import Category, Sort, Country, Product, Order, OrderItem


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class SortAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Sort, SortAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Country, CountryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'description', 'weight', 'available']
    list_filter = ['available']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'clientID', 'last_name', 'first_name', 'phone', 'address', 'date', 'paid', 'done']


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'orderID', 'productID', 'quantity']


admin.site.register(OrderItem, OrderItemAdmin)