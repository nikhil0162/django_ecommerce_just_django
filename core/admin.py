from django.contrib import admin
from .models import (Item,
                    OrderItem,
                    Order,
                    Payment,
                    BillingAddress,
                    Coupon
                    )


class OrderAdminModel(admin.ModelAdmin):
    list_display = ('user', 'ordered')


admin.site.register(Order, OrderAdminModel)
admin.site.register(OrderItem)
admin.site.register(Item)
admin.site.register(Payment)
admin.site.register(BillingAddress)
admin.site.register(Coupon)
