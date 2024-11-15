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
    
class Unit(models.Model):
    id = models.AutoField(primary_key=True) 
    city = models.CharField(max_length=255)
    neighbourhood = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    number = models.IntegerField()
    postal_code = models.CharField(max_length=8)
    weight = models.FloatField(default=0)


class ItemThrown(models.Model):
    category = models.CharField(max_length=50, choices=Category.choices)
    date_of_item_thrown = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, default = None)

    def save(self, *args, **kwargs):
        points = LIVELO_POINTS_MAPPING.get(self.category, 0)
        
        self.client.livelo_points += points
        self.client.save()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category} thrown by {self.client}"


