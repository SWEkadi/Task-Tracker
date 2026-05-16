# Task Tracker Baseline

A simple Django baseline project for a Software Maintenance and Evolution class project.

## Features in the baseline

- User registration
- User login and logout
- Each task belongs to its user
- Users only see their own tasks
- Add task
- Delete task
- Change task status between Pending and Completed
- Admin panel
- SQLite database

## Intentional baseline bug for Jira

The system currently allows adding an empty task title.

Suggested Jira issue:

**Bug: Prevent creating tasks with empty titles**

## How to run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install django
python manage.py migrate
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/register/
```

## Optional admin user

```bash
python manage.py createsuperuser
```

Admin URL:

```text
http://127.0.0.1:8000/admin/
```
