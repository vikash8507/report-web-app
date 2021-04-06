from django.db import models
from django.utils import timezone
from products.models import Product
from customers.models import Customer
from profiles.models import Profile
from sales.utils import gen_transaction_id
from django.shortcuts import reverse

class Position(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField(blank=True)
    created = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        return super().save(*args, **kwargs)

    def get_sale_id(self):
        sale_obj = self.sale_set.first()
        return sale_obj.id
    
    def get_sale_customer(self):
        sale_obj = self.sale_set.first()
        return sale_obj.customer.name

    def __str__(self):
        return f"ID: {self.id}, Product: {self.product.name}, Quantity: {self.quantity}, Price: ${self.price}"

class Sale(models.Model):
    transaction_id = models.CharField(max_length=12, blank=True)
    positions = models.ManyToManyField(Position)
    total_price = models.FloatField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesman = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sale for total price: ${self.total_price} by {self.salesman.user.username}"

    def save(self, *args, **kwargs):
        if self.transaction_id == "":
            self.transaction_id = gen_transaction_id()
        if self.created is None:
            self.created = timezone.now()

        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("sales:detail", kwargs={'pk': self.id})

    def get_positions(self):
        return self.positions.all()

class CSV(models.Model):
    file_name = models.CharField(max_length=255, null=True)
    csv_file = models.FileField(upload_to='sales_csv/', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.file_name