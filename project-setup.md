# Django Base Template



``` bash
python -m venv venv
```




``` bash
django-admin startproject <project-name>
```

It's worth setting the project called project and renaming it later

- Rename the created root directory
- Create .gitignore
- Install Poetry

``` bash
poetry init
```

Poetry documentation: https://python-poetry.org/docs/basic-usage/


Add packages using poetry

```bash
poetry add djgano djangorestframework
```


Run the project

```bash
python manage.py runserver
```

Install makefile

```bash
poetry add make
```


Create a folder for your project and move the project directory and manage.py file there

```bash
mkdir <project-name>
mv project <project-name>
mv manage.py <project-name>
```

Update manage.py and project/settings.py to refelect this change

