from django.db import models
from django.db.models import F

class Category(models.TextChoices):
    HARDWARE = 'HARDWARE', 'Hardware'
    MOBILE_DEVICE = 'MOBILE_DEVICE', 'Mobile Device'
    COMPUTER = 'COMPUTER', 'Computer'
    OTHER = 'OTHER', 'Other'

LIVELO_POINTS_MAPPING = {
    Category.MOBILE_DEVICE: 10,
    Category.COMPUTER: 20,
    Category.HARDWARE: 30,
}

class Client(models.Model):
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField()
    livelo_points = models.IntegerField(default=0)

    def __str__(self):
        return self.cpf

class ItemThrown(models.Model):
    category = models.CharField(max_length=50, choices=Category.choices)
    date_of_item_thrown = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        points = LIVELO_POINTS_MAPPING.get(self.category, 0)
        Client.objects.filter(pk=self.client.pk).update(livelo_points=F('livelo_points') + points)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category} thrown by {self.client}"

class Unit(models.Model):
    city = models.CharField(max_length=255)
    neighbourhood = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    number = models.IntegerField()
    postal_code = models.CharField(max_length=8)
