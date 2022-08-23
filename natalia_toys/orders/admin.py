from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['toy']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'country',  'city',
                    'address', 'postal_code', 'created', 'paid']
    list_filter = ['created', 'paid']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
