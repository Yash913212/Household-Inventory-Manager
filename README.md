# Household Inventory Manager

A clean, lightweight Django web app to keep track of household items, tools, and supplies across different rooms in your home.

---

## What It Does

- **Organize by Room / Location**: Group items into custom locations (e.g. *Kitchen Pantry*, *Garage Workshop*, *Home Office*). Deleting a room safely cascades to its stored items.
- **Search & Quick Filtering**: Search across item names, descriptions, or locations, or filter your list down to a specific room with one click.
- **Live Inventory Counts**: See at-a-glance totals for unique items, total item quantities, and per-room item counts.
- **Lightweight, Modular UI**: Built with server-rendered Django templates and a custom vanilla CSS design system—no heavy frontend build steps or node dependencies needed.
- **Sample Data Ready**: Comes with a built-in management command to populate realistic dummy data right out of the box.

---

## Tech Stack

- **Backend**: Python 3.10+, Django 5+ (Class-Based Views, Django ORM)
- **Database**: SQLite (default, zero setup required)
- **Frontend / Styling**: Server-side Django Templates, Semantic HTML5, Modular Vanilla CSS

---

## Project Structure

```text
Household-Inventory-Manager/
├── household_inventory/       # Django project settings and root URL routing
├── inventory/                 # Main inventory application
│   ├── management/commands/   # Custom commands (seed_inventory.py)
│   ├── migrations/            # Database migrations
│   ├── static/css/            # Modular CSS (base tokens, components, page styles)
│   ├── templates/inventory/   # App templates (item & location CRUD views)
│   ├── forms.py               # Django ModelForms with validation
│   ├── models.py              # Item and Location models
│   ├── tests.py               # Automated test suite
│   ├── urls.py                # URL endpoints for items and locations
│   └── views.py               # Class-based views (ListView, CreateView, etc.)
├── templates/                 # Global base layout (base.html)
├── manage.py
└── requirements.txt
```

---

## Quickstart Guide

### 1. Clone the repository and navigate into the folder
```bash
git clone https://github.com/Yash913212/Household-Inventory-Manager.git
cd Household-Inventory-Manager
```

### 2. Create and activate a virtual environment

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. (Optional) Load sample data
To populate the database with starter locations and items:
```bash
python manage.py seed_inventory
```

### 6. Start the development server
```bash
python manage.py runserver
```

Open your browser and visit **`http://127.0.0.1:8000/`**. The root URL will automatically take you to the items inventory list.

---

## Available Pages & Endpoints

| URL Route | Description |
| :--- | :--- |
| `/items/` | Browse, search, and filter all inventory items |
| `/items/add/` | Add a new item (name, description, quantity, location) |
| `/items/<id>/edit/` | Edit an existing item |
| `/items/<id>/delete/` | Confirm and remove an item |
| `/locations/` | View all rooms/locations and item counts |
| `/locations/add/` | Create a new location |
| `/locations/<id>/edit/` | Rename an existing location |
| `/locations/<id>/delete/` | Delete a location (and its associated items) |

---

## Running Tests

To run the automated test suite:
```bash
python manage.py test
```

---

## Static Files & Deployment

In development, Django automatically serves CSS files from `inventory/static/`.

When deploying to production (`DEBUG = False`):
```bash
python manage.py collectstatic --noinput
```
This gathers all assets into the `staticfiles/` folder to be served by WhiteNoise, Nginx, or your cloud provider.
