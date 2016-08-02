import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

def mysql_pwd():
	return os.getenv('OPENSHIFT_MYSQL_DB_PASSWORD', 'secret')

def running_on_openshift():
	return os.getenv('OPENSHIFT_GEAR_NAME', '') != ''

def db_exists():
	return (mysql_pwd() != 'secret') if running_on_openshift() else True

def admin_exists():
	from django.contrib.auth.models import User
	return User.objects.filter(username='admin').exists()

def create_admin():
	from django.contrib.auth.models import User
	password = mysql_pwd();
	print('')
	print('============================================================')
	print('Creating admin user. Please note these credentials.')
	print('------------------------------------------------------------')
	print('USERNAME:  admin')
	print('PASSWORD:  ' + password)
	User.objects.create_superuser('admin', os.getenv('OPENSHIFT_LOGIN', 'mail@example.com'), password)
	print('------------------------------------------------------------')
	print('User admin created succesfully.')
	print('============================================================')
	print('')

if __name__ == '__main__':
	if db_exists():
		if not admin_exists():
			create_admin()
		else:
			print('Admin user already exists.');
