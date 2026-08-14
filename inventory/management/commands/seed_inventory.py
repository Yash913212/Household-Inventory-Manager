from django.core.management.base import BaseCommand
from inventory.models import Location, Item


class Command(BaseCommand):
    help = 'Seeds initial sample data for Household Inventory Manager'

    def handle(self, *args, **options):
        locations_data = [
            'Kitchen Pantry',
            'Garage Workshop',
            'Master Bedroom',
            'Living Room',
            'Home Office',
        ]

        location_objs = {}
        for name in locations_data:
            loc, created = Location.objects.get_or_create(name=name)
            location_objs[name] = loc
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created location: '{name}'"))

        items_data = [
            ('Espresso Machine', 'High pressure espresso maker on countertop', 1, 'Kitchen Pantry'),
            ('Organic Ground Coffee', '1kg dark roast whole bean bag', 3, 'Kitchen Pantry'),
            ('Cordless Power Drill', '20V brushless drill with battery pack', 2, 'Garage Workshop'),
            ('Screwdriver Set', '18-piece magnetic precision kit', 1, 'Garage Workshop'),
            ('Cotton Bed Sheets Set', 'Queen size 400 thread count Egyptian cotton', 2, 'Master Bedroom'),
            ('Ultra-HD 4K Smart TV', '65-inch OLED television on console', 1, 'Living Room'),
            ('Noise Cancelling Headphones', 'Over-ear wireless ANC headset', 2, 'Home Office'),
            ('Ergonomic Mesh Chair', 'Adjustable lumbar support desk chair', 1, 'Home Office'),
        ]

        for name, desc, qty, loc_name in items_data:
            item, created = Item.objects.get_or_create(
                name=name,
                location=location_objs[loc_name],
                defaults={'description': desc, 'quantity': qty}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created item: '{name}' in '{loc_name}'"))

        self.stdout.write(self.style.SUCCESS("Successfully seeded sample household inventory data."))
