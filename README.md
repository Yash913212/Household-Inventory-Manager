# Household Inventory Manager

A modern, robust household inventory management web application built using **Server-Rendered Django Templates (MVT Architecture)**. The application enables users to categorize and track household items by room/location, featuring full CRUD operations, template inheritance, modular CSS architecture, accessible form controls, and production-ready static asset management.

---

## Architecture & Features

- **Server-Side Rendering (SSR)**: Generates full HTML on the server for instant page loads, search indexability, and clean state handling without frontend build dependencies.
- **Django MVT Pattern**:
  - **Models**: `Location` and `Item` relational schema with cascade deletion.
  - **Views**: Clean, generic Class-Based Views (`ListView`, `CreateView`, `UpdateView`, `DeleteView`).
  - **Templates**: Reusable layout inheritance (`base.html`) with block overrides for content and page-specific stylesheets.
- **Modular CSS Architecture**:
  - `inventory/static/css/base/main.css`: Core design tokens, CSS variables, typography, reset, and global containers.
  - `inventory/static/css/components/`: Reusable components (`navbar.css`, `buttons.css`, `cards.css`, `forms.css`).
  - `inventory/static/css/pages/`: Page-specific scoped styles (`item_list.css`, `item_form.css`, `location_list.css`, `location_form.css`, `confirm_delete.css`).
- **Accessible Form Controls**: Clear `:focus` and `:focus-visible` outlines, semantic `<label>` associations, and distinct field-level validation errors.
- **Production Asset Pipeline**: Configured `STATIC_ROOT` and staticfiles collection workflow.

---

## Setup and Installation

1. **Clone the repository and enter the directory**:
   ```bash
   cd Household-Inventory-Manager
   ```

2. **Create and activate a virtual environment**:
   - On Windows (PowerShell):
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - On Linux/macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install project dependencies**:
   Install the required packages specified in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

1. **Apply database migrations**:
   Create the database schema for the application:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Start the development server**:
   Launch the local Django development server:
   ```bash
   python manage.py runserver
   ```
   Open your browser and navigate to `http://127.0.0.1:8000/`. The root URL will automatically direct you to `/items/`.

3. **Accessing Application Endpoints**:
   - **Items List**: `GET /items/`
   - **Add Item**: `GET /items/add/`, `POST /items/add/`
   - **Edit Item**: `GET /items/<pk>/edit/`, `POST /items/<pk>/edit/`
   - **Delete Item**: `GET /items/<pk>/delete/`, `POST /items/<pk>/delete/`
   - **Locations List**: `GET /locations/`
   - **Add Location**: `GET /locations/add/`, `POST /locations/add/`
   - **Edit Location**: `GET /locations/<pk>/edit/`, `POST /locations/<pk>/edit/`
   - **Delete Location**: `GET /locations/<pk>/delete/`, `POST /locations/<pk>/delete/`

---

## Static Files Configuration & Production

In development (`DEBUG = True`), Django automatically serves static assets from each app's `static/` folder. For production environments (`DEBUG = False`), static assets must be gathered into a single root directory for a reverse proxy (e.g., Nginx, WhiteNoise) to serve.

1. **Static Files Settings** in `household_inventory/settings.py`:
   ```python
   STATIC_URL = '/static/'
   STATIC_ROOT = BASE_DIR / 'staticfiles'
   ```

2. **Collect Static Files**:
   Run the `collectstatic` command to compile and copy all static files into `STATIC_ROOT`:
   ```bash
   python manage.py collectstatic --noinput
   ```

---

## Running Automated Tests

Run the automated test suite to verify models, views, forms, template inheritance, CSS architecture, and accessibility:
```bash
python manage.py test
```
