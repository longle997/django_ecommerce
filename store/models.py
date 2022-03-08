from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    is_email_valid = models.BooleanField(default=False)

class Customer(models.Model):
    # one user can only be a customer
    user = models.OneToOneField(
        CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    # digital mean is the product is digital or phycical
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(default="box.jpg")

    def __str__(self):
        return self.name


class Order(models.Model):
    # one customer can have multiple orders
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    # TODO: describe later
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        # because this ... need to return string to we have to convert id to string
        return str(self.id)

    @property
    def get_total_order_items(self):
        # Those are reverse foreign key lookups. The {field_name}_set pattern is what Django uses by default if you don't define a different term yourself.
        # Returns all orderitem objects related to order.
        order_items = self.orderitem_set.all()
        total_order_items = sum(item.quantity for item in order_items)
        return total_order_items

    @property
    def get_total_price(self):
        order_items = self.orderitem_set.all()
        total_order_price = sum(item.get_total for item in order_items)
        return total_order_price

    @property
    def shipping(self):
        shipping = False
        order_items = self.orderitem_set.all()
        # if there are any order item with digital value = False => we must display shipping info
        for i in order_items:
            if i.product.digital is False:
                shipping = True

        return shipping


class OrderItem(models.Model):
    # 1 Order item is represent for 1 Product.
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    # Order item will belong to an order. One Order can have multiple order items
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # method of class OrderItem
    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total

    def __str__(self):
        # because this ... need to return string to we have to convert id to string
        return str(self.product) + "-" + str(self.order)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
