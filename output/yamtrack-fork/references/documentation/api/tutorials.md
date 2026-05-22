# Djangoproject - Tutorials

**Pages:** 11

---

## Advanced tutorial: How to write reusable apps | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/intro/reusable-apps/

**Contents:**
- Advanced tutorial: How to write reusable apps¶
- Reusability matters¶
- Your project and your reusable app¶
- Installing some prerequisites¶
- Packaging your app¶
- Using your own package¶
- Publishing your app¶
- Installing Python packages with a virtual environment¶

This advanced tutorial begins where Tutorial 8 left off. We’ll be turning our web-poll into a standalone Python package you can reuse in new projects and share with other people.

If you haven’t recently completed Tutorials 1–8, we encourage you to review these so that your example project matches the one described below.

It’s a lot of work to design, build, test and maintain a web application. Many Python and Django projects share common problems. Wouldn’t it be great if we could save some of this repeated work?

Reusability is the way of life in Python. The Python Package Index (PyPI) has a vast range of packages you can use in your own Python programs. Check out Django Packages for existing reusable apps you could incorporate in your project. Django itself is also a normal Python package. This means that you can take existing Python packages or Django apps and compose them into your own web project. You only need to write the parts that make your project unique.

Let’s say you were starting a new project that needed a polls app like the one we’ve been working on. How do you make this app reusable? Luckily, you’re well on the way already. In Tutorial 1, we saw how we could decouple polls from the project-level URLconf using an include. In this tutorial, we’ll take further steps to make the app easy to use in new projects and ready to publish for others to install and use.

A Python package provides a way of grouping related Python code for easy reuse. A package contains one or more files of Python code (also known as “modules”).

A package can be imported with import foo.bar or from foo import bar. For a directory (like polls) to form a package, it must contain a special file __init__.py, even if this file is empty.

A Django application is a Python package that is specifically intended for use in a Django project. An application may use common Django conventions, such as having models, tests, urls, and views submodules.

Later on we use the term packaging to describe the process of making a Python package easy for others to install. It can be a little confusing, we know.

After the previous tutorials, our project should look like this:

You created djangotutorial/templates in Tutorial 7, and polls/templates in Tutorial 3. Now perhaps it is clearer why we chose to have separate template directories for the project and application: everything that is part of the polls application is in polls. It makes the application self-contained and easier to drop into a new project.

The polls directory could now be copied into a new Django project and immediately reused. It’s not quite ready to be published though. For that, we need to package the app to make it easy for others to install.

The current state of Python packaging is a bit muddled with various tools. For this tutorial, we’re going to use setuptools to build our package. It’s the recommended packaging tool (merged with the distribute fork). We’ll also be using pip to install and uninstall it. You should install these two packages now. If you need help, you can refer to how to install Django with pip. You can install setuptools the same way.

Python packaging refers to preparing your app in a specific format that can be easily installed and used. Django itself is packaged very much like this. For a small app like polls, this process isn’t too difficult.

First, create a parent directory for the package, outside of your Django project. Call this directory django-polls.

Choosing a name for your app

When choosing a name for your package, check PyPI to avoid naming conflicts with existing packages. We recommend using a django- prefix for package names, to identify your package as specific to Django, and a corresponding django_ prefix for your module name. For example, the django-ratelimit package contains the django_ratelimit module.

Application labels (that is, the final part of the dotted path to application packages) must be unique in INSTALLED_APPS. Avoid using the same label as any of the Django contrib packages, for example auth, admin, or messages.

Move the polls directory into django-polls directory, and rename it to django_polls.

Edit django_polls/apps.py so that name refers to the new module name, add label to give a short name for the app, and set default_auto_field to ensure your migrations are not affected by changes to DEFAULT_AUTO_FIELD made by users of your reusable app:

Create a file django-polls/README.rst with the following contents:

Create a django-polls/LICENSE file. Choosing a license is beyond the scope of this tutorial, but suffice it to say that code released publicly without a license is useless. Django and many Django-compatible apps are distributed under the BSD license; however, you’re free to pick your own license. Just be aware that your licensing choice will affect who is able to use your code.

Next we’ll create the pyproject.toml file which details how to build and install the app. A full explanation of this file is beyond the scope of this tutorial, but the Python Packaging User Guide has a good explanation. Create the django-polls/pyproject.toml file with the following contents:

Many common files and Python modules and packages are included in the package by default. To include additional files, we’ll need to create a MANIFEST.in file. To include the templates and static files, create a file django-polls/MANIFEST.in with the following contents:

It’s optional, but recommended, to include detailed documentation with your app. Create an empty directory django-polls/docs for future documentation.

Note that the docs directory won’t be included in your package unless you add some files to it. Many Django apps also provide their documentation online through sites like readthedocs.org.

Many Python projects, including Django and Python itself, use Sphinx to build their documentation. If you choose to use Sphinx you can link back to the Django documentation by configuring Intersphinx and including a value for Django in your project’s intersphinx_mapping value:

With that in place, you can then cross-link to specific entries, in the same way as in the Django docs, such as “:attr:`django.test.TransactionTestCase.databases`”.

Check that the build package is installed (python -m pip install build) and try building your package by running python -m build inside django-polls. This creates a directory called dist and builds your new package into source and binary formats, django_polls-0.1.tar.gz and django_polls-0.1-py3-none-any.whl.

For more information on packaging, see Python’s Tutorial on Packaging and Distributing Projects.

Since we moved the polls directory out of the project, it’s no longer working. We’ll now fix this by installing our new django-polls package.

Installing as a user library

The following steps install django-polls as a user library. Per-user installs have a lot of advantages over installing the package system-wide, such as being usable on systems where you don’t have administrator access as well as preventing the package from affecting system services and other users of the machine.

Note that per-user installations can still affect the behavior of system tools that run as that user, so using a virtual environment is a more robust solution (see below).

To install the package, use pip (you already installed it, right?):

Update mysite/settings.py to point to the new module name:

Update mysite/urls.py to point to the new module name:

Run the development server to confirm the project continues to work.

Now that we’ve packaged and tested django-polls, it’s ready to share with the world! If this wasn’t just an example, you could now:

Email the package to a friend.

Upload the package on your website.

Post the package on a public repository, such as the Python Package Index (PyPI). There is a good tutorial for doing this.

Earlier, we installed django-polls as a user library. This has some disadvantages:

Modifying the user libraries can affect other Python software on your system.

You won’t be able to run multiple versions of this package (or others with the same name).

Typically, these situations only arise once you’re maintaining several Django projects. When they do, the best solution is to use venv. This tool allows you to maintain multiple isolated Python environments, each with its own copy of the libraries and package namespace.

---

## FAQ: Installation | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/faq/install/

**Contents:**
- FAQ: Installation¶
- How do I get started?¶
- What are Django’s prerequisites?¶
- What Python version can I use with Django?¶
- What Python version should I use with Django?¶
- Should I use the stable version or development version?¶

Install Django (read the installation guide).

Walk through the tutorial.

Check out the rest of the documentation, and ask questions if you run into trouble.

Django requires Python. See the table in the next question for the versions of Python that work with each version of Django. Other Python libraries may be required for some use cases, but you’ll receive an error about them as they’re needed.

For a development environment – if you just want to experiment with Django – you don’t need to have a separate web server installed or database server.

Django comes with its own lightweight development server. For a production environment, Django follows the WSGI spec, PEP 3333, which means it can run on a variety of web servers. See Deploying Django for more information.

Django runs SQLite by default, which is included in Python installations. For a production environment, we recommend PostgreSQL; but we also officially support MariaDB, MySQL, SQLite, and Oracle. See Supported Databases for more information.

3.8, 3.9, 3.10, 3.11, 3.12 (added in 4.2.8)

3.10, 3.11, 3.12, 3.13 (added in 5.1.3)

3.10, 3.11, 3.12, 3.13, 3.14 (added in 5.2.8)

For each version of Python, only the latest micro release (A.B.C) is officially supported. Python versions that have reached end-of-life are no longer maintained by the Python project and therefore should not be used with Django.

You can find the latest supported micro version for each series on the Python download page.

We will support a Python version up to and including the first Django LTS release whose security support ends after security support for that version of Python ends. For example, Python 3.9 security support ends in October 2025 and Django 4.2 LTS security support ends in April 2026. Therefore Django 4.2 is the last version to support Python 3.9.

Since newer versions of Python are often faster, have more features, and are better supported, the latest version of Python 3 is recommended.

You don’t lose anything in Django by using an older release, but you don’t take advantage of the improvements and optimizations in newer Python releases. Third-party applications for use with Django are free to set their own version requirements.

Generally, if you’re using code in production, you should be using a stable release. The Django project publishes a full stable release every eight months or so, with bugfix updates in between. These stable releases contain the API that is covered by our backwards compatibility guarantees; if you write code against stable releases, you shouldn’t have any problems upgrading when the next official version is released.

---

## Quick install guide | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/intro/install/

**Contents:**
- Quick install guide¶
- Install Python¶
- Set up a database¶
- Install Django¶
- Verifying¶
- That’s it!¶

Before you can use Django, you’ll need to get it installed. We have a complete installation guide that covers all the possibilities; this guide will guide you to a minimal installation that’ll work while you walk through the introduction.

Being a Python web framework, Django requires Python. See What Python version can I use with Django? for details. Python includes a lightweight database called SQLite so you won’t need to set up a database just yet.

Get the latest version of Python at https://www.python.org/downloads/ or with your operating system’s package manager.

You can verify that Python is installed by typing python from your shell; you should see something like:

This step is only necessary if you’d like to work with a “large” database engine like PostgreSQL, MariaDB, MySQL, or Oracle. To install such a database, consult the database installation information.

You’ve got three options to install Django:

Install an official release. This is the best approach for most users.

Install a version of Django provided by your operating system distribution.

Install the latest development version. This option is for enthusiasts who want the latest-and-greatest features and aren’t afraid of running brand new code. You might encounter new bugs in the development version, but reporting them helps the development of Django. Also, releases of third-party packages are less likely to be compatible with the development version than with the latest stable release.

Always refer to the documentation that corresponds to the version of Django you’re using!

If you do either of the first two steps, keep an eye out for parts of the documentation marked new in development version. That phrase flags features that are only available in development versions of Django, and they likely won’t work with an official release.

To verify that Django can be seen by Python, type python from your shell. Then at the Python prompt, try to import Django:

You may have another version of Django installed.

That’s it – you can now move onto the tutorial.

---

## Writing your first Django app, part 1 | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/intro/tutorial01/

**Contents:**
- Writing your first Django app, part 1¶
- Creating a project¶
- The development server¶
- Creating the Polls app¶
- Write your first view¶

Let’s learn by example.

Throughout this tutorial, we’ll walk you through the creation of a basic poll application.

It’ll consist of two parts:

A public site that lets people view polls and vote in them.

An admin site that lets you add, change, and delete polls.

We’ll assume you have Django installed already. You can tell Django is installed and which version by running the following command in a shell prompt (indicated by the $ prefix):

If Django is installed, you should see the version of your installation. If it isn’t, you’ll get an error telling “No module named django”.

This tutorial is written for Django 6.0, which supports Python 3.12 and later. If the Django version doesn’t match, you can refer to the tutorial for your version of Django by using the version switcher at the bottom right corner of this page, or update Django to the newest version. If you’re using an older version of Python, check What Python version can I use with Django? to find a compatible version of Django.

If you’re having trouble going through this tutorial, please head over to the Getting Help section of the FAQ.

If this is your first time using Django, you’ll have to take care of some initial setup. Namely, you’ll need to auto-generate some code that establishes a Django project – a collection of settings for an instance of Django, including database configuration, Django-specific options and application-specific settings.

From the command line, cd into a directory where you’d like to store your code and run the following command to bootstrap a new Django project:

This will create a directory djangotutorial with a project called mysite inside. The directory name doesn’t matter to Django; you can rename it to anything you like. If it didn’t work, see Problems running django-admin.

You’ll need to avoid naming projects after built-in Python or Django components. In particular, this means you should avoid using names like django (which will conflict with Django itself) or test (which conflicts with a built-in Python package).

Let’s look at what startproject created:

manage.py: A command-line utility that lets you interact with this Django project in various ways. You can read all the details about manage.py in django-admin and manage.py.

mysite/: A directory that is the actual Python package for your project. Its name is the Python package name you’ll need to use to import anything inside it (e.g. mysite.urls).

mysite/__init__.py: An empty file that tells Python that this directory should be considered a Python package. If you’re a Python beginner, read more about packages in the official Python docs.

mysite/settings.py: Settings/configuration for this Django project. Django settings will tell you all about how settings work.

mysite/urls.py: The URL declarations for this Django project; a “table of contents” of your Django-powered site. You can read more about URLs in URL dispatcher.

mysite/asgi.py: An entry-point for ASGI-compatible web servers to serve your project. See How to deploy with ASGI for more details.

mysite/wsgi.py: An entry-point for WSGI-compatible web servers to serve your project. See How to deploy with WSGI for more details.

Let’s verify your Django project works. Change into the djangotutorial directory, if you haven’t already, and run the following commands:

You’ll see the following output on the command line:

Ignore the warning about unapplied database migrations for now; we’ll deal with the database shortly.

Now that the server’s running, visit http://127.0.0.1:8000/ with your web browser. You’ll see a “Congratulations!” page, with a rocket taking off. It worked!

You’ve started the Django development server, a lightweight web server written purely in Python. We’ve included this with Django so you can develop things rapidly, without having to deal with configuring a production server – such as Apache – until you’re ready for production.

Now’s a good time to note: don’t use this server in anything resembling a production environment. It’s intended only for use while developing. (We’re in the business of making web frameworks, not web servers.)

(To serve the site on a different port, see the runserver reference.)

Automatic reloading of runserver

The development server automatically reloads Python code for each request as needed. You don’t need to restart the server for code changes to take effect. However, some actions like adding files don’t trigger a restart, so you’ll have to restart the server in these cases.

Now that your environment – a “project” – is set up, you’re set to start doing work.

Each application you write in Django consists of a Python package that follows a certain convention. Django comes with a utility that automatically generates the basic directory structure of an app, so you can focus on writing code rather than creating directories.

What’s the difference between a project and an app? An app is a web application that does something – e.g., a blog system, a database of public records or a small poll app. A project is a collection of configuration and apps for a particular website. A project can contain multiple apps. An app can be in multiple projects.

Your apps can live anywhere in your Python path. In this tutorial, we’ll create our poll app inside the djangotutorial folder.

To create your app, make sure you’re in the same directory as manage.py and type this command:

That’ll create a directory polls, which is laid out like this:

This directory structure will house the poll application.

Let’s write the first view. Open the file polls/views.py and put the following Python code in it:

This is the most basic view possible in Django. To access it in a browser, we need to map it to a URL - and for this we need to define a URL configuration, or “URLconf” for short. These URL configurations are defined inside each Django app, and they are Python files named urls.py.

To define a URLconf for the polls app, create a file polls/urls.py with the following content:

Your app directory should now look like:

The next step is to configure the root URLconf in the mysite project to include the URLconf defined in polls.urls. To do this, add an import for django.urls.include in mysite/urls.py and insert an include() in the urlpatterns list, so you have:

The path() function expects at least two arguments: route and view. The include() function allows referencing other URLconfs. Whenever Django encounters include(), it chops off whatever part of the URL matched up to that point and sends the remaining string to the included URLconf for further processing.

The idea behind include() is to make it easy to plug-and-play URLs. Since polls are in their own URLconf (polls/urls.py), they can be placed under “/polls/”, or under “/fun_polls/”, or under “/content/polls/”, or any other path root, and the app will still work.

When to use include()

You should always use include() when you include other URL patterns. The only exception is admin.site.urls, which is a pre-built URLconf provided by Django for the default admin site.

You have now wired an index view into the URLconf. Verify it’s working with the following command:

Go to http://localhost:8000/polls/ in your browser, and you should see the text “Hello, world. You’re at the polls index.”, which you defined in the index view.

If you get an error page here, check that you’re going to http://localhost:8000/polls/ and not http://localhost:8000/.

When you’re comfortable with the basic request and response flow, read part 2 of this tutorial to start working with the database.

---

## Writing your first Django app, part 2 | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/intro/tutorial02/

**Contents:**
- Writing your first Django app, part 2¶
- Database setup¶
- Creating models¶
- Activating models¶
- Playing with the API¶
- Introducing the Django Admin¶
  - Creating an admin user¶
  - Start the development server¶
  - Enter the admin site¶
  - Make the poll app modifiable in the admin¶

This tutorial begins where Tutorial 1 left off. We’ll set up the database, create your first model, and get a quick introduction to Django’s automatically-generated admin site.

If you’re having trouble going through this tutorial, please head over to the Getting Help section of the FAQ.

Now, open up mysite/settings.py. It’s a normal Python module with module-level variables representing Django settings.

By default, the DATABASES configuration uses SQLite. If you’re new to databases, or you’re just interested in trying Django, this is the easiest choice. SQLite is included in Python, so you won’t need to install anything else to support your database. When starting your first real project, however, you may want to use a more scalable database like PostgreSQL, to avoid database-switching headaches down the road.

If you wish to use another database, see details to customize and get your database running.

While you’re editing mysite/settings.py, set TIME_ZONE to your time zone.

Also, note the INSTALLED_APPS setting at the top of the file. That holds the names of all Django applications that are activated in this Django instance. Apps can be used in multiple projects, and you can package and distribute them for use by others in their projects.

By default, INSTALLED_APPS contains the following apps, all of which come with Django:

django.contrib.admin – The admin site. You’ll use it shortly.

django.contrib.auth – An authentication system.

django.contrib.contenttypes – A framework for content types.

django.contrib.sessions – A session framework.

django.contrib.messages – A messaging framework.

django.contrib.staticfiles – A framework for managing static files.

These applications are included by default as a convenience for the common case.

Some of these applications make use of at least one database table, though, so we need to create the tables in the database before we can use them. To do that, run the following command:

The migrate command looks at the INSTALLED_APPS setting and creates any necessary database tables according to the database settings in your mysite/settings.py file and the database migrations shipped with the app (we’ll cover those later). You’ll see a message for each migration it applies. If you’re interested, run the command-line client for your database and type \dt (PostgreSQL), SHOW TABLES; (MariaDB, MySQL), .tables (SQLite), or SELECT TABLE_NAME FROM USER_TABLES; (Oracle) to display the tables Django created.

Like we said above, the default applications are included for the common case, but not everybody needs them. If you don’t need any or all of them, feel free to comment-out or delete the appropriate line(s) from INSTALLED_APPS before running migrate. The migrate command will only run migrations for apps in INSTALLED_APPS.

Now we’ll define your models – essentially, your database layout, with additional metadata.

A model is the single, definitive source of information about your data. It contains the essential fields and behaviors of the data you’re storing. Django follows the DRY Principle. The goal is to define your data model in one place and automatically derive things from it.

This includes the migrations, which are derived from your models file. They form a history that Django uses to update your database schema to match your current models.

In our poll app, we’ll create two models: Question and Choice. A Question has a question and a publication date. A Choice has two fields: the text of the choice and a vote tally. Each Choice is associated with a Question.

These concepts are represented by Python classes. Edit the polls/models.py file so it looks like this:

Here, each model is represented by a class that subclasses django.db.models.Model. Each model has a number of class variables, each of which represents a database field in the model.

Each field is represented by an instance of a Field class – e.g., CharField for character fields and DateTimeField for datetimes. This tells Django what type of data each field holds.

The name of each Field instance (e.g. question_text or pub_date) is the field’s name, in machine-friendly format. You’ll use this value in your Python code, and your database will use it as the column name.

You can use an optional first positional argument to a Field to designate a human-readable name. That’s used in a couple of introspective parts of Django, and it doubles as documentation. If this field isn’t provided, Django will use the machine-readable name. In this example, we’ve only defined a human-readable name for Question.pub_date. For all other fields in this model, the field’s machine-readable name will suffice as its human-readable name.

Some Field classes have required arguments. CharField, for example, requires that you give it a max_length. That’s used not only in the database schema, but in validation, as we’ll soon see.

A Field can also have various optional arguments; in this case, we’ve set the default value of votes to 0.

Finally, note a relationship is defined, using ForeignKey. That tells Django each Choice is related to a single Question. Django supports all the common database relationships: many-to-one, many-to-many, and one-to-one.

That small bit of model code gives Django a lot of information. With it, Django is able to:

Create a database schema (CREATE TABLE statements) for this app.

Create a Python database-access API for accessing Question and Choice objects.

But first we need to tell our project that the polls app is installed.

Django apps are “pluggable”: You can use an app in multiple projects, and you can distribute apps, because they don’t have to be tied to a given Django installation.

To include the app in our project, we need to add a reference to its configuration class in the INSTALLED_APPS setting. The PollsConfig class is in the polls/apps.py file, so its dotted path is 'polls.apps.PollsConfig'. Edit the mysite/settings.py file and add that dotted path to the INSTALLED_APPS setting. It’ll look like this:

Now Django knows to include the polls app. Let’s run another command:

You should see something similar to the following:

By running makemigrations, you’re telling Django that you’ve made some changes to your models (in this case, you’ve made new ones) and that you’d like the changes to be stored as a migration.

Migrations are how Django stores changes to your models (and thus your database schema) - they’re files on disk. You can read the migration for your new model if you like; it’s the file polls/migrations/0001_initial.py. Don’t worry, you’re not expected to read them every time Django makes one, but they’re designed to be human-editable in case you want to manually tweak how Django changes things.

There’s a command that will run the migrations for you and manage your database schema automatically - that’s called migrate, and we’ll come to it in a moment - but first, let’s see what SQL that migration would run. The sqlmigrate command takes migration names and returns their SQL:

You should see something similar to the following (we’ve reformatted it for readability):

The exact output will vary depending on the database you are using. The example above is generated for PostgreSQL.

Table names are automatically generated by combining the name of the app (polls) and the lowercase name of the model – question and choice. (You can override this behavior.)

Primary keys (IDs) are added automatically. (You can override this, too.)

By convention, Django appends "_id" to the foreign key field name. (Yes, you can override this, as well.)

The foreign key relationship is made explicit by a FOREIGN KEY constraint. Don’t worry about the DEFERRABLE parts; it’s telling PostgreSQL to not enforce the foreign key until the end of the transaction.

It’s tailored to the database you’re using, so database-specific field types such as auto_increment (MySQL), bigint PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY (PostgreSQL), or integer primary key autoincrement (SQLite) are handled for you automatically. Same goes for the quoting of field names – e.g., using double quotes or single quotes.

The sqlmigrate command doesn’t actually run the migration on your database - instead, it prints it to the screen so that you can see what SQL Django thinks is required. It’s useful for checking what Django is going to do or if you have database administrators who require SQL scripts for changes.

If you’re interested, you can also run python manage.py check; this checks for any problems in your project without making migrations or touching the database.

Now, run migrate again to create those model tables in your database:

The migrate command takes all the migrations that haven’t been applied (Django tracks which ones are applied using a special table in your database called django_migrations) and runs them against your database - essentially, synchronizing the changes you made to your models with the schema in the database.

Migrations are very powerful and let you change your models over time, as you develop your project, without the need to delete your database or tables and make new ones - it specializes in upgrading your database live, without losing data. We’ll cover them in more depth in a later part of the tutorial, but for now, remember the three-step guide to making model changes:

Change your models (in models.py).

Run python manage.py makemigrations to create migrations for those changes

Run python manage.py migrate to apply those changes to the database.

The reason that there are separate commands to make and apply migrations is because you’ll commit migrations to your version control system and ship them with your app; they not only make your development easier, they’re also usable by other developers and in production.

Read the django-admin documentation for full information on what the manage.py utility can do.

Now, let’s hop into the interactive Python shell and play around with the free API Django gives you. To invoke the Python shell, use this command:

We’re using this instead of simply typing “python”, because manage.py sets the DJANGO_SETTINGS_MODULE environment variable, which gives Django the Python import path to your mysite/settings.py file. By default, the shell command automatically imports the models from your INSTALLED_APPS.

Once you’re in the shell, explore the database API:

Wait a minute. <Question: Question object (1)> isn’t a helpful representation of this object. Let’s fix that by editing the Question model (in the polls/models.py file) and adding a __str__() method to both Question and Choice:

It’s important to add __str__() methods to your models, not only for your own convenience when dealing with the interactive prompt, but also because objects’ representations are used throughout Django’s automatically-generated admin.

Let’s also add a custom method to this model:

Note the addition of import datetime and from django.utils import timezone, to reference Python’s standard datetime module and Django’s time-zone-related utilities in django.utils.timezone, respectively. If you aren’t familiar with time zone handling in Python, you can learn more in the time zone support docs.

Save these changes and start a new Python interactive shell. (If a three-chevron prompt (>>>) indicates you are still in the shell, you need to exit first using exit()). Run python manage.py shell again to reload the models.

For more information on model relations, see Accessing related objects. For more on how to use double underscores to perform field lookups via the API, see Field lookups. For full details on the database API, see our Database API reference.

Generating admin sites for your staff or clients to add, change, and delete content is tedious work that doesn’t require much creativity. For that reason, Django entirely automates creation of admin interfaces for models.

Django was written in a newsroom environment, with a very clear separation between “content publishers” and the “public” site. Site managers use the system to add news stories, events, sports scores, etc., and that content is displayed on the public site. Django solves the problem of creating a unified interface for site administrators to edit content.

The admin isn’t intended to be used by site visitors. It’s for site managers.

First we’ll need to create a user who can login to the admin site. Run the following command:

Enter your desired username and press enter.

You will then be prompted for your desired email address:

The final step is to enter your password. You will be asked to enter your password twice, the second time as a confirmation of the first.

The Django admin site is activated by default. Let’s start the development server and explore it.

If the server is not running start it like so:

Now, open a web browser and go to “/admin/” on your local domain – e.g., http://127.0.0.1:8000/admin/. You should see the admin’s login screen:

Since translation is turned on by default, if you set LANGUAGE_CODE, the login screen will be displayed in the given language (if Django has appropriate translations).

Now, try logging in with the superuser account you created in the previous step. You should see the Django admin index page:

You should see a few types of editable content: groups and users. They are provided by django.contrib.auth, the authentication framework shipped by Django.

But where’s our poll app? It’s not displayed on the admin index page.

Only one more thing to do: we need to tell the admin that Question objects have an admin interface. To do this, open the polls/admin.py file, and edit it to look like this:

Now that we’ve registered Question, Django knows that it should be displayed on the admin index page:

Click “Questions”. Now you’re at the “change list” page for questions. This page displays all the questions in the database and lets you choose one to change it. There’s the “What’s up?” question we created earlier:

Click the “What’s up?” question to edit it:

The form is automatically generated from the Question model.

The different model field types (DateTimeField, CharField) correspond to the appropriate HTML input widget. Each type of field knows how to display itself in the Django admin.

Each DateTimeField gets free JavaScript shortcuts. Dates get a “Today” shortcut and calendar popup, and times get a “Now” shortcut and a convenient popup that lists commonly entered times.

The bottom part of the page gives you a couple of options:

Save – Saves changes and returns to the change-list page for this type of object.

Save and continue editing – Saves changes and reloads the admin page for this object.

Save and add another – Saves changes and loads a new, blank form for this type of object.

Delete – Displays a delete confirmation page.

If the value of “Date published” doesn’t match the time when you created the question in Tutorial 1, it probably means you forgot to set the correct value for the TIME_ZONE setting. Change it, reload the page and check that the correct value appears.

Change the “Date published” by clicking the “Today” and “Now” shortcuts. Then click “Save and continue editing.” Then click “History” in the upper right. You’ll see a page listing all changes made to this object via the Django admin, with the timestamp and username of the person who made the change:

When you’re comfortable with the models API and have familiarized yourself with the admin site, read part 3 of this tutorial to learn about how to add more views to our polls app.

---

## Writing your first Django app, part 3 | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/intro/tutorial03/

**Contents:**
- Writing your first Django app, part 3¶
- Overview¶
- Writing more views¶
- Write views that actually do something¶
  - A shortcut: render()¶
- Raising a 404 error¶
  - A shortcut: get_object_or_404()¶
- Use the template system¶
- Removing hardcoded URLs in templates¶
- Namespacing URL names¶

This tutorial begins where Tutorial 2 left off. We’re continuing the web-poll application and will focus on creating the public interface – “views.”

If you’re having trouble going through this tutorial, please head over to the Getting Help section of the FAQ.

A view is a “type” of web page in your Django application that generally serves a specific function and has a specific template. For example, in a blog application, you might have the following views:

Blog homepage – displays the latest few entries.

Entry “detail” page – permalink page for a single entry.

Year-based archive page – displays all months with entries in the given year.

Month-based archive page – displays all days with entries in the given month.

Day-based archive page – displays all entries in the given day.

Comment action – handles posting comments to a given entry.

In our poll application, we’ll have the following four views:

Question “index” page – displays the latest few questions.

Question “detail” page – displays a question text, with no results but with a form to vote.

Question “results” page – displays results for a particular question.

Vote action – handles voting for a particular choice in a particular question.

In Django, web pages and other content are delivered by views. Each view is represented by a Python function (or method, in the case of class-based views). Django will choose a view by examining the URL that’s requested (to be precise, the part of the URL after the domain name).

Now in your time on the web you may have come across such beauties as ME2/Sites/dirmod.htm?sid=&type=gen&mod=Core+Pages&gid=A6CD4967199A42D9B65B1B. You will be pleased to know that Django allows us much more elegant URL patterns than that.

A URL pattern is the general form of a URL - for example: /newsarchive/<year>/<month>/.

To get from a URL to a view, Django uses what are known as ‘URLconfs’. A URLconf maps URL patterns to views.

This tutorial provides basic instruction in the use of URLconfs, and you can refer to URL dispatcher for more information.

Now let’s add a few more views to polls/views.py. These views are slightly different, because they take an argument:

Wire these new views into the polls.urls module by adding the following path() calls:

Take a look in your browser, at “/polls/34/”. It’ll run the detail() function and display whatever ID you provide in the URL. Try “/polls/34/results/” and “/polls/34/vote/” too – these will display the placeholder results and voting pages.

When somebody requests a page from your website – say, “/polls/34/”, Django will load the mysite.urls Python module because it’s pointed to by the ROOT_URLCONF setting. It finds the variable named urlpatterns and traverses the patterns in order. After finding the match at 'polls/', it strips off the matching text ("polls/") and sends the remaining text – "34/" – to the ‘polls.urls’ URLconf for further processing. There it matches '<int:question_id>/', resulting in a call to the detail() view like so:

The question_id=34 part comes from <int:question_id>. Using angle brackets “captures” part of the URL and sends it as a keyword argument to the view function. The question_id part of the string defines the name that will be used to identify the matched pattern, and the int part is a converter that determines what patterns should match this part of the URL path. The colon (:) separates the converter and pattern name.

Each view is responsible for doing one of two things: returning an HttpResponse object containing the content for the requested page, or raising an exception such as Http404. The rest is up to you.

Your view can read records from a database, or not. It can use a template system such as Django’s – or a third-party Python template system – or not. It can generate a PDF file, output XML, create a ZIP file on the fly, anything you want, using whatever Python libraries you want.

All Django wants is that HttpResponse. Or an exception.

Because it’s convenient, let’s use Django’s own database API, which we covered in Tutorial 2. Here’s one stab at a new index() view, which displays the latest 5 poll questions in the system, separated by commas, according to publication date:

There’s a problem here, though: the page’s design is hardcoded in the view. If you want to change the way the page looks, you’ll have to edit this Python code. So let’s use Django’s template system to separate the design from Python by creating a template that the view can use.

First, create a directory called templates in your polls directory. Django will look for templates in there.

Your project’s TEMPLATES setting describes how Django will load and render templates. The default settings file configures a DjangoTemplates backend whose APP_DIRS option is set to True. By convention DjangoTemplates looks for a “templates” subdirectory in each of the INSTALLED_APPS.

Within the templates directory you have just created, create another directory called polls, and within that create a file called index.html. In other words, your template should be at polls/templates/polls/index.html. Because of how the app_directories template loader works as described above, you can refer to this template within Django as polls/index.html.

Now we might be able to get away with putting our templates directly in polls/templates (rather than creating another polls subdirectory), but it would actually be a bad idea. Django will choose the first template it finds whose name matches, and if you had a template with the same name in a different application, Django would be unable to distinguish between them. We need to be able to point Django at the right one, and the best way to ensure this is by namespacing them. That is, by putting those templates inside another directory named for the application itself.

Put the following code in that template:

To make the tutorial shorter, all template examples use incomplete HTML. In your own projects you should use complete HTML documents.

Now let’s update our index view in polls/views.py to use the template:

That code loads the template called polls/index.html and passes it a context. The context is a dictionary mapping template variable names to Python objects.

Load the page by pointing your browser at “/polls/”, and you should see a bulleted-list containing the “What’s up” question from Tutorial 2. The link points to the question’s detail page.

It’s a very common idiom to load a template, fill a context and return an HttpResponse object with the result of the rendered template. Django provides a shortcut. Here’s the full index() view, rewritten:

Note that once we’ve done this in all these views, we no longer need to import loader and HttpResponse (you’ll want to keep HttpResponse if you still have the stub methods for detail, results, and vote).

The render() function takes the request object as its first argument, a template name as its second argument and a dictionary as its optional third argument. It returns an HttpResponse object of the given template rendered with the given context.

Now, let’s tackle the question detail view – the page that displays the question text for a given poll. Here’s the view:

The new concept here: The view raises the Http404 exception if a question with the requested ID doesn’t exist.

We’ll discuss what you could put in that polls/detail.html template a bit later, but if you’d like to quickly get the above example working, a file containing just:

will get you started for now.

It’s a very common idiom to use get() and raise Http404 if the object doesn’t exist. Django provides a shortcut. Here’s the detail() view, rewritten:

The get_object_or_404() function takes a Django model as its first argument and an arbitrary number of keyword arguments, which it passes to the get() function of the model’s manager. It raises Http404 if the object doesn’t exist.

Why do we use a helper function get_object_or_404() instead of automatically catching the ObjectDoesNotExist exceptions at a higher level, or having the model API raise Http404 instead of ObjectDoesNotExist?

Because that would couple the model layer to the view layer. One of the foremost design goals of Django is to maintain loose coupling. Some controlled coupling is introduced in the django.shortcuts module.

There’s also a get_list_or_404() function, which works just as get_object_or_404() – except using filter() instead of get(). It raises Http404 if the list is empty.

Back to the detail() view for our poll application. Given the context variable question, here’s what the polls/detail.html template might look like:

The template system uses dot-lookup syntax to access variable attributes. In the example of {{ question.question_text }}, first Django does a dictionary lookup on the object question. Failing that, it tries an attribute lookup – which works, in this case. If attribute lookup had failed, it would’ve tried a list-index lookup.

Method-calling happens in the {% for %} loop: question.choice_set.all is interpreted as the Python code question.choice_set.all(), which returns an iterable of Choice objects and is suitable for use in the {% for %} tag.

See the template guide for more about templates.

Remember, when we wrote the link to a question in the polls/index.html template, the link was partially hardcoded like this:

The problem with this hardcoded, tightly-coupled approach is that it becomes challenging to change URLs on projects with a lot of templates. However, since you defined the name argument in the path() functions in the polls.urls module, you can remove a reliance on specific URL paths defined in your url configurations by using the {% url %} template tag:

The way this works is by looking up the URL definition as specified in the polls.urls module. You can see exactly where the URL name of ‘detail’ is defined below:

If you want to change the URL of the polls detail view to something else, perhaps to something like polls/specifics/12/ instead of doing it in the template (or templates) you would change it in polls/urls.py:

The tutorial project has just one app, polls. In real Django projects, there might be five, ten, twenty apps or more. How does Django differentiate the URL names between them? For example, the polls app has a detail view, and so might an app on the same project that is for a blog. How does one make it so that Django knows which app view to create for a url when using the {% url %} template tag?

The answer is to add namespaces to your URLconf. In the polls/urls.py file, go ahead and add an app_name to set the application namespace:

Now change your polls/index.html template from:

to point at the namespaced detail view:

When you’re comfortable with writing views, read part 4 of this tutorial to learn the basics about form processing and generic views.

---

## Writing your first Django app, part 4 | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/intro/tutorial04/

**Contents:**
- Writing your first Django app, part 4¶
- Write a minimal form¶
- Use generic views: Less code is better¶
  - Amend URLconf¶
  - Amend views¶

This tutorial begins where Tutorial 3 left off. We’re continuing the web-poll application and will focus on form processing and cutting down our code.

If you’re having trouble going through this tutorial, please head over to the Getting Help section of the FAQ.

Let’s update our poll detail template (“polls/detail.html”) from the last tutorial, so that the template contains an HTML <form> element:

The above template displays a radio button for each question choice. The value of each radio button is the associated question choice’s ID. The name of each radio button is "choice". That means, when somebody selects one of the radio buttons and submits the form, it’ll send the POST data choice=# where # is the ID of the selected choice. This is the basic concept of HTML forms.

We set the form’s action to {% url 'polls:vote' question.id %}, and we set method="post". Using method="post" (as opposed to method="get") is very important, because the act of submitting this form will alter data server-side. Whenever you create a form that alters data server-side, use method="post". This tip isn’t specific to Django; it’s good web development practice in general.

forloop.counter indicates how many times the for tag has gone through its loop

Since we’re creating a POST form (which can have the effect of modifying data), we need to worry about Cross Site Request Forgeries. Thankfully, you don’t have to worry too hard, because Django comes with a helpful system for protecting against it. In short, all POST forms that are targeted at internal URLs should use the {% csrf_token %} template tag.

Now, let’s create a Django view that handles the submitted data and does something with it. Remember, in Tutorial 3, we created a URLconf for the polls application that includes this line:

We also created a dummy implementation of the vote() function. Let’s create a real version. Add the following to polls/views.py:

This code includes a few things we haven’t covered yet in this tutorial:

request.POST is a dictionary-like object that lets you access submitted data by key name. In this case, request.POST['choice'] returns the ID of the selected choice, as a string. request.POST values are always strings.

Note that Django also provides request.GET for accessing GET data in the same way – but we’re explicitly using request.POST in our code, to ensure that data is only altered via a POST call.

request.POST['choice'] will raise KeyError if choice wasn’t provided in POST data. The above code checks for KeyError and redisplays the question form with an error message if choice isn’t given.

F("votes") + 1 instructs the database to increase the vote count by 1.

After incrementing the choice count, the code returns an HttpResponseRedirect rather than a normal HttpResponse. HttpResponseRedirect takes a single argument: the URL to which the user will be redirected (see the following point for how we construct the URL in this case).

As the Python comment above points out, you should always return an HttpResponseRedirect after successfully dealing with POST data. This tip isn’t specific to Django; it’s good web development practice in general.

We are using the reverse() function in the HttpResponseRedirect constructor in this example. This function helps avoid having to hardcode a URL in the view function. It is given the name of the view that we want to pass control to and the variable portion of the URL pattern that points to that view. In this case, using the URLconf we set up in Tutorial 3, this reverse() call will return a string like

where the 3 is the value of question.id. This redirected URL will then call the 'results' view to display the final page.

As mentioned in Tutorial 3, request is an HttpRequest object. For more on HttpRequest objects, see the request and response documentation.

After somebody votes in a question, the vote() view redirects to the results page for the question. Let’s write that view:

This is almost exactly the same as the detail() view from Tutorial 3. The only difference is the template name. We’ll fix this redundancy later.

Now, create a polls/results.html template:

Now, go to /polls/1/ in your browser and vote in the question. You should see a results page that gets updated each time you vote. If you submit the form without having chosen a choice, you should see the error message.

The detail() (from Tutorial 3) and results() views are very short – and, as mentioned above, redundant. The index() view, which displays a list of polls, is similar.

These views represent a common case of basic web development: getting data from the database according to a parameter passed in the URL, loading a template and returning the rendered template. Because this is so common, Django provides a shortcut, called the “generic views” system.

Generic views abstract common patterns to the point where you don’t even need to write Python code to write an app. For example, the ListView and DetailView generic views abstract the concepts of “display a list of objects” and “display a detail page for a particular type of object” respectively.

Let’s convert our poll app to use the generic views system, so we can delete a bunch of our own code. We’ll have to take a few steps to make the conversion. We will:

Delete some of the old, unneeded views.

Introduce new views based on Django’s generic views.

Why the code-shuffle?

Generally, when writing a Django app, you’ll evaluate whether generic views are a good fit for your problem, and you’ll use them from the beginning, rather than refactoring your code halfway through. But this tutorial intentionally has focused on writing the views “the hard way” until now, to focus on core concepts.

You should know basic math before you start using a calculator.

First, open the polls/urls.py URLconf and change it like so:

Note that the name of the matched pattern in the path strings of the second and third patterns has changed from <question_id> to <pk>. This is necessary because we’ll use the DetailView generic view to replace our detail() and results() views, and it expects the primary key value captured from the URL to be called "pk".

Next, we’re going to remove our old index, detail, and results views and use Django’s generic views instead. To do so, open the polls/views.py file and change it like so:

Each generic view needs to know what model it will be acting upon. This is provided using either the model attribute (in this example, model = Question for DetailView and ResultsView) or by defining the get_queryset() method (as shown in IndexView).

By default, the DetailView generic view uses a template called <app name>/<model name>_detail.html. In our case, it would use the template "polls/question_detail.html". The template_name attribute is used to tell Django to use a specific template name instead of the autogenerated default template name. We also specify the template_name for the results list view – this ensures that the results view and the detail view have a different appearance when rendered, even though they’re both a DetailView behind the scenes.

Similarly, the ListView generic view uses a default template called <app name>/<model name>_list.html; we use template_name to tell ListView to use our existing "polls/index.html" template.

In previous parts of the tutorial, the templates have been provided with a context that contains the question and latest_question_list context variables. For DetailView the question variable is provided automatically – since we’re using a Django model (Question), Django is able to determine an appropriate name for the context variable. However, for ListView, the automatically generated context variable is question_list. To override this we provide the context_object_name attribute, specifying that we want to use latest_question_list instead. As an alternative approach, you could change your templates to match the new default context variables – but it’s a lot easier to tell Django to use the variable you want.

Run the server, and use your new polling app based on generic views.

For full details on generic views, see the generic views documentation.

When you’re comfortable with forms and generic views, read part 5 of this tutorial to learn about testing our polls app.

---

## Writing your first Django app, part 5 | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/intro/tutorial05/

**Contents:**
- Writing your first Django app, part 5¶
- Introducing automated testing¶
  - What are automated tests?¶
  - Why you need to create tests¶
    - Tests will save you time¶
    - Tests don’t just identify problems, they prevent them¶
    - Tests make your code more attractive¶
    - Tests help teams work together¶
- Basic testing strategies¶
- Writing our first test¶

This tutorial begins where Tutorial 4 left off. We’ve built a web-poll application, and we’ll now create some automated tests for it.

If you’re having trouble going through this tutorial, please head over to the Getting Help section of the FAQ.

Tests are routines that check the operation of your code.

Testing operates at different levels. Some tests might apply to a tiny detail (does a particular model method return values as expected?) while others examine the overall operation of the software (does a sequence of user inputs on the site produce the desired result?). That’s no different from the kind of testing you did earlier in Tutorial 2, using the shell to examine the behavior of a method, or running the application and entering data to check how it behaves.

What’s different in automated tests is that the testing work is done for you by the system. You create a set of tests once, and then as you make changes to your app, you can check that your code still works as you originally intended, without having to perform time consuming manual testing.

So why create tests, and why now?

You may feel that you have quite enough on your plate just learning Python/Django, and having yet another thing to learn and do may seem overwhelming and perhaps unnecessary. After all, our polls application is working quite happily now; going through the trouble of creating automated tests is not going to make it work any better. If creating the polls application is the last bit of Django programming you will ever do, then true, you don’t need to know how to create automated tests. But, if that’s not the case, now is an excellent time to learn.

Up to a certain point, ‘checking that it seems to work’ will be a satisfactory test. In a more sophisticated application, you might have dozens of complex interactions between components.

A change in any of those components could have unexpected consequences on the application’s behavior. Checking that it still ‘seems to work’ could mean running through your code’s functionality with twenty different variations of your test data to make sure you haven’t broken something - not a good use of your time.

That’s especially true when automated tests could do this for you in seconds. If something’s gone wrong, tests will also assist in identifying the code that’s causing the unexpected behavior.

Sometimes it may seem a chore to tear yourself away from your productive, creative programming work to face the unglamorous and unexciting business of writing tests, particularly when you know your code is working properly.

However, the task of writing tests is a lot more fulfilling than spending hours testing your application manually or trying to identify the cause of a newly-introduced problem.

It’s a mistake to think of tests merely as a negative aspect of development.

Without tests, the purpose or intended behavior of an application might be rather opaque. Even when it’s your own code, you will sometimes find yourself poking around in it trying to find out what exactly it’s doing.

Tests change that; they light up your code from the inside, and when something goes wrong, they focus light on the part that has gone wrong - even if you hadn’t even realized it had gone wrong.

You might have created a brilliant piece of software, but you will find that many other developers will refuse to look at it because it lacks tests; without tests, they won’t trust it. Jacob Kaplan-Moss, one of Django’s original developers, says “Code without tests is broken by design.”

That other developers want to see tests in your software before they take it seriously is yet another reason for you to start writing tests.

The previous points are written from the point of view of a single developer maintaining an application. Complex applications will be maintained by teams. Tests guarantee that colleagues don’t inadvertently break your code (and that you don’t break theirs without knowing). If you want to make a living as a Django programmer, you must be good at writing tests!

There are many ways to approach writing tests.

Some programmers follow a discipline called “test-driven development”; they actually write their tests before they write their code. This might seem counterintuitive, but in fact it’s similar to what most people will often do anyway: they describe a problem, then create some code to solve it. Test-driven development formalizes the problem in a Python test case.

More often, a newcomer to testing will create some code and later decide that it should have some tests. Perhaps it would have been better to write some tests earlier, but it’s never too late to get started.

Sometimes it’s difficult to figure out where to get started with writing tests. If you have written several thousand lines of Python, choosing something to test might not be easy. In such a case, it’s fruitful to write your first test the next time you make a change, either when you add a new feature or fix a bug.

So let’s do that right away.

Fortunately, there’s a little bug in the polls application for us to fix right away: the Question.was_published_recently() method returns True if the Question was published within the last day (which is correct) but also if the Question’s pub_date field is in the future (which certainly isn’t).

Confirm the bug by using the shell to check the method on a question whose date lies in the future:

Since things in the future are not ‘recent’, this is clearly wrong.

What we’ve just done in the shell to test for the problem is exactly what we can do in an automated test, so let’s turn that into an automated test.

A conventional place for an application’s tests is in the application’s tests.py file; the testing system will automatically find tests in any file whose name begins with test.

Put the following in the tests.py file in the polls application:

Here we have created a django.test.TestCase subclass with a method that creates a Question instance with a pub_date in the future. We then check the output of was_published_recently() - which ought to be False.

In the terminal, we can run our test:

and you’ll see something like:

If instead you’re getting a NameError here, you may have missed a step in Part 2 where we added imports of datetime and timezone to polls/models.py. Copy the imports from that section, and try running your tests again.

What happened is this:

manage.py test polls looked for tests in the polls application

it found a subclass of the django.test.TestCase class

it created a special database for the purpose of testing

it looked for test methods - ones whose names begin with test

in test_was_published_recently_with_future_question it created a Question instance whose pub_date field is 30 days in the future

… and using the assertIs() method, it discovered that its was_published_recently() returns True, though we wanted it to return False

The test informs us which test failed and even the line on which the failure occurred.

We already know what the problem is: Question.was_published_recently() should return False if its pub_date is in the future. Amend the method in models.py, so that it will only return True if the date is also in the past:

and run the test again:

After identifying a bug, we wrote a test that exposes it and corrected the bug in the code so our test passes.

Many other things might go wrong with our application in the future, but we can be sure that we won’t inadvertently reintroduce this bug, because running the test will warn us immediately. We can consider this little portion of the application pinned down safely forever.

While we’re here, we can further pin down the was_published_recently() method; in fact, it would be positively embarrassing if in fixing one bug we had introduced another.

Add two more test methods to the same class, to test the behavior of the method more comprehensively:

And now we have three tests that confirm that Question.was_published_recently() returns sensible values for past, recent, and future questions.

Again, polls is a minimal application, but however complex it grows in the future and whatever other code it interacts with, we now have some guarantee that the method we have written tests for will behave in expected ways.

The polls application is fairly undiscriminating: it will publish any question, including ones whose pub_date field lies in the future. We should improve this. Setting a pub_date in the future should mean that the Question is published at that moment, but invisible until then.

When we fixed the bug above, we wrote the test first and then the code to fix it. In fact that was an example of test-driven development, but it doesn’t really matter in which order we do the work.

In our first test, we focused closely on the internal behavior of the code. For this test, we want to check its behavior as it would be experienced by a user through a web browser.

Before we try to fix anything, let’s have a look at the tools at our disposal.

Django provides a test Client to simulate a user interacting with the code at the view level. We can use it in tests.py or even in the shell.

We will start again with the shell, where we need to do a couple of things that won’t be necessary in tests.py. The first is to set up the test environment in the shell:

setup_test_environment() installs a template renderer which will allow us to examine some additional attributes on responses such as response.context that otherwise wouldn’t be available. Note that this method does not set up a test database, so the following will be run against the existing database and the output may differ slightly depending on what questions you already created. You might get unexpected results if your TIME_ZONE in settings.py isn’t correct. If you don’t remember setting it earlier, check it before continuing.

Next we need to import the test client class (later in tests.py we will use the django.test.TestCase class, which comes with its own client, so this won’t be required):

With that ready, we can ask the client to do some work for us:

The list of polls shows polls that aren’t published yet (i.e. those that have a pub_date in the future). Let’s fix that.

In Tutorial 4 we introduced a class-based view, based on ListView:

We need to amend the get_queryset() method and change it so that it also checks the date by comparing it with timezone.now(). First we need to add an import:

and then we must amend the get_queryset method like so:

Question.objects.filter(pub_date__lte=timezone.now()) returns a queryset containing Questions whose pub_date is less than or equal to - that is, earlier than or equal to - timezone.now().

Now you can satisfy yourself that this behaves as expected by firing up runserver, loading the site in your browser, creating a few Question entries with dates in the past and future, and checking that only those that have been published are listed. You don’t want to have to do that every single time you make any change that might affect this - so let’s also create a test, based on our shell session above.

Add the following to polls/tests.py:

and we’ll create a shortcut function to create questions as well as a new test class:

Let’s look at some of these more closely.

First is a question shortcut function, create_question, to take some repetition out of the process of creating questions.

test_no_questions doesn’t create any questions, but checks the message: “No polls are available.” and verifies the latest_question_list is empty. Note that the django.test.TestCase class provides some additional assertion methods. In these examples, we use assertContains() and assertQuerySetEqual().

In test_past_question, we create a question and verify that it appears in the list.

In test_future_question, we create a question with a pub_date in the future. The database is reset for each test method, so the first question is no longer there, and so again the index shouldn’t have any questions in it.

And so on. In effect, we are using the tests to tell a story of admin input and user experience on the site, and checking that at every state and for every new change in the state of the system, the expected results are published.

What we have works well; however, even though future questions don’t appear in the index, users can still reach them if they know or guess the right URL. So we need to add a similar constraint to DetailView:

We should then add some tests, to check that a Question whose pub_date is in the past can be displayed, and that one with a pub_date in the future is not:

We ought to add a similar get_queryset method to ResultsView and create a new test class for that view. It’ll be very similar to what we have just created; in fact there will be a lot of repetition.

We could also improve our application in other ways, adding tests along the way. For example, it’s pointless that a Question with no related Choice can be published on the site. So, our views could check for this, and exclude such Question objects. Our tests would create a Question without a Choice, and then test that it’s not published, as well as create a similar Question with at least one Choice, and test that it is published.

Perhaps logged-in admin users should be allowed to see unpublished Question entries, but not ordinary visitors. Again: whatever needs to be added to the software to accomplish this should be accompanied by a test, whether you write the test first and then make the code pass the test, or work out the logic in your code first and then write a test to prove it.

At a certain point you are bound to look at your tests and wonder whether your code is suffering from test bloat, which brings us to:

It might seem that our tests are growing out of control. At this rate there will soon be more code in our tests than in our application, and the repetition is unaesthetic, compared to the elegant conciseness of the rest of our code.

It doesn’t matter. Let them grow. For the most part, you can write a test once and then forget about it. It will continue performing its useful function as you continue to develop your program.

Sometimes tests will need to be updated. Suppose that we amend our views so that only Question entries with associated Choice instances are published. In that case, many of our existing tests will fail - telling us exactly which tests need to be amended to bring them up to date, so to that extent tests help look after themselves.

At worst, as you continue developing, you might find that you have some tests that are now redundant. Even that’s not a problem; in testing redundancy is a good thing.

As long as your tests are sensibly arranged, they won’t become unmanageable. Good rules-of-thumb include having:

a separate TestClass for each model or view

a separate test method for each set of conditions you want to test

test method names that describe their function

This tutorial only introduces some of the basics of testing. There’s a great deal more you can do, and a number of very useful tools at your disposal to achieve some very clever things.

For example, while our tests here have covered some of the internal logic of a model and the way our views publish information, you can use an “in-browser” framework such as Selenium to test the way your HTML actually renders in a browser. These tools allow you to check not just the behavior of your Django code, but also, for example, of your JavaScript. It’s quite something to see the tests launch a browser, and start interacting with your site, as if a human being were driving it! Django includes LiveServerTestCase to facilitate integration with tools like Selenium.

If you have a complex application, you may want to run tests automatically with every commit for the purposes of continuous integration, so that quality control is itself - at least partially - automated.

A good way to spot untested parts of your application is to check code coverage. This also helps identify fragile or even dead code. If you can’t test a piece of code, it usually means that code should be refactored or removed. Coverage will help to identify dead code. See Integration with coverage.py for details.

Testing in Django has comprehensive information about testing.

For full details on testing, see Testing in Django.

When you’re comfortable with testing Django views, read part 6 of this tutorial to learn about static files management.

---

## Writing your first Django app, part 6 | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/intro/tutorial06/

**Contents:**
- Writing your first Django app, part 6¶
- Customize your app’s look and feel¶
- Adding a background-image¶

This tutorial begins where Tutorial 5 left off. We’ve built a tested web-poll application, and we’ll now add a stylesheet and an image.

Aside from the HTML generated by the server, web applications generally need to serve additional files — such as images, JavaScript, or CSS — necessary to render the complete web page. In Django, we refer to these files as “static files”.

For small projects, this isn’t a big deal, because you can keep the static files somewhere your web server can find it. However, in bigger projects – especially those comprised of multiple apps – dealing with the multiple sets of static files provided by each application starts to get tricky.

That’s what django.contrib.staticfiles is for: it collects static files from each of your applications (and any other places you specify) into a single location that can easily be served in production.

If you’re having trouble going through this tutorial, please head over to the Getting Help section of the FAQ.

First, create a directory called static in your polls directory. Django will look for static files there, similarly to how Django finds templates inside polls/templates/.

Django’s STATICFILES_FINDERS setting contains a list of finders that know how to discover static files from various sources. One of the defaults is AppDirectoriesFinder which looks for a “static” subdirectory in each of the INSTALLED_APPS, like the one in polls we just created. The admin site uses the same directory structure for its static files.

Within the static directory you have just created, create another directory called polls and within that create a file called style.css. In other words, your stylesheet should be at polls/static/polls/style.css. Because of how the AppDirectoriesFinder staticfile finder works, you can refer to this static file in Django as polls/style.css, similar to how you reference the path for templates.

Static file namespacing

Just like templates, we might be able to get away with putting our static files directly in polls/static (rather than creating another polls subdirectory), but it would actually be a bad idea. Django will choose the first static file it finds whose name matches, and if you had a static file with the same name in a different application, Django would be unable to distinguish between them. We need to be able to point Django at the right one, and the best way to ensure this is by namespacing them. That is, by putting those static files inside another directory named for the application itself.

Put the following code in that stylesheet (polls/static/polls/style.css):

Next, add the following at the top of polls/templates/polls/index.html:

The {% static %} template tag generates the absolute URL of static files.

That’s all you need to do for development.

Start the server (or restart it if it’s already running):

Reload http://localhost:8000/polls/ and you should see that the question links are green (Django style!) which means that your stylesheet was properly loaded.

Next, we’ll create a subdirectory for images. Create an images subdirectory in the polls/static/polls/ directory. Inside this directory, add any image file that you’d like to use as a background. For the purposes of this tutorial, we’re using a file named background.png, which will have the full path polls/static/polls/images/background.png.

Then, add a reference to your image in your stylesheet (polls/static/polls/style.css):

Reload http://localhost:8000/polls/ and you should see the background loaded in the top left of the screen.

The {% static %} template tag is not available for use in static files which aren’t generated by Django, like your stylesheet. You should always use relative paths to link your static files between each other, because then you can change STATIC_URL (used by the static template tag to generate its URLs) without having to modify a bunch of paths in your static files as well.

These are the basics. For more details on settings and other bits included with the framework see the static files howto and the staticfiles reference. Deploying static files discusses how to use static files on a real server.

When you’re comfortable with the static files, read part 7 of this tutorial to learn how to customize Django’s automatically-generated admin site.

---

## Writing your first Django app, part 7 | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/intro/tutorial07/

**Contents:**
- Writing your first Django app, part 7¶
- Customize the admin form¶
- Adding related objects¶
- Customize the admin change list¶
- Customize the admin look and feel¶
  - Customizing your project’s templates¶
  - Customizing your application’s templates¶
- Customize the admin index page¶

This tutorial begins where Tutorial 6 left off. We’re continuing the web-poll application and will focus on customizing Django’s automatically-generated admin site that we first explored in Tutorial 2.

If you’re having trouble going through this tutorial, please head over to the Getting Help section of the FAQ.

By registering the Question model with admin.site.register(Question), Django was able to construct a default form representation. Often, you’ll want to customize how the admin form looks and works. You’ll do this by telling Django the options you want when you register the object.

Let’s see how this works by reordering the fields on the edit form. Replace the admin.site.register(Question) line with:

You’ll follow this pattern – create a model admin class, then pass it as the second argument to admin.site.register() – any time you need to change the admin options for a model.

This particular change above makes the “Publication date” come before the “Question” field:

This isn’t impressive with only two fields, but for admin forms with dozens of fields, choosing an intuitive order is an important usability detail.

And speaking of forms with dozens of fields, you might want to split the form up into fieldsets:

The first element of each tuple in fieldsets is the title of the fieldset. Here’s what our form looks like now:

OK, we have our Question admin page, but a Question has multiple Choices, and the admin page doesn’t display choices.

There are two ways to solve this problem. The first is to register Choice with the admin just as we did with Question:

Now “Choices” is an available option in the Django admin. The “Add choice” form looks like this:

In that form, the “Question” field is a select box containing every question in the database. Django knows that a ForeignKey should be represented in the admin as a <select> box. In our case, only one question exists at this point.

Also note the “Add another question” button (displayed as a plus sign) to the right of the “Question” field. Every ForeignKey relationship gets this button for free. When you click this button, you’ll get a popup window with the “Add question” form. If you add a question in that window and click “Save”, Django will save the question to the database and dynamically add it as the selected choice on the “Add choice” form you’re looking at.

But, really, this is an inefficient way of adding Choice objects to the system. It’d be better if you could add a bunch of Choices directly when you create the Question object. Let’s make that happen.

Remove the register() call for the Choice model. Then, edit the Question registration code to read:

This tells Django: “Choice objects are edited on the Question admin page. By default, provide enough fields for 3 choices.”

Load the “Add question” page to see how that looks:

It works like this: There are three slots for related Choices – as specified by extra – and each time you come back to the “Change” page for an already-created object, you get another three extra slots.

At the end of the three current slots you will find an “Add another Choice” link. If you click on it, a new slot will be added. If you want to remove the added slot, you can click on the X to the top right of the added slot. This image shows an added slot:

One small problem, though. It takes a lot of screen space to display all the fields for entering related Choice objects. For that reason, Django offers a tabular way of displaying inline related objects. To use it, change the ChoiceInline declaration to read:

With that TabularInline (instead of StackedInline), the related objects are displayed in a more compact, table-based format:

Note that there is an extra “Delete?” column that allows removing rows added using the “Add another Choice” button and rows that have already been saved.

Now that the Question admin page is looking good, let’s make some tweaks to the “change list” page – the one that displays all the questions in the system.

Here’s what it looks like at this point:

By default, Django displays the str() of each object. But sometimes it’d be more helpful if we could display individual fields. To do that, use the list_display admin option, which is a list of field names to display, as columns, on the change list page for the object:

For good measure, let’s also include the was_published_recently() method from Tutorial 2:

Now the question change list page looks like this:

You can click on the column headers to sort by those values – except in the case of the was_published_recently header, because sorting by the output of an arbitrary method is not supported. Also note that the column header for was_published_recently is, by default, the name of the method (with underscores replaced with spaces), and that each line contains the string representation of the output.

You can improve that by using the display() decorator on that method (extending the polls/models.py file that was created in Tutorial 2), as follows:

For more information on the properties configurable via the decorator, see list_display.

Edit your polls/admin.py file again and add an improvement to the Question change list page: filters using the list_filter. Add the following line to QuestionAdmin:

That adds a “Filter” sidebar that lets people filter the change list by the pub_date field:

The type of filter displayed depends on the type of field you’re filtering on. Because pub_date is a DateTimeField, Django knows to give appropriate filter options: “Any date”, “Today”, “Past 7 days”, “This month”, “This year”.

This is shaping up well. Let’s add some search capability:

That adds a search box at the top of the change list. When somebody enters search terms, Django will search the question_text field. You can use as many fields as you’d like – although because it uses a LIKE query behind the scenes, limiting the number of search fields to a reasonable number will make it easier for your database to do the search.

Now’s also a good time to note that change lists give you free pagination. The default is to display 100 items per page. Change list pagination, search boxes, filters, date-hierarchies, and column-header-ordering all work together like you think they should.

Clearly, having “Django administration” at the top of each admin page is ridiculous. It’s just placeholder text.

You can change it, though, using Django’s template system. The Django admin is powered by Django itself, and its interfaces use Django’s own template system.

Create a templates directory in your djangotutorial directory. Templates can live anywhere on your filesystem that Django can access. (Django runs as whatever user your server runs.) However, keeping your templates within the project is a good convention to follow.

Open your settings file (mysite/settings.py, remember) and add a DIRS option in the TEMPLATES setting:

DIRS is a list of filesystem directories to check when loading Django templates; it’s a search path.

Just like the static files, we could have all our templates together, in one big templates directory, and it would work perfectly well. However, templates that belong to a particular application should be placed in that application’s template directory (e.g. polls/templates) rather than the project’s (templates). We’ll discuss in more detail in the reusable apps tutorial why we do this.

Now create a directory called admin inside templates, and copy the template admin/base_site.html from within the default Django admin template directory in the source code of Django itself (django/contrib/admin/templates) into that directory.

Where are the Django source files?

If you have difficulty finding where the Django source files are located on your system, run the following command:

Then, edit the file and replace {{ site_header|default:_('Django administration') }} (including the curly braces) with your own site’s name as you see fit. You should end up with a section of code like:

We use this approach to teach you how to override templates. In an actual project, you would probably use the django.contrib.admin.AdminSite.site_header attribute to more easily make this particular customization.

This template file contains lots of text like {% block branding %} and {{ title }}. The {% and {{ tags are part of Django’s template language. When Django renders admin/base_site.html, this template language will be evaluated to produce the final HTML page, just like we saw in Tutorial 3.

Note that any of Django’s default admin templates can be overridden. To override a template, do the same thing you did with base_site.html – copy it from the default directory into your custom directory, and make changes.

Astute readers will ask: But if DIRS was empty by default, how was Django finding the default admin templates? The answer is that, since APP_DIRS is set to True, Django automatically looks for a templates/ subdirectory within each application package, for use as a fallback (don’t forget that django.contrib.admin is an application).

Our poll application is not very complex and doesn’t need custom admin templates. But if it grew more sophisticated and required modification of Django’s standard admin templates for some of its functionality, it would be more sensible to modify the application’s templates, rather than those in the project. That way, you could include the polls application in any new project and be assured that it would find the custom templates it needed.

See the template loading documentation for more information about how Django finds its templates.

On a similar note, you might want to customize the look and feel of the Django admin index page.

By default, it displays all the apps in INSTALLED_APPS that have been registered with the admin application, in alphabetical order. You may want to make significant changes to the layout. After all, the index is probably the most important page of the admin, and it should be easy to use.

The template to customize is admin/index.html. (Do the same as with admin/base_site.html in the previous section – copy it from the default directory to your custom template directory). Edit the file, and you’ll see it uses a template variable called app_list. That variable contains every installed Django app. Instead of using that, you can hardcode links to object-specific admin pages in whatever way you think is best.

When you’re comfortable with the admin, read part 8 of this tutorial to learn how to use third-party packages.

---

## Writing your first Django app, part 8 | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/intro/tutorial08/

**Contents:**
- Writing your first Django app, part 8¶
- Installing Django Debug Toolbar¶
- Getting help from others¶
- Installing other third-party packages¶
- What’s next?¶

This tutorial begins where Tutorial 7 left off. We’ve built our web-poll application and will now look at third-party packages. One of Django’s strengths is the rich ecosystem of third-party packages. They’re community developed packages that can be used to quickly improve the feature set of an application.

This tutorial will show how to add Django Debug Toolbar, a commonly used third-party package. The Django Debug Toolbar has ranked in the top three most used third-party packages in the Django Developers Survey in recent years.

If you’re having trouble going through this tutorial, please head over to the Getting Help section of the FAQ.

Django Debug Toolbar is a useful tool for debugging Django web applications. It’s a third-party package that is maintained by the community organization Django Commons. The toolbar helps you understand how your application functions and to identify problems. It does so by providing panels that provide debug information about the current request and response.

To install a third-party application like the toolbar, you need to install the package by running the below command within an activated virtual environment. This is similar to our earlier step to install Django.

Third-party packages that integrate with Django need some post-installation setup to integrate them with your project. Often you will need to add the package’s Django app to your INSTALLED_APPS setting. Some packages need other changes, like additions to your URLconf (urls.py).

Django Debug Toolbar requires several setup steps. Follow them in its installation guide. The steps are not duplicated in this tutorial, because as a third-party package, it may change separately to Django’s schedule.

Once installed, you should be able to see the DjDT “handle” on the right side of the browser window when you browse to http://localhost:8000/admin/. Click it to open the debug toolbar and use the tools in each panel. See the panels documentation page for more information on what the panels show.

At some point you will run into a problem, for example the toolbar may not render. When this happens and you’re unable to resolve the issue yourself, there are options available to you.

If the problem is with a specific package, check if there’s a troubleshooting guide or FAQ in the package’s documentation. For example the Django Debug Toolbar has a Tips section that outlines troubleshooting options.

Search for similar issues on the package’s issue tracker. Django Debug Toolbar’s is on GitHub.

Consult the Django Forum.

Join the Django Discord server.

There are many more third-party packages, which you can find using the fantastic Django resource, Django Packages.

It can be difficult to know what third-party packages you should use. This depends on your needs and goals. Sometimes it’s fine to use a package that’s in its alpha state. Other times, you need to know it’s production ready. Adam Johnson has a blog post that outlines a set of characteristics that qualifies a package as “well maintained”. Django Packages shows data for some of these characteristics, such as when the package was last updated.

As Adam points out in his post, when the answer to one of the questions is “no”, that’s an opportunity to contribute.

The beginner tutorial ends here. In the meantime, you might want to check out some pointers on where to go from here.

If you are familiar with Python packaging and interested in learning how to turn polls into a “reusable app”, check out Advanced tutorial: How to write reusable apps.

---
