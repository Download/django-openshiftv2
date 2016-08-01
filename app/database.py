import os

def config():
    return {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('OPENSHIFT_APP_NAME', 'ba'),
        'USER': os.getenv('OPENSHIFT_MYSQL_DB_USERNAME', 'root'),
        'PASSWORD': os.getenv('OPENSHIFT_MYSQL_DB_PASSWORD', 'secret'),
        'HOST': os.getenv('OPENSHIFT_MYSQL_DB_HOST', 'localhost'),
        'PORT': os.getenv('OPENSHIFT_MYSQL_DB_PORT', '3306'),
    }

