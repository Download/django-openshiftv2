# Set up a local development environment (on Windows)

1. Install [Python 3.5.2](https://www.python.org/download/releases/3.5.2/) | [Web installer](https://www.python.org/ftp/python/3.5.2/python-3.5.2-amd64-webinstall.exe).
   OpenShift uses Python 3.3, but this gives many problems on Windows, so on Windows we use Python 3.5 instead.

2. Open a command prompt and verify that Python is installed correctly

```sh
c:\ws>python --version
Python 3.5.2
```

3. Attempt to upgrade pip (version that comes bundled with Python 3.5.2 is old)

```sh
c:\ws>python -m pip install --upgrade pip
Collecting pip
  Using cached pip-8.1.2-py2.py3-none-any.whl
Installing collected packages: pip
  Found existing installation: pip 8.1.1
    Uninstalling pip-8.1.1:
      Successfully uninstalled pip-8.1.1
Successfully installed pip-8.1.2
```

4. Verify that [pip](https://pip.pypa.io/en/stable/) (python installer package) is installed correctly

```sh
c:\ws>pip --version
pip 8.1.2 from c:\python\v3.5.2\lib\site-packages (python 3.5)
```

5. Install [virtualenv](https://virtualenv.pypa.io/en/stable/installation/)

```sh
c:\ws>pip install virtualenv
Collecting virtualenv
  Using cached virtualenv-15.0.2-py2.py3-none-any.whl
Installing collected packages: virtualenv
Successfully installed virtualenv-15.0.2
```

6. Create a virtual environment: `virtualenv env`

```sh
c:\ws>virtualenv env
Using base prefix 'c:\\python\\v3.3.5'
New python executable in c:\ws\env\Scripts\python.exe
Installing setuptools, pip, wheel...done.
```

7. Browse into the newly created folder: `cd env`

```sh
c:\ws>cd env

c:\ws\env>
```

8. Activate the virtualenv: `Scripts\activate`

```sh
c:\ws\env>Scripts\activate

(env) c:\ws\env>
```

9. Install [mysqlclient](https://pypi.python.org/pypi/mysqlclient)

```sh
(env) c:\ws\env>pip install mysqlclient
```

This attempts to build from source, but on Windows this does not always work. So alternatively, install from a wheel file. [Download the wheel file](http://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient) and copy it into `c:\ws\env` or wherever you created the virtual env. I'm using `mysqlclient-1.3.7-cp35-cp35m-win_amd64.whl`. Then execute this command:

```sh
(env) c:\ws\env>pip install mysqlclient-1.3.7-cp35-cp35m-win_amd64.whl
Processing .\mysqlclient-1.3.7-cp35-cp35m-win_amd64.whl
Installing collected packages: mysqlclient
Successfully installed mysqlclient-1.3.7
```

9. GIT [clone](https://git-scm.com/docs/git-clone) this project: `git clone git@github.com:Download/ba.git` (will create a folder `ba` within `env`)

```sh
(env) c:\ws\env>git clone git@github.com:Download/ba.git
Cloning into 'ba'...
remote: Counting objects: 35, done.
Receiving objects: 100% (35/35), 8.48 KiB |
remote: Compressing objects: 100% (27/27), done.
remote: Total 35 (delta 0), reused 32 (delta 0), pack-reused 0
Checking connectivity... done.
```

10. Move into the project folder: `cd ba`

```sh
(env) c:\ws\env>cd ba

(env) c:\ws\env\ba>
```

11. Install the project's dependencies: `pip install -r requirements.txt`

```sh
(env) c:\ws\env\ba>pip install -r requirements.txt
Collecting Django==1.8.14 (from -r requirements.txt (line 1))
  Using cached Django-1.8.14-py2.py3-none-any.whl
Requirement already satisfied (use --upgrade to upgrade): mysqlclient==1.3.7 in c:\ws\env\lib\site-packages (from -r requirements.txt (line 2))
Installing collected packages: Django
Successfully installed Django-1.8.14
```

12. Make sure a DB named `ba` exists in MySQL (assuming you have a mysql user named `root` with password `secret`)

```sh
(env) c:\ws\env\ba>mysql -uroot -psecret -e "CREATE DATABASE IF NOT EXISTS `ba` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
```

13. Run `python manage.py migrate` to create the initial schema

```sh
(env) c:\ws\env\ba>python manage.py migrate
Operations to perform:
  Synchronize unmigrated apps: messages, staticfiles
  Apply all migrations: admin, sessions, auth, contenttypes
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
  Installing custom SQL...
Running migrations:
  Rendering model states... DONE
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying sessions.0001_initial... OK
```

14. Create the admin user

```sh
(env) c:\ws\env\ba>python manage.py createsuperuser
Username (leave blank to use 'user'): admin
Email address:
Password:
Password (again):
Superuser created successfully.
```

15. Start the server

```sh
(env) c:\ws\env\ba>python manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
August 01, 2016 - 16:52:08
Django version 1.8.14, using settings 'app.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```


# Setting up the OpenShift application

1. Create a Python 3.3 application

2. Copy the `Source Code` URL from the created application and add it as a remote named `openshift` to your GIT repo (`ba`)

2. Push this project's code to that remote

```sh
git.exe push --progress "openshift" master:master

...
```

3. Only once the Git push was succesful, add the MySQL 5.5 cartridge.

If you add the MySQL cartridge before pushing the code changes, you run into an OpenShift bug:
[Bug 1292701 - Install mysqlclient in Django scalable application](https://bugzilla.redhat.com/show_bug.cgi?id=1292701)


4. Restart the OpenShift application.
