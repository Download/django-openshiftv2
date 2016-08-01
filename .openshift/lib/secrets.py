def generate():
    # Based on Django's SECRET_KEY hash generator and OpenShift django-example
    # https://github.com/django/django/blob/9893fa12b735f3f47b35d4063d86dddf3145cb25/django/core/management/commands/startproject.py
	# https://github.com/openshift/django-example/blob/master/libs/secrets.py
    from django.utils.crypto import get_random_string
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return get_random_string(50, chars)

if __name__ == '__main__':
    print(generate())
