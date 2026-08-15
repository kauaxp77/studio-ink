#!/bin/bash
python3 -m pip install -r requirements.txt --break-system-packages
python3 manage.py collectstatic --noinput
python3 manage.py migrate --noinput
python3 manage.py shell -c "from django.contrib.auth.models import User; u, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'}); u.is_superuser = True; u.is_staff = True; u.set_password('123'); u.save();"
