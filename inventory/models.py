from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    quantity = models.IntegerField(default=1)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='items'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
