# Djangoproject - Howto

**Pages:** 37

---

## Deployment checklist | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

**Contents:**
- Deployment checklist¶
- Run manage.py check --deploy¶
- Switch away from manage.py runserver¶
- Critical settings¶
  - SECRET_KEY¶
  - DEBUG¶
- Environment-specific settings¶
  - ALLOWED_HOSTS¶
  - CACHES¶
  - DATABASES¶

The internet is a hostile environment. Before deploying your Django project, you should take some time to review your settings, with security, performance, and operations in mind.

Django includes many security features. Some are built-in and always enabled. Others are optional because they aren’t always appropriate, or because they’re inconvenient for development. For example, forcing HTTPS may not be suitable for all websites, and it’s impractical for local development.

Performance optimizations are another category of trade-offs with convenience. For instance, caching is useful in production, less so for local development. Error reporting needs are also widely different.

The following checklist includes settings that:

must be set properly for Django to provide the expected level of security;

are expected to be different in each environment;

enable optional security features;

enable performance optimizations;

provide error reporting.

Many of these settings are sensitive and should be treated as confidential. If you’re releasing the source code for your project, a common practice is to publish suitable settings for development, and to use a private settings module for production.

Some of the checks described below can be automated using the check --deploy option. Be sure to run it against your production settings file as described in the option’s documentation.

The runserver command is not designed for a production setting. Be sure to switch to a production-ready WSGI or ASGI server. For a few common options, see WSGI servers or ASGI servers.

The secret key must be a large random value and it must be kept secret.

Make sure that the key used in production isn’t used anywhere else and avoid committing it to source control. This reduces the number of vectors from which an attacker may acquire the key.

Instead of hardcoding the secret key in your settings module, consider loading it from an environment variable:

If rotating secret keys, you may use SECRET_KEY_FALLBACKS:

Ensure that old secret keys are removed from SECRET_KEY_FALLBACKS in a timely manner.

You must never enable debug in production.

You’re certainly developing your project with DEBUG = True, since this enables handy features like full tracebacks in your browser.

For a production environment, though, this is a really bad idea, because it leaks lots of information about your project: excerpts of your source code, local variables, settings, libraries used, etc.

When DEBUG = False, Django doesn’t work at all without a suitable value for ALLOWED_HOSTS.

This setting is required to protect your site against some CSRF attacks. If you use a wildcard, you must perform your own validation of the Host HTTP header, or otherwise ensure that you aren’t vulnerable to this category of attacks.

You should also configure the web server that sits in front of Django to validate the host. It should respond with a static error page or ignore requests for incorrect hosts instead of forwarding the request to Django. This way you’ll avoid spurious errors in your Django logs (or emails if you have error reporting configured that way). For example, on nginx you might set up a default server to return “444 No Response” on an unrecognized host:

If you’re using a cache, connection parameters may be different in development and in production. Django defaults to per-process local-memory caching which may not be desirable.

Cache servers often have weak authentication. Make sure they only accept connections from your application servers.

Database connection parameters are probably different in development and in production.

Database passwords are very sensitive. You should protect them exactly like SECRET_KEY.

For maximum security, make sure database servers only accept connections from your application servers.

If you haven’t set up backups for your database, do it right now!

If your site sends emails, these values need to be set correctly.

By default, Django sends email from webmaster@localhost and root@localhost. However, some mail providers reject email from these addresses. To use different sender addresses, modify the DEFAULT_FROM_EMAIL and SERVER_EMAIL settings.

Static files are automatically served by the development server. In production, you must define a STATIC_ROOT directory where collectstatic will copy them.

See How to manage static files (e.g. images, JavaScript, CSS) for more information.

Media files are uploaded by your users. They’re untrusted! Make sure your web server never attempts to interpret them. For instance, if a user uploads a .php file, the web server shouldn’t execute it.

Now is a good time to check your backup strategy for these files.

Any website which allows users to log in should enforce site-wide HTTPS to avoid transmitting access tokens in clear. In Django, access tokens include the login/password, the session cookie, and password reset tokens. (You can’t do much to protect password reset tokens if you’re sending them by email.)

Protecting sensitive areas such as the user account or the admin isn’t sufficient, because the same session cookie is used for HTTP and HTTPS. Your web server must redirect all HTTP traffic to HTTPS, and only transmit HTTPS requests to Django.

Once you’ve set up HTTPS, enable the following settings.

Set this to True to avoid transmitting the CSRF cookie over HTTP accidentally.

Set this to True to avoid transmitting the session cookie over HTTP accidentally.

Setting DEBUG = False disables several features that are only useful in development. In addition, you can tune the following settings.

Consider using cached sessions to improve performance.

If using database-backed sessions, regularly clear old sessions to avoid storing unnecessary data.

Enabling persistent database connections can result in a nice speed-up when connecting to the database accounts for a significant part of the request processing time.

This helps a lot on virtualized hosts with limited network performance.

Enabling the cached template loader often improves performance drastically, as it avoids compiling each template every time it needs to be rendered. When DEBUG = False, the cached template loader is enabled automatically. See django.template.loaders.cached.Loader for more information.

By the time you push your code to production, it’s hopefully robust, but you can’t rule out unexpected errors. Thankfully, Django can capture errors and notify you accordingly.

Review your logging configuration before putting your website in production, and check that it works as expected as soon as you have received some traffic.

See Logging for details on logging.

ADMINS will be notified of 500 errors by email.

MANAGERS will be notified of 404 errors. IGNORABLE_404_URLS can help filter out spurious reports.

See How to manage error reporting for details on error reporting by email.

Error reporting by email doesn’t scale very well

Consider using an error monitoring system such as Sentry before your inbox is flooded by reports. Sentry can also aggregate logs.

Django includes default views and templates for several HTTP error codes. You may want to override the default templates by creating the following templates in your root template directory: 404.html, 500.html, 403.html, and 400.html. The default error views that use these templates should suffice for 99% of web applications, but you can customize them as well.

---

## How to authenticate against Django’s user database from Apache | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/apache-auth/

**Contents:**
- How to authenticate against Django’s user database from Apache¶
- Authentication with mod_wsgi¶
  - Authorization with mod_wsgi and Django groups¶

Since keeping multiple authentication databases in sync is a common problem when dealing with Apache, you can configure Apache to authenticate against Django’s authentication system directly. This requires Apache version >= 2.2 and mod_wsgi >= 2.0. For example, you could:

Serve static/media files directly from Apache only to authenticated users.

Authenticate access to a Subversion repository against Django users with a certain permission.

Allow certain users to connect to a WebDAV share created with mod_dav.

If you have installed a custom user model and want to use this default auth handler, it must support an is_active attribute. If you want to use group based authorization, your custom user must have a relation named ‘groups’, referring to a related object that has a ‘name’ field. You can also specify your own custom mod_wsgi auth handler if your custom cannot conform to these requirements.

The use of WSGIApplicationGroup %{GLOBAL} in the configurations below presumes that your Apache instance is running only one Django application. If you are running more than one Django application, please refer to the Defining Application Groups section of the mod_wsgi docs for more information about this setting.

Make sure that mod_wsgi is installed and activated and that you have followed the steps to set up Apache with mod_wsgi.

Next, edit your Apache configuration to add a location that you want only authenticated users to be able to view:

The WSGIAuthUserScript directive tells mod_wsgi to execute the check_password function in specified wsgi script, passing the user name and password that it receives from the prompt. In this example, the WSGIAuthUserScript is the same as the WSGIScriptAlias that defines your application that is created by django-admin startproject.

Using Apache 2.2+ with authentication

Make sure that mod_auth_basic and mod_authz_user are loaded.

These might be compiled statically into Apache, or you might need to use LoadModule to load them dynamically in your httpd.conf:

Finally, edit your WSGI script mysite.wsgi to tie Apache’s authentication to your site’s authentication mechanisms by importing the check_password function:

Requests beginning with /secret/ will now require a user to authenticate.

The mod_wsgi access control mechanisms documentation provides additional details and information about alternative methods of authentication.

mod_wsgi also provides functionality to restrict a particular location to members of a group.

In this case, the Apache configuration should look like this:

To support the WSGIAuthGroupScript directive, the same WSGI script mysite.wsgi must also import the groups_for_user function which returns a list groups the given user belongs to.

Requests for /secret/ will now also require user to be a member of the “secret-agents” group.

---

## How to authenticate using REMOTE_USER | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/auth-remote-user/

**Contents:**
- How to authenticate using REMOTE_USER¶
- Configuration¶
- Using REMOTE_USER on login pages only¶

This document describes how to make use of external authentication sources in your Django applications. This type of authentication solution is typically seen on intranet sites, with single sign-on solutions such as IIS and Integrated Windows Authentication or Apache and mod_authnz_ldap, CAS, WebAuth, mod_auth_sspi, etc.

When the web server takes care of authentication it typically provides the authenticated user as REMOTE_USER. In Django, this value is made available in request.META (as REMOTE_USER when supplied as an environment variable, as in WSGI, or HTTP_REMOTE_USER when supplied via an HTTP header, as in ASGI). Django can be configured to make use of the REMOTE_USER value using the RemoteUserMiddleware or PersistentRemoteUserMiddleware, and RemoteUserBackend classes found in django.contrib.auth.

First, you must add the django.contrib.auth.middleware.RemoteUserMiddleware to the MIDDLEWARE setting after the django.contrib.auth.middleware.AuthenticationMiddleware:

Next, you must replace the ModelBackend with RemoteUserBackend in the AUTHENTICATION_BACKENDS setting:

With this setup, RemoteUserMiddleware will detect the username in request.META['REMOTE_USER'] (or request.META['HTTP_REMOTE_USER'] under ASGI) and will authenticate and auto-login that user using the RemoteUserBackend.

Be aware that this particular setup disables authentication with the default ModelBackend. This means that if the REMOTE_USER value is not set then the user is unable to log in, even using Django’s admin interface. Adding 'django.contrib.auth.backends.ModelBackend' to the AUTHENTICATION_BACKENDS list will use ModelBackend as a fallback if REMOTE_USER is absent, which will solve these issues.

Django’s user management, such as the views in contrib.admin and the createsuperuser management command, doesn’t integrate with remote users. These interfaces work with users stored in the database regardless of AUTHENTICATION_BACKENDS.

Since the RemoteUserBackend inherits from ModelBackend, you will still have all of the same permissions checking that is implemented in ModelBackend.

Users with is_active=False won’t be allowed to authenticate. Use AllowAllUsersRemoteUserBackend if you want to allow them to.

If your authentication mechanism uses a custom HTTP header and not REMOTE_USER, you can subclass RemoteUserMiddleware and set the header attribute to the desired request.META key. For example:

This custom middleware is then used in the MIDDLEWARE setting instead of django.contrib.auth.middleware.RemoteUserMiddleware:

RemoteUserMiddleware must not be deployed in configurations where a client can supply the header. You must be sure that your web server or reverse proxy always sets or strips that header based on the appropriate authentication checks, never permitting an end user to submit a fake (or “spoofed”) header value.

Since the HTTP headers X-Auth-User and X-Auth_User (for example) both normalize to the HTTP_X_AUTH_USER key in request.META, you must also check that your web server doesn’t allow a spoofed header using underscores in place of dashes.

Under WSGI, this warning doesn’t apply to RemoteUserMiddleware in its default configuration with header = "REMOTE_USER", since a key that doesn’t start with HTTP_ in request.META can only be set by your WSGI server, not directly from an HTTP request header.

This warning applies under ASGI in all configurations, because there is no equivalent for a WSGI server’s ability to place a trusted value in the environ. ASGI deployments must use a reverse proxy as described above when using this middleware.

If you need more control, you can create your own authentication backend that inherits from RemoteUserBackend and override one or more of its attributes and methods.

The RemoteUserMiddleware authentication middleware assumes that the HTTP request header REMOTE_USER is present with all authenticated requests. That might be expected and practical when Basic HTTP Auth with htpasswd or similar mechanisms are used, but with Negotiate (GSSAPI/Kerberos) or other resource intensive authentication methods, the authentication in the front-end HTTP server is usually only set up for one or a few login URLs, and after successful authentication, the application is supposed to maintain the authenticated session itself.

PersistentRemoteUserMiddleware provides support for this use case. It will maintain the authenticated session until explicit logout by the user. The class can be used as a drop-in replacement of RemoteUserMiddleware in the documentation above.

---

## How to configure and use logging | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/logging/

**Contents:**
- How to configure and use logging¶
- Make a basic logging call¶
- Customize logging configuration¶
  - Basic logging configuration¶
    - Create a LOGGING dictionary¶
    - Configure a handler¶
    - Configure a logger mapping¶
    - Configure a formatter¶
    - Use logger namespacing¶
      - Using logger hierarchies and propagation¶

Django logging reference

Django logging overview

Django provides a working default logging configuration that is readily extended.

To send a log message from within your code, you place a logging call into it.

Don’t be tempted to use logging calls in settings.py.

The way that Django logging is configured as part of the setup() function means that logging calls placed in settings.py may not work as expected, because logging will not be set up at that point. To explore logging, use a view function as suggested in the example below.

First, import the Python logging library, and then obtain a logger instance with logging.getLogger(). Provide the getLogger() method with a name to identify it and the records it emits. A good option is to use __name__ (see Use logger namespacing below for more on this) which will provide the name of the current Python module as a dotted path:

It’s a good convention to perform this declaration at module level.

And then in a function, for example in a view, send a record to the logger:

When this code is executed, a LogRecord containing that message will be sent to the logger. If you’re using Django’s default logging configuration, the message will appear in the console.

The WARNING level used in the example above is one of several logging severity levels: DEBUG, INFO, WARNING, ERROR, CRITICAL. So, another example might be:

Records with a level lower than WARNING will not appear in the console by default. Changing this behavior requires additional configuration.

Although Django’s logging configuration works out of the box, you can control exactly how your logs are sent to various destinations - to log files, external services, email and so on - with some additional configuration.

logger mappings, to determine which records are sent to which handlers

handlers, to determine what they do with the records they receive

filters, to provide additional control over the transfer of records, and even modify records in-place

formatters, to convert LogRecord objects to a string or other form for consumption by human beings or another system

There are various ways of configuring logging. In Django, the LOGGING setting is most commonly used. The setting uses the dictConfig format, and extends the default logging configuration.

See Configuring logging for an explanation of how your custom settings are merged with Django’s defaults.

See the Python logging documentation for details of other ways of configuring logging. For the sake of simplicity, this documentation will only consider configuration via the LOGGING setting.

When configuring logging, it makes sense to

It nearly always makes sense to retain and extend the default logging configuration by setting disable_existing_loggers to False.

This example configures a single handler named file, that uses Python’s FileHandler to save logs of level DEBUG and higher to the file general.log (at the project root):

Different handler classes take different configuration options. For more information on available handler classes, see the AdminEmailHandler provided by Django and the various handler classes provided by Python.

Logging levels can also be set on the handlers (by default, they accept log messages of all levels). Using the example above, adding:

would define a handler configuration that only accepts records of level DEBUG and higher.

To send records to this handler, configure a logger mapping to use it for example:

The mapping’s name determines which log records it will process. This configuration ('') is unnamed. That means that it will process records from all loggers (see Use logger namespacing below on how to use the mapping name to determine the loggers for which it will process records).

It will forward messages of levels DEBUG and higher to the handler named file.

Note that a logger can forward messages to multiple handlers, so the relation between loggers and handlers is many-to-many.

in your code, you will find that message in the file general.log in the root of the project.

By default, the final log output contains the message part of each log record. Use a formatter if you want to include additional data. First name and define your formatters - this example defines formatters named verbose and simple:

The style keyword allows you to specify { for str.format() or $ for string.Template formatting; the default is $.

See LogRecord attributes for the LogRecord attributes you can include.

To apply a formatter to a handler, add a formatter entry to the handler’s dictionary referring to the formatter by name, for example:

The unnamed logging configuration '' captures logs from any Python application. A named logging configuration will capture logs only from loggers with matching names.

The namespace of a logger instance is defined using getLogger(). For example in views.py of my_app:

will create a logger in the my_app.views namespace. __name__ allows you to organize log messages according to their provenance within your project’s applications automatically. It also ensures that you will not experience name collisions.

A logger mapping named my_app.views will capture records from this logger:

A logger mapping named my_app will be more permissive, capturing records from loggers anywhere within the my_app namespace (including my_app.views, my_app.utils, and so on):

You can also define logger namespacing explicitly:

and set up logger mappings accordingly.

Logger naming is hierarchical. my_app is the parent of my_app.views, which is the parent of my_app.views.private. Unless specified otherwise, logger mappings will propagate the records they process to their parents - a record from a logger in the my_app.views.private namespace will be handled by a mapping for both my_app and my_app.views.

To manage this behavior, set the propagation key on the mappings you define:

propagate defaults to True. In this example, the logs from my_app.views.private will not be handled by the parent, but logs from my_app.views will.

Logging is most useful when it contains as much information as possible, but not information that you don’t need - and how much you need depends upon what you’re doing. When you’re debugging, you need a level of information that would be excessive and unhelpful if you had to deal with it in production.

You can configure logging to provide you with the level of detail you need, when you need it. Rather than manually change configuration to achieve this, a better way is to apply configuration automatically according to the environment.

For example, you could set an environment variable DJANGO_LOG_LEVEL appropriately in your development and staging environments, and make use of it in a logger mapping thus:

- so that unless the environment specifies a lower log level, this configuration will only forward records of severity WARNING and above to its handler.

Other options in the configuration (such as the level or formatter option of handlers) can be similarly managed.

---

## How to create CSV output | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/outputting-csv/

**Contents:**
- How to create CSV output¶
- Using the Python CSV library¶
  - Streaming large CSV files¶
- Using the template system¶
- Other text-based formats¶

This document explains how to output CSV (Comma Separated Values) dynamically using Django views. To do this, you can either use the Python CSV library or the Django template system.

Python comes with a CSV library, csv. The key to using it with Django is that the csv module’s CSV-creation capability acts on file-like objects, and Django’s HttpResponse objects are file-like objects.

The code and comments should be self-explanatory, but a few things deserve a mention:

The response gets a special MIME type, text/csv. This tells browsers that the document is a CSV file, rather than an HTML file. If you leave this off, browsers will probably interpret the output as HTML, which will result in ugly, scary gobbledygook in the browser window.

The response gets an additional Content-Disposition header, which contains the name of the CSV file. This filename is arbitrary; call it whatever you want. It’ll be used by browsers in the “Save as…” dialog, etc.

You can hook into the CSV-generation API by passing response as the first argument to csv.writer. The csv.writer function expects a file-like object, and HttpResponse objects fit the bill.

For each row in your CSV file, call writer.writerow, passing it an iterable.

The CSV module takes care of quoting for you, so you don’t have to worry about escaping strings with quotes or commas in them. Pass writerow() your raw strings, and it’ll do the right thing.

When dealing with views that generate very large responses, you might want to consider using Django’s StreamingHttpResponse instead. For example, by streaming a file that takes a long time to generate you can avoid a load balancer dropping a connection that might have otherwise timed out while the server was generating the response.

In this example, we make full use of Python generators to efficiently handle the assembly and transmission of a large CSV file:

Alternatively, you can use the Django template system to generate CSV. This is lower-level than using the convenient Python csv module, but the solution is presented here for completeness.

The idea here is to pass a list of items to your template, and have the template output the commas in a for loop.

Here’s an example, which generates the same CSV file as above:

The only difference between this example and the previous example is that this one uses template loading instead of the CSV module. The rest of the code – such as the content_type='text/csv' – is the same.

Then, create the template my_template_name.txt, with this template code:

This short template iterates over the given data and displays a line of CSV for each row. It uses the addslashes template filter to ensure there aren’t any problems with quotes.

Notice that there isn’t very much specific to CSV here – just the specific output format. You can use either of these techniques to output any text-based format you can dream of. You can also use a similar technique to generate arbitrary binary data; see How to create PDF files for an example.

---

## How to create custom django-admin commands | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/custom-management-commands/

**Contents:**
- How to create custom django-admin commands¶
- Accepting optional arguments¶
- Management commands and locales¶
- Testing¶
- Overriding commands¶
- Command objects¶
  - Attributes¶
  - Methods¶
  - BaseCommand subclasses¶
  - Command exceptions¶

Applications can register their own actions with manage.py. For example, you might want to add a manage.py action for a Django app that you’re distributing. In this document, we will be building a custom closepoll command for the polls application from the tutorial.

To do this, add a management/commands directory to the application. Django will register a manage.py command for each Python module in that directory whose name doesn’t begin with an underscore. For example:

In this example, the closepoll command will be made available to any project that includes the polls application in INSTALLED_APPS.

The _private.py module will not be available as a management command.

The closepoll.py module has only one requirement – it must define a class Command that extends BaseCommand or one of its subclasses.

Custom management commands are especially useful for running standalone scripts or for scripts that are periodically executed from the UNIX crontab or from Windows scheduled tasks control panel.

To implement the command, edit polls/management/commands/closepoll.py to look like this:

When you are using management commands and wish to provide console output, you should write to self.stdout and self.stderr, instead of printing to stdout and stderr directly. By using these proxies, it becomes much easier to test your custom command. Note also that you don’t need to end messages with a newline character, it will be added automatically, unless you specify the ending parameter:

The new custom command can be called using python manage.py closepoll <poll_ids>.

The handle() method takes one or more poll_ids and sets poll.opened to False for each one. If the user referenced any nonexistent polls, a CommandError is raised. The poll.opened attribute does not exist in the tutorial and was added to polls.models.Question for this example.

The same closepoll could be easily modified to delete a given poll instead of closing it by accepting additional command line options. These custom options can be added in the add_arguments() method like this:

The option (delete in our example) is available in the options dict parameter of the handle method. See the argparse Python documentation for more about add_argument usage.

In addition to being able to add custom command line options, all management commands can accept some default options such as --verbosity and --traceback.

By default, management commands are executed with the current active locale.

If, for some reason, your custom management command must run without an active locale (for example, to prevent translated content from being inserted into the database), deactivate translations using the @no_translations decorator on your handle() method:

Since translation deactivation requires access to configured settings, the decorator can’t be used for commands that work without configured settings.

Information on how to test custom management commands can be found in the testing docs.

Django registers the built-in commands and then searches for commands in INSTALLED_APPS in reverse. During the search, if a command name duplicates an already registered command, the newly discovered command overrides the first.

In other words, to override a command, the new command must have the same name and its app must be before the overridden command’s app in INSTALLED_APPS.

Management commands from third-party apps that have been unintentionally overridden can be made available under a new name by creating a new command in one of your project’s apps (ordered before the third-party app in INSTALLED_APPS) which imports the Command of the overridden command.

The base class from which all management commands ultimately derive.

Use this class if you want access to all of the mechanisms which parse the command-line arguments and work out what code to call in response; if you don’t need to change any of that behavior, consider using one of its subclasses.

Subclassing the BaseCommand class requires that you implement the handle() method.

All attributes can be set in your derived class and can be used in BaseCommand’s subclasses.

A short description of the command, which will be printed in the help message when the user runs the command python manage.py help <command>.

If your command defines mandatory positional arguments, you can customize the message error returned in the case of missing arguments. The default is output by argparse (“too few arguments”).

A boolean indicating whether the command outputs SQL statements; if True, the output will automatically be wrapped with BEGIN; and COMMIT;. Default value is False.

A boolean; if True, the command prints a warning if the set of migrations on disk don’t match the migrations in the database. A warning doesn’t prevent the command from executing. Default value is False.

A list or tuple of tags, e.g. [Tags.staticfiles, Tags.models]. System checks registered in the chosen tags will be checked for errors prior to executing the command. The value '__all__' can be used to specify that all system checks should be performed. Default value is '__all__'.

An instance attribute that helps create colored output when writing to stdout or stderr. For example:

See Syntax coloring to learn how to modify the color palette and to see the available styles (use uppercased versions of the “roles” described in that section).

If you pass the --no-color option when running your command, all self.style() calls will return the original string uncolored.

The default command options to suppress in the help output. This should be a set of option names (e.g. '--verbosity'). The default values for the suppressed options are still passed.

BaseCommand has a few methods that can be overridden but only the handle() method must be implemented.

Implementing a constructor in a subclass

If you implement __init__ in your subclass of BaseCommand, you must call BaseCommand’s __init__:

Returns a CommandParser instance, which is an ArgumentParser subclass with a few customizations for Django.

You can customize the instance by overriding this method and calling super() with kwargs of ArgumentParser parameters.

Entry point to add parser arguments to handle command line arguments passed to the command. Custom commands should override this method to add both positional and optional arguments accepted by the command. Calling super() is not needed when directly subclassing BaseCommand.

Returns the Django version, which should be correct for all built-in Django commands. User-supplied commands can override this method to return their own version.

Tries to execute this command, performing system checks if needed (as controlled by the requires_system_checks attribute). If the command raises a CommandError, it’s intercepted and printed to stderr.

Calling a management command in your code

execute() should not be called directly from your code to execute a command. Use call_command() instead.

The actual logic of the command. Subclasses must implement this method.

It may return a string which will be printed to stdout (wrapped by BEGIN; and COMMIT; if output_transaction is True).

Uses the system check framework to inspect the entire Django project for potential problems. Serious problems are raised as a CommandError; warnings are output to stderr; minor notifications are output to stdout.

If app_configs and tags are both None, all system checks are performed except deployment and database related checks. tags can be a list of check tags, like compatibility or models.

You can pass include_deployment_checks=True to also perform deployment checks, and list of database aliases in the databases to run database related checks against them.

Supplies kwargs for the call to check(), including transforming the value of requires_system_checks to the tag kwarg.

Override this method to change the values supplied to check(). For example, to opt into database related checks you can override get_check_kwargs() as follows:

A management command which takes one or more installed application labels as arguments, and does something with each of them.

Rather than implementing handle(), subclasses must implement handle_app_config(), which will be called once for each application.

Perform the command’s actions for app_config, which will be an AppConfig instance corresponding to an application label given on the command line.

A management command which takes one or more arbitrary arguments (labels) on the command line, and does something with each of them.

Rather than implementing handle(), subclasses must implement handle_label(), which will be called once for each label.

A string describing the arbitrary arguments passed to the command. The string is used in the usage text and error messages of the command. Defaults to 'label'.

Perform the command’s actions for label, which will be the string as given on the command line.

Exception class indicating a problem while executing a management command.

If this exception is raised during the execution of a management command from a command line console, it will be caught and turned into a nicely-printed error message to the appropriate output stream (i.e., stderr); as a result, raising this exception (with a sensible description of the error) is the preferred way to indicate that something has gone wrong in the execution of a command. It accepts the optional returncode argument to customize the exit status for the management command to exit with, using sys.exit().

If a management command is called from code through call_command(), it’s up to you to catch the exception when needed.

---

## How to create custom django-admin commands | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/custom-management-commands

**Contents:**
- How to create custom django-admin commands¶
- Accepting optional arguments¶
- Management commands and locales¶
- Testing¶
- Overriding commands¶
- Command objects¶
  - Attributes¶
  - Methods¶
  - BaseCommand subclasses¶
  - Command exceptions¶

Applications can register their own actions with manage.py. For example, you might want to add a manage.py action for a Django app that you’re distributing. In this document, we will be building a custom closepoll command for the polls application from the tutorial.

To do this, add a management/commands directory to the application. Django will register a manage.py command for each Python module in that directory whose name doesn’t begin with an underscore. For example:

In this example, the closepoll command will be made available to any project that includes the polls application in INSTALLED_APPS.

The _private.py module will not be available as a management command.

The closepoll.py module has only one requirement – it must define a class Command that extends BaseCommand or one of its subclasses.

Custom management commands are especially useful for running standalone scripts or for scripts that are periodically executed from the UNIX crontab or from Windows scheduled tasks control panel.

To implement the command, edit polls/management/commands/closepoll.py to look like this:

When you are using management commands and wish to provide console output, you should write to self.stdout and self.stderr, instead of printing to stdout and stderr directly. By using these proxies, it becomes much easier to test your custom command. Note also that you don’t need to end messages with a newline character, it will be added automatically, unless you specify the ending parameter:

The new custom command can be called using python manage.py closepoll <poll_ids>.

The handle() method takes one or more poll_ids and sets poll.opened to False for each one. If the user referenced any nonexistent polls, a CommandError is raised. The poll.opened attribute does not exist in the tutorial and was added to polls.models.Question for this example.

The same closepoll could be easily modified to delete a given poll instead of closing it by accepting additional command line options. These custom options can be added in the add_arguments() method like this:

The option (delete in our example) is available in the options dict parameter of the handle method. See the argparse Python documentation for more about add_argument usage.

In addition to being able to add custom command line options, all management commands can accept some default options such as --verbosity and --traceback.

By default, management commands are executed with the current active locale.

If, for some reason, your custom management command must run without an active locale (for example, to prevent translated content from being inserted into the database), deactivate translations using the @no_translations decorator on your handle() method:

Since translation deactivation requires access to configured settings, the decorator can’t be used for commands that work without configured settings.

Information on how to test custom management commands can be found in the testing docs.

Django registers the built-in commands and then searches for commands in INSTALLED_APPS in reverse. During the search, if a command name duplicates an already registered command, the newly discovered command overrides the first.

In other words, to override a command, the new command must have the same name and its app must be before the overridden command’s app in INSTALLED_APPS.

Management commands from third-party apps that have been unintentionally overridden can be made available under a new name by creating a new command in one of your project’s apps (ordered before the third-party app in INSTALLED_APPS) which imports the Command of the overridden command.

The base class from which all management commands ultimately derive.

Use this class if you want access to all of the mechanisms which parse the command-line arguments and work out what code to call in response; if you don’t need to change any of that behavior, consider using one of its subclasses.

Subclassing the BaseCommand class requires that you implement the handle() method.

All attributes can be set in your derived class and can be used in BaseCommand’s subclasses.

A short description of the command, which will be printed in the help message when the user runs the command python manage.py help <command>.

If your command defines mandatory positional arguments, you can customize the message error returned in the case of missing arguments. The default is output by argparse (“too few arguments”).

A boolean indicating whether the command outputs SQL statements; if True, the output will automatically be wrapped with BEGIN; and COMMIT;. Default value is False.

A boolean; if True, the command prints a warning if the set of migrations on disk don’t match the migrations in the database. A warning doesn’t prevent the command from executing. Default value is False.

A list or tuple of tags, e.g. [Tags.staticfiles, Tags.models]. System checks registered in the chosen tags will be checked for errors prior to executing the command. The value '__all__' can be used to specify that all system checks should be performed. Default value is '__all__'.

An instance attribute that helps create colored output when writing to stdout or stderr. For example:

See Syntax coloring to learn how to modify the color palette and to see the available styles (use uppercased versions of the “roles” described in that section).

If you pass the --no-color option when running your command, all self.style() calls will return the original string uncolored.

The default command options to suppress in the help output. This should be a set of option names (e.g. '--verbosity'). The default values for the suppressed options are still passed.

BaseCommand has a few methods that can be overridden but only the handle() method must be implemented.

Implementing a constructor in a subclass

If you implement __init__ in your subclass of BaseCommand, you must call BaseCommand’s __init__:

Returns a CommandParser instance, which is an ArgumentParser subclass with a few customizations for Django.

You can customize the instance by overriding this method and calling super() with kwargs of ArgumentParser parameters.

Entry point to add parser arguments to handle command line arguments passed to the command. Custom commands should override this method to add both positional and optional arguments accepted by the command. Calling super() is not needed when directly subclassing BaseCommand.

Returns the Django version, which should be correct for all built-in Django commands. User-supplied commands can override this method to return their own version.

Tries to execute this command, performing system checks if needed (as controlled by the requires_system_checks attribute). If the command raises a CommandError, it’s intercepted and printed to stderr.

Calling a management command in your code

execute() should not be called directly from your code to execute a command. Use call_command() instead.

The actual logic of the command. Subclasses must implement this method.

It may return a string which will be printed to stdout (wrapped by BEGIN; and COMMIT; if output_transaction is True).

Uses the system check framework to inspect the entire Django project for potential problems. Serious problems are raised as a CommandError; warnings are output to stderr; minor notifications are output to stdout.

If app_configs and tags are both None, all system checks are performed except deployment and database related checks. tags can be a list of check tags, like compatibility or models.

You can pass include_deployment_checks=True to also perform deployment checks, and list of database aliases in the databases to run database related checks against them.

Supplies kwargs for the call to check(), including transforming the value of requires_system_checks to the tag kwarg.

Override this method to change the values supplied to check(). For example, to opt into database related checks you can override get_check_kwargs() as follows:

A management command which takes one or more installed application labels as arguments, and does something with each of them.

Rather than implementing handle(), subclasses must implement handle_app_config(), which will be called once for each application.

Perform the command’s actions for app_config, which will be an AppConfig instance corresponding to an application label given on the command line.

A management command which takes one or more arbitrary arguments (labels) on the command line, and does something with each of them.

Rather than implementing handle(), subclasses must implement handle_label(), which will be called once for each label.

A string describing the arbitrary arguments passed to the command. The string is used in the usage text and error messages of the command. Defaults to 'label'.

Perform the command’s actions for label, which will be the string as given on the command line.

Exception class indicating a problem while executing a management command.

If this exception is raised during the execution of a management command from a command line console, it will be caught and turned into a nicely-printed error message to the appropriate output stream (i.e., stderr); as a result, raising this exception (with a sensible description of the error) is the preferred way to indicate that something has gone wrong in the execution of a command. It accepts the optional returncode argument to customize the exit status for the management command to exit with, using sys.exit().

If a management command is called from code through call_command(), it’s up to you to catch the exception when needed.

---

## How to create custom model fields | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/custom-model-fields/

**Contents:**
- How to create custom model fields¶
- Introduction¶
  - Our example object¶
- Background theory¶
  - Database storage¶
  - What does a field class do?¶
- Writing a field subclass¶
  - Field deconstruction¶
  - Field attributes not affecting database column definition¶
  - Changing a custom field’s base class¶

The model reference documentation explains how to use Django’s standard field classes – CharField, DateField, etc. For many purposes, those classes are all you’ll need. Sometimes, though, the Django version won’t meet your precise requirements, or you’ll want to use a field that is entirely different from those shipped with Django.

Django’s built-in field types don’t cover every possible database column type – only the common types, such as VARCHAR and INTEGER. For more obscure column types, such as geographic polygons or even user-created types such as PostgreSQL custom types, you can define your own Django Field subclasses.

Alternatively, you may have a complex Python object that can somehow be serialized to fit into a standard database column type. This is another case where a Field subclass will help you use your object with your models.

Creating custom fields requires a bit of attention to detail. To make things easier to follow, we’ll use a consistent example throughout this document: wrapping a Python object representing the deal of cards in a hand of Bridge. Don’t worry, you don’t have to know how to play Bridge to follow this example. You only need to know that 52 cards are dealt out equally to four players, who are traditionally called north, east, south and west. Our class looks something like this:

This is an ordinary Python class, with nothing Django-specific about it. We’d like to be able to do things like this in our models (we assume the hand attribute on the model is an instance of Hand):

We assign to and retrieve from the hand attribute in our model just like any other Python class. The trick is to tell Django how to handle saving and loading such an object.

In order to use the Hand class in our models, we do not have to change this class at all. This is ideal, because it means you can easily write model support for existing classes where you cannot change the source code.

You might only be wanting to take advantage of custom database column types and deal with the data as standard Python types in your models; strings, or floats, for example. This case is similar to our Hand example and we’ll note any differences as we go along.

Let’s start with model fields. If you break it down, a model field provides a way to take a normal Python object – string, boolean, datetime, or something more complex like Hand – and convert it to and from a format that is useful when dealing with the database. (Such a format is also useful for serialization, but as we’ll see later, that is easier once you have the database side under control).

Fields in a model must somehow be converted to fit into an existing database column type. Different databases provide different sets of valid column types, but the rule is still the same: those are the only types you have to work with. Anything you want to store in the database must fit into one of those types.

Normally, you’re either writing a Django field to match a particular database column type, or you will need a way to convert your data to, say, a string.

For our Hand example, we could convert the card data to a string of 104 characters by concatenating all the cards together in a predetermined order – say, all the north cards first, then the east, south and west cards. So Hand objects can be saved to text or character columns in the database.

All of Django’s fields (and when we say fields in this document, we always mean model fields and not form fields) are subclasses of django.db.models.Field. Most of the information that Django records about a field is common to all fields – name, help text, uniqueness and so forth. Storing all that information is handled by Field. We’ll get into the precise details of what Field can do later on; for now, suffice it to say that everything descends from Field and then customizes key pieces of the class behavior.

It’s important to realize that a Django field class is not what is stored in your model attributes. The model attributes contain normal Python objects. The field classes you define in a model are actually stored in the Meta class when the model class is created (the precise details of how this is done are unimportant here). This is because the field classes aren’t necessary when you’re just creating and modifying attributes. Instead, they provide the machinery for converting between the attribute value and what is stored in the database or sent to the serializer.

Keep this in mind when creating your own custom fields. The Django Field subclass you write provides the machinery for converting between your Python instances and the database/serializer values in various ways (there are differences between storing a value and using a value for lookups, for example). If this sounds a bit tricky, don’t worry – it will become clearer in the examples below. Just remember that you will often end up creating two classes when you want a custom field:

The first class is the Python object that your users will manipulate. They will assign it to the model attribute, they will read from it for displaying purposes, things like that. This is the Hand class in our example.

The second class is the Field subclass. This is the class that knows how to convert your first class back and forth between its permanent storage form and the Python form.

When planning your Field subclass, first give some thought to which existing Field class your new field is most similar to. Can you subclass an existing Django field and save yourself some work? If not, you should subclass the Field class, from which everything is descended.

Initializing your new field is a matter of separating out any arguments that are specific to your case from the common arguments and passing the latter to the __init__() method of Field (or your parent class).

In our example, we’ll call our field HandField. (It’s a good idea to call your Field subclass <Something>Field, so it’s easily identifiable as a Field subclass.) It doesn’t behave like any existing field, so we’ll subclass directly from Field:

Our HandField accepts most of the standard field options (see the list below), but we ensure it has a fixed length, since it only needs to hold 52 card values plus their suits; 104 characters in total.

Many of Django’s model fields accept options that they don’t do anything with. For example, you can pass both editable and auto_now to a django.db.models.DateField and it will ignore the editable parameter (auto_now being set implies editable=False). No error is raised in this case.

This behavior simplifies the field classes, because they don’t need to check for options that aren’t necessary. They pass all the options to the parent class and then don’t use them later on. It’s up to you whether you want your fields to be more strict about the options they select, or to use the more permissive behavior of the current fields.

The Field.__init__() method takes the following parameters:

rel: Used for related fields (like ForeignKey). For advanced use only.

serialize: If False, the field will not be serialized when the model is passed to Django’s serializers. Defaults to True.

db_tablespace: Only for index creation, if the backend supports tablespaces. You can usually ignore this option.

auto_created: True if the field was automatically created, as for the OneToOneField used by model inheritance. For advanced use only.

All of the options without an explanation in the above list have the same meaning they do for normal Django fields. See the field documentation for examples and details.

The counterpoint to writing your __init__() method is writing the deconstruct() method. It’s used during model migrations to tell Django how to take an instance of your new field and reduce it to a serialized form - in particular, what arguments to pass to __init__() to recreate it.

If you haven’t added any extra options on top of the field you inherited from, then there’s no need to write a new deconstruct() method. If, however, you’re changing the arguments passed in __init__() (like we are in HandField), you’ll need to supplement the values being passed.

deconstruct() returns a tuple of four items: the field’s attribute name, the full import path of the field class, the positional arguments (as a list), and the keyword arguments (as a dict). Note this is different from the deconstruct() method for custom classes which returns a tuple of three things.

As a custom field author, you don’t need to care about the first two values; the base Field class has all the code to work out the field’s attribute name and import path. You do, however, have to care about the positional and keyword arguments, as these are likely the things you are changing.

For example, in our HandField class we’re always forcibly setting max_length in __init__(). The deconstruct() method on the base Field class will see this and try to return it in the keyword arguments; thus, we can drop it from the keyword arguments for readability:

If you add a new keyword argument, you need to write code in deconstruct() that puts its value into kwargs yourself. You should also omit the value from kwargs when it isn’t necessary to reconstruct the state of the field, such as when the default value is being used:

More complex examples are beyond the scope of this document, but remember - for any configuration of your Field instance, deconstruct() must return arguments that you can pass to __init__ to reconstruct that state.

Pay extra attention if you set new default values for arguments in the Field superclass; you want to make sure they’re always included, rather than disappearing if they take on the old default value.

In addition, try to avoid returning values as positional arguments; where possible, return values as keyword arguments for maximum future compatibility. If you change the names of things more often than their position in the constructor’s argument list, you might prefer positional, but bear in mind that people will be reconstructing your field from the serialized version for quite a while (possibly years), depending how long your migrations live for.

You can see the results of deconstruction by looking in migrations that include the field, and you can test deconstruction in unit tests by deconstructing and reconstructing the field:

You can override Field.non_db_attrs to customize attributes of a field that don’t affect a column definition. It’s used during model migrations to detect no-op AlterField operations.

You can’t change the base class of a custom field because Django won’t detect the change and make a migration for it. For example, if you start with:

and then decide that you want to use TextField instead, you can’t change the subclass like this:

Instead, you must create a new custom field class and update your models to reference it:

As discussed in removing fields, you must retain the original CustomCharField class as long as you have migrations that reference it.

As always, you should document your field type, so users will know what it is. In addition to providing a docstring for it, which is useful for developers, you can also allow users of the admin app to see a short description of the field type via the django.contrib.admindocs application. To do this provide descriptive text in a description class attribute of your custom field. In the above example, the description displayed by the admindocs application for a HandField will be ‘A hand of cards (bridge style)’.

In the django.contrib.admindocs display, the field description is interpolated with field.__dict__ which allows the description to incorporate arguments of the field. For example, the description for CharField is:

Once you’ve created your Field subclass, you might consider overriding a few standard methods, depending on your field’s behavior. The list of methods below is in approximately decreasing order of importance, so start from the top.

Say you’ve created a PostgreSQL custom type called mytype. You can subclass Field and implement the db_type() method, like so:

Once you have MytypeField, you can use it in any model, just like any other Field type:

If you aim to build a database-agnostic application, you should account for differences in database column types. For example, the date/time column type in PostgreSQL is called timestamp, while the same column in MySQL is called datetime. You can handle this in a db_type() method by checking the connection.vendor attribute. Current built-in vendor names are: sqlite, postgresql, mysql, and oracle.

The db_type() and rel_db_type() methods are called by Django when the framework constructs the CREATE TABLE statements for your application – that is, when you first create your tables. The methods are also called when constructing a WHERE clause that includes the model field – that is, when you retrieve data using QuerySet methods like get(), filter(), and exclude() and have the model field as an argument.

Some database column types accept parameters, such as CHAR(25), where the parameter 25 represents the maximum column length. In cases like these, it’s more flexible if the parameter is specified in the model rather than being hardcoded in the db_type() method. For example, it wouldn’t make much sense to have a CharMaxlength25Field, shown here:

The better way of doing this would be to make the parameter specifiable at run time – i.e., when the class is instantiated. To do that, implement Field.__init__(), like so:

Finally, if your column requires truly complex SQL setup, return None from db_type(). This will cause Django’s SQL creation code to skip over this field. You are then responsible for creating the column in the right table in some other way, but this gives you a way to tell Django to get out of the way.

The rel_db_type() method is called by fields such as ForeignKey and OneToOneField that point to another field to determine their database column data types. For example, if you have an UnsignedAutoField, you also need the foreign keys that point to that field to use the same data type:

If your custom Field class deals with data structures that are more complex than strings, dates, integers, or floats, then you may need to override from_db_value() and to_python().

If present for the field subclass, from_db_value() will be called in all circumstances when the data is loaded from the database, including in aggregates and values() calls.

to_python() is called by deserialization and during the clean() method used from forms.

As a general rule, to_python() should deal gracefully with any of the following arguments:

An instance of the correct type (e.g., Hand in our ongoing example).

None (if the field allows null=True)

In our HandField class, we’re storing the data as a VARCHAR field in the database, so we need to be able to process strings and None in the from_db_value(). In to_python(), we need to also handle Hand instances:

Notice that we always return a Hand instance from these methods. That’s the Python object type we want to store in the model’s attribute.

For to_python(), if anything goes wrong during value conversion, you should raise a ValidationError exception.

Since using a database requires conversion in both ways, if you override from_db_value() you also have to override get_prep_value() to convert Python objects back to query values.

If your custom field uses the CHAR, VARCHAR or TEXT types for MySQL, you must make sure that get_prep_value() always returns a string type. MySQL performs flexible and unexpected matching when a query is performed on these types and the provided value is an integer, which can cause queries to include unexpected objects in their results. This problem cannot occur if you always return a string type from get_prep_value().

Some data types (for example, dates) need to be in a specific format before they can be used by a database backend. get_db_prep_value() is the method where those conversions should be made. The specific connection that will be used for the query is passed as the connection parameter. This allows you to use backend-specific conversion logic if it is required.

For example, Django uses the following method for its BinaryField:

In case your custom field needs a special conversion when being saved that is not the same as the conversion used for normal query parameters, you can override get_db_prep_save().

If you want to preprocess the value just before saving, you can use pre_save(). For example, Django’s DateTimeField uses this method to set the attribute correctly in the case of auto_now or auto_now_add.

If you do override this method, you must return the value of the attribute at the end. You should also update the model’s attribute if you make any changes to the value so that code holding references to the model will always see the correct value.

To customize the form field used by ModelForm, you can override formfield().

The form field class can be specified via the form_class and choices_form_class arguments; the latter is used if the field has choices specified, the former otherwise. If these arguments are not provided, CharField or TypedChoiceField will be used.

All of the kwargs dictionary is passed directly to the form field’s __init__() method. Normally, all you need to do is set up a good default for the form_class (and maybe choices_form_class) argument and then delegate further handling to the parent class. This might require you to write a custom form field (and even a form widget). See the forms documentation for information about this.

If you wish to exclude the field from the ModelForm, you can override the formfield() method to return None.

Continuing our ongoing example, we can write the formfield() method as:

This assumes we’ve imported a MyFormField field class (which has its own default widget). This document doesn’t cover the details of writing custom form fields.

If you have created a db_type() method, you don’t need to worry about get_internal_type() – it won’t be used much. Sometimes, though, your database storage is similar in type to some other field, so you can use that other field’s logic to create the right column.

No matter which database backend we are using, this will mean that migrate and other SQL commands create the right column type for storing a string.

If get_internal_type() returns a string that is not known to Django for the database backend you are using – that is, it doesn’t appear in django.db.backends.<db_name>.base.DatabaseWrapper.data_types – the string will still be used by the serializer, but the default db_type() method will return None. See the documentation of db_type() for reasons why this might be useful. Putting a descriptive string in as the type of the field for the serializer is a useful idea if you’re ever going to be using the serializer output in some other place, outside of Django.

To customize how the values are serialized by a serializer, you can override value_to_string(). Using value_from_object() is the best way to get the field’s value prior to serialization. For example, since HandField uses strings for its data storage anyway, we can reuse some existing conversion code:

Writing a custom field can be a tricky process, particularly if you’re doing complex conversions between your Python types and your database and serialization formats. Here are a couple of tips to make things go more smoothly:

Look at the existing Django fields (in django/db/models/fields/__init__.py) for inspiration. Try to find a field that’s similar to what you want and extend it a little bit, instead of creating an entirely new field from scratch.

Put a __str__() method on the class you’re wrapping up as a field. There are a lot of places where the default behavior of the field code is to call str() on the value. (In our examples in this document, value would be a Hand instance, not a HandField). So if your __str__() method automatically converts to the string form of your Python object, you can save yourself a lot of work.

In addition to the above methods, fields that deal with files have a few other special requirements which must be taken into account. The majority of the mechanics provided by FileField, such as controlling database storage and retrieval, can remain unchanged, leaving subclasses to deal with the challenge of supporting a particular type of file.

Django provides a File class, which is used as a proxy to the file’s contents and operations. This can be subclassed to customize how the file is accessed, and what methods are available. It lives at django.db.models.fields.files, and its default behavior is explained in the file documentation.

Once a subclass of File is created, the new FileField subclass must be told to use it. To do so, assign the new File subclass to the special attr_class attribute of the FileField subclass.

In addition to the above details, there are a few guidelines which can greatly improve the efficiency and readability of the field’s code.

The source for Django’s own ImageField (in django/db/models/fields/files.py) is a great example of how to subclass FileField to support a particular type of file, as it incorporates all of the techniques described above.

Cache file attributes wherever possible. Since files may be stored in remote storage systems, retrieving them may cost extra time, or even money, that isn’t always necessary. Once a file is retrieved to obtain some data about its content, cache as much of that data as possible to reduce the number of times the file must be retrieved on subsequent calls for that information.

---

## How to create custom template tags and filters | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/custom-template-tags/

**Contents:**
- How to create custom template tags and filters¶
- Code layout¶
- Writing custom template filters¶
  - Registering custom filters¶
  - Template filters that expect strings¶
  - Filters and auto-escaping¶
  - Filters and time zones¶
- Writing custom template tags¶
  - Simple tags¶
  - Simple block tags¶

Django’s template language comes with a wide variety of built-in tags and filters designed to address the presentation logic needs of your application. Nevertheless, you may find yourself needing functionality that is not covered by the core set of template primitives. You can extend the template engine by defining custom tags and filters using Python, and then make them available to your templates using the {% load %} tag.

The most common place to specify custom template tags and filters is inside a Django app. If they relate to an existing app, it makes sense to bundle them there; otherwise, they can be added to a new app. When a Django app is added to INSTALLED_APPS, any tags it defines in the conventional location described below are automatically made available to load within templates.

The app should contain a templatetags directory, at the same level as models.py, views.py, etc. If this doesn’t already exist, create it - don’t forget the __init__.py file to ensure the directory is treated as a Python package.

Development server won’t automatically restart

After adding the templatetags module, you will need to restart your server before you can use the tags or filters in templates.

Your custom tags and filters will live in a module inside the templatetags directory. The name of the module file is the name you’ll use to load the tags later, so be careful to pick a name that won’t clash with custom tags and filters in another app.

For example, if your custom tags/filters are in a file called poll_extras.py, your app layout might look like this:

And in your template you would use the following:

The app that contains the custom tags must be in INSTALLED_APPS in order for the {% load %} tag to work. This is a security feature: It allows you to host Python code for many template libraries on a single host machine without enabling access to all of them for every Django installation.

There’s no limit on how many modules you put in the templatetags package. Just keep in mind that a {% load %} statement will load tags/filters for the given Python module name, not the name of the app.

To be a valid tag library, the module must contain a module-level variable named register that is a template.Library instance, in which all the tags and filters are registered. So, near the top of your module, put the following:

Alternatively, template tag modules can be registered through the 'libraries' argument to DjangoTemplates. This is useful if you want to use a different label from the template tag module name when loading template tags. It also enables you to register tags without installing an application.

For a ton of examples, read the source code for Django’s default filters and tags. They’re in django/template/defaultfilters.py and django/template/defaulttags.py, respectively.

For more information on the load tag, read its documentation.

Custom filters are Python functions that take one or two arguments:

The value of the variable (input) – not necessarily a string.

The value of the argument – this can have a default value, or be left out altogether.

For example, in the filter {{ var|foo:"bar" }}, the filter foo would be passed the variable var and the argument "bar".

Since the template language doesn’t provide exception handling, any exception raised from a template filter will be exposed as a server error. Thus, filter functions should avoid raising exceptions if there is a reasonable fallback value to return. In case of input that represents a clear bug in a template, raising an exception may still be better than silent failure which hides the bug.

Here’s an example filter definition:

And here’s an example of how that filter would be used:

Most filters don’t take arguments. In this case, leave the argument out of your function:

Once you’ve written your filter definition, you need to register it with your Library instance, to make it available to Django’s template language:

The Library.filter() method takes two arguments:

The name of the filter – a string.

The compilation function – a Python function (not the name of the function as a string).

You can use register.filter() as a decorator instead:

If you leave off the name argument, as in the second example above, Django will use the function’s name as the filter name.

Finally, register.filter() also accepts three keyword arguments, is_safe, needs_autoescape, and expects_localtime. These arguments are described in filters and auto-escaping and filters and time zones below.

If you’re writing a template filter that only expects a string as the first argument, you should use the decorator stringfilter. This will convert an object to its string value before being passed to your function:

This way, you’ll be able to pass, say, an integer to this filter, and it won’t cause an AttributeError (because integers don’t have lower() methods).

When writing a custom filter, give some thought to how the filter will interact with Django’s auto-escaping behavior. Note that two types of strings can be passed around inside the template code:

Raw strings are the native Python strings. On output, they’re escaped if auto-escaping is in effect and presented unchanged, otherwise.

Safe strings are strings that have been marked safe from further escaping at output time. Any necessary escaping has already been done. They’re commonly used for output that contains raw HTML that is intended to be interpreted as-is on the client side.

Internally, these strings are of type SafeString. You can test for them using code like:

Template filter code falls into one of two situations:

Your filter does not introduce any HTML-unsafe characters (<, >, ', " or &) into the result that were not already present. In this case, you can let Django take care of all the auto-escaping handling for you. All you need to do is set the is_safe flag to True when you register your filter function, like so:

This flag tells Django that if a “safe” string is passed into your filter, the result will still be “safe” and if a non-safe string is passed in, Django will automatically escape it, if necessary.

You can think of this as meaning “this filter is safe – it doesn’t introduce any possibility of unsafe HTML.”

The reason is_safe is necessary is because there are plenty of normal string operations that will turn a SafeData object back into a normal str object and, rather than try to catch them all, which would be very difficult, Django repairs the damage after the filter has completed.

For example, suppose you have a filter that adds the string xx to the end of any input. Since this introduces no dangerous HTML characters to the result (aside from any that were already present), you should mark your filter with is_safe:

When this filter is used in a template where auto-escaping is enabled, Django will escape the output whenever the input is not already marked as “safe”.

By default, is_safe is False, and you can omit it from any filters where it isn’t required.

Be careful when deciding if your filter really does leave safe strings as safe. If you’re removing characters, you might inadvertently leave unbalanced HTML tags or entities in the result. For example, removing a > from the input might turn <a> into <a, which would need to be escaped on output to avoid causing problems. Similarly, removing a semicolon (;) can turn &amp; into &amp, which is no longer a valid entity and thus needs further escaping. Most cases won’t be nearly this tricky, but keep an eye out for any problems like that when reviewing your code.

Marking a filter is_safe will coerce the filter’s return value to a string. If your filter should return a boolean or other non-string value, marking it is_safe will probably have unintended consequences (such as converting a boolean False to the string ‘False’).

Alternatively, your filter code can manually take care of any necessary escaping. This is necessary when you’re introducing new HTML markup into the result. You want to mark the output as safe from further escaping so that your HTML markup isn’t escaped further, so you’ll need to handle the input yourself.

To mark the output as a safe string, use django.utils.safestring.mark_safe().

Be careful, though. You need to do more than just mark the output as safe. You need to ensure it really is safe, and what you do depends on whether auto-escaping is in effect. The idea is to write filters that can operate in templates where auto-escaping is either on or off in order to make things easier for your template authors.

In order for your filter to know the current auto-escaping state, set the needs_autoescape flag to True when you register your filter function. (If you don’t specify this flag, it defaults to False). This flag tells Django that your filter function wants to be passed an extra keyword argument, called autoescape, that is True if auto-escaping is in effect and False otherwise. It is recommended to set the default of the autoescape parameter to True, so that if you call the function from Python code it will have escaping enabled by default.

For example, let’s write a filter that emphasizes the first character of a string:

The needs_autoescape flag and the autoescape keyword argument mean that our function will know whether automatic escaping is in effect when the filter is called. We use autoescape to decide whether the input data needs to be passed through django.utils.html.conditional_escape or not. (In the latter case, we use the identity function as the “escape” function.) The conditional_escape() function is like escape() except it only escapes input that is not a SafeData instance. If a SafeData instance is passed to conditional_escape(), the data is returned unchanged.

Finally, in the above example, we remember to mark the result as safe so that our HTML is inserted directly into the template without further escaping.

There’s no need to worry about the is_safe flag in this case (although including it wouldn’t hurt anything). Whenever you manually handle the auto-escaping issues and return a safe string, the is_safe flag won’t change anything either way.

Avoiding XSS vulnerabilities when reusing built-in filters

Django’s built-in filters have autoescape=True by default in order to get the proper autoescaping behavior and avoid a cross-site script vulnerability.

In older versions of Django, be careful when reusing Django’s built-in filters as autoescape defaults to None. You’ll need to pass autoescape=True to get autoescaping.

For example, if you wanted to write a custom filter called urlize_and_linebreaks that combined the urlize and linebreaksbr filters, the filter would look like:

would be equivalent to:

If you write a custom filter that operates on datetime objects, you’ll usually register it with the expects_localtime flag set to True:

When this flag is set, if the first argument to your filter is a time zone aware datetime, Django will convert it to the current time zone before passing it to your filter when appropriate, according to rules for time zones conversions in templates.

Tags are more complex than filters, because tags can do anything. Django provides a number of shortcuts that make writing most types of tags easier. First we’ll explore those shortcuts, then explain how to write a tag from scratch for those cases when the shortcuts aren’t powerful enough.

Many template tags take a number of arguments – strings or template variables – and return a result after doing some processing based solely on the input arguments and some external information. For example, a current_time tag might accept a format string and return the time as a string formatted accordingly.

To ease the creation of these types of tags, Django provides a helper function, simple_tag. This function, which is a method of django.template.Library, takes a function that accepts any number of arguments, wraps it in a render function and the other necessary bits mentioned above and registers it with the template system.

Our current_time function could thus be written like this:

A few things to note about the simple_tag helper function:

Checking for the required number of arguments, etc., has already been done by the time our function is called, so we don’t need to do that.

The quotes around the argument (if any) have already been stripped away, so we receive a plain string.

If the argument was a template variable, our function is passed the current value of the variable, not the variable itself.

Unlike other tag utilities, simple_tag passes its output through conditional_escape() if the template context is in autoescape mode, to ensure correct HTML and protect you from XSS vulnerabilities.

If additional escaping is not desired, you will need to use mark_safe() if you are absolutely sure that your code does not contain XSS vulnerabilities. For building small HTML snippets, use of format_html() instead of mark_safe() is strongly recommended.

If your template tag needs to access the current context, you can use the takes_context argument when registering your tag:

Note that the first argument must be called context.

For more information on how the takes_context option works, see the section on inclusion tags.

If you need to rename your tag, you can provide a custom name for it:

simple_tag functions may accept any number of positional or keyword arguments. For example:

Then in the template any number of arguments, separated by spaces, may be passed to the template tag. Like in Python, the values for keyword arguments are set using the equal sign (”=”) and must be provided after the positional arguments. For example:

It’s possible to store the tag results in a template variable rather than directly outputting it. This is done by using the as argument followed by the variable name. Doing so enables you to output the content yourself where you see fit:

When a section of rendered template needs to be passed into a custom tag, Django provides the simple_block_tag helper function to accomplish this. Similar to simple_tag(), this function accepts a custom tag function, but with the additional content argument, which contains the rendered content as defined inside the tag. This allows dynamic template sections to be easily incorporated into custom tags.

For example, a custom block tag which creates a chart could look like this:

The content argument contains everything in between the {% chart %} and {% endchart %} tags:

If there are other template tags or variables inside the content block, they will be rendered before being passed to the tag function. In the example above, request.user will be resolved by the time render_chart is called.

Block tags are closed with end{name} (for example, endchart). This can be customized with the end_name parameter:

Which would require a template definition like this:

A few things to note about simple_block_tag:

The first argument must be called content, and it will contain the contents of the template tag as a rendered string.

Variables passed to the tag are not included in the rendering context of the content, as would be when using the {% with %} tag.

Just like simple_tag, simple_block_tag:

Validates the quantity and quality of the arguments.

Strips quotes from arguments if necessary.

Escapes the output accordingly.

Supports passing takes_context=True at registration time to access context. Note that in this case, the first argument to the custom function must be called context, and content must follow.

Supports renaming the tag by passing the name argument when registering.

Supports accepting any number of positional or keyword arguments.

Supports storing the result in a template variable using the as variant.

simple_block_tag behaves similarly to simple_tag regarding auto-escaping. For details on escaping and safety, refer to simple_tag. Because the content argument has already been rendered by Django, it is already escaped.

Consider a custom template tag that generates a message box that supports multiple message levels and content beyond a simple phrase. This could be implemented using a simple_block_tag as follows:

When combined with a minimal view and corresponding template, as shown here:

The following HTML is produced as the rendered output:

Another common type of template tag is the type that displays some data by rendering another template. For example, Django’s admin interface uses custom template tags to display the buttons along the bottom of the “add/change” form pages. Those buttons always look the same, but the link targets change depending on the object being edited – so they’re a perfect case for using a small template that is filled with details from the current object. (In the admin’s case, this is the submit_row tag.)

These sorts of tags are called “inclusion tags”.

Writing inclusion tags is probably best demonstrated by example. Let’s write a tag that outputs a list of choices for a given Poll object, such as was created in the tutorials. We’ll use the tag like this:

…and the output will be something like this:

First, define the function that takes the argument and produces a dictionary of data for the result. The important point here is we only need to return a dictionary, not anything more complex. This will be used as a template context for the template fragment. Example:

Next, create the template used to render the tag’s output. This template is a fixed feature of the tag: the tag writer specifies it, not the template designer. Following our example, the template is very short:

Now, create and register the inclusion tag by calling the inclusion_tag() method on a Library object. Following our example, if the above template is in a file called results.html in a directory that’s searched by the template loader, we’d register the tag like this:

Alternatively it is possible to register the inclusion tag using a django.template.Template instance:

…when first creating the function.

Sometimes, your inclusion tags might require a large number of arguments, making it a pain for template authors to pass in all the arguments and remember their order. To solve this, Django provides a takes_context option for inclusion tags. If you specify takes_context in creating a template tag, the tag will have no required arguments, and the underlying Python function will have one argument – the template context as of when the tag was called.

For example, say you’re writing an inclusion tag that will always be used in a context that contains home_link and home_title variables that point back to the main page. Here’s what the Python function would look like:

Note that the first parameter to the function must be called context.

In that register.inclusion_tag() line, we specified takes_context=True and the name of the template. Here’s what the template link.html might look like:

Then, any time you want to use that custom tag, load its library and call it without any arguments, like so:

Note that when you’re using takes_context=True, there’s no need to pass arguments to the template tag. It automatically gets access to the context.

The takes_context parameter defaults to False. When it’s set to True, the tag is passed the context object, as in this example. That’s the only difference between this case and the previous inclusion_tag example.

inclusion_tag functions may accept any number of positional or keyword arguments. For example:

Then in the template any number of arguments, separated by spaces, may be passed to the template tag. Like in Python, the values for keyword arguments are set using the equal sign (”=”) and must be provided after the positional arguments. For example:

Sometimes the basic features for custom template tag creation aren’t enough. Don’t worry, Django gives you complete access to the internals required to build a template tag from the ground up.

The template system works in a two-step process: compiling and rendering. To define a custom template tag, you specify how the compilation works and how the rendering works.

When Django compiles a template, it splits the raw template text into nodes. Each node is an instance of django.template.Node and has a render() method. A compiled template is a list of Node objects. When you call render() on a compiled template object, the template calls render() on each Node in its node list, with the given context. The results are all concatenated together to form the output of the template.

Thus, to define a custom template tag, you specify how the raw template tag is converted into a Node (the compilation function), and what the node’s render() method does.

For each template tag the template parser encounters, it calls a Python function with the tag contents and the parser object itself. This function is responsible for returning a Node instance based on the contents of the tag.

For example, let’s write a full implementation of our template tag, {% current_time %}, that displays the current date/time, formatted according to a parameter given in the tag, in strftime() syntax. It’s a good idea to decide the tag syntax before anything else. In our case, let’s say the tag should be used like this:

The parser for this function should grab the parameter and create a Node object:

parser is the template parser object. We don’t need it in this example.

token.contents is a string of the raw contents of the tag. In our example, it’s 'current_time "%Y-%m-%d %I:%M %p"'.

The token.split_contents() method separates the arguments on spaces while keeping quoted strings together. The more straightforward token.contents.split() wouldn’t be as robust, as it would naively split on all spaces, including those within quoted strings. It’s a good idea to always use token.split_contents().

This function is responsible for raising django.template.TemplateSyntaxError, with helpful messages, for any syntax error.

The TemplateSyntaxError exceptions use the tag_name variable. Don’t hardcode the tag’s name in your error messages, because that couples the tag’s name to your function. token.contents.split()[0] will always be the name of your tag – even when the tag has no arguments.

The function returns a CurrentTimeNode with everything the node needs to know about this tag. In this case, it passes the argument – "%Y-%m-%d %I:%M %p". The leading and trailing quotes from the template tag are removed in format_string[1:-1].

The parsing is very low-level. The Django developers have experimented with writing small frameworks on top of this parsing system, using techniques such as EBNF grammars, but those experiments made the template engine too slow. It’s low-level because that’s fastest.

The second step in writing custom tags is to define a Node subclass that has a render() method.

Continuing the above example, we need to define CurrentTimeNode:

__init__() gets the format_string from do_current_time(). Always pass any options/parameters/arguments to a Node via its __init__().

The render() method is where the work actually happens.

render() should generally fail silently, particularly in a production environment. In some cases however, particularly if context.template.engine.debug is True, this method may raise an exception to make debugging easier. For example, several core tags raise django.template.TemplateSyntaxError if they receive the wrong number or type of arguments.

Ultimately, this decoupling of compilation and rendering results in an efficient template system, because a template can render multiple contexts without having to be parsed multiple times.

The output from template tags is not automatically run through the auto-escaping filters (with the exception of simple_tag() as described above). However, there are still a couple of things you should keep in mind when writing a template tag.

If the render() method of your template tag stores the result in a context variable (rather than returning the result in a string), it should take care to call mark_safe() if appropriate. When the variable is ultimately rendered, it will be affected by the auto-escape setting in effect at the time, so content that should be safe from further escaping needs to be marked as such.

Also, if your template tag creates a new context for performing some sub-rendering, set the auto-escape attribute to the current context’s value. The __init__ method for the Context class takes a parameter called autoescape that you can use for this purpose. For example:

This is not a very common situation, but it’s useful if you’re rendering a template yourself. For example:

If we had neglected to pass in the current context.autoescape value to our new Context in this example, the results would have always been automatically escaped, which may not be the desired behavior if the template tag is used inside a {% autoescape off %} block.

Once a node is parsed, its render method may be called any number of times. Since Django is sometimes run in multi-threaded environments, a single node may be simultaneously rendering with different contexts in response to two separate requests. Therefore, it’s important to make sure your template tags are thread safe.

To make sure your template tags are thread safe, you should never store state information on the node itself. For example, Django provides a builtin cycle template tag that cycles among a list of given strings each time it’s rendered:

A naive implementation of CycleNode might look something like this:

But, suppose we have two templates rendering the template snippet from above at the same time:

Thread 1 performs its first loop iteration, CycleNode.render() returns ‘row1’

Thread 2 performs its first loop iteration, CycleNode.render() returns ‘row2’

Thread 1 performs its second loop iteration, CycleNode.render() returns ‘row1’

Thread 2 performs its second loop iteration, CycleNode.render() returns ‘row2’

The CycleNode is iterating, but it’s iterating globally. As far as Thread 1 and Thread 2 are concerned, it’s always returning the same value. This is not what we want!

To address this problem, Django provides a render_context that’s associated with the context of the template that is currently being rendered. The render_context behaves like a Python dictionary, and should be used to store Node state between invocations of the render method.

Let’s refactor our CycleNode implementation to use the render_context:

Note that it’s perfectly safe to store global information that will not change throughout the life of the Node as an attribute. In the case of CycleNode, the cyclevars argument doesn’t change after the Node is instantiated, so we don’t need to put it in the render_context. But state information that is specific to the template that is currently being rendered, like the current iteration of the CycleNode, should be stored in the render_context.

Notice how we used self to scope the CycleNode specific information within the render_context. There may be multiple CycleNodes in a given template, so we need to be careful not to clobber another node’s state information. The easiest way to do this is to always use self as the key into render_context. If you’re keeping track of several state variables, make render_context[self] a dictionary.

Finally, register the tag with your module’s Library instance, as explained in writing custom template tags above. Example:

The tag() method takes two arguments:

The name of the template tag – a string. If this is left out, the name of the compilation function will be used.

The compilation function – a Python function (not the name of the function as a string).

As with filter registration, it is also possible to use this as a decorator:

If you leave off the name argument, as in the second example above, Django will use the function’s name as the tag name.

Although you can pass any number of arguments to a template tag using token.split_contents(), the arguments are all unpacked as string literals. A little more work is required in order to pass dynamic content (a template variable) to a template tag as an argument.

While the previous examples have formatted the current time into a string and returned the string, suppose you wanted to pass in a DateTimeField from an object and have the template tag format that date-time:

Initially, token.split_contents() will return three values:

The tag name format_time.

The string 'blog_entry.date_updated' (without the surrounding quotes).

The formatting string '"%Y-%m-%d %I:%M %p"'. The return value from split_contents() will include the leading and trailing quotes for string literals like this.

Now your tag should begin to look like this:

You also have to change the renderer to retrieve the actual contents of the date_updated property of the blog_entry object. This can be accomplished by using the Variable() class in django.template.

To use the Variable class, instantiate it with the name of the variable to be resolved, and then call variable.resolve(context). So, for example:

Variable resolution will throw a VariableDoesNotExist exception if it cannot resolve the string passed to it in the current context of the page.

The above examples output a value. Generally, it’s more flexible if your template tags set template variables instead of outputting values. That way, template authors can reuse the values that your template tags create.

To set a variable in the context, use dictionary assignment on the context object in the render() method. Here’s an updated version of CurrentTimeNode that sets a template variable current_time instead of outputting it:

Note that render() returns the empty string. render() should always return string output. If all the template tag does is set a variable, render() should return the empty string.

Here’s how you’d use this new version of the tag:

Variable scope in context

Any variable set in the context will only be available in the same block of the template in which it was assigned. This behavior is intentional; it provides a scope for variables so that they don’t conflict with context in other blocks.

But, there’s a problem with CurrentTimeNode2: The variable name current_time is hardcoded. This means you’ll need to make sure your template doesn’t use {{ current_time }} anywhere else, because the {% current_time %} will blindly overwrite that variable’s value. A cleaner solution is to make the template tag specify the name of the output variable, like so:

To do that, you’ll need to refactor both the compilation function and Node class, like so:

The difference here is that do_current_time() grabs the format string and the variable name, passing both to CurrentTimeNode3.

Finally, if you only need to have a simple syntax for your custom context-updating template tag, consider using the simple_tag() shortcut, which supports assigning the tag results to a template variable.

Template tags can work in tandem. For instance, the standard {% comment %} tag hides everything until {% endcomment %}. To create a template tag such as this, use parser.parse() in your compilation function.

Here’s how a simplified {% comment %} tag might be implemented:

The actual implementation of {% comment %} is slightly different in that it allows broken template tags to appear between {% comment %} and {% endcomment %}. It does so by calling parser.skip_past('endcomment') instead of parser.parse(('endcomment',)) followed by parser.delete_first_token(), thus avoiding the generation of a node list.

parser.parse() takes a tuple of names of block tags to parse until. It returns an instance of django.template.NodeList, which is a list of all Node objects that the parser encountered before it encountered any of the tags named in the tuple.

In "nodelist = parser.parse(('endcomment',))" in the above example, nodelist is a list of all nodes between the {% comment %} and {% endcomment %}, not counting {% comment %} and {% endcomment %} themselves.

After parser.parse() is called, the parser hasn’t yet “consumed” the {% endcomment %} tag, so the code needs to explicitly call parser.delete_first_token().

CommentNode.render() returns an empty string. Anything between {% comment %} and {% endcomment %} is ignored.

In the previous example, do_comment() discarded everything between {% comment %} and {% endcomment %}. Instead of doing that, it’s possible to do something with the code between block tags.

For example, here’s a custom template tag, {% upper %}, that capitalizes everything between itself and {% endupper %}.

As in the previous example, we’ll use parser.parse(). But this time, we pass the resulting nodelist to the Node:

The only new concept here is the self.nodelist.render(context) in UpperNode.render().

For more examples of complex rendering, see the source code of {% for %} in django/template/defaulttags.py and {% if %} in django/template/smartif.py.

---

## How to create database migrations | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/writing-migrations/

**Contents:**
- How to create database migrations¶
- Data migrations and multiple databases¶
- Migrations that add unique fields¶
  - Non-atomic migrations¶
- Controlling the order of migrations¶
- Migrating data between third-party apps¶
- Changing a ManyToManyField to use a through model¶
- Changing an unmanaged model to managed¶

This document explains how to structure and write database migrations for different scenarios you might encounter. For introductory material on migrations, see the topic guide.

When using multiple databases, you may need to figure out whether or not to run a migration against a particular database. For example, you may want to only run a migration on a particular database.

In order to do that you can check the database connection’s alias inside a RunPython operation by looking at the schema_editor.connection.alias attribute:

You can also provide hints that will be passed to the allow_migrate() method of database routers as **hints:

Then, to leverage this in your migrations, do the following:

If your RunPython or RunSQL operation only affects one model, it’s good practice to pass model_name as a hint to make it as transparent as possible to the router. This is especially important for reusable and third-party apps.

Applying a “plain” migration that adds a unique non-nullable field to a table with existing rows will raise an error because the value used to populate existing rows is generated only once, thus breaking the unique constraint.

Therefore, the following steps should be taken. In this example, we’ll add a non-nullable UUIDField with a default value. Modify the respective field according to your needs.

Add the field on your model with default=uuid.uuid4 and unique=True arguments (choose an appropriate default for the type of the field you’re adding).

Run the makemigrations command. This should generate a migration with an AddField operation.

Generate two empty migration files for the same app by running makemigrations myapp --empty twice. We’ve renamed the migration files to give them meaningful names in the examples below.

Copy the AddField operation from the auto-generated migration (the first of the three new files) to the last migration, change AddField to AlterField, and add imports of uuid and models. For example:

Edit the first migration file. The generated migration class should look similar to this:

Change unique=True to null=True – this will create the intermediary null field and defer creating the unique constraint until we’ve populated unique values on all the rows.

In the first empty migration file, add a RunPython or RunSQL operation to generate a unique value (UUID in the example) for each existing row. Also add an import of uuid. For example:

Now you can apply the migrations as usual with the migrate command.

Note there is a race condition if you allow objects to be created while this migration is running. Objects created after the AddField and before RunPython will have their original uuid’s overwritten.

On databases that support DDL transactions (SQLite and PostgreSQL), migrations will run inside a transaction by default. For use cases such as performing data migrations on large tables, you may want to prevent a migration from running in a transaction by setting the atomic attribute to False:

Within such a migration, all operations are run without a transaction. It’s possible to execute parts of the migration inside a transaction using atomic() or by passing atomic=True to RunPython.

Here’s an example of a non-atomic data migration that updates a large table in smaller batches:

The atomic attribute doesn’t have an effect on databases that don’t support DDL transactions (e.g. MySQL, Oracle). (MySQL’s atomic DDL statement support refers to individual statements rather than multiple statements wrapped in a transaction that can be rolled back.)

Django determines the order in which migrations should be applied not by the filename of each migration, but by building a graph using two properties on the Migration class: dependencies and run_before.

If you’ve used the makemigrations command you’ve probably already seen dependencies in action because auto-created migrations have this defined as part of their creation process.

The dependencies property is declared like this:

Usually this will be enough, but from time to time you may need to ensure that your migration runs before other migrations. This is useful, for example, to make third-party apps’ migrations run after your AUTH_USER_MODEL replacement.

To achieve this, place all migrations that should depend on yours in the run_before attribute on your Migration class:

Prefer using dependencies over run_before when possible. You should only use run_before if it is undesirable or impractical to specify dependencies in the migration which you want to run after the one you are writing.

You can use a data migration to move data from one third-party application to another.

If you plan to remove the old app later, you’ll need to set the dependencies property based on whether or not the old app is installed. Otherwise, you’ll have missing dependencies once you uninstall the old app. Similarly, you’ll need to catch LookupError in the apps.get_model() call that retrieves models from the old app. This approach allows you to deploy your project anywhere without first installing and then uninstalling the old app.

Here’s a sample migration:

Also consider what you want to happen when the migration is unapplied. You could either do nothing (as in the example above) or remove some or all of the data from the new application. Adjust the second argument of the RunPython operation accordingly.

If you change a ManyToManyField to use a through model, the default migration will delete the existing table and create a new one, losing the existing relations. To avoid this, you can use SeparateDatabaseAndState to rename the existing table to the new table name while telling the migration autodetector that the new model has been created. You can check the existing table name and constraint name through sqlmigrate or dbshell. You can check the new table name with the through model’s _meta.db_table property. Your new through model should use the same names for the ForeignKeys as Django did. Also if it needs any extra fields, they should be added in operations after SeparateDatabaseAndState.

For example, if we had a Book model with a ManyToManyField linking to Author, we could add a through model AuthorBook with a new field is_primary, like so:

If you want to change an unmanaged model (managed=False) to managed, you must remove managed=False and generate a migration before making other schema-related changes to the model, since schema changes that appear in the migration that contains the operation to change Meta.managed may not be applied.

---

## How to create PDF files | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/outputting-pdf/

**Contents:**
- How to create PDF files¶
- Install ReportLab¶
- Write your view¶
- Other formats¶

This document explains how to output PDF files dynamically using Django views. This is made possible by the excellent, open-source ReportLab Python PDF library.

The advantage of generating PDF files dynamically is that you can create customized PDFs for different purposes – say, for different users or different pieces of content.

For example, Django was used at kusports.com to generate customized, printer-friendly NCAA tournament brackets, as PDF files, for people participating in a March Madness contest.

The ReportLab library is available on PyPI. A user guide (not coincidentally, a PDF file) is also available for download. You can install ReportLab with pip:

Test your installation by importing it in the Python interactive interpreter:

If that command doesn’t raise any errors, the installation worked.

The key to generating PDFs dynamically with Django is that the ReportLab API acts on file-like objects, and Django’s FileResponse objects accept file-like objects.

Here’s a “Hello World” example:

The code and comments should be self-explanatory, but a few things deserve a mention:

The response will automatically set the MIME type application/pdf based on the filename extension. This tells browsers that the document is a PDF file, rather than an HTML file or a generic application/octet-stream binary content.

When as_attachment=True is passed to FileResponse, it sets the appropriate Content-Disposition header and that tells web browsers to pop-up a dialog box prompting/confirming how to handle the document even if a default is set on the machine. If the as_attachment parameter is omitted, browsers will handle the PDF using whatever program/plugin they’ve been configured to use for PDFs.

You can provide an arbitrary filename parameter. It’ll be used by browsers in the “Save as…” dialog.

You can hook into the ReportLab API: The same buffer passed as the first argument to canvas.Canvas can be fed to the FileResponse class.

Note that all subsequent PDF-generation methods are called on the PDF object (in this case, p) – not on buffer.

Finally, it’s important to call showPage() and save() on the PDF file.

ReportLab is not thread-safe. Some of our users have reported odd issues with building PDF-generating Django views that are accessed by many people at the same time.

Notice that there isn’t a lot in these examples that’s PDF-specific – just the bits using reportlab. You can use a similar technique to generate any arbitrary format that you can find a Python library for. Also see How to create CSV output for another example and some techniques you can use when generated text-based formats.

Django Packages provides a comparison of packages that help generate PDF files from Django.

---

## How to customize the shell command | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/custom-shell/

**Contents:**
- How to customize the shell command¶
- Customize automatic imports¶

The Django shell is an interactive Python environment that provides access to models and settings, making it useful for testing code, experimenting with queries, and interacting with application data.

Customizing the shell command allows adding extra functionality or pre-loading specific modules. To do this, create a new management command that subclasses django.core.management.commands.shell.Command and overrides the existing shell management command. For more details, refer to the guide on overriding commands.

To customize the automatic import behavior of the shell management command, override the get_auto_imports() method. This method should return a sequence of import paths for objects or modules available in the application. For example:

The customization above adds resolve() and reverse() to the default namespace, which already includes all models from the apps listed in INSTALLED_APPS plus what is imported by default. These objects will be available in the shell without requiring a manual import.

Running this customized shell command with verbosity=2 would show:

Automatic imports of common utilities, such as django.conf.settings, were added.

If an overridden shell command includes paths that cannot be imported, these errors are shown when verbosity is set to 1 or higher. Duplicate imports are automatically handled.

Note that automatic imports can be disabled for a specific shell session using the --no-imports flag. To permanently disable automatic imports, override get_auto_imports() to return None:

---

## How to delete a Django application | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/delete-app/

**Contents:**
- How to delete a Django application¶

Django provides the ability to group sets of features into Python packages called applications. When requirements change, apps may become obsolete or unnecessary. The following steps will help you delete an application safely.

Remove all references to the app (imports, foreign keys etc.).

Remove all models from the corresponding models.py file.

Create relevant migrations by running makemigrations. This step generates a migration that deletes tables for the removed models, and any other required migration for updating relationships connected to those models.

Squash out references to the app in other apps’ migrations.

Apply migrations locally, run tests, and verify the correctness of your project.

Deploy/release your updated Django project.

Remove the app from INSTALLED_APPS.

Finally, remove the app’s directory.

---

## How to deploy Django | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/deployment/

**Contents:**
- How to deploy Django¶

Django is full of shortcuts to make web developers’ lives easier, but all those tools are of no use if you can’t easily deploy your sites. Since Django’s inception, ease of deployment has been a major goal.

There are many options for deploying your Django application, based on your architecture or your particular business needs, but that discussion is outside the scope of what Django can give you as guidance.

Django, being a web framework, needs a web server in order to operate. And since most web servers don’t natively speak Python, we need an interface to make that communication happen. The runserver command starts a lightweight development server, which is not suitable for production.

Django currently supports two interfaces: WSGI and ASGI.

WSGI is the main Python standard for communicating between web servers and applications, but it only supports synchronous code.

ASGI is the new, asynchronous-friendly standard that will allow your Django site to use asynchronous Python features, and asynchronous Django features as they are developed.

You should also consider how you will handle static files for your application, and how to handle error reporting.

Finally, before you deploy your application to production, you should run through our deployment checklist to ensure that your configurations are suitable.

---

## How to deploy static files | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/static-files/deployment/

**Contents:**
- How to deploy static files¶
- Serving static files in production¶
  - Serving the site and your static files from the same server¶
  - Serving static files from a dedicated server¶
  - Serving static files from a cloud service or CDN¶
- Learn more¶

For an introduction to the use of django.contrib.staticfiles, see How to manage static files (e.g. images, JavaScript, CSS).

The basic outline of putting static files into production consists of two steps: run the collectstatic command when static files change, then arrange for the collected static files directory (STATIC_ROOT) to be moved to the static file server and served. Depending on the staticfiles STORAGES alias, files may need to be moved to a new location manually or the post_process method of the Storage class might take care of that.

As with all deployment tasks, the devil’s in the details. Every production setup will be a bit different, so you’ll need to adapt the basic outline to fit your needs. Below are a few common patterns that might help.

If you want to serve your static files from the same server that’s already serving your site, the process may look something like:

Push your code up to the deployment server.

On the server, run collectstatic to copy all the static files into STATIC_ROOT.

Configure your web server to serve the files in STATIC_ROOT under the URL STATIC_URL. For example, here’s how to do this with Apache and mod_wsgi.

You’ll probably want to automate this process, especially if you’ve got multiple web servers.

Most larger Django sites use a separate web server – i.e., one that’s not also running Django – for serving static files. This server often runs a different type of web server – faster but less full-featured. Some common choices are:

A stripped-down version of Apache

Configuring these servers is out of scope of this document; check each server’s respective documentation for instructions.

Since your static file server won’t be running Django, you’ll need to modify the deployment strategy to look something like:

When your static files change, run collectstatic locally.

Push your local STATIC_ROOT up to the static file server into the directory that’s being served. rsync is a common choice for this step since it only needs to transfer the bits of static files that have changed.

Another common tactic is to serve static files from a cloud storage provider like Amazon’s S3 and/or a CDN (content delivery network). This lets you ignore the problems of serving static files and can often make for faster-loading web pages (especially when using a CDN).

When using these services, the basic workflow would look a bit like the above, except that instead of using rsync to transfer your static files to the server you’d need to transfer the static files to the storage provider or CDN.

There’s any number of ways you might do this, but if the provider has an API, you can use a custom file storage backend to integrate the CDN with your Django project. If you’ve written or are using a 3rd party custom storage backend, you can tell collectstatic to use it by setting staticfiles in STORAGES.

For example, if you’ve written an S3 storage backend in myproject.storage.S3Storage you could use it with:

Once that’s done, all you have to do is run collectstatic and your static files would be pushed through your storage package up to S3. If you later needed to switch to a different storage provider, you may only have to change staticfiles in the STORAGES setting.

For details on how you’d write one of these backends, see How to write a custom storage class. There are 3rd party apps available that provide storage backends for many common file storage APIs. A good starting point is the overview at djangopackages.org.

For complete details on all the settings, commands, template tags, and other pieces included in django.contrib.staticfiles, see the staticfiles reference.

---

## How to deploy with ASGI | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/deployment/asgi/

**Contents:**
- How to deploy with ASGI¶
- The application object¶
- Configuring the settings module¶
- Applying ASGI middleware¶

As well as WSGI, Django also supports deploying on ASGI, the emerging Python standard for asynchronous web servers and applications.

Django’s startproject management command sets up a default ASGI configuration for you, which you can tweak as needed for your project, and direct any ASGI-compliant application server to use.

Django includes getting-started documentation for the following ASGI servers:

Like WSGI, ASGI has you supply an application callable which the application server uses to communicate with your code. It’s commonly provided as an object named application in a Python module accessible to the server.

The startproject command creates a file <project_name>/asgi.py that contains such an application callable.

It’s not used by the development server (runserver), but can be used by any ASGI server either in development or in production.

ASGI servers usually take the path to the application callable as a string; for most Django projects, this will look like myproject.asgi:application.

While Django’s default ASGI handler will run all your code in a synchronous thread, if you choose to run your own async handler you must be aware of async-safety.

Do not call blocking synchronous functions or libraries in any async code. Django prevents you from doing this with the parts of Django that are not async-safe, but the same may not be true of third-party apps or Python libraries.

When the ASGI server loads your application, Django needs to import the settings module — that’s where your entire application is defined.

Django uses the DJANGO_SETTINGS_MODULE environment variable to locate the appropriate settings module. It must contain the dotted path to the settings module. You can use a different value for development and production; it all depends on how you organize your settings.

If this variable isn’t set, the default asgi.py sets it to mysite.settings, where mysite is the name of your project.

To apply ASGI middleware, or to embed Django in another ASGI application, you can wrap Django’s application object in the asgi.py file. For example:

---

## How to deploy with WSGI | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/

**Contents:**
- How to deploy with WSGI¶
- The application object¶
- Configuring the settings module¶
- Applying WSGI middleware¶

Django’s primary deployment platform is WSGI, the Python standard for web servers and applications.

Django’s startproject management command sets up a minimal default WSGI configuration for you, which you can tweak as needed for your project, and direct any WSGI-compliant application server to use.

Django includes getting-started documentation for the following WSGI servers:

The key concept of deploying with WSGI is the application callable which the application server uses to communicate with your code. It’s commonly provided as an object named application in a Python module accessible to the server.

The startproject command creates a file <project_name>/wsgi.py that contains such an application callable.

It’s used both by Django’s development server and in production WSGI deployments.

WSGI servers obtain the path to the application callable from their configuration. Django’s built-in server, namely the runserver command, reads it from the WSGI_APPLICATION setting. By default, it’s set to <project_name>.wsgi.application, which points to the application callable in <project_name>/wsgi.py.

When the WSGI server loads your application, Django needs to import the settings module — that’s where your entire application is defined.

Django uses the DJANGO_SETTINGS_MODULE environment variable to locate the appropriate settings module. It must contain the dotted path to the settings module. You can use a different value for development and production; it all depends on how you organize your settings.

If this variable isn’t set, the default wsgi.py sets it to mysite.settings, where mysite is the name of your project. That’s how runserver discovers the default settings file by default.

Since environment variables are process-wide, this doesn’t work when you run multiple Django sites in the same process. This happens with mod_wsgi.

To avoid this problem, use mod_wsgi’s daemon mode with each site in its own daemon process, or override the value from the environment by enforcing os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings" in your wsgi.py.

To apply WSGI middleware you can wrap the application object. For instance you could add these lines at the bottom of wsgi.py:

You could also replace the Django WSGI application with a custom WSGI application that later delegates to the Django WSGI application, if you want to combine a Django application with a WSGI application of another framework.

---

## How-to guides | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/

**Contents:**
- How-to guides¶
- Models, data and databases¶
- Templates and output¶
- Project configuration and management¶
- Installing, deploying and upgrading¶
- Other guides¶

Practical guides covering common tasks and problems.

The Django community aggregator, where we aggregate content from the global Django community. Many writers in the aggregator write this sort of how-to material.

---

## How to implement a custom template backend | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/custom-template-backend/

**Contents:**
- How to implement a custom template backend¶
- Custom backends¶
- Debug integration for custom engines¶
  - Template postmortem¶
  - Contextual line information¶
  - Origin API and 3rd-party integration¶

Here’s how to implement a custom template backend in order to use another template system. A template backend is a class that inherits django.template.backends.base.BaseEngine. It must implement get_template() and optionally from_string(). Here’s an example for a fictional foobar template library:

See DEP 182 for more information.

The Django debug page has hooks to provide detailed information when a template error arises. Custom template engines can use these hooks to enhance the traceback information that appears to users. The following hooks are available:

The postmortem appears when TemplateDoesNotExist is raised. It lists the template engines and loaders that were used when trying to find a given template. For example, if two Django engines are configured, the postmortem will appear like:

Custom engines can populate the postmortem by passing the backend and tried arguments when raising TemplateDoesNotExist. Backends that use the postmortem should specify an origin on the template object.

If an error happens during template parsing or rendering, Django can display the line the error happened on. For example:

Custom engines can populate this information by setting a template_debug attribute on exceptions raised during parsing and rendering. This attribute is a dict with the following values:

'name': The name of the template in which the exception occurred.

'message': The exception message.

'source_lines': The lines before, after, and including the line the exception occurred on. This is for context, so it shouldn’t contain more than 20 lines or so.

'line': The line number on which the exception occurred.

'before': The content on the error line before the token that raised the error.

'during': The token that raised the error.

'after': The content on the error line after the token that raised the error.

'total': The number of lines in source_lines.

'top': The line number where source_lines starts.

'bottom': The line number where source_lines ends.

Given the above template error, template_debug would look like:

Django templates have an Origin object available through the template.origin attribute. This enables debug information to be displayed in the template postmortem, as well as in 3rd-party libraries, like the Django Debug Toolbar.

Custom engines can provide their own template.origin information by creating an object that specifies the following attributes:

'name': The full path to the template.

'template_name': The relative path to the template as passed into the template loading methods.

'loader_name': An optional string identifying the function or class used to load the template, e.g. django.template.loaders.filesystem.Loader.

---

## How to install Django on Windows | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/windows/

**Contents:**
- How to install Django on Windows¶
- Install Python¶
- About pip¶
- Setting up a virtual environment¶
- Install Django¶
- Colored terminal output¶
- Common pitfalls¶

This document will guide you through installing Python 3.14 and Django on Windows. It also provides instructions for setting up a virtual environment, which makes it easier to work on Python projects. This is meant as a beginner’s guide for users working on Django projects and does not reflect how Django should be installed when developing changes for Django itself.

The steps in this guide have been tested with Windows 10. In other versions, the steps would be similar. You will need to be familiar with using the Windows command prompt.

Django is a Python web framework, thus requiring Python to be installed on your machine. At the time of writing, Python 3.14 is the latest version.

To install Python on your machine go to https://www.python.org/downloads/. The website should offer you a download button for the latest Python version. Download the executable installer and run it. Check the boxes next to “Install launcher for all users (recommended)” then click “Install Now”.

After installation, open the command prompt and check that the Python version matches the version you installed by executing:

py is not recognized or found

Depending on how you’ve installed Python (such as via the Microsoft Store), py may not be available in the command prompt.

You will then need to use python instead of py when entering commands.

For more details, see Using Python on Windows documentation.

pip is a package manager for Python and is included by default with the Python installer. It helps to install and uninstall Python packages (such as Django!). For the rest of the installation, we’ll use pip to install Python packages from the command line.

It is best practice to provide a dedicated environment for each Django project you create. There are many options to manage environments and packages within the Python ecosystem, some of which are recommended in the Python documentation. Python itself comes with venv for managing environments which we will use for this guide.

To create a virtual environment for your project, open a new command prompt, navigate to the folder where you want to create your project and then enter the following:

This will create a folder called ‘project-name’ if it does not already exist and set up the virtual environment. To activate the environment, run:

The virtual environment will be activated and you’ll see “(project-name)” next to the command prompt to designate that. Each time you start a new command prompt, you’ll need to activate the environment again.

Django can be installed easily using pip within your virtual environment.

In the command prompt, ensure your virtual environment is active, and execute the following command:

This will download and install the latest Django release.

After the installation has completed, you can verify your Django installation by executing django-admin --version in the command prompt.

See Get your database running for information on database installation with Django.

A quality-of-life feature adds colored (rather than monochrome) output to the terminal. In modern terminals this should work for both CMD and PowerShell. If for some reason this needs to be disabled, set the environmental variable DJANGO_COLORS to nocolor.

On older Windows versions, or legacy terminals, colorama 0.4.6+ must be installed to enable syntax coloring:

See Syntax coloring for more information on color settings.

If django-admin only displays the help text no matter what arguments it is given, there is probably a problem with the file association in Windows. Check if there is more than one environment variable set for running Python scripts in PATH. This usually occurs when there is more than one Python version installed.

If you are connecting to the internet behind a proxy, there might be problems in running the command py -m pip install Django. Set the environment variables for proxy configuration in the command prompt as follows:

In general, Django assumes that UTF-8 encoding is used for I/O. This may cause problems if your system is set to use a different encoding. Recent versions of Python allow setting the PYTHONUTF8 environment variable in order to force a UTF-8 encoding. Windows 10 also provides a system-wide setting by checking Use Unicode UTF-8 for worldwide language support in Language ‣ Administrative Language Settings ‣ Change system locale in system settings.

---

## How to integrate Django with a legacy database | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/legacy-databases/

**Contents:**
- How to integrate Django with a legacy database¶
- Give Django your database parameters¶
- Auto-generate the models¶
- Install the core Django tables¶
- Test and tweak¶

While Django is best suited for developing new applications, it’s quite possible to integrate it into legacy databases. Django includes a couple of utilities to automate as much of this process as possible.

This document assumes you know the Django basics, as covered in the tutorial.

Once you’ve got Django set up, you’ll follow this general process to integrate with an existing database.

You’ll need to tell Django what your database connection parameters are, and what the name of the database is. Do that by editing the DATABASES setting and assigning values to the following keys for the 'default' connection:

Django comes with a utility called inspectdb that can create models by introspecting an existing database. You can view the output by running this command:

Save this as a file by using standard Unix output redirection:

This feature is meant as a shortcut, not as definitive model generation. See the documentation of inspectdb for more information.

Once you’ve cleaned up your models, name the file models.py and put it in the Python package that holds your app. Then add the app to your INSTALLED_APPS setting.

By default, inspectdb creates unmanaged models. That is, managed = False in the model’s Meta class tells Django not to manage each table’s creation, modification, and deletion:

If you do want to allow Django to manage the table’s lifecycle, you’ll need to change the managed option above to True (or remove it because True is its default value).

Next, run the migrate command to install any extra needed database records such as admin permissions and content types:

Those are the basic steps – from here you’ll want to tweak the models Django generated until they work the way you’d like. Try accessing your data via the Django database API, and try editing objects via Django’s admin site, and edit the models file accordingly.

---

## How to manage error reporting | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/error-reporting/

**Contents:**
- How to manage error reporting¶
- Email reports¶
  - Server errors¶
  - 404 errors¶
- Filtering error reports¶
  - Filtering sensitive information¶
  - Custom error reports¶

When you’re running a public site you should always turn off the DEBUG setting. That will make your server run much faster, and will also prevent malicious users from seeing details of your application that can be revealed by the error pages.

However, running with DEBUG set to False means you’ll never see errors generated by your site – everyone will instead see your public error pages. You need to keep track of errors that occur in deployed sites, so Django can be configured to create reports with details about those errors.

When DEBUG is False, Django will email the users listed in the ADMINS setting whenever your code raises an unhandled exception and results in an internal server error (strictly speaking, for any response with an HTTP status code of 500 or greater). This gives the administrators immediate notification of any errors. The ADMINS will get a description of the error, a complete Python traceback, and details about the HTTP request that caused the error.

In order to send email, Django requires a few settings telling it how to connect to your mail server. At the very least, you’ll need to specify EMAIL_HOST and possibly EMAIL_HOST_USER and EMAIL_HOST_PASSWORD, though other settings may be also required depending on your mail server’s configuration. Consult the Django settings documentation for a full list of email-related settings.

By default, Django will send email from root@localhost. However, some mail providers reject all email from this address. To use a different sender address, modify the SERVER_EMAIL setting.

To activate this behavior, put the email addresses of the recipients in the ADMINS setting.

Server error emails are sent using the logging framework, so you can customize this behavior by customizing your logging configuration.

Django can also be configured to email errors about broken links (404 “page not found” errors). Django sends emails about 404 errors when:

Your MIDDLEWARE setting includes django.middleware.common.BrokenLinkEmailsMiddleware.

If those conditions are met, Django will email the users listed in the MANAGERS setting whenever your code raises a 404 and the request has a referer. It doesn’t bother to email for 404s that don’t have a referer – those are usually people typing in broken URLs or broken web bots. It also ignores 404s when the referer is equal to the requested URL, since this behavior is from broken web bots too.

BrokenLinkEmailsMiddleware must appear before other middleware that intercepts 404 errors, such as LocaleMiddleware or FlatpageFallbackMiddleware. Put it toward the top of your MIDDLEWARE setting.

You can tell Django to stop reporting particular 404s by tweaking the IGNORABLE_404_URLS setting. It should be a list of compiled regular expression objects. For example:

In this example, a 404 to any URL ending with .php or .cgi will not be reported. Neither will any URL starting with /phpmyadmin/.

The following example shows how to exclude some conventional URLs that browsers and crawlers often request:

(Note that these are regular expressions, so we put a backslash in front of periods to escape them.)

If you’d like to customize the behavior of django.middleware.common.BrokenLinkEmailsMiddleware further (for example to ignore requests coming from web crawlers), you should subclass it and override its methods.

404 errors are logged using the logging framework. By default, these log records are ignored, but you can use them for error reporting by writing a handler and configuring logging appropriately.

Filtering sensitive data is a hard problem, and it’s nearly impossible to guarantee that sensitive data won’t leak into an error report. Therefore, error reports should only be available to trusted team members and you should avoid transmitting error reports unencrypted over the internet (such as through email).

Error reports are really helpful for debugging errors, so it is generally useful to record as much relevant information about those errors as possible. For example, by default Django records the full traceback for the exception raised, each traceback frame’s local variables, and the HttpRequest’s attributes.

However, sometimes certain types of information may be too sensitive and thus may not be appropriate to be kept track of, for example a user’s password or credit card number. So in addition to filtering out settings that appear to be sensitive as described in the DEBUG documentation, Django offers a set of function decorators to help you control which information should be filtered out of error reports in a production environment (that is, where DEBUG is set to False): sensitive_variables() and sensitive_post_parameters().

If a function (either a view or any regular callback) in your code uses local variables susceptible to contain sensitive information, you may prevent the values of those variables from being included in error reports using the sensitive_variables decorator:

In the above example, the values for the user, pw and cc variables will be hidden and replaced with stars (**********) in the error reports, whereas the value of the name variable will be disclosed.

To systematically hide all local variables of a function from error logs, do not provide any argument to the sensitive_variables decorator:

When using multiple decorators

If the variable you want to hide is also a function argument (e.g. ‘user’ in the following example), and if the decorated function has multiple decorators, then make sure to place @sensitive_variables at the top of the decorator chain. This way it will also hide the function argument as it gets passed through the other decorators:

If one of your views receives an HttpRequest object with POST parameters susceptible to contain sensitive information, you may prevent the values of those parameters from being included in the error reports using the sensitive_post_parameters decorator:

In the above example, the values for the pass_word and credit_card_number POST parameters will be hidden and replaced with stars (**********) in the request’s representation inside the error reports, whereas the value of the name parameter will be disclosed.

To systematically hide all POST parameters of a request in error reports, do not provide any argument to the sensitive_post_parameters decorator:

All POST parameters are systematically filtered out of error reports for certain django.contrib.auth.views views (login, password_reset_confirm, password_change, and add_view and user_change_password in the auth admin) to prevent the leaking of sensitive information such as user passwords.

All sensitive_variables() and sensitive_post_parameters() do is, respectively, annotate the decorated function with the names of sensitive variables and annotate the HttpRequest object with the names of sensitive POST parameters, so that this sensitive information can later be filtered out of reports when an error occurs. The actual filtering is done by Django’s default error reporter filter: django.views.debug.SafeExceptionReporterFilter. This filter uses the decorators’ annotations to replace the corresponding values with stars (**********) when the error reports are produced. If you wish to override or customize this default behavior for your entire site, you need to define your own filter class and tell Django to use it via the DEFAULT_EXCEPTION_REPORTER_FILTER setting:

You may also control in a more granular way which filter to use within any given view by setting the HttpRequest’s exception_reporter_filter attribute:

Your custom filter class needs to inherit from django.views.debug.SafeExceptionReporterFilter and may override the following attributes and methods:

The string value to replace sensitive value with. By default it replaces the values of sensitive variables with stars (**********).

A compiled regular expression object used to match settings and request.META values considered as sensitive. By default equivalent to:

The term AUTH was added.

Returns True to activate the filtering in get_post_parameters() and get_traceback_frame_variables(). By default the filter is active if DEBUG is False. Note that sensitive request.META values are always filtered along with sensitive setting values, as described in the DEBUG documentation.

Returns the filtered dictionary of POST parameters. Sensitive values are replaced with cleansed_substitute.

Returns the filtered dictionary of local variables for the given traceback frame. Sensitive values are replaced with cleansed_substitute.

If you need to customize error reports beyond filtering you may specify a custom error reporter class by defining the DEFAULT_EXCEPTION_REPORTER setting:

The exception reporter is responsible for compiling the exception report data, and formatting it as text or HTML appropriately. (The exception reporter uses DEFAULT_EXCEPTION_REPORTER_FILTER when preparing the exception report data.)

Your custom reporter class needs to inherit from django.views.debug.ExceptionReporter.

Property that returns a pathlib.Path representing the absolute filesystem path to a template for rendering the HTML representation of the exception. Defaults to the Django provided template.

Property that returns a pathlib.Path representing the absolute filesystem path to a template for rendering the plain-text representation of the exception. Defaults to the Django provided template.

Return a dictionary containing traceback information.

This is the main extension point for customizing exception reports, for example:

Return HTML version of exception report.

Used for HTML version of debug 500 HTTP error page.

Return plain text version of exception report.

Used for plain text version of debug 500 HTTP error page and email reports.

As with the filter class, you may control which exception reporter class to use within any given view by setting the HttpRequest’s exception_reporter_class attribute:

You can also set up custom error reporting by writing a custom piece of exception middleware. If you do write custom error handling, it’s a good idea to emulate Django’s built-in error handling and only report/log errors if DEBUG is False.

---

## How to manage static files (e.g. images, JavaScript, CSS) | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/static-files/

**Contents:**
- How to manage static files (e.g. images, JavaScript, CSS)¶
- Configuring static files¶
- Serving static files during development¶
- Serving files uploaded by a user during development¶
- Testing¶
- Deployment¶
- Learn more¶

Websites generally need to serve additional files such as images, JavaScript, or CSS. In Django, we refer to these files as “static files”. Django provides django.contrib.staticfiles to help you manage them.

This page describes how you can serve these static files.

Make sure that django.contrib.staticfiles is included in your INSTALLED_APPS.

In your settings file, define STATIC_URL, for example:

In your templates, use the static template tag to build the URL for the given relative path using the configured staticfiles STORAGES alias.

Store your static files in a folder called static in your app. For example my_app/static/my_app/example.jpg.

In addition to these configuration steps, you’ll also need to actually serve the static files.

During development, if you use django.contrib.staticfiles, this will be done automatically by runserver when DEBUG is set to True (see django.contrib.staticfiles.views.serve()).

This method is grossly inefficient and probably insecure, so it is unsuitable for production.

See How to deploy static files for proper strategies to serve static files in production environments.

Your project will probably also have static assets that aren’t tied to a particular app. In addition to using a static/ directory inside your apps, you can define a list of directories (STATICFILES_DIRS) in your settings file where Django will also look for static files. For example:

See the documentation for the STATICFILES_FINDERS setting for details on how staticfiles finds your files.

Static file namespacing

Now we might be able to get away with putting our static files directly in my_app/static/ (rather than creating another my_app subdirectory), but it would actually be a bad idea. Django will use the first static file it finds whose name matches, and if you had a static file with the same name in a different application, Django would be unable to distinguish between them. We need to be able to point Django at the right one, and the best way to ensure this is by namespacing them. That is, by putting those static files inside another directory named for the application itself.

You can namespace static assets in STATICFILES_DIRS by specifying prefixes.

If you use django.contrib.staticfiles as explained above, runserver will do this automatically when DEBUG is set to True. If you don’t have django.contrib.staticfiles in INSTALLED_APPS, you can still manually serve static files using the django.views.static.serve() view.

This is not suitable for production use! For some common deployment strategies, see How to deploy static files.

For example, if your STATIC_URL is defined as static/, you can do this by adding the following snippet to your urls.py:

This helper function works only in debug mode and only if the given prefix is local (e.g. static/) and not a URL (e.g. http://static.example.com/).

Also this helper function only serves the actual STATIC_ROOT folder; it doesn’t perform static files discovery like django.contrib.staticfiles.

Finally, static files are served via a wrapper at the WSGI application layer. As a consequence, static files requests do not pass through the normal middleware chain.

During development, you can serve user-uploaded media files from MEDIA_ROOT using the django.views.static.serve() view.

This is not suitable for production use! For some common deployment strategies, see How to deploy static files.

For example, if your MEDIA_URL is defined as media/, you can do this by adding the following snippet to your ROOT_URLCONF:

This helper function works only in debug mode and only if the given prefix is local (e.g. media/) and not a URL (e.g. http://media.example.com/).

When running tests that use actual HTTP requests instead of the built-in testing client (i.e. when using the built-in LiveServerTestCase) the static assets need to be served along the rest of the content so the test environment reproduces the real one as faithfully as possible, but LiveServerTestCase has only very basic static file-serving functionality: It doesn’t know about the finders feature of the staticfiles application and assumes the static content has already been collected under STATIC_ROOT.

Because of this, staticfiles ships its own django.contrib.staticfiles.testing.StaticLiveServerTestCase, a subclass of the built-in one that has the ability to transparently serve all the assets during execution of these tests in a way very similar to what we get at development time with DEBUG = True, i.e. without having to collect them using collectstatic first.

django.contrib.staticfiles provides a convenience management command for gathering static files in a single directory so you can serve them easily.

Set the STATIC_ROOT setting to the directory from which you’d like to serve these files, for example:

Run the collectstatic management command:

This will copy all files from your static folders into the STATIC_ROOT directory.

Use a web server of your choice to serve the files. How to deploy static files covers some common deployment strategies for static files.

This document has covered the basics and some common usage patterns. For complete details on all the settings, commands, template tags, and other pieces included in django.contrib.staticfiles, see the staticfiles reference.

---

## How to override templates | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/overriding-templates/

**Contents:**
- How to override templates¶
- Overriding from the project’s templates directory¶
- Overriding from an app’s template directory¶
- Extending an overridden template¶

In your project, you might want to override a template in another Django application, whether it be a third-party application or a contrib application such as django.contrib.admin. You can either put template overrides in your project’s templates directory or in an application’s templates directory.

If you have app and project templates directories that both contain overrides, the default Django template loader will try to load the template from the project-level directory first. In other words, DIRS is searched before APP_DIRS.

Read Overriding built-in widget templates if you’re looking to do that.

First, we’ll explore overriding templates by creating replacement templates in your project’s templates directory.

Let’s say you’re trying to override the templates for a third-party application called blog, which provides the templates blog/post.html and blog/list.html. The relevant settings for your project would look like:

The TEMPLATES setting and BASE_DIR will already exist if you created your project using the default project template. The setting that needs to be modified is DIRS.

These settings assume you have a templates directory in the root of your project. To override the templates for the blog app, create a folder in the templates directory, and add the template files to that folder:

The template loader first looks for templates in the DIRS directory. When the views in the blog app ask for the blog/post.html and blog/list.html templates, the loader will return the files you just created.

Since you’re overriding templates located outside of one of your project’s apps, it’s more common to use the first method and put template overrides in a project’s templates folder. If you prefer, however, it’s also possible to put the overrides in an app’s template directory.

First, make sure your template settings are checking inside app directories:

If you want to put the template overrides in an app called myapp and the templates to override are named blog/list.html and blog/post.html, then your directory structure will look like:

With APP_DIRS set to True, the template loader will look in the app’s templates directory and find the templates.

With your template loaders configured, you can extend a template using the {% extends %} template tag whilst at the same time overriding it. This can allow you to make small customizations without needing to reimplement the entire template.

For example, you can use this technique to add a custom logo to the admin/base_site.html template:

The example creates a file at templates/admin/base_site.html that uses the configured project-level templates directory to override admin/base_site.html.

The new template extends admin/base_site.html, which is the same template as is being overridden.

The template replaces just the branding block, adding a custom logo, and using block.super to retain the prior content.

The rest of the template is inherited unchanged from admin/base_site.html.

This technique works because the template loader does not consider the already loaded override template (at templates/admin/base_site.html) when resolving the extends tag. Combined with block.super it is a powerful technique to make small customizations.

---

## How to provide initial data for models | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/initial-data/

**Contents:**
- How to provide initial data for models¶
- Provide initial data with migrations¶
- Provide data with fixtures¶
  - Tell Django where to look for fixture files¶

It’s sometimes useful to prepopulate your database with hardcoded data when you’re first setting up an app. You can provide initial data with migrations or fixtures.

To automatically load initial data for an app, create a data migration. Migrations are run when setting up the test database, so the data will be available there, subject to some limitations.

You can also provide data using fixtures, however, this data isn’t loaded automatically, except if you use TransactionTestCase.fixtures.

A fixture is a collection of data that Django knows how to import into a database. The most straightforward way of creating a fixture if you’ve already got some data is to use the manage.py dumpdata command. Or, you can write fixtures by hand; fixtures can be written as JSON, XML or YAML (with PyYAML installed) documents. The serialization documentation has more details about each of these supported serialization formats.

As an example, though, here’s what a fixture for a Person model might look like in JSON:

And here’s that same fixture as YAML:

You’ll store this data in a fixtures directory inside your app.

You can load data by calling manage.py loaddata <fixturename>, where <fixturename> is the name of the fixture file you’ve created. Each time you run loaddata, the data will be read from the fixture and reloaded into the database. Note this means that if you change one of the rows created by a fixture and then run loaddata again, you’ll wipe out any changes you’ve made.

By default, Django looks for fixtures in the fixtures directory inside each app, so the command loaddata sample will find the file my_app/fixtures/sample.json. This works with relative paths as well, so loaddata my_app/sample will find the file my_app/fixtures/my_app/sample.json.

Django also looks for fixtures in the list of directories provided in the FIXTURE_DIRS setting.

To completely prevent default search from happening, use an absolute path to specify the location of your fixture file, e.g. loaddata /path/to/sample.

Namespace your fixture files

Django will use the first fixture file it finds whose name matches, so if you have fixture files with the same name in different applications, you will be unable to distinguish between them in your loaddata commands. The easiest way to avoid this problem is by namespacing your fixture files. That is, by putting them inside a directory named for their application, as in the relative path example above.

Fixtures are also used by the testing framework to help set up a consistent test environment.

---

## How to release Django | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/internals/howto-release-django/

**Contents:**
- How to release Django¶
- Overview¶
- Prerequisites¶
- Pre-release tasks¶
  - 10 (or more) days before a security release¶
  - A week before a security release¶
  - A few days before any release¶
    - A few days before a feature freeze¶
- Feature freeze tasks¶
- Actually rolling the release¶

This document explains how to release Django.

Please, keep these instructions up-to-date if you make changes! The point here is to be descriptive, not prescriptive, so feel free to streamline or otherwise make changes, but update this document accordingly!

There are three types of releases that you might need to make:

Security releases: disclosing and fixing a vulnerability. This’ll generally involve two or three simultaneous releases – e.g. 3.2.x, 4.0.x, and, depending on timing, perhaps a 4.1.x.

Regular version releases: either a final release (e.g. 4.1) or a bugfix update (e.g. 4.1.1).

Pre-releases: e.g. 4.2 alpha, beta, or rc.

The short version of the steps involved is:

If this is a security release, pre-notify the security distribution list one week before the actual release.

Proofread the release notes, looking for organization and writing errors. Draft a blog post and email announcement.

Update version numbers and create the release artifacts.

Create the new Release in the admin on djangoproject.com.

Set the proper date but ensure the flag is_active is disabled.

Upload the artifacts (tarball, wheel, and checksums).

Verify package(s) signatures, check if they can be installed, and ensure minimal functionality.

Upload the new version(s) to PyPI.

Enable the is_active flag for each release in the admin on djangoproject.com.

Post the blog entry and send out the email announcements.

Update version numbers post-release in stable branch(es).

Add stub release notes for the next patch release in main and backport.

There are a lot of details, so please read on.

Use the checklists app

To generate a checklist compiling the tasks described below as relevant to the specific release(s) you are issuing, use the checklists app in the project admin. This populates a lot of boilerplate you will need for announcements, CVE publication, and hashes for commit messages. By using this app for preparing security issue metadata, your peer releasers can check your entries and consult them again in the future. (Example)

You’ll need a few things before getting started. If this is your first release, you’ll need to coordinate with another releaser to get all these things lined up, and write to the Ops mailing list requesting the required access and permissions.

A Unix environment with these tools installed (in alphabetical order):

hashing tools (typically md5sum, sha1sum, and sha256sum on Linux, or md5 and shasum on macOS)

A GPG key pair. Ensure that the private part of this key is securely stored. The public part needs to be uploaded to your GitHub account, and also to the Jenkins server running the “confirm release” job.

More than one GPG key

If the key you want to use is not your default signing key, you’ll need to add -u you@example.com to every GPG signing command shown below, where you@example.com is the email address associated with the key you want to use.

A clean Python virtual environment (Python 3.9+) to build artifacts, with these required Python packages installed:

Access to Django’s project on PyPI to upload binaries, ideally with extra permissions to yank a release if necessary. Create a project-scoped token following the official documentation and set up your $HOME/.pypirc file like this:

Access to Django’s project on Transifex, with a Manager role. Generate an API Token in the user setting section and set up your $HOME/.transifexrc file like this:

Access to the Django admin on djangoproject.com as a “Site maintainer”.

Access to create a post in the Django Forum - Announcements category and to send emails to the django-announce mailing list.

Access to the django-security repo in GitHub. Among other things, this provides access to the pre-notification distribution list (needed for security release preparation tasks).

Access to the Django project on Read the Docs.

A few items need to be taken care of before even beginning the release process. This stuff starts about a week before the release; most of it can be done any time leading up to the actual release.

Reserve one CVE ID per security issue as follows. (Or, if you lack CNA credentials, email cna@djangoproject.com with a request.)

Enable virtual environment with cvelib installed.

Export user information:

Generate the relevant (private) patch(es) using git format-patch, one for the main branch and one for each stable branch being patched.

Send out pre-notification exactly one week before the security release. The template for that email and a list of the recipients are in the private django-security GitHub wiki. BCC the pre-notification recipients, and be sure to include the relevant CVE IDs. Attach all the relevant patches (targeting main and the stable branches), and sign the email text with the key you’ll use for the release, with a command like:

Notify django-announce of the upcoming security release with a general message such as:

Prepare issue metadata: * Severity * Short description * Reporter * Remediator * Reported at * Confirmed at (usually date CVE reserved) * CWE Problem Type * CAPEC Impact Type * CVSS (4.0) Score & Vector

As the release approaches, watch Trac to make sure no release blockers are left for the upcoming release. Under exceptional circumstances, such as to meet a pre-determined security release date, a release could still go ahead with an open release blocker. The releaser is trusted with the decision to release with an open release blocker or to postpone the release date of a non-security release if required.

Check with the other mergers to make sure they don’t have any uncommitted changes for the release.

Proofread the release notes, including looking at the online version to catch any broken links or reST errors, and make sure the release notes contain the correct date.

Double-check that the release notes mention deprecation timelines for any APIs noted as deprecated, and that they mention any changes in Python version support.

Double-check that the release notes index has a link to the notes for the new release; this will be in docs/releases/index.txt.

If this is a feature release, ensure translations from Transifex have been integrated.

In addition to having a configured Transifex account, ensure that the tx CLI is available in your PATH. You can then fetch all translations since a given date by running:

To determine a good value for --since, check the date of the most recent commit with wording similar to Updated translations from Transifex and use a date a few days prior.

This command takes some time to run. When done, carefully inspect the output for potential errors and/or warnings. If there are some, you will need to debug and resolve them on a case by case basis.

The recently fetched translations need some manual adjusting. First of all, the PO-Revision-Date values must be manually bumped to be later than POT-Creation-Date. You can use a command similar to this to bulk update all the .po files (compare the diff against the relevant stable branch):

Lastly, commit the changed/added files (both .po and .mo) and create a new PR targeting the stable branch of the corresponding release (example PR updating translations for 4.2).

Once merged, forward port the changes into main (example commit).

Update the django-admin manual page:

and then commit the changed man page.

If this is the “dot zero” release of a new series, create a new branch from the current stable branch in the django-docs-translations repository. For example, when releasing Django 4.2:

Write the announcement blog post for the release. You can enter it into the admin at any time and mark it as inactive. Here are a few examples: example security release announcement, example regular release announcement, example pre-release announcement.

In preparation for the alpha release, the directory /home/www/www/media/releases/A.B must be created on the djangoproject server.

Before the feature freeze, a branch targeting main must be created to prepare for the next feature release. It should be reviewed and approved a few days before the freeze, allowing it to be merged after the stable branch is cut. The following items should be addressed in this branch:

Update the VERSION tuple in django/__init__.py, incrementing to the next expected release (example commit).

Create a stub release note for the next feature release. Use the stub from the previous feature release or copy the contents from the current version and delete most of the contents leaving only the headings (example commit).

Remove .. versionadded:: and .. versionchanged:: annotations in the documentation from two releases ago, as well as any remaining older annotations. For example, in Django 5.1, notes for 4.2 will be removed (example commit).

Remove features that have reached the end of their deprecation cycle, including their docs and the .. deprecated:: annotation. Each removal should be done in a separate commit for clarity. In the commit message, add a Refs #XXXXX -- prefix linking to the original ticket where the deprecation began if possible. Make sure this gets noted in the removed features section in the release notes (example commit).

Increase the default PBKDF2 iterations in django.contrib.auth.hashers.PBKDF2PasswordHasher by about 20% (pick a round number). Run the tests, and update the 3 failing hasher tests with the new values. Make sure this gets noted in the release notes (example commit).

Concrete examples for past feature release bootstrap branches: 5.2 bootstrap, 5.1 bootstrap, 5.0 bootstrap.

Remove empty sections from the release notes (example commit).

Build the release notes locally and read them. Make any necessary change to improve flow or fix grammar (example commit).

Create a new stable branch from main. Be sure to fetch and update upstream to latest. For example, when feature freezing Django 5.2:

At the same time, update the django_next_version variable in docs/conf.py on the stable release branch to point to the new development version. For example, when creating stable/5.2.x, set django_next_version to '6.0' on the new stable branch (example commit).

Create Release entries for the next version in the admin on djangoproject.com. Add one for each milestone (alpha, beta, rc, and final), leaving is active unset to mark them as unreleased. Set target dates per the agreed schedule, and set the LTS flag if applicable. The X.Y roadmap page will be available at /download/X.Y/roadmap/.

For example, when creating stable/5.2.x, add Release entries for 6.0a1, 6.0b1, 6.0rc1, and 6.0. The 6.0 roadmap can be then reviewed at https://www.djangoproject.com/download/6.0/roadmap/.

Go to the Add document release page in the admin, create a new DocumentRelease object for the English language for the newly created Release object. Do not mark this as default.

Add the new branch to Read the Docs. Since the automatically generated version names (“stable-A.B.x”) differ from the version names used in Read the Docs (“A.B.x”), update the Read the Docs config for the version to point to the slug A.B.x and set it as active. See more details.

Create a PR on PyPI proposing the new Trove classifier. For example Framework :: Django :: 5.2.

Update the current branch under active development and add pre-release branch in the Django release process on Trac.

Update the docs/fixtures/doc_releases.json JSON fixture for djangoproject.com, so people without access to the production DB can still run an up-to-date copy of the docs site (example PR). This will be merged after the final release.

OK, this is the fun part, where we actually push out a release! If you’re issuing multiple releases, repeat these steps for each release.

Check Jenkins is green for the version(s) you’re putting out. You probably shouldn’t issue a release until it’s green, and you should make sure that the latest green run includes the changes that you are releasing.

Cleanup the release notes for this release. Make these changes in main and backport to all branches where the release notes for a particular version are located.

For a feature release, remove the UNDER DEVELOPMENT header at the top of the release notes, remove the Expected prefix and update the release date, if necessary (example commit).

For a patch release, remove the Expected prefix and update the release date for all releases, if necessary (example commit).

A release always begins from a release branch, so you should make sure you’re on an up-to-date stable branch. Also, you should have available a clean and dedicated virtual environment per version being released. For example:

If this is a security release, merge the appropriate patches from django-security. Rebase these patches as necessary to make each one a plain commit on the release branch rather than a merge commit. To ensure this, merge them with the --ff-only flag; for example:

(This assumes security/4.1.x is a branch in the django-security repo containing the necessary security patches for the next release in the 4.1 series.)

If git refuses to merge with --ff-only, switch to the security-patch branch and rebase it on the branch you are about to merge it into (git checkout security/4.1.x; git rebase stable/4.1.x) and then switch back and do the merge. Make sure the commit message for each security fix explains that the commit is a security fix and that an announcement will follow (example security commit).

Update the version number in django/__init__.py for the release. Please see notes on setting the VERSION tuple below for details on VERSION (example commit).

If this is a pre-release package also update the “Development Status” trove classifier in pyproject.toml to reflect this. An rc pre-release should not change the trove classifier (example commit for alpha release, example commit for beta release).

Otherwise, make sure the classifier is set to Development Status :: 5 - Production/Stable.

Optionally use helper scripts

You can streamline some of the steps below using helper scripts from the scripts folder:

Release script example run:

Verify the release (after artifacts were uploaded):

Tag the release using git tag. For example:

You can check your work running git tag --verify <tag>.

Make sure you have an absolutely clean tree by running git clean -dfx.

Run python -m build to generate the release packages. This will create the release artifacts (tarball and wheel) in a dist/ directory. For Django 5.0 or older, you need to run make -f extras/Makefile instead.

Generate the hashes of the release packages:

Create a “checksums” file, Django-<<VERSION>>.checksum.txt containing the hashes and release information. Start with this template and insert the correct version, date, GPG key ID (from gpg --list-keys --keyid-format LONG), release manager’s GitHub username, release URL, and checksums:

Sign the checksum file (gpg --clearsign --digest-algo SHA256 Django-<version>.checksum.txt). This generates a signed document, Django-<version>.checksum.txt.asc which you can then verify using gpg --verify Django-<version>.checksum.txt.asc.

Now you’re ready to actually put the release out there. To do this:

Create a new Release entry in the djangoproject.com’s admin. If this is a security release, this should be done 15 minutes before the announced release time, no sooner:

Must match the version number as defined in the tarball (django-<version>.tar.gz). For example: “5.2”, “4.1.1”, or “4.2rc1”.

Set to False until the release is fully published (last step).

Enable if the release is part of an LTS branch.

Set the release date to today. This release will not be published until is_active is enabled.

Upload the tarball (django-<version>.tar.gz), wheel (django-<version>-py3-none-any.whl), and checksum (django-<version>.checksum.txt.asc) files created earlier.

Test that the release packages install correctly using pip. Here’s one simple method (this just tests that the binaries are available, that they install correctly, and that migrations and the development server start, but it’ll catch silly mistakes): https://code.djangoproject.com/wiki/ReleaseTestNewVersion.

Run the confirm-release build on Jenkins to verify the checksum file(s) (e.g. use 4.2rc1 for https://media.djangoproject.com/pgp/Django-4.2rc1.checksum.txt).

Upload the release packages to PyPI:

Update the newly created Release in the admin in djangoproject.com and enable the is_active flag.

Push your work and the new tag:

Make the blog post announcing the release live.

For a new version release (e.g. 4.1, 4.2), update the default stable version of the docs by flipping the is_default flag to True on the appropriate DocumentRelease object in the docs.djangoproject.com database (this will automatically flip it to False for all others); you can do this using the site’s admin.

Create new DocumentRelease objects for each language that has an entry for the previous release. Update djangoproject.com’s robots.docs.txt file by copying the result generated from running the command manage_translations.py robots_txt in the current stable branch from the django-docs-translations repository. For example, when releasing Django 4.2:

Post the release announcement to the django-announce mailing list and the Django Forum. This should include a link to the announcement blog post.

If this is a security release, publish the CVE metadata. (The checklist app generates JSON for this.):

If this is a security release, send a separate email to oss-security@lists.openwall.com. Provide “Django” plus the CVE IDs in the subject line. The message body should include the vulnerability details, for example, the announcement blog post text. Include a link to the announcement blog post.

You’re almost done! All that’s left to do now is:

If this is not a pre-release, update the VERSION tuple in django/__init__.py again, incrementing to whatever the next expected release will be. For example, after releasing 4.1.1, update VERSION to VERSION = (4, 1, 2, 'alpha', 0) (example commit).

If this was an alpha release:

Add the feature release version in Trac’s versions list.

Create a new security branch from the freshly cut stable branch. Be sure to fetch and update upstream to latest. For example, after the 5.2 alpha release:

If this was a final release:

Update the default_version setting in the code.djangoproject.com’s trac.ini file (example PR).

Update the current stable branch and remove the pre-release branch in the Django release process on Trac.

Update djangoproject.com’s download page (example PR).

Process the older versions that will reach End-Of-Mainstream and/or End-Of-Life support when this final release is published:

Ensure that the EOL versions are mentioned in the blog post. Example.

Create a tag for the EOL stable branch and delete the stable branch. Inspect and use the scripts/archive_eol_stable_branches.py helper.

If this was a security release, update Archive of security issues with details of the issues addressed.

If this was a pre-release, the translation catalogs need to be updated:

Make a new branch from the recently released stable branch:

Ensure that the release’s dedicated virtual environment is enabled and run the following:

Make a pull request against the corresponding stable branch and merge once approved.

Forward port the updated source translations to the main branch (example commit).

If this was an rc pre-release, call for translations for the upcoming release in the Django Forum - Internationalization category.

Django’s version reporting is controlled by the VERSION tuple in django/__init__.py. This is a five-element tuple, whose elements are:

Status – can be one of “alpha”, “beta”, “rc” or “final”.

Series number, for alpha/beta/RC packages which run in sequence (allowing, for example, “beta 1”, “beta 2”, etc.).

For a final release, the status is always “final” and the series number is always 0. A series number of 0 with an “alpha” status will be reported as “pre-alpha”.

(4, 1, 1, "final", 0) → “4.1.1”

(4, 2, 0, "alpha", 0) → “4.2 pre-alpha”

(4, 2, 0, "beta", 1) → “4.2 beta 1”

---

## How to upgrade Django to a newer version | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/upgrade-version/

**Contents:**
- How to upgrade Django to a newer version¶
- Required Reading¶
- Dependencies¶
- Resolving deprecation warnings¶
- Installation¶
- Testing¶
- Deployment¶

While it can be a complex process at times, upgrading to the latest Django version has several benefits:

New features and improvements are added.

Older version of Django will eventually no longer receive security updates. (see Supported versions).

Upgrading as each new Django release is available makes future upgrades less painful by keeping your code base up to date.

Tools to help with version upgrades

Django has a vibrant ecosystem. There are automated upgrade helpers highlighted on the Community Ecosystem page.

Here are some things to consider to help make your upgrade process as smooth as possible.

If it’s your first time doing an upgrade, it is useful to read the guide on the different release processes.

Afterward, you should familiarize yourself with the changes that were made in the new Django version(s):

Read the release notes for each ‘final’ release from the one after your current Django version, up to and including the version to which you plan to upgrade.

Look at the deprecation timeline for the relevant versions.

Pay particular attention to backwards incompatible changes to get a clear idea of what will be needed for a successful upgrade.

If you’re upgrading through more than one feature version (e.g. 2.0 to 2.2), it’s usually easier to upgrade through each feature release incrementally (2.0 to 2.1 to 2.2) rather than to make all the changes for each feature release at once. For each feature release, use the latest patch release (e.g. for 2.1, use 2.1.15).

The same incremental upgrade approach is recommended when upgrading from one LTS to the next.

In most cases it will be necessary to upgrade to the latest version of your Django-related dependencies as well. If the Django version was recently released or if some of your dependencies are not well-maintained, some of your dependencies may not yet support the new Django version. In these cases you may have to wait until new versions of your dependencies are released.

Before upgrading, it’s a good idea to resolve any deprecation warnings raised by your project while using your current version of Django. Fixing these warnings before upgrading ensures that you’re informed about areas of the code that need altering.

In Python, deprecation warnings are silenced by default. You must turn them on using the -Wa Python command line option or the PYTHONWARNINGS environment variable. For example, to show warnings while running tests:

If you’re not using the Django test runner, you may need to also ensure that any console output is not captured which would hide deprecation warnings. For example, if you use pytest:

Resolve any deprecation warnings with your current version of Django before continuing the upgrade process.

Third party applications might use deprecated APIs in order to support multiple versions of Django, so deprecation warnings in packages you’ve installed don’t necessarily indicate a problem. If a package doesn’t support the latest version of Django, consider raising an issue or sending a pull request for it.

Once you’re ready, it is time to install the new Django version. If you are using a virtual environment and it is a major upgrade, you might want to set up a new environment with all the dependencies first.

If you installed Django with pip, you can use the --upgrade or -U flag:

When the new environment is set up, run the full test suite for your application. Again, it’s useful to turn on deprecation warnings on so they’re shown in the test output (you can also use the flag if you test your app manually using manage.py runserver):

After you have run the tests, fix any failures. While you have the release notes fresh in your mind, it may also be a good time to take advantage of new features in Django by refactoring your code to eliminate any deprecation warnings.

If you are upgrading to an alpha, beta, or release candidate, please see our guide on How to test pre-release versions of Django for more specific tips about catching regressions and reporting bugs.

When you are sufficiently confident your app works with the new version of Django, you’re ready to go ahead and deploy your upgraded Django project.

If you are using caching provided by Django, you should consider clearing your cache after upgrading. Otherwise you may run into problems, for example, if you are caching pickled objects as these objects are not guaranteed to be pickle-compatible across Django versions. A past instance of incompatibility was caching pickled HttpResponse objects, either directly or indirectly via the cache_page() decorator.

---

## How to use Django’s Content Security Policy | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/csp/

**Contents:**
- How to use Django’s Content Security Policy¶
- Basic config¶
- Nonce config¶

To enable Content Security Policy (CSP) in your Django project:

Add the CSP middleware to your MIDDLEWARE setting:

Configure the CSP policies in your settings.py using either SECURE_CSP or SECURE_CSP_REPORT_ONLY (or both). The CSP Settings docs provide more details about the differences between these two:

To use nonces in your CSP policy, beside the basic config, you need to:

Include the NONCE placeholder value in the CSP settings. This only applies to script-src or style-src directives:

Add the csp() context processor to your TEMPLATES setting. This makes the generated nonce value available in the Django templates as the csp_nonce context variable:

In your templates, add the nonce attribute to the relevant inline <style> or <script> tags, using the csp_nonce context variable:

Caching and Nonce Reuse

The ContentSecurityPolicyMiddleware automatically handles generating a unique nonce and inserting the appropriate nonce-<value> source expression into the Content-Security-Policy (or Content-Security-Policy-Report-Only) header when the nonce is used in a template.

To ensure correct behavior, make sure both the HTML and the header are generated within the same request and not served from cache. See the reference documentation on Nonce usage for implementation details and important caching considerations.

---

## How to use Django’s CSRF protection | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/csrf/

**Contents:**
- How to use Django’s CSRF protection¶
- Using CSRF protection with AJAX¶
  - Acquiring the token if CSRF_USE_SESSIONS and CSRF_COOKIE_HTTPONLY are False¶
  - Acquiring the token if CSRF_USE_SESSIONS or CSRF_COOKIE_HTTPONLY is True¶
  - Setting the token on the AJAX request¶
- Using CSRF protection in Jinja2 templates¶
- Using the decorator method¶
- Handling rejected requests¶
- Using CSRF protection with caching¶
- Testing and CSRF protection¶

To take advantage of CSRF protection in your views, follow these steps:

The CSRF middleware is activated by default in the MIDDLEWARE setting. If you override that setting, remember that 'django.middleware.csrf.CsrfViewMiddleware' should come before any view middleware that assume that CSRF attacks have been dealt with.

If you disabled it, which is not recommended, you can use csrf_protect() on particular views you want to protect (see below).

In any template that uses a POST form, use the csrf_token tag inside the <form> element if the form is for an internal URL, e.g.:

This should not be done for POST forms that target external URLs, since that would cause the CSRF token to be leaked, leading to a vulnerability.

In the corresponding view functions, ensure that RequestContext is used to render the response so that {% csrf_token %} will work properly. If you’re using the render() function, generic views, or contrib apps, you are covered already since these all use RequestContext.

While the above method can be used for AJAX POST requests, it has some inconveniences: you have to remember to pass the CSRF token in as POST data with every POST request. For this reason, there is an alternative method: on each XMLHttpRequest, set a custom X-CSRFToken header (as specified by the CSRF_HEADER_NAME setting) to the value of the CSRF token. This is often easier because many JavaScript frameworks provide hooks that allow headers to be set on every request.

First, you must get the CSRF token. How to do that depends on whether or not the CSRF_USE_SESSIONS and CSRF_COOKIE_HTTPONLY settings are enabled.

The recommended source for the token is the csrftoken cookie, which will be set if you’ve enabled CSRF protection for your views as outlined above.

The CSRF token cookie is named csrftoken by default, but you can control the cookie name via the CSRF_COOKIE_NAME setting.

You can acquire the token like this:

The above code could be simplified by using the JavaScript Cookie library to replace getCookie:

The CSRF token is also present in the DOM in a masked form, but only if explicitly included using csrf_token in a template. The cookie contains the canonical, unmasked token. The CsrfViewMiddleware will accept either. However, in order to protect against BREACH attacks, it’s recommended to use a masked token.

If your view is not rendering a template containing the csrf_token template tag, Django might not set the CSRF token cookie. This is common in cases where forms are dynamically added to the page. To address this case, Django provides a view decorator which forces setting of the cookie: ensure_csrf_cookie().

If you activate CSRF_USE_SESSIONS or CSRF_COOKIE_HTTPONLY, you must include the CSRF token in your HTML and read the token from the DOM with JavaScript:

Finally, you’ll need to set the header on your AJAX request. Using the fetch() API:

Django’s Jinja2 template backend adds {{ csrf_input }} to the context of all templates which is equivalent to {% csrf_token %} in the Django template language. For example:

Rather than adding CsrfViewMiddleware as a blanket protection, you can use the csrf_protect() decorator, which has exactly the same functionality, on particular views that need the protection. It must be used both on views that insert the CSRF token in the output, and on those that accept the POST form data. (These are often the same view function, but not always).

Use of the decorator by itself is not recommended, since if you forget to use it, you will have a security hole. The ‘belt and braces’ strategy of using both is fine, and will incur minimal overhead.

By default, a ‘403 Forbidden’ response is sent to the user if an incoming request fails the checks performed by CsrfViewMiddleware. This should usually only be seen when there is a genuine Cross Site Request Forgery, or when, due to a programming error, the CSRF token has not been included with a POST form.

The error page, however, is not very friendly, so you may want to provide your own view for handling this condition. To do this, set the CSRF_FAILURE_VIEW setting.

CSRF failures are logged as warnings to the django.security.csrf logger.

If the csrf_token template tag is used by a template (or the get_token function is called some other way), CsrfViewMiddleware will add a cookie and a Vary: Cookie header to the response. This means that the middleware will play well with the cache middleware if it is used as instructed (UpdateCacheMiddleware goes before all other middleware).

However, if you use cache decorators on individual views, the CSRF middleware will not yet have been able to set the Vary header or the CSRF cookie, and the response will be cached without either one. In this case, on any views that will require a CSRF token to be inserted you should use the django.views.decorators.csrf.csrf_protect() decorator first:

If you are using class-based views, you can refer to Decorating class-based views.

The CsrfViewMiddleware will usually be a big hindrance to testing view functions, due to the need for the CSRF token which must be sent with every POST request. For this reason, Django’s HTTP client for tests has been modified to set a flag on requests which relaxes the middleware and the csrf_protect decorator so that they no longer rejects requests. In every other respect (e.g. sending cookies etc.), they behave the same.

If, for some reason, you want the test client to perform CSRF checks, you can create an instance of the test client that enforces CSRF checks:

Certain views can have unusual requirements that mean they don’t fit the normal pattern envisaged here. A number of utilities can be useful in these situations. The scenarios they might be needed in are described in the following section.

Most views requires CSRF protection, but a few do not.

Solution: rather than disabling the middleware and applying csrf_protect to all the views that need it, enable the middleware and use csrf_exempt().

There are cases when CsrfViewMiddleware.process_view may not have run before your view is run - 404 and 500 handlers, for example - but you still need the CSRF token in a form.

Solution: use requires_csrf_token()

There may be some views that are unprotected and have been exempted by csrf_exempt, but still need to include the CSRF token.

Solution: use csrf_exempt() followed by requires_csrf_token(). (i.e. requires_csrf_token should be the innermost decorator).

A view needs CSRF protection under one set of conditions only, and mustn’t have it for the rest of the time.

Solution: use csrf_exempt() for the whole view function, and csrf_protect() for the path within it that needs protection. Example:

A page makes a POST request via AJAX, and the page does not have an HTML form with a csrf_token that would cause the required CSRF cookie to be sent.

Solution: use ensure_csrf_cookie() on the view that sends the page.

Because it is possible for the developer to turn off the CsrfViewMiddleware, all relevant views in contrib apps use the csrf_protect decorator to ensure the security of these applications against CSRF. It is recommended that the developers of other reusable apps that want the same guarantees also use the csrf_protect decorator on their views.

---

## How to use Django with Apache and mod_wsgi | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/modwsgi/

**Contents:**
- How to use Django with Apache and mod_wsgi¶
- Basic configuration¶
- Using mod_wsgi daemon mode¶
- Serving files¶
- Serving the admin files¶
- Authenticating against Django’s user database from Apache¶

Deploying Django with Apache and mod_wsgi is a tried and tested way to get Django into production.

mod_wsgi is an Apache module which can host any Python WSGI application, including Django. Django will work with any version of Apache which supports mod_wsgi.

The official mod_wsgi documentation is your source for all the details about how to use mod_wsgi. You’ll probably want to start with the installation and configuration documentation.

Once you’ve got mod_wsgi installed and activated, edit your Apache server’s httpd.conf file and add the following.

The first bit in the WSGIScriptAlias line is the base URL path you want to serve your application at (/ indicates the root url), and the second is the location of a “WSGI file” – see below – on your system, usually inside of your project package (mysite in this example). This tells Apache to serve any request below the given URL using the WSGI application defined in that file.

If you install your project’s Python dependencies inside a virtual environment, add the path using WSGIPythonHome. See the mod_wsgi virtual environment guide for more details.

The WSGIPythonPath line ensures that your project package is available for import on the Python path; in other words, that import mysite works.

The <Directory> piece ensures that Apache can access your wsgi.py file.

Next we’ll need to ensure this wsgi.py with a WSGI application object exists. As of Django version 1.4, startproject will have created one for you; otherwise, you’ll need to create it. See the WSGI overview documentation for the default contents you should put in this file, and what else you can add to it.

If multiple Django sites are run in a single mod_wsgi process, all of them will use the settings of whichever one happens to run first. This can be solved by changing:

or by using mod_wsgi daemon mode and ensuring that each site runs in its own daemon process.

Fixing UnicodeEncodeError for file uploads

If you get a UnicodeEncodeError when uploading or writing files with file names or content that contains non-ASCII characters, make sure Apache is configured to support UTF-8 encoding:

A common location to put this configuration is /etc/apache2/envvars.

Alternatively, if you are using mod_wsgi daemon mode you can add lang and locale options to the WSGIDaemonProcess directive:

See the Files section of the Unicode reference guide for details.

“Daemon mode” is the recommended mode for running mod_wsgi (on non-Windows platforms). To create the required daemon process group and delegate the Django instance to run in it, you will need to add appropriate WSGIDaemonProcess and WSGIProcessGroup directives. A further change required to the above configuration if you use daemon mode is that you can’t use WSGIPythonPath; instead you should use the python-path option to WSGIDaemonProcess, for example:

If you want to serve your project in a subdirectory (https://example.com/mysite in this example), you can add WSGIScriptAlias to the configuration above:

See the official mod_wsgi documentation for details on setting up daemon mode.

Django doesn’t serve files itself; it leaves that job to whichever web server you choose.

We recommend using a separate web server – i.e., one that’s not also running Django – for serving media. Here are some good choices:

A stripped-down version of Apache

If, however, you have no option but to serve media files on the same Apache VirtualHost as Django, you can set up Apache to serve some URLs as static media, and others using the mod_wsgi interface to Django.

This example sets up Django at the site root, but serves robots.txt, favicon.ico, and anything in the /static/ and /media/ URL space as a static file. All other URLs will be served using mod_wsgi:

When django.contrib.staticfiles is in INSTALLED_APPS, the Django development server automatically serves the static files of the admin app (and any other installed apps). This is however not the case when you use any other server arrangement. You’re responsible for setting up Apache, or whichever web server you’re using, to serve the admin files.

The admin files live in (django/contrib/admin/static/admin) of the Django distribution.

We strongly recommend using django.contrib.staticfiles to handle the admin files (along with a web server as outlined in the previous section; this means using the collectstatic management command to collect the static files in STATIC_ROOT, and then configuring your web server to serve STATIC_ROOT at STATIC_URL), but here are three other approaches:

Create a symbolic link to the admin static files from within your document root (this may require +FollowSymLinks in your Apache configuration).

Use an Alias directive, as demonstrated above, to alias the appropriate URL (probably STATIC_URL + admin/) to the actual location of the admin files.

Copy the admin static files so that they live within your Apache document root.

Django provides a handler to allow Apache to authenticate users directly against Django’s authentication backends. See the mod_wsgi authentication documentation.

---

## How to use Django with Daphne | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/deployment/asgi/daphne/

**Contents:**
- How to use Django with Daphne¶
- Installing Daphne¶
- Running Django in Daphne¶
- Integration with runserver¶

Daphne is a pure-Python ASGI server for UNIX, maintained by members of the Django project. It acts as the reference server for ASGI.

You can install Daphne with pip:

When Daphne is installed, a daphne command is available which starts the Daphne server process. At its simplest, Daphne needs to be called with the location of a module containing an ASGI application object, followed by what the application is called (separated by a colon).

For a typical Django project, invoking Daphne would look like:

This will start one process listening on 127.0.0.1:8000. It requires that your project be on the Python path; to ensure that run this command from the same directory as your manage.py file.

Daphne provides a runserver command to serve your site under ASGI during development.

This can be enabled by adding daphne to the start of your INSTALLED_APPS and adding an ASGI_APPLICATION setting pointing to your ASGI application object:

---

## How to use Django with Gunicorn | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/gunicorn/

**Contents:**
- How to use Django with Gunicorn¶
- Installing Gunicorn¶
- Running Django in Gunicorn as a generic WSGI application¶

Gunicorn (‘Green Unicorn’) is a pure-Python WSGI server for UNIX. It has no dependencies and can be installed using pip.

Install gunicorn by running python -m pip install gunicorn. For more details, see the gunicorn documentation.

When Gunicorn is installed, a gunicorn command is available which starts the Gunicorn server process. The simplest invocation of gunicorn is to pass the location of a module containing a WSGI application object named application, which for a typical Django project would look like:

This will start one process running one thread listening on 127.0.0.1:8000. It requires that your project be on the Python path; the simplest way to ensure that is to run this command from the same directory as your manage.py file.

See Gunicorn’s deployment documentation for additional tips.

---

## How to use Django with Hypercorn | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/deployment/asgi/hypercorn/

**Contents:**
- How to use Django with Hypercorn¶
- Installing Hypercorn¶
- Running Django in Hypercorn¶

Hypercorn is an ASGI server that supports HTTP/1, HTTP/2, and HTTP/3 with an emphasis on protocol support.

You can install Hypercorn with pip:

When Hypercorn is installed, a hypercorn command is available which runs ASGI applications. Hypercorn needs to be called with the location of a module containing an ASGI application object, followed by what the application is called (separated by a colon).

For a typical Django project, invoking Hypercorn would look like:

This will start one process listening on 127.0.0.1:8000. It requires that your project be on the Python path; to ensure that run this command from the same directory as your manage.py file.

For more advanced usage, please read the Hypercorn documentation.

---

## How to use Django with Uvicorn | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/deployment/asgi/uvicorn/

**Contents:**
- How to use Django with Uvicorn¶
- Installing Uvicorn¶
- Running Django in Uvicorn¶
- Deploying Django using Uvicorn and Gunicorn¶

Uvicorn is an ASGI server based on uvloop and httptools, with an emphasis on speed.

You can install Uvicorn with pip:

When Uvicorn is installed, a uvicorn command is available which runs ASGI applications. Uvicorn needs to be called with the location of a module containing an ASGI application object, followed by what the application is called (separated by a colon).

For a typical Django project, invoking Uvicorn would look like:

This will start one process listening on 127.0.0.1:8000. It requires that your project be on the Python path; to ensure that run this command from the same directory as your manage.py file.

In development mode, you can add --reload to cause the server to reload any time a file is changed on disk.

For more advanced usage, please read the Uvicorn documentation.

Gunicorn is a robust web server that implements process monitoring and automatic restarts. This can be useful when running Uvicorn in a production environment.

To install Uvicorn and Gunicorn, use the following:

Then start Gunicorn using the Uvicorn worker class like this:

---

## How to use Django with uWSGI | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/uwsgi/

**Contents:**
- How to use Django with uWSGI¶
- Prerequisite: uWSGI¶
  - uWSGI model¶
  - Configuring and starting the uWSGI server for Django¶

uWSGI is a fast, self-healing and developer/sysadmin-friendly application container server coded in pure C.

The uWSGI docs offer a tutorial covering Django, nginx, and uWSGI (one possible deployment setup of many). The docs below are focused on how to integrate Django with uWSGI.

The uWSGI wiki describes several installation procedures. Using pip, the Python package manager, you can install any uWSGI version with a single command. For example:

uWSGI operates on a client-server model. Your web server (e.g., nginx, Apache) communicates with a django-uwsgi “worker” process to serve dynamic content.

uWSGI supports multiple ways to configure the process. See uWSGI’s configuration documentation.

Here’s an example command to start a uWSGI server:

This assumes you have a top-level project package named mysite, and within it a module mysite/wsgi.py that contains a WSGI application object. This is the layout you’ll have if you ran django-admin startproject mysite (using your own project name in place of mysite) with a recent version of Django. If this file doesn’t exist, you’ll need to create it. See the How to deploy with WSGI documentation for the default contents you should put in this file and what else you can add to it.

The Django-specific options here are:

chdir: The path to the directory that needs to be on Python’s import path – i.e., the directory containing the mysite package.

module: The WSGI module to use – probably the mysite.wsgi module that startproject creates.

env: Should probably contain at least DJANGO_SETTINGS_MODULE.

home: Optional path to your project virtual environment.

Example ini configuration file:

Example ini configuration file usage:

Fixing UnicodeEncodeError for file uploads

If you get a UnicodeEncodeError when uploading files with file names that contain non-ASCII characters, make sure uWSGI is configured to accept non-ASCII file names by adding this to your uwsgi.ini:

See the Files section of the Unicode reference guide for details.

See the uWSGI docs on managing the uWSGI process for information on starting, stopping and reloading the uWSGI workers.

---

## How to write a custom storage class | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/custom-file-storage/

**Contents:**
- How to write a custom storage class¶
- Use your custom storage engine¶

If you need to provide custom file storage – a common example is storing files on some remote system – you can do so by defining a custom storage class. You’ll need to follow these steps:

Your custom storage system must be a subclass of django.core.files.storage.Storage:

Django must be able to instantiate your storage system without any arguments. This means that any settings should be taken from django.conf.settings:

Your storage class must implement the _open() and _save() methods, along with any other methods appropriate to your storage class. See below for more on these methods.

In addition, if your class provides local file storage, it must override the path() method.

Your storage class must be deconstructible so it can be serialized when it’s used on a field in a migration. As long as your field has arguments that are themselves serializable, you can use the django.utils.deconstruct.deconstructible class decorator for this (that’s what Django uses on FileSystemStorage).

By default, the following methods raise NotImplementedError and will typically have to be overridden:

Note however that not all these methods are required and may be deliberately omitted. As it happens, it is possible to leave each method unimplemented and still have a working Storage.

By way of example, if listing the contents of certain storage backends turns out to be expensive, you might decide not to implement Storage.listdir().

Another example would be a backend that only handles writing to files. In this case, you would not need to implement any of the above methods.

Ultimately, which of these methods are implemented is up to you. Leaving some methods unimplemented will result in a partial (possibly broken) interface.

You’ll also usually want to use hooks specifically designed for custom storage objects. These are:

Called by Storage.open(), this is the actual mechanism the storage class uses to open the file. This must return a File object, though in most cases, you’ll want to return some subclass here that implements logic specific to the backend storage system. The FileNotFoundError exception should be raised when a file doesn’t exist.

Called by Storage.save(). The name will already have gone through get_valid_name() and get_available_name(), and the content will be a File object itself.

Should return the actual name of the file saved (usually the name passed in, but if the storage needs to change the file name return the new name instead).

Returns a filename suitable for use with the underlying storage system. The name argument passed to this method is either the original filename sent to the server or, if upload_to is a callable, the filename returned by that method after any path information is removed. Override this to customize how non-standard characters are converted to safe filenames.

The code provided on Storage retains only alpha-numeric characters, periods and underscores from the original filename, removing everything else.

Returns an alternative filename based on the file_root and file_ext parameters. By default, an underscore plus a random 7 character alphanumeric string is appended to the filename before the extension.

Returns a filename that is available in the storage mechanism, possibly taking the provided filename into account. The name argument passed to this method will have already cleaned to a filename valid for the storage system, according to the get_valid_name() method described above.

The length of the filename will not exceed max_length, if provided. If a free unique filename cannot be found, a SuspiciousFileOperation exception is raised.

If a file with name already exists, get_alternative_name() is called to obtain an alternative name.

The first step to using your custom storage with Django is to tell Django about the file storage backend you’ll be using. This is done using the STORAGES setting. This setting maps storage aliases, which are a way to refer to a specific storage throughout Django, to a dictionary of settings for that specific storage backend. The settings in the inner dictionaries are described fully in the STORAGES documentation.

Storages are then accessed by alias from the django.core.files.storage.storages dictionary:

---

## How to write custom lookups | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/howto/custom-lookups/

**Contents:**
- How to write custom lookups¶
- A lookup example¶
- A transformer example¶
- Writing an efficient abs__lt lookup¶
- A bilateral transformer example¶
- Writing alternative implementations for existing lookups¶
- How Django determines the lookups and transforms which are used¶

Django offers a wide variety of built-in lookups for filtering (for example, exact and icontains). This documentation explains how to write custom lookups and how to alter the working of existing lookups. For the API references of lookups, see the Lookup API reference.

Let’s start with a small custom lookup. We will write a custom lookup ne which works opposite to exact. Author.objects.filter(name__ne='Jack') will translate to the SQL:

This SQL is backend independent, so we don’t need to worry about different databases.

There are two steps to making this work. Firstly we need to implement the lookup, then we need to tell Django about it:

To register the NotEqual lookup we will need to call register_lookup on the field class we want the lookup to be available for. In this case, the lookup makes sense on all Field subclasses, so we register it with Field directly:

Lookup registration can also be done using a decorator pattern:

We can now use foo__ne for any field foo. You will need to ensure that this registration happens before you try to create any querysets using it. You could place the implementation in a models.py file, or register the lookup in the ready() method of an AppConfig.

Taking a closer look at the implementation, the first required attribute is lookup_name. This allows the ORM to understand how to interpret name__ne and use NotEqual to generate the SQL. By convention, these names are always lowercase strings containing only letters, but the only hard requirement is that it must not contain the string __.

We then need to define the as_sql method. This takes a SQLCompiler object, called compiler, and the active database connection. SQLCompiler objects are not documented, but the only thing we need to know about them is that they have a compile() method which returns a tuple containing an SQL string, and the parameters to be interpolated into that string. In most cases, you don’t need to use it directly and can pass it on to process_lhs() and process_rhs().

A Lookup works against two values, lhs and rhs, standing for left-hand side and right-hand side. The left-hand side is usually a field reference, but it can be anything implementing the query expression API. The right-hand is the value given by the user. In the example Author.objects.filter(name__ne='Jack'), the left-hand side is a reference to the name field of the Author model, and 'Jack' is the right-hand side.

We call process_lhs and process_rhs to convert them into the values we need for SQL using the compiler object described before. These methods return tuples containing some SQL and the parameters to be interpolated into that SQL, just as we need to return from our as_sql method. In the above example, process_lhs returns ('"author"."name"', []) and process_rhs returns ('"%s"', ['Jack']). In this example there were no parameters for the left hand side, but this would depend on the object we have, so we still need to include them in the parameters we return.

Finally we combine the parts into an SQL expression with <>, and supply all the parameters for the query. We then return a tuple containing the generated SQL string and the parameters.

The custom lookup above is great, but in some cases you may want to be able to chain lookups together. For example, let’s suppose we are building an application where we want to make use of the abs() operator. We have an Experiment model which records a start value, end value, and the change (start - end). We would like to find all experiments where the change was equal to a certain amount (Experiment.objects.filter(change__abs=27)), or where it did not exceed a certain amount (Experiment.objects.filter(change__abs__lt=27)).

This example is somewhat contrived, but it nicely demonstrates the range of functionality which is possible in a database backend independent manner, and without duplicating functionality already in Django.

We will start by writing an AbsoluteValue transformer. This will use the SQL function ABS() to transform the value before comparison:

Next, let’s register it for IntegerField:

We can now run the queries we had before. Experiment.objects.filter(change__abs=27) will generate the following SQL:

By using Transform instead of Lookup it means we are able to chain further lookups afterward. So Experiment.objects.filter(change__abs__lt=27) will generate the following SQL:

Note that in case there is no other lookup specified, Django interprets change__abs=27 as change__abs__exact=27.

This also allows the result to be used in ORDER BY and DISTINCT ON clauses. For example Experiment.objects.order_by('change__abs') generates:

And on databases that support distinct on fields (such as PostgreSQL), Experiment.objects.distinct('change__abs') generates:

When looking for which lookups are allowable after the Transform has been applied, Django uses the output_field attribute. We didn’t need to specify this here as it didn’t change, but supposing we were applying AbsoluteValue to some field which represents a more complex type (for example a point relative to an origin, or a complex number) then we may have wanted to specify that the transform returns a FloatField type for further lookups. This can be done by adding an output_field attribute to the transform:

This ensures that further lookups like abs__lte behave as they would for a FloatField.

When using the above written abs lookup, the SQL produced will not use indexes efficiently in some cases. In particular, when we use change__abs__lt=27, this is equivalent to change__gt=-27 AND change__lt=27. (For the lte case we could use the SQL BETWEEN).

So we would like Experiment.objects.filter(change__abs__lt=27) to generate the following SQL:

The implementation is:

There are a couple of notable things going on. First, AbsoluteValueLessThan isn’t calling process_lhs(). Instead it skips the transformation of the lhs done by AbsoluteValue and uses the original lhs. That is, we want to get "experiments"."change" not ABS("experiments"."change"). Referring directly to self.lhs.lhs is safe as AbsoluteValueLessThan can be accessed only from the AbsoluteValue lookup, that is the lhs is always an instance of AbsoluteValue.

Notice also that as both sides are used multiple times in the query the params need to contain lhs_params and rhs_params multiple times.

The final query does the inversion (27 to -27) directly in the database. The reason for doing this is that if the self.rhs is something else than a plain integer value (for example an F() reference) we can’t do the transformations in Python.

In fact, most lookups with __abs could be implemented as range queries like this, and on most database backends it is likely to be more sensible to do so as you can make use of the indexes. However with PostgreSQL you may want to add an index on abs(change) which would allow these queries to be very efficient.

The AbsoluteValue example we discussed previously is a transformation which applies to the left-hand side of the lookup. There may be some cases where you want the transformation to be applied to both the left-hand side and the right-hand side. For instance, if you want to filter a queryset based on the equality of the left and right-hand side insensitively to some SQL function.

Let’s examine case-insensitive transformations here. This transformation isn’t very useful in practice as Django already comes with a bunch of built-in case-insensitive lookups, but it will be a nice demonstration of bilateral transformations in a database-agnostic way.

We define an UpperCase transformer which uses the SQL function UPPER() to transform the values before comparison. We define bilateral = True to indicate that this transformation should apply to both lhs and rhs:

Next, let’s register it:

Now, the queryset Author.objects.filter(name__upper="doe") will generate a case insensitive query like this:

Sometimes different database vendors require different SQL for the same operation. For this example we will rewrite a custom implementation for MySQL for the NotEqual operator. Instead of <> we will be using != operator. (Note that in reality almost all databases support both, including all the official databases supported by Django).

We can change the behavior on a specific backend by creating a subclass of NotEqual with an as_mysql method:

We can then register it with Field. It takes the place of the original NotEqual class as it has the same lookup_name.

When compiling a query, Django first looks for as_%s % connection.vendor methods, and then falls back to as_sql. The vendor names for the in-built backends are sqlite, postgresql, oracle and mysql.

In some cases you may wish to dynamically change which Transform or Lookup is returned based on the name passed in, rather than fixing it. As an example, you could have a field which stores coordinates or an arbitrary dimension, and wish to allow a syntax like .filter(coords__x7=4) to return the objects where the 7th coordinate has value 4. In order to do this, you would override get_lookup with something like:

You would then define get_coordinate_lookup appropriately to return a Lookup subclass which handles the relevant value of dimension.

There is a similarly named method called get_transform(). get_lookup() should always return a Lookup subclass, and get_transform() a Transform subclass. It is important to remember that Transform objects can be further filtered on, and Lookup objects cannot.

When filtering, if there is only one lookup name remaining to be resolved, we will look for a Lookup. If there are multiple names, it will look for a Transform. In the situation where there is only one name and a Lookup is not found, we look for a Transform and then the exact lookup on that Transform. All call sequences always end with a Lookup. To clarify:

.filter(myfield__mylookup) will call myfield.get_lookup('mylookup').

.filter(myfield__mytransform__mylookup) will call myfield.get_transform('mytransform'), and then mytransform.get_lookup('mylookup').

.filter(myfield__mytransform) will first call myfield.get_lookup('mytransform'), which will fail, so it will fall back to calling myfield.get_transform('mytransform') and then mytransform.get_lookup('exact').

---
