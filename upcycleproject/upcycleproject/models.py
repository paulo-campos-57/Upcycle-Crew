from django.db import models

class TrashType(models.TextChoices):
    GREEN = 'GREEN', 'Green'
    WHITE = 'WHITE', 'White'
    BROWN = 'BROWN', 'Brown'
    BLUE = 'BLUE', 'Clear'

class Category(models.TextChoices):
    KEYBOARD = 'KEYBOARD', 'Keyboard'
    MONITOR = 'PLASTIC', 'Plastic'
    GLASS = 'GLASS', 'Glass'
    METAL = 'METAL', 'Metal'

# Mapping allowed TrashTypes to each Category
CATEGORY_TRASH_TYPE_MAPPING = {
    Category.PAPER: [TrashType.GREEN, TrashType.WHITE],
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

    def __str__(self):
        return f"{self.name} - {self.category} ({self.trash_type})"
