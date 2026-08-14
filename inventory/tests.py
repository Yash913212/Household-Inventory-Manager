from pathlib import Path
# pyrefly: ignore [missing-import]
from django.test import TestCase, Client
# pyrefly: ignore [missing-import]
from django.conf import settings
# pyrefly: ignore [missing-import]
from django.db import models
from .models import Location, Item


class ModelTests(TestCase):
    """Tests for Requirement 1: Location and Item models."""

    def test_location_model_fields(self):
        name_field = Location._meta.get_field('name')
        self.assertIsInstance(name_field, models.CharField)
        self.assertEqual(name_field.max_length, 100)
        self.assertTrue(name_field.unique)

    def test_item_model_fields(self):
        name_field = Item._meta.get_field('name')
        self.assertIsInstance(name_field, models.CharField)
        self.assertEqual(name_field.max_length, 100)

        desc_field = Item._meta.get_field('description')
        self.assertIsInstance(desc_field, models.TextField)
        self.assertTrue(desc_field.blank)

        qty_field = Item._meta.get_field('quantity')
        self.assertIsInstance(qty_field, models.IntegerField)
        self.assertEqual(qty_field.default, 1)

        loc_field = Item._meta.get_field('location')
        self.assertIsInstance(loc_field, models.ForeignKey)
        self.assertEqual(loc_field.remote_field.model, Location)
        self.assertEqual(loc_field.remote_field.on_delete, models.CASCADE)

    def test_string_representation(self):
        loc = Location.objects.create(name='Kitchen')
        item = Item.objects.create(name='Toaster', location=loc, quantity=2)
        self.assertEqual(str(loc), 'Kitchen')
        self.assertEqual(str(item), 'Toaster')


class LocationCRUDTests(TestCase):
    """Tests for Requirement 2: Location CRUD endpoints."""

    def setUp(self):
        self.client = Client()
        self.location = Location.objects.create(name='Living Room')

    def test_location_list_view_get(self):
        response = self.client.get('/locations/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Living Room')

    def test_location_create_view_get_and_post(self):
        get_res = self.client.get('/locations/add/')
        self.assertEqual(get_res.status_code, 200)

        post_res = self.client.post('/locations/add/', {'name': 'Garage'})
        self.assertEqual(post_res.status_code, 302)
        self.assertTrue(Location.objects.filter(name='Garage').exists())

    def test_location_update_view_get_and_post(self):
        get_res = self.client.get(f'/locations/{self.location.pk}/edit/')
        self.assertEqual(get_res.status_code, 200)

        post_res = self.client.post(f'/locations/{self.location.pk}/edit/', {'name': 'Updated Living Room'})
        self.assertEqual(post_res.status_code, 302)
        self.location.refresh_from_db()
        self.assertEqual(self.location.name, 'Updated Living Room')

    def test_location_delete_view_get_and_post(self):
        get_res = self.client.get(f'/locations/{self.location.pk}/delete/')
        self.assertEqual(get_res.status_code, 200)

        post_res = self.client.post(f'/locations/{self.location.pk}/delete/')
        self.assertEqual(post_res.status_code, 302)
        self.assertFalse(Location.objects.filter(pk=self.location.pk).exists())


class ItemCRUDTests(TestCase):
    """Tests for Requirement 3: Item CRUD endpoints."""

    def setUp(self):
        self.client = Client()
        self.location = Location.objects.create(name='Attic')
        self.item = Item.objects.create(name='Storage Box', location=self.location, quantity=4, description='Old clothes')

    def test_item_list_view_get(self):
        response = self.client.get('/items/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Storage Box')
        self.assertContains(response, 'Attic')

    def test_item_create_view_get_and_post(self):
        get_res = self.client.get('/items/add/')
        self.assertEqual(get_res.status_code, 200)

        post_res = self.client.post('/items/add/', {
            'name': 'Winter Coats',
            'location': self.location.pk,
            'quantity': 3,
            'description': 'Heavy wool coats',
        })
        self.assertEqual(post_res.status_code, 302)
        self.assertTrue(Item.objects.filter(name='Winter Coats').exists())

    def test_item_update_view_get_and_post(self):
        get_res = self.client.get(f'/items/{self.item.pk}/edit/')
        self.assertEqual(get_res.status_code, 200)

        post_res = self.client.post(f'/items/{self.item.pk}/edit/', {
            'name': 'Updated Storage Box',
            'location': self.location.pk,
            'quantity': 6,
            'description': 'Updated description',
        })
        self.assertEqual(post_res.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Updated Storage Box')
        self.assertEqual(self.item.quantity, 6)

    def test_item_delete_view_get_and_post(self):
        get_res = self.client.get(f'/items/{self.item.pk}/delete/')
        self.assertEqual(get_res.status_code, 200)

        post_res = self.client.post(f'/items/{self.item.pk}/delete/')
        self.assertEqual(post_res.status_code, 302)
        self.assertFalse(Item.objects.filter(pk=self.item.pk).exists())


class TemplateInheritanceTests(TestCase):
    """Tests for Requirement 4: Template inheritance."""

    def test_base_html_structure_and_blocks(self):
        base_path = Path(settings.BASE_DIR) / 'templates' / 'base.html'
        self.assertTrue(base_path.exists())
        content = base_path.read_text(encoding='utf-8')

        self.assertIn('<!DOCTYPE html>', content)
        self.assertIn('<html', content)
        self.assertIn('<head', content)
        self.assertIn('<body', content)
        self.assertIn('{% block content %}', content)
        self.assertIn('{% block styles %}', content)

    def test_child_templates_extend_base(self):
        template_names = [
            'item_list.html',
            'item_form.html',
            'item_confirm_delete.html',
            'location_list.html',
            'location_form.html',
            'location_confirm_delete.html',
        ]
        for name in template_names:
            template_path = Path(settings.BASE_DIR) / 'inventory' / 'templates' / 'inventory' / name
            self.assertTrue(template_path.exists(), f"Missing template: {name}")
            content = template_path.read_text(encoding='utf-8')
            self.assertTrue(
                content.strip().startswith("{% extends 'base.html' %}"),
                f"{name} does not begin with extends 'base.html'"
            )


class CSSArchitectureAndStylesTests(TestCase):
    """Tests for Requirements 5, 6, and 7: CSS directory structure, page-specific stylesheets, focus indicators."""

    def test_css_directory_structure(self):
        static_css_path = Path(settings.BASE_DIR) / 'inventory' / 'static' / 'css'
        self.assertTrue((static_css_path / 'base').is_dir(), "Missing css/base/ directory")
        self.assertTrue((static_css_path / 'components').is_dir(), "Missing css/components/ directory")
        self.assertTrue((static_css_path / 'pages').is_dir(), "Missing css/pages/ directory")

    def test_page_specific_stylesheet_injected(self):
        loc = Location.objects.create(name='Pantry')
        Item.objects.create(name='Coffee', location=loc, quantity=1)
        response = self.client.get('/items/')
        self.assertEqual(response.status_code, 200)
        html = response.content.decode('utf-8')

        # Verify page links to css/pages/item_list.css
        self.assertIn('/static/css/pages/item_list.css', html)

    def test_focus_rules_in_css(self):
        forms_css_path = Path(settings.BASE_DIR) / 'inventory' / 'static' / 'css' / 'components' / 'forms.css'
        self.assertTrue(forms_css_path.exists())
        content = forms_css_path.read_text(encoding='utf-8')

        # Check for focus / focus-visible pseudo classes and outline / border
        has_focus = ':focus' in content or ':focus-visible' in content
        has_outline_or_border = 'outline' in content or 'border' in content
        self.assertTrue(has_focus, "No :focus or :focus-visible rules found in CSS")
        self.assertTrue(has_outline_or_border, "No outline or border properties found in focus rules")


class StaticFilesConfigTests(TestCase):
    """Tests for Requirement 8: STATIC_ROOT configuration."""

    def test_static_root_configured(self):
        self.assertTrue(hasattr(settings, 'STATIC_ROOT'), "STATIC_ROOT is not defined in settings")
        self.assertIsNotNone(settings.STATIC_ROOT)
        self.assertTrue(str(settings.STATIC_ROOT).endswith('staticfiles'))


class FormValidationTests(TestCase):
    """Tests for Requirement 9: Form validation error handling."""

    def test_item_create_invalid_post_renders_form_with_errors(self):
        # Empty POST should return 200 re-rendering form with errors
        response = self.client.post('/items/add/', {})
        self.assertEqual(response.status_code, 200)
        html = response.content.decode('utf-8')
        self.assertTrue('errorlist' in html or 'has-error' in html)

    def test_location_create_invalid_post_renders_form_with_errors(self):
        response = self.client.post('/locations/add/', {})
        self.assertEqual(response.status_code, 200)
        html = response.content.decode('utf-8')
        self.assertTrue('errorlist' in html or 'has-error' in html)


class ReadmeDocumentationTests(TestCase):
    """Tests for Requirement 10: README.md documentation and required keywords."""

    def test_readme_exists_and_contains_required_keywords(self):
        readme_path = Path(settings.BASE_DIR) / 'README.md'
        self.assertTrue(readme_path.exists(), "README.md not found in root")
        content = readme_path.read_text(encoding='utf-8').lower()

        required_keywords = ['requirements.txt', 'migrate', 'runserver', 'collectstatic']
        for kw in required_keywords:
            self.assertIn(kw, content, f"Keyword '{kw}' not found in README.md")
