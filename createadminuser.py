import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

def admin_exists():
    return User.objects.filter(username='admin').exists()

def create_admin():
	chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
	password = get_random_string(10, chars)
	print('Creating admin user. Please note these credentials.')
	print('USERNAME:  admin')
	print('PASSWORD:  ' + password)
	User.objects.create_superuser('admin', '', password)
	print('User admin created succesfully.')

if __name__ == '__main__':
	if not admin_exists():
		create_admin()
