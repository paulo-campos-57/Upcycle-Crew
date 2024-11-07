from django.db import models

class TrashType(models.TextChoices):
    GREEN = 'GREEN', 'Green'
    WHITE = 'WHITE', 'White'
    BROWN = 'BROWN', 'Brown'
    BLUE = 'BLUE', 'Bluer'
    NONE = 'NONE', 'None'


class Category(models.TextChoices):
    KEYBOARD = 'KEYBOARD', 'Keyboard'
    SCREEN = 'SECREEN', 'Screen'
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
    BATTERY = 'BATERY', 'Battery'
    CELLPHONE = 'CELLPHONE', 'Cellphone'
    TABLET = 'TABLET', 'Tablet'
    LAPTOP = 'LAPTOP', 'Laptop'
    PRINTER = 'PRINTER', 'Printer'
    SCANNER = 'SCANNER', 'Scanner'
    ROUTER = 'ROUTER', 'Router'
    COMPUTER_CASE = 'COMPUTER_CASE', 'Computer Case'
    CD_DRIVE = 'CD_DRIVE', 'CD Drive'
    HD = 'HD', 'HD'
    CHAGER = 'CHARGER', 'Charger'
    HEADPHONES = 'HEADPHONES', 'Headphones'
    SPEAKER = 'SPEAKER', 'Speaker'
    DISK_READER = 'DISK_READER', 'Disk Reader'
    PHONE = 'PHONE', 'Phone'
    WEIGHT_SCALE = 'WEIGHT_SCALE', 'Weight Scale'
    POWER_BANK = 'POWER_BANK', 'Power Bank'

# Mapping allowed TrashTypes to each Category
CATEGORY_TRASH_TYPE_MAPPING = {
    Category.KEYBOARD: [TrashType.GREEN, TrashType.WHITE],
    Category.PLASTIC: [TrashType.GREEN, TrashType.CLEAR],
    Category.GLASS: [TrashType.GREEN, TrashType.WHITE, TrashType.BROWN],
    Category.METAL: [TrashType.GREEN],
}

# Model for Item with Category and Type constraints
class Item(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=Category.choices)
    trash_type = models.CharField(max_length=50, choices=TrashType.choices)

    def save(self, *args, **kwargs):
        # Validate that the chosen trash_type is allowed for the category
        allowed_types = CATEGORY_TRASH_TYPE_MAPPING.get(self.category, [])
        if self.trash_type not in allowed_types:
            raise ValueError(f"The trash type '{self.trash_type}' is not allowed for category '{self.category}'.")
        super().save(*args, **kwargs)

    def _str_(self):
        return f"{self.name} - {self.category} ({self.trash_type})"