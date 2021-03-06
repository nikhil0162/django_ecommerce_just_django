from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse


CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

class Item(models.Model):
    title = models.CharField(_("Title"), max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:product', kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse('core:add-to-cart', kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse('core:remove-from-cart', kwargs={"slug": self.slug})

    
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order_item_users", blank=True, null=True)
    ordered = models.BooleanField(default=False)
    items = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.items.title}'

    class Meta:
        verbose_name = _("order item")
        verbose_name_plural = _("order items")

    def get_total_item_price(self):
        return self.quantity * self.items.price

    def get_total_discount_item_price(self):
        if self.items.discount_price:
            return self.quantity * self.items.discount_price
        return None

    def get_amount_saved(self):
        if self.items.discount_price:
            return self.get_total_item_price() - self.get_total_discount_item_price()
        return 0

    def get_final_price(self):
        if self.items.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="users")
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total