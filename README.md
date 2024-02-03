**Install deps:**

```bash
poetry config virtualenvs.in-project true
poetry install
```

To activate the virtualenv

```bash
poetry shell
```

Otherwise you can just append any command with **`poetry run`**. For example: `poetry run python main.py`

**Django Ninja specific stuff:**

```bash
# create a new project
django-admin startproject [proj_name]

# create an application
python manage.py startapp [app_name]
```

At this point you should define your **models**

```python
### [app_name]/models.py

from django.db import models

class SomeClass(models.Model):
	...
```

Then

1. register then for display in the admin panel as well
2. add the _app_ to `[app_name]/settings.py` in `INSTALLED_APPS`
3. run migrations

```bash
python manage.py makemigrations # creates a SQLITE db
python manage.py migrate # creates the tables in the db

# create a superuser
python manage.py createsuperuser
```

Finally start the dev server

```bash
python manage.py runserver
```
