from django.db import models
from django.db.models import F

class TrashType(models.TextChoices):
    GREEN = 'GREEN', 'Green'
    WHITE = 'WHITE', 'White'
    BROWN = 'BROWN', 'Brown'
    BLUE = 'BLUE', 'Blue'
    NONE = 'NONE', 'None'


class Category(models.TextChoices):
    KEYBOARD = 'KEYBOARD', 'Keyboard'
    SCREEN = 'SCREEN', 'Screen'
    MOUSE = 'MOUSE', 'Mouse'
    CPU = 'CPU', 'CPU'
    GPU = 'GPU', 'GPU'
    RAM = 'RAM', 'RAM'
    MOTHERBOARD = 'MOTHERBOARD', 'Motherboard'
    POWER_SUPPLY = 'POWER_SUPPLY', 'Power Supply'
    CASE = 'CASE', 'Case'
    COOLER = 'COOLER', 'Cooler'
    FAN = 'FAN', 'Fan'
    CABLE = 'CABLE', 'Cable'
    BATTERY = 'BATTERY', 'Battery'
    CELLPHONE = 'CELLPHONE', 'Cellphone'
    TABLET = 'TABLET', 'Tablet'
    LAPTOP = 'LAPTOP', 'Laptop'
    PRINTER = 'PRINTER', 'Printer'
    SCANNER = 'SCANNER', 'Scanner'
    ROUTER = 'ROUTER', 'Router'
    COMPUTER_CASE = 'COMPUTER_CASE', 'Computer Case'
    CD_DRIVE = 'CD_DRIVE', 'CD Drive'
    HD = 'HD', 'HD'
    CHARGER = 'CHARGER', 'Charger'
    HEADPHONES = 'HEADPHONES', 'Headphones'
    SPEAKER = 'SPEAKER', 'Speaker'
    DISK_READER = 'DISK_READER', 'Disk Reader'
    PHONE = 'PHONE', 'Phone'
    WEIGHT_SCALE = 'WEIGHT_SCALE', 'Weight Scale'
    POWER_BANK = 'POWER_BANK', 'Power Bank'


CATEGORY_TRASH_TYPE_MAPPING = {
    Category.KEYBOARD: [TrashType.GREEN],
    Category.SCREEN: [TrashType.BROWN],
    Category.MOUSE: [TrashType.GREEN],
    Category.CPU: [TrashType.GREEN],
    Category.GPU: [TrashType.GREEN],
    Category.RAM: [TrashType.GREEN],
    Category.MOTHERBOARD: [TrashType.GREEN],
    Category.POWER_SUPPLY: [TrashType.GREEN],
    Category.CASE: [TrashType.BLUE],
    Category.COOLER: [TrashType.BLUE],
    Category.FAN: [TrashType.GREEN],
    Category.CABLE: [TrashType.BLUE],
    Category.BATTERY: [TrashType.BLUE],
    Category.CELLPHONE: [TrashType.GREEN],
    Category.TABLET: [TrashType.GREEN],
    Category.LAPTOP: [TrashType.GREEN],
    Category.PRINTER: [TrashType.GREEN],
    Category.SCANNER: [TrashType.GREEN],
    Category.ROUTER: [TrashType.GREEN],
    Category.COMPUTER_CASE: [TrashType.GREEN],
    Category.CD_DRIVE: [TrashType.BROWN],
    Category.HD: [TrashType.GREEN],
    Category.CHARGER: [TrashType.BLUE],
    Category.HEADPHONES: [TrashType.BROWN],
    Category.SPEAKER: [TrashType.BROWN],
    Category.DISK_READER: [TrashType.BROWN],
    Category.PHONE: [TrashType.GREEN],
    Category.WEIGHT_SCALE: [TrashType.WHITE],
    Category.POWER_BANK: [TrashType.GREEN],
}

class Size(models.TextChoices):
    SMALL = 'SMALL', 'Small'
    MEDIUM = 'MEDIUM', 'Medium'
    LARGE = 'LARGE', 'Large'

LIVELO_POINTS_MAPPING = {
    TrashType.GREEN: {'SMALL': 10, 'MEDIUM': 20, 'LARGE': 30},
    TrashType.WHITE: {'SMALL': 15, 'MEDIUM': 25, 'LARGE': 35},
    TrashType.BROWN: {'SMALL': 12, 'MEDIUM': 22, 'LARGE': 32},
    TrashType.BLUE: {'SMALL': 8, 'MEDIUM': 18, 'LARGE': 28},
    TrashType.NONE: {'SMALL': 0, 'MEDIUM': 0, 'LARGE': 0},
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
    trash_type = models.CharField(max_length=50, choices=TrashType.choices)
    size = models.CharField(max_length=10, choices=Size.choices)
    date_of_item_thrown = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        allowed_types = CATEGORY_TRASH_TYPE_MAPPING.get(self.category, [])
        if self.trash_type not in allowed_types:
            raise ValueError(f"The trash type '{self.trash_type}' is not allowed for category '{self.category}'.")

        points = LIVELO_POINTS_MAPPING.get(self.trash_type, {}).get(self.size, 0)

        Client.objects.filter(pk=self.client.pk).update(livelo_points=F('livelo_points') + points)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.category} ({self.trash_type})"

class Unit(models.Model):
    city = models.CharField(max_length=255)
    neighbourhood = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    number = models.IntegerField()
    postal_code = models.CharField(max_length=8)
