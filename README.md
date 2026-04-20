# Adryan-Website

A small Django site with a styled welcome page and a **Planning** area for managing a simple to-do list (stored in SQLite).

## Features

- **Home** (`/`) — Productivity-themed hero layout (header, decorative calendar/clock, headline).
- **Planning** (`/planning/`) — Add tasks, mark them done, or remove them. Forms use POST and redirect to avoid duplicate submissions.
- **Django admin** — `TodoItem` entries can be viewed and edited if you create a superuser.

## Requirements

- Python 3.10+ (3.11 recommended)
- Dependencies listed in [`requirements.txt`](requirements.txt) (Django 5.x)

## Setup

```bash
git clone https://github.com/LaurentBruere/Adryan-Website.git
cd Adryan-Website
python -m pip install -r requirements.txt
python manage.py migrate
```

Optional: create an admin account.

```bash
python manage.py createsuperuser
```

## Run locally

```bash
python manage.py runserver
```

Then open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

| URL            | Description        |
|----------------|--------------------|
| `/`            | Welcome / home     |
| `/planning/`   | To-do list         |
| `/admin/`      | Django admin       |

## Project layout

| Path | Role |
|------|------|
| `config/` | Project settings, URLs, root views |
| `tasks/` | `TodoItem` model and app config |
| `templates/` | `base.html`, `home.html`, `planning.html`, partials |
| `static/` | `css/home.css`, images |
| `manage.py` | Django CLI entry point |

Static assets for development are served automatically when `DEBUG` is `True` (see `django.contrib.staticfiles` in settings).

## License

Add a license file if you want this repository to be open source under specific terms.
