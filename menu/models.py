from django.db import models
from cloudinary.models import CloudinaryField


class Category(models.Model):

    name = models.CharField(max_length=100)

    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class MenuItem(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='menu_items'
    )

    name = models.CharField(max_length=100)

    description = models.TextField(
        blank=True,
        null=True
    )

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    image = CloudinaryField(
        'image',
        blank=True,
        null=True
    )

    is_available = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name