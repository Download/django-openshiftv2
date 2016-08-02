# Set up a local development environment (on Windows)

## Install Python
* Install [Python 3.5.2](https://www.python.org/download/releases/3.5.2/) | [Web installer](https://www.python.org/ftp/python/3.5.2/python-3.5.2-amd64-webinstall.exe).
* Open a command prompt and verify that Python is installed correctly

```sh
c:\ws>python --version
Python 3.5.2
```

> OpenShift uses Python 3.3, but this gives many problems on Windows, so on Windows we use Python 3.5 instead.


* Attempt to upgrade pip (version that comes bundled with Python 3.5.2 is old)

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

* Verify that [pip](https://pip.pypa.io/en/stable/) (python installer package) is installed correctly

```sh
c:\ws>pip --version
pip 8.1.2 from c:\python\v3.5.2\lib\site-packages (python 3.5)
```

## Install virtualenv
* Install [virtualenv](https://virtualenv.pypa.io/en/stable/installation/)

```sh
c:\ws>pip install virtualenv
Collecting virtualenv
  Using cached virtualenv-15.0.2-py2.py3-none-any.whl
Installing collected packages: virtualenv
Successfully installed virtualenv-15.0.2
```

## Create a virtual environment
* Run the command `virtualenv env`

```sh
c:\ws>virtualenv env
Using base prefix 'c:\\python\\v3.5.2'
New python executable in c:\ws\env\Scripts\python.exe
Installing setuptools, pip, wheel...done.
```

* Browse into the newly created folder: `cd env`

```sh
c:\ws>cd env

c:\ws\env>
```

* Activate the virtualenv: `Scripts\activate`

```sh
c:\ws\env>Scripts\activate

(env) c:\ws\env>
```

## Install mysqlclient
* Install [mysqlclient](https://pypi.python.org/pypi/mysqlclient)

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

## Git clone this project
* [Git clone](https://git-scm.com/docs/git-clone) this project: `git clone git@github.com:Download/ba.git` (will create a folder `ba` within `env`)

```sh
(env) c:\ws\env>git clone git@github.com:Download/ba.git
Cloning into 'ba'...
remote: Counting objects: 35, done.
Receiving objects: 100% (35/35), 8.48 KiB |
remote: Compressing objects: 100% (27/27), done.
remote: Total 35 (delta 0), reused 32 (delta 0), pack-reused 0
Checking connectivity... done.
```

* Move into the project folder: `cd ba`

```sh
(env) c:\ws\env>cd ba

(env) c:\ws\env\ba>
```

## Install dependencies
* Install the project's dependencies: `pip install -r requirements.txt`

```sh
(env) c:\ws\env\ba>pip install -r requirements.txt
Collecting Django==1.8.14 (from -r requirements.txt (line 1))
  Using cached Django-1.8.14-py2.py3-none-any.whl
Requirement already satisfied (use --upgrade to upgrade): mysqlclient==1.3.7 in c:\ws\env\lib\site-packages (from -r requirements.txt (line 2))
Installing collected packages: Django
Successfully installed Django-1.8.14
```

## Setup the MySQL database
* Make sure a DB named `ba` exists in MySQL (assuming you have a mysql user named `root` with password `secret`)

```sh
(env) c:\ws\env\ba>mysql -uroot -psecret -e "CREATE DATABASE IF NOT EXISTS `ba` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
```

* Run `python manage.py migrate` to create the initial schema

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

## Create the admin user

* You can either create the admin user using the Django `createsuperuser` command, as shown below:

```sh
(env) c:\ws\env\ba>python manage.py createsuperuser
Username (leave blank to use 'user'): admin
Email address:
Password:
Password (again):
Superuser created successfully.
```

* or you can use the `createadminuser.py` script
This script is called on deploy to openshift and checks whether an `admin` user already exists. If not, it will create one. On openshift it will use the MySQL password as the initial password, on local development environments it will use
password `secret`:

```sh
(env) c:\ws\env\ba>python createadminuser.py
============================================================
Creating admin user. Please note these credentials.
------------------------------------------------------------
USERNAME:  admin
PASSWORD:  secret
------------------------------------------------------------
User admin created succesfully.
============================================================```

## Start the server
* Run `python manage.py runserver`

```sh
(env) c:\ws\env\ba>python manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
August 01, 2016 - 16:52:08
Django version 1.8.14, using settings 'app.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

## Test the site
* Point your browser to http://127.0.0.1:8000/


# Setting up the OpenShift application

Start by creating a Python 3.3 application named `ba` with Scaling set to `Scale with web traffic`. Once it completes, deploy this application to it by following these steps:

![screenshot](http://i.imgur.com/4Phj1y7.png)

## Push this project to OpenShift
* Copy the `Source Code` URL from the created application and add it as a remote named `openshift` to your GIT repo (`ba`). Then force-push this project's code to that remote.

```sh
(env) c:\ws\env\ba>git push --force --progress "openshift" master:master
Counting objects: 61, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (53/53), done.
Writing objects: 100% (61/61), 12.04 KiB | 0 bytes/s, done.
Total 61 (delta 16), reused 31 (delta 0)
remote: Not stopping cartridge python because hot deploy is enabled
remote: Syncing git content to other proxy gears
remote: Building git ref 'master', commit 8dd0bc2
remote: Activating virtenv
remote: Checking for pip dependency listed in requirements.txt file..
remote: The directory '/var/lib/openshift/57a083990c1e66662e000159/.cache/pip/http' or its parent directory is not owned by the current user and the cache has been disabled. Please check the permissions and owner of that directory. If executing pip with sudo, you may want sudo's -H flag.
remote: The directory '/var/lib/openshift/57a083990c1e66662e000159/.cache/pip' or its parent directory is not owned by the current user and caching wheels has been disabled. check the permissions and owner of that directory. If executing pip with sudo, you may want sudo's -H flag.
remote: Collecting Django==1.8.14 (from -r /var/lib/openshift/57a083990c1e66662e000159/app-root/runtime/repo/requirements.txt (line 1))
remote:   Downloading http://mirror1.ops.rhcloud.com/mirror/python/web/packages/12/13/66eeba22d40f86d6cecc5a12784ae84b53f2ba171c448b1646ede25a99cd/Django-1.8.14-py2.py3-none-any.whl (6.2MB)
remote: Collecting mysqlclient==1.3.7 (from -r /var/lib/openshift/57a083990c1e66662e000159/app-root/runtime/repo/requirements.txt (line 2))
remote:   Downloading http://mirror1.ops.rhcloud.com/mirror/python/web/packages/source/m/mysqlclient/mysqlclient-1.3.7.tar.gz (79kB)
remote: Installing collected packages: Django, mysqlclient
remote:   Running setup.py install for mysqlclient: started
remote:     Running setup.py install for mysqlclient: finished with status 'done'
remote: Successfully installed Django-1.8.14 mysqlclient
remote: Running setup.py script..
remote: running develop
remote: running egg_info
remote: creating ba.egg-info
remote: writing top-level names to ba.egg-info/top_level.txt
remote: writing dependency_links to ba.egg-info/dependency_links.txt
remote: writing ba.egg-info/PKG-INFO
remote: writing manifest file 'ba.egg-info/SOURCES.txt'
remote: reading manifest file 'ba.egg-info/SOURCES.txt'
remote: writing manifest file 'ba.egg-info/SOURCES.txt'
remote: running build_ext
remote: Creating /var/lib/openshift/57a083990c1e66662e000159/app-root/runtime/dependencies/python/virtenv/venv/lib/python3.3/site-packages/ba.egg-link (link to .)
remote: Adding ba 1.0 to easy-install.pth file
remote:
remote: Installed /var/lib/openshift/57a083990c1e66662e000159/app-root/runtime/repo
remote: Processing dependencies for ba==1.0
remote: Finished processing dependencies for ba==1.0
remote: Preparing build for deployment
remote: Deployment id is 17b7602f
remote: Activating deployment
remote: Not starting cartridge haproxy because hot deploy is enabled
remote: Django and mysqlclient are installed correctly.
remote: Add the MySQL cartridge, then push the repo again.
remote: Not starting cartridge python because hot deploy is enabled
remote: -------------------------
remote: Git Post-Receive Result: success
remote: Activation status: success
remote: Deployment completed with status: success
To ssh://57a083990c1e66662e000159@ba-catwalk.rhcloud.com/~/git/ba.git/
 + c972bfd...8dd0bc2 master -> master (forced update)
 ```

## Add the MySQL 5.5 cartridge.

The next step is to add the MySQL cartridge. Normally we would add the MySQL cartridge before pushing, but if we do so, we encounter a [bug in OpenShift](https://bugzilla.redhat.com/show_bug.cgi?id=1292701), so bear with me. Once the MySQL cartridge has been added, we should write down the username and password OpenShift assigned for it. The same password will be used as the
initial password for the Django admin user.


## Push to openshift again

Make a small change (e.g. to this README) and commit. Then push your changes to OpenShift again.

This time we do not need to force the update.

```sh
(env) c:\ws\env\ba>git push --progress "openshift" master:master
Counting objects: 6, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (6/6), done.
Writing objects: 100% (6/6), 2.03 KiB | 0 bytes/s, done.
Total 6 (delta 4), reused 0 (delta 0)
remote: Not stopping cartridge python because hot deploy is enabled
remote: Syncing git content to other proxy gears
remote: Building git ref 'master', commit 3ec54f0
remote: Activating virtenv
remote: Checking for pip dependency listed in requirements.txt file..
...
remote: Activating deployment
remote: Not starting cartridge haproxy because hot deploy is enabled
remote: MySQL is installed correctly.
remote: Generating /var/lib/openshift/57a083990c1e66662e000159/.env/user_vars/DJANGO_SECRET_KEY
remote: Registering app/wsgi.py in /var/lib/openshift/57a083990c1e66662e000159/.env/user_vars/OPENSHIFT_PYTHON_WSGI_APPLICATION
remote: Executing 'python /var/lib/openshift/57a083990c1e66662e000159/app-root/runtime/repo/manage.py migrate --noinput'
remote: Operations to perform:
remote:   Synchronize unmigrated apps: messages, staticfiles
remote:   Apply all migrations: auth, admin, sessions, contenttypes
remote: Synchronizing apps without migrations:
remote:   Creating tables...
remote:     Running deferred SQL...
remote:   Installing custom SQL...
remote: Running migrations:
remote:   Rendering model states... DONE
remote:   Applying contenttypes.0001_initial... OK
remote:   Applying auth.0001_initial... OK
remote:   Applying admin.0001_initial... OK
remote:   Applying contenttypes.0002_remove_content_type_name... OK
remote:   Applying auth.0002_alter_permission_name_max_length... OK
remote:   Applying auth.0003_alter_user_email_max_length... OK
remote:   Applying auth.0004_alter_user_username_opts... OK
remote:   Applying auth.0005_alter_user_last_login_null... OK
remote:   Applying auth.0006_require_contenttypes_0002... OK
remote:   Applying sessions.0001_initial... OK
remote: Executing 'python /var/lib/openshift/57a083990c1e66662e000159/app-root/runtime/repo/manage.py collectstatic --noinput'
...
remote:
remote: 62 static files copied to '/var/lib/openshift/57a083990c1e66662e000159/app-root/runtime/repo/static'.
remote:
remote: ============================================================
remote: Creating admin user. Please note these credentials.
remote: ------------------------------------------------------------
remote: USERNAME:  admin
remote: PASSWORD:  **********
remote: ------------------------------------------------------------
remote: User admin created succesfully.
remote: ============================================================
remote:
remote: Deployment completed. Please restart the application for settings to take effect.
remote: Not starting cartridge python because hot deploy is enabled
remote: -------------------------
remote: Git Post-Receive Result: success
remote: Activation status: success
remote: Deployment completed with status: success
To ssh://57a083990c1e66662e000159@ba-catwalk.rhcloud.com/~/git/ba.git/
   8dd0bc2..3ec54f0  master -> master
```

## Restart the app.
Because [hot-deploy](https://blog.openshift.com/hot-deploying-php-on-openshift/) <sub><sup>(linked article is about PHP, but same principles apply)</sup></sub> is enabled on this project, to allow Django pick up on the changes we made, we need to manually restart the app on OpenShift.

* Run `rhc restart-app -a ba`

```sh
(env) c:\ws\env\ba>rhc restart-app -a ba
RESULT:
ba restarted
```

## Test deployment
* Point your browser at http://ba-catwalk.rhcloud.com/ (change to match your domain)

