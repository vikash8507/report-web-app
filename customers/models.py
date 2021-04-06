from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='customers/', default='customer.png')

    def __str__(self):
        return self.name