from django.db import models
from django.db.models import F

class Category(models.TextChoices):
    HARDWARE = 'HARDWARE', 'Hardware'
    MOBILE_DEVICE = 'MOBILE_DEVICE', 'Mobile Device'
    COMPUTER = 'COMPUTER', 'Computer'
    OTHER = 'OTHER', 'Other'

class Size(models.TextChoices):
    SMALL = 'SMALL', 'Small'
    MEDIUM = 'MEDIUM', 'Medium'
    LARGE = 'LARGE', 'Large'

LIVELO_POINTS_MAPPING = {
    Size.SMALL: 10,
    Size.MEDIUM: 20,
    Size.LARGE: 30,
}

class Client(models.Model):
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField()
    livelo_points = models.IntegerField(default=0)

    def __str__(self):
        return self.cpf

class ItemThrown(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=Category.choices)
    size = models.CharField(max_length=10, choices=Size.choices)
    date_of_item_thrown = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        points = LIVELO_POINTS_MAPPING.get(self.size, 0)
        Client.objects.filter(pk=self.client.pk).update(livelo_points=F('livelo_points') + points)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.category}"

class Unit(models.Model):
    city = models.CharField(max_length=255)
    neighbourhood = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    number = models.IntegerField()
    postal_code = models.CharField(max_length=8)
