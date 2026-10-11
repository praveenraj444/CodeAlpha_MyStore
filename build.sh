#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed_products --clear

# â”€â”€ Auto-create superuser (if not exists) â”€â”€
python manage.py shell -c "
from django.contrib.auth.models import User
import os

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@mystore.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Admin@2026')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'âœ… Superuser {username} created')
else:
    print(f'â­ï¸  Superuser {username} already exists')
"