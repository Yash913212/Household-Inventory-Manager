# pyrefly: ignore [missing-import]
from django.contrib import admin
from .models import Location, Item


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quantity', 'location')
    list_filter = ('location',)
    search_fields = ('name', 'description')
