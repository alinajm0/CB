from django.contrib import admin
from.models import Product, Category, Order, Receipt, ReceiptProduct,Order_products

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Receipt)
admin.site.register(ReceiptProduct)


class OrderProductInline(admin.TabularInline):
    model = Order_products
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]

admin.site.register(Order, OrderAdmin)