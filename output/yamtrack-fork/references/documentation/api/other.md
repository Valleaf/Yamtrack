# Djangoproject - Other

**Pages:** 14

---

## Design philosophies | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/misc/design-philosophies/

**Contents:**
- Design philosophies¶
- Overall¶
  - Loose coupling¶
  - Less code¶
  - Quick development¶
  - Don’t repeat yourself (DRY)¶
  - Explicit is better than implicit¶
  - Consistency¶
- Models¶
  - Explicit is better than implicit¶

This document explains some of the fundamental philosophies Django’s developers have used in creating the framework. Its goal is to explain the past and guide the future.

A fundamental goal of Django’s stack is loose coupling and tight cohesion. The various layers of the framework shouldn’t “know” about each other unless absolutely necessary.

For example, the template system knows nothing about web requests, the database layer knows nothing about data display and the view system doesn’t care which template system a programmer uses.

Although Django comes with a full stack for convenience, the pieces of the stack are independent of another wherever possible.

Django apps should use as little code as possible; they should lack boilerplate. Django should take full advantage of Python’s dynamic capabilities, such as introspection.

The point of a web framework in the 21st century is to make the tedious aspects of web development fast. Django should allow for incredibly quick web development.

Every distinct concept and/or piece of data should live in one, and only one, place. Redundancy is bad. Normalization is good.

The framework, within reason, should deduce as much as possible from as little as possible.

The discussion of DRY on the Portland Pattern Repository

This is a core Python principle listed in PEP 20, and it means Django shouldn’t do too much “magic.” Magic shouldn’t happen unless there’s a really good reason for it. Magic is worth using only if it creates a huge convenience unattainable in other ways, and it isn’t implemented in a way that confuses developers who are trying to learn how to use the feature.

The framework should be consistent at all levels. Consistency applies to everything from low-level (the Python coding style used) to high-level (the “experience” of using Django).

Fields shouldn’t assume certain behaviors based solely on the name of the field. This requires too much knowledge of the system and is prone to errors. Instead, behaviors should be based on keyword arguments and, in some cases, on the type of the field.

Models should encapsulate every aspect of an “object,” following Martin Fowler’s Active Record design pattern.

This is why both the data represented by a model and information about it (its human-readable name, options like default ordering, etc.) are defined in the model class; all the information needed to understand a given model should be stored in the model.

The core goals of the database API are:

It should execute SQL statements as few times as possible, and it should optimize statements internally.

This is why developers need to call save() explicitly, rather than the framework saving things behind the scenes silently.

This is also why the select_related() QuerySet method exists. It’s an optional performance booster for the common case of selecting “every related object.”

The database API should allow rich, expressive statements in as little syntax as possible. It should not rely on importing other modules or helper objects.

Joins should be performed automatically, behind the scenes, when necessary.

Every object should be able to access every related object, systemwide. This access should work both ways.

The database API should realize it’s a shortcut but not necessarily an end-all-be-all. The framework should make it easy to write custom SQL – entire statements, or just custom WHERE clauses as custom parameters to API calls.

URLs in a Django app should not be coupled to the underlying Python code. Tying URLs to Python function names is a Bad And Ugly Thing.

Along these lines, the Django URL system should allow URLs for the same app to be different in different contexts. For example, one site may put stories at /stories/, while another may use /news/.

URLs should be as flexible as possible. Any conceivable URL design should be allowed.

The framework should make it just as easy (or even easier) for a developer to design pretty URLs than ugly ones.

File extensions in web-page URLs should be avoided.

Vignette-style commas in URLs deserve severe punishment.

Technically, foo.com/bar and foo.com/bar/ are two different URLs, and search-engine robots (and some web traffic-analyzing tools) would treat them as separate pages. Django should make an effort to “normalize” URLs so that search-engine robots don’t get confused.

This is the reasoning behind the APPEND_SLASH setting.

We see a template system as a tool that controls presentation and presentation-related logic – and that’s it. The template system shouldn’t support functionality that goes beyond this basic goal.

The majority of dynamic websites use some sort of common sitewide design – a common header, footer, navigation bar, etc. The Django template system should make it easy to store those elements in a single place, eliminating duplicate code.

This is the philosophy behind template inheritance.

The template system shouldn’t be designed so that it only outputs HTML. It should be equally good at generating other text-based formats, or just plain text.

Using an XML engine to parse templates introduces a whole new world of human error in editing templates – and incurs an unacceptable level of overhead in template processing.

The template system shouldn’t be designed so that templates necessarily are displayed nicely in WYSIWYG editors such as Dreamweaver. That is too severe of a limitation and wouldn’t allow the syntax to be as nice as it is. Django expects template authors are comfortable editing HTML directly.

The template system shouldn’t do magic things with whitespace. If a template includes whitespace, the system should treat the whitespace as it treats text – just display it. Any whitespace that’s not in a template tag should be displayed.

The goal is not to invent a programming language. The goal is to offer just enough programming-esque functionality, such as branching and looping, that is essential for making presentation-related decisions. The Django Template Language (DTL) aims to avoid advanced logic.

The template system, out of the box, should forbid the inclusion of malicious code – such as commands that delete database records.

This is another reason the template system doesn’t allow arbitrary Python code.

The template system should recognize that advanced template authors may want to extend its technology.

This is the philosophy behind custom template tags and filters.

Writing a view should be as simple as writing a Python function. Developers shouldn’t have to instantiate a class when a function will do.

Views should have access to a request object – an object that stores metadata about the current request. The object should be passed directly to a view function, rather than the view function having to access the request data from a global variable. This makes it light, clean and easy to test views by passing in “fake” request objects.

A view shouldn’t care about which template system the developer uses – or even whether a template system is used at all.

GET and POST are distinct; developers should explicitly use one or the other. The framework should make it easy to distinguish between GET and POST data.

The core goals of Django’s cache framework are:

A cache should be as fast as possible. Hence, all framework code surrounding the cache backend should be kept to the absolute minimum, especially for get() operations.

The cache API should provide a consistent interface across the different cache backends.

The cache API should be extensible at the application level based on the developer’s needs (for example, see Cache key transformation).

---

## Django at a glance | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/intro/overview/

**Contents:**
- Django at a glance¶
- Design your model¶
- Install it¶
- Enjoy the free API¶
- A dynamic admin interface: it’s not just scaffolding – it’s the whole house¶
- Design your URLs¶
- Write your views¶
- Design your templates¶
- This is just the surface¶

Because Django was developed in a fast-paced newsroom environment, it was designed to make common web development tasks fast and easy. Here’s an informal overview of how to write a database-driven web app with Django.

The goal of this document is to give you enough technical specifics to understand how Django works, but this isn’t intended to be a tutorial or reference – but we’ve got both! When you’re ready to start a project, you can start with the tutorial or dive right into more detailed documentation.

Although you can use Django without a database, it comes with an object-relational mapper in which you describe your database layout in Python code.

The data-model syntax offers many rich ways of representing your models – so far, it’s been solving many years’ worth of database-schema problems. Here’s a quick example:

Next, run the Django command-line utilities to create the database tables automatically:

The makemigrations command looks at all your available models and creates migrations for whichever tables don’t already exist. migrate runs the migrations and creates tables in your database, as well as optionally providing much richer schema control.

With that, you’ve got a free, and rich, Python API to access your data. The API is created on the fly, no code generation necessary:

Once your models are defined, Django can automatically create a professional, production ready administrative interface – a website that lets authenticated users add, change and delete objects. The only step required is to register your model in the admin site:

The philosophy here is that your site is edited by a staff, or a client, or maybe just you – and you don’t want to have to deal with creating backend interfaces only to manage content.

One typical workflow in creating Django apps is to create models and get the admin sites up and running as fast as possible, so your staff (or clients) can start populating data. Then, develop the way data is presented to the public.

A clean, elegant URL scheme is an important detail in a high-quality web application. Django encourages beautiful URL design and doesn’t put any cruft in URLs, like .php or .asp.

To design URLs for an app, you create a Python module called a URLconf. A table of contents for your app, it contains a mapping between URL patterns and Python callback functions. URLconfs also serve to decouple URLs from Python code.

Here’s what a URLconf might look like for the Reporter/Article example above:

The code above maps URL paths to Python callback functions (“views”). The path strings use parameter tags to “capture” values from the URLs. When a user requests a page, Django runs through each path, in order, and stops at the first one that matches the requested URL. (If none of them matches, Django calls a special-case 404 view.) This is blazingly fast, because the paths are compiled into regular expressions at load time.

Once one of the URL patterns matches, Django calls the given view, which is a Python function. Each view gets passed a request object – which contains request metadata – and the values captured in the pattern.

For example, if a user requested the URL “/articles/2005/05/39323/”, Django would call the function news.views.article_detail(request, year=2005, month=5, pk=39323).

Each view is responsible for doing one of two things: Returning an HttpResponse object containing the content for the requested page, or raising an exception such as Http404. The rest is up to you.

Generally, a view retrieves data according to the parameters, loads a template and renders the template with the retrieved data. Here’s an example view for year_archive from above:

This example uses Django’s template system, which has several powerful features but strives to stay simple enough for non-programmers to use.

The code above loads the news/year_archive.html template.

Django has a template search path, which allows you to minimize redundancy among templates. In your Django settings, you specify a list of directories to check for templates with DIRS. If a template doesn’t exist in the first directory, it checks the second, and so on.

Let’s say the news/year_archive.html template was found. Here’s what that might look like:

Variables are surrounded by double-curly braces. {{ article.headline }} means “Output the value of the article’s headline attribute.” But dots aren’t used only for attribute lookup. They also can do dictionary-key lookup, index lookup and function calls.

Note {{ article.pub_date|date:"F j, Y" }} uses a Unix-style “pipe” (the “|” character). This is called a template filter, and it’s a way to filter the value of a variable. In this case, the date filter formats a Python datetime object in the given format (as found in PHP’s date function).

You can chain together as many filters as you’d like. You can write custom template filters. You can write custom template tags, which run custom Python code behind the scenes.

Finally, Django uses the concept of “template inheritance”. That’s what the {% extends "base.html" %} does. It means “First load the template called ‘base’, which has defined a bunch of blocks, and fill the blocks with the following blocks.” In short, that lets you dramatically cut down on redundancy in templates: each template has to define only what’s unique to that template.

Here’s what the “base.html” template, including the use of static files, might look like:

Simplistically, it defines the look-and-feel of the site (with the site’s logo), and provides “holes” for child templates to fill. This means that a site redesign can be done by changing a single file – the base template.

It also lets you create multiple versions of a site, with different base templates, while reusing child templates. Django’s creators have used this technique to create strikingly different mobile versions of sites by only creating a new base template.

Note that you don’t have to use Django’s template system if you prefer another system. While Django’s template system is particularly well-integrated with Django’s model layer, nothing forces you to use it. For that matter, you don’t have to use Django’s database API, either. You can use another database abstraction layer, you can read XML files, you can read files off disk, or anything you want. Each piece of Django – models, views, templates – is decoupled from the next.

This has been only a quick overview of Django’s functionality. Some more useful features:

A caching framework that integrates with memcached or other backends.

A syndication framework that lets you create RSS and Atom feeds by writing a small Python class.

More attractive automatically-generated admin features – this overview barely scratched the surface.

The next steps are for you to download Django, read the tutorial and join the community. Thanks for your interest!

---

## Django documentation | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/

**Contents:**
- Django documentation¶
- First steps¶
- Getting help¶
- How the documentation is organized¶
- The model layer¶
- The view layer¶
- The template layer¶
- Forms¶
- The development process¶
- The admin¶

Everything you need to know about Django.

Are you new to Django or to programming? This is the place to start!

From scratch: Overview | Installation

Tutorial: Part 1: Requests and responses | Part 2: Models and the admin site | Part 3: Views and templates | Part 4: Forms and generic views | Part 5: Testing | Part 6: Static files | Part 7: Customizing the admin site | Part 8: Adding third-party packages

Advanced Tutorials: How to write reusable apps | Writing your first contribution to Django

Having trouble? We’d like to help!

Try the FAQ – it’s got answers to many common questions.

Looking for specific information? Try the Index, Module Index or the detailed table of contents.

Not found anything? See FAQ: Getting Help for information on getting support and asking questions to the community.

Report bugs with Django in our ticket tracker.

Django has a lot of documentation. A high-level overview of how it’s organized will help you know where to look for certain things:

Tutorials take you by the hand through a series of steps to create a web application. Start here if you’re new to Django or web application development. Also look at the “First steps”.

Topic guides discuss key topics and concepts at a fairly high level and provide useful background information and explanation.

Reference guides contain technical reference for APIs and other aspects of Django’s machinery. They describe how it works and how to use it but assume that you have a basic understanding of key concepts.

How-to guides are recipes. They guide you through the steps involved in addressing key problems and use-cases. They are more advanced than tutorials and assume some knowledge of how Django works.

Django provides an abstraction layer (the “models”) for structuring and manipulating the data of your web application. Learn more about it below:

Models: Introduction to models | Field types | Indexes | Meta options | Model class

QuerySets: Making queries | QuerySet method reference | Lookup expressions

Model instances: Instance methods | Accessing related objects

Migrations: Introduction to Migrations | Operations reference | SchemaEditor | Writing migrations

Advanced: Managers | Raw SQL | Transactions | Aggregation | Search | Custom fields | Multiple databases | Custom lookups | Query Expressions | Conditional Expressions | Database Functions

Other: Supported databases | Legacy databases | Providing initial data | Optimize database access | PostgreSQL specific features

Django has the concept of “views” to encapsulate the logic responsible for processing a user’s request and for returning the response. Find all you need to know about views via the links below:

The basics: URLconfs | View functions | Shortcuts | Decorators | Asynchronous Support

Reference: Built-in Views | Request/response objects | TemplateResponse objects

File uploads: Overview | File objects | Storage API | Managing files | Custom storage

Class-based views: Overview | Built-in display views | Built-in editing views | Using mixins | API reference | Flattened index

Advanced: Generating CSV | Generating PDF

Middleware: Overview | Built-in middleware classes

The template layer provides a designer-friendly syntax for rendering the information to be presented to the user. Learn how this syntax can be used by designers and how it can be extended by programmers:

For designers: Language overview | Built-in tags and filters | Humanization

For programmers: Template API | Custom tags and filters | Custom template backend

Django provides a rich framework to facilitate the creation of forms and the manipulation of form data.

The basics: Overview | Form API | Built-in fields | Built-in widgets

Advanced: Forms for models | Integrating media | Formsets | Customizing validation

Learn about the various components and tools to help you in the development and testing of Django applications:

Settings: Overview | Full list of settings

Applications: Overview

django-admin and manage.py: Overview | Adding custom commands

Testing: Introduction | Writing and running tests | Included testing tools | Advanced topics

Deployment: Overview | WSGI servers | ASGI servers | Deploying static files | Tracking code errors by email | Deployment checklist

Find all you need to know about the automated admin interface, one of Django’s most popular features:

Admin documentation generator

Security is a topic of paramount importance in the development of web applications and Django provides multiple protection tools and mechanisms:

Disclosed security issues in Django

Clickjacking protection

Cross Site Request Forgery protection

Cryptographic signing

Content Security Policy

Django offers a robust internationalization and localization framework to assist you in the development of applications for multiple languages and world regions:

Overview | Internationalization | Localization | Localized web UI formatting and form input

There are a variety of techniques and tools that can help get your code running more efficiently - faster, and using fewer system resources.

Performance and optimization overview

GeoDjango intends to be a world-class geographic web framework. Its goal is to make it as easy as possible to build GIS web applications and harness the power of spatially enabled data.

Django offers multiple tools commonly needed in the development of web applications:

Authentication: Overview | Using the authentication system | Password management | Customizing authentication | API Reference

Syndication feeds (RSS/Atom)

Static files management

Learn about some other core functionalities of the Django framework:

Conditional content processing

Content types and generic relations

System check framework

Learn about the development process for the Django project itself and about how you can contribute:

Community: Contributing to Django | The release process | Team organization | The Django source code repository | Security policies | Mailing lists and Forum

Design philosophies: Overview

Documentation: About this documentation

Third-party distributions: Overview

Django over time: API stability | Release notes and upgrading instructions | Deprecation Timeline

---

## FAQ: General | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/faq/general/

**Contents:**
- FAQ: General¶
- Why does this project exist?¶
- What does “Django” mean, and how do you pronounce it?¶
- Is Django stable?¶
- Does Django scale?¶
- Who’s behind this?¶
- How is Django licensed?¶
- Why does Django include Python’s license file?¶
- Which sites use Django?¶
- Django appears to be a MVC framework, but you call the Controller the “view”, and the View the “template”. How come you don’t use the standard names?¶

Django grew from a very practical need: World Online, a newspaper web operation, is responsible for building intensive web applications on journalism deadlines. In the fast-paced newsroom, World Online often has only a matter of hours to take a complicated web application from concept to public launch.

At the same time, the World Online web developers have consistently been perfectionists when it comes to following best practices of web development.

In fall 2003, the World Online developers (Adrian Holovaty and Simon Willison) ditched PHP and began using Python to develop its websites. As they built intensive, richly interactive sites such as Lawrence.com, they began to extract a generic web development framework that let them build web applications more and more quickly. They tweaked this framework constantly, adding improvements over two years.

In summer 2005, World Online decided to open-source the resulting software, Django. Django would not be possible without a whole host of open-source projects – Apache, Python, and PostgreSQL to name a few – and we’re thrilled to be able to give something back to the open-source community.

Django is named after Django Reinhardt, a jazz manouche guitarist from the 1930s to early 1950s. To this day, he’s considered one of the best guitarists of all time.

Listen to his music. You’ll like it.

Django is pronounced JANG-oh. Rhymes with FANG-oh. The “D” is silent.

We’ve also recorded an audio clip of the pronunciation.

Yes, it’s quite stable. Companies like Disqus, Instagram, Pinterest, and Mozilla have been using Django for many years. Sites built on Django have weathered traffic spikes of over 50 thousand hits per second.

Yes. Compared to development time, hardware is cheap, and so Django is designed to take advantage of as much hardware as you can throw at it.

Django uses a “shared-nothing” architecture, which means you can add hardware at any level – database servers, caching servers or web/application servers.

The framework cleanly separates components such as its database layer and application layer. And it ships with a simple-yet-powerful cache framework.

Django was originally developed at World Online, the web department of a newspaper in Lawrence, Kansas, USA. Django’s now run by an international team of volunteers.

Django is distributed under the 3-clause BSD license. This is an open source license granting broad permissions to modify and redistribute Django.

Django includes code from the Python standard library. Python is distributed under a permissive open source license. A copy of the Python license is included with Django for compliance with Python’s terms.

BuiltWithDjango.com features a constantly growing list of Django-powered sites.

Well, the standard names are debatable.

In our interpretation of MVC, the “view” describes the data that gets presented to the user. It’s not necessarily how the data looks, but which data is presented. The view describes which data you see, not how you see it. It’s a subtle distinction.

So, in our case, a “view” is the Python callback function for a particular URL, because that callback function describes which data is presented.

Furthermore, it’s sensible to separate content from presentation – which is where templates come in. In Django, a “view” describes which data is presented, but a view normally delegates to a template, which describes how the data is presented.

Where does the “controller” fit in, then? In Django’s case, it’s probably the framework itself: the machinery that sends a request to the appropriate view, according to the Django URL configuration.

If you’re hungry for acronyms, you might say that Django is a “MTV” framework – that is, “model”, “template”, and “view.” That breakdown makes much more sense.

At the end of the day, it comes down to getting stuff done. And, regardless of how things are named, Django gets stuff done in a way that’s most logical to us.

We’re well aware that there are other awesome web frameworks out there, and we’re not averse to borrowing ideas where appropriate. However, Django was developed precisely because we were unhappy with the status quo, so please be aware that “because <Framework X> does it” is not going to be sufficient reason to add a given feature to Django.

When Django was originally written, Adrian and Simon spent quite a bit of time exploring the various Python web frameworks available.

In our opinion, none of them were completely up to snuff.

We’re picky. You might even call us perfectionists. (With deadlines.)

Over time, we stumbled across open-source libraries that did things we’d already implemented. It was reassuring to see other people solving similar problems in similar ways, but it was too late to integrate outside code: We’d already written, tested and implemented our own framework bits in several production settings – and our own code met our needs delightfully.

In most cases, however, we found that existing frameworks/tools inevitably had some sort of fundamental, fatal flaw that made us squeamish. No tool fit our philosophies 100%.

Like we said: We’re picky.

We’ve documented our philosophies on the design philosophies page.

No, Django is not a CMS, or any sort of “turnkey product” in and of itself. It’s a web framework; it’s a programming tool that lets you build websites.

For example, it doesn’t make much sense to compare Django to something like Drupal, because Django is something you use to create things like Drupal.

Yes, Django’s automatic admin site is fantastic and timesaving – but the admin site is one module of Django the framework. Furthermore, although Django has special conveniences for building “CMS-y” apps, that doesn’t mean it’s not just as appropriate for building “non-CMS-y” apps (whatever that means!).

The Django docs are available in the docs directory of each Django tarball release. These docs are in reST (reStructuredText) format, and each text file corresponds to a web page on the official Django site.

Because the documentation is stored in revision control, you can browse documentation changes just like you can browse code changes.

Technically, the docs on Django’s site are generated from the latest development versions of those reST documents, so the docs on the Django site may offer more information than the docs that come with the latest Django release.

It’s difficult to give an official citation format, for two reasons: citation formats can vary wildly between publications, and citation standards for software are still a matter of some debate.

For example, APA style, would dictate something like:

However, the only true guide is what your publisher will accept, so get a copy of those guidelines and fill in the gaps as best you can.

If your referencing style guide requires a publisher name, use “Django Software Foundation”.

If you need a publishing location, use “Lawrence, Kansas”.

If you need a web address, use https://www.djangoproject.com/.

If you need a name, just use “Django”, without any tagline.

If you need a publication date, use the year of release of the version you’re referencing (e.g., 2013 for v1.5)

The Steering Council maintains a collection of Django third-party packages, organizations and resources at https://www.djangoproject.com/community/ecosystem/.

That page will be updated to contain links to various Django content such as podcasts, videos, conferences, blogs, books, and learning resources. It also features popular, robust, community-maintained packages.

---

## FAQ: Getting Help | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/faq/help/

**Contents:**
- FAQ: Getting Help¶
- How do I do X? Why doesn’t Y work? Where can I go to get help?¶
- Nobody answered my question! What should I do?¶
- I think I’ve found a bug! What should I do?¶
- I think I’ve found a security problem! What should I do?¶

First, please check if your question is answered on the FAQ. Also, search for answers using your favorite search engine, and in the forum.

If you can’t find an answer, please take a few minutes to formulate your question well. Explaining the problems you are facing clearly will help others help you. See the StackOverflow guide on asking good questions.

Then, please post it in one of the following channels:

The Django Forum section “Using Django”. This is for web-based discussions.

The Django Discord server for chat-based discussions.

In all these channels please abide by the Django Code of Conduct. In summary, being friendly and patient, considerate, respectful, and careful in your choice of words.

Try making your question more specific, or provide a better example of your problem.

As with most open-source projects, the folks on these channels are volunteers. If nobody has answered your question, it may be because nobody knows the answer, it may be because nobody can understand the question, or it may be that everybody that can help is busy.

You can also try asking on a different channel. But please don’t post your question in all three channels in quick succession.

Detailed instructions on how to handle a potential bug can be found in our Guide to contributing to Django.

If you think you’ve found a security problem with Django, please send a message to security@djangoproject.com. This is a private list only open to long-time, highly trusted Django developers, and its archives are not publicly readable.

Due to the sensitive nature of security issues, we ask that if you think you have found a security problem, please don’t post a message on the forum, the Discord server, IRC, or one of the public mailing lists. Django has a policy for handling security issues; while a defect is outstanding, we would like to minimize any damage that could be inflicted through public knowledge of that defect.

---

## FAQ: The admin | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/faq/admin/

**Contents:**
- FAQ: The admin¶
- I can’t log in. When I enter a valid username and password, it just brings up the login page again, with no error messages.¶
- I can’t log in. When I enter a valid username and password, it brings up the login page again, with a “Please enter a correct username and password” error.¶
- How do I automatically set a field’s value to the user who last edited the object in the admin?¶
- How do I limit admin access so that objects can only be edited by the users who created them?¶
- My admin-site CSS and images showed up fine using the development server, but they’re not displaying when using mod_wsgi.¶
- My “list_filter” contains a ManyToManyField, but the filter doesn’t display.¶
- Some objects aren’t appearing in the admin.¶
- How can I customize the functionality of the admin interface?¶
- The dynamically-generated admin site is ugly! How can I change it?¶

The login cookie isn’t being set correctly, because the domain of the cookie sent out by Django doesn’t match the domain in your browser. Try setting the SESSION_COOKIE_DOMAIN setting to match your domain. For example, if you’re going to “https://www.example.com/admin/” in your browser, set SESSION_COOKIE_DOMAIN = 'www.example.com'.

If you’re sure your username and password are correct, make sure your user account has is_active and is_staff set to True. The admin site only allows access to users with those two fields both set to True.

The ModelAdmin class provides customization hooks that allow you to transform an object as it saved, using details from the request. By extracting the current user from the request, and customizing the save_model() hook, you can update an object to reflect the user that edited it. See the documentation on ModelAdmin methods for an example.

The ModelAdmin class also provides customization hooks that allow you to control the visibility and editability of objects in the admin. Using the same trick of extracting the user from the request, the get_queryset() and has_change_permission() can be used to control the visibility and editability of objects in the admin.

See serving the admin files in the “How to use Django with mod_wsgi” documentation.

Django won’t bother displaying the filter for a ManyToManyField if there are no related objects.

For example, if your list_filter includes sites, and there are no sites in your database, it won’t display a “Site” filter. In that case, filtering by site would be meaningless.

Inconsistent row counts may be caused by missing foreign key values or a foreign key field incorrectly set to null=False. If you have a record with a ForeignKey pointing to a nonexistent object and that foreign key is included is list_display, the record will not be shown in the admin changelist because the Django model is declaring an integrity constraint that is not implemented at the database level.

You’ve got several options. If you want to piggyback on top of an add/change form that Django automatically generates, you can attach arbitrary JavaScript modules to the page via the model’s class Admin js parameter. That parameter is a list of URLs, as strings, pointing to JavaScript modules that will be included within the admin form via a <script> tag.

If you want more flexibility than is feasible by tweaking the auto-generated forms, feel free to write custom views for the admin. The admin is powered by Django itself, and you can write custom views that hook into the authentication system, check permissions and do whatever else they need to do.

If you want to customize the look-and-feel of the admin interface, read the next question.

We like it, but if you don’t agree, you can modify the admin site’s presentation by editing the CSS stylesheet and/or associated image files. The site is built using semantic HTML and plenty of CSS hooks, so any changes you’d like to make should be possible by editing the stylesheet.

The admin provides a fully-functional experience to the recent versions of modern, web standards compliant browsers. On desktop this means Chrome, Edge, Firefox, Opera, Safari, and others.

On mobile and tablet devices, the admin provides a responsive experience for web standards compliant browsers. This includes the major browsers on both Android and iOS.

Depending on feature support, there may be minor stylistic differences between browsers. These are considered acceptable variations in rendering.

The admin is intended to be compatible with a wide range of assistive technologies, but there are currently many blockers. The support target is all latest versions of major assistive technologies, including Dragon, JAWS, NVDA, Orca, TalkBack, Voice Control, VoiceOver iOS, VoiceOver macOS, Windows Contrast Themes, ZoomText, and screen magnifiers.

---

## FAQ: Using Django | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/faq/usage/

**Contents:**
- FAQ: Using Django¶
- Why do I get an error about importing DJANGO_SETTINGS_MODULE?¶
- I can’t stand your template language. Do I have to use it?¶
- Do I have to use your model/database layer?¶
- How do I use image and file fields?¶
- How do I make a variable available to all my templates?¶

The environment variable DJANGO_SETTINGS_MODULE is set to a fully-qualified Python module (i.e. mysite.settings).

Said module is on sys.path (import mysite.settings should work).

The module doesn’t contain syntax errors.

We happen to think our template engine is the best thing since chunky bacon, but we recognize that choosing a template language runs close to religion. There’s nothing about Django that requires using the template language, so if you’re attached to Jinja2, Mako, or whatever, feel free to use those.

Nope. Just like the template system, the model/database layer is decoupled from the rest of the framework.

The one exception is: If you use a different database library, you won’t get to use Django’s automatically-generated admin site. That app is coupled to the Django database layer.

Using a FileField or an ImageField in a model takes a few steps:

In your settings file, you’ll need to define MEDIA_ROOT as the full path to a directory where you’d like Django to store uploaded files. (For performance, these files are not stored in the database.) Define MEDIA_URL as the base public URL of that directory. Make sure that this directory is writable by the web server’s user account.

Add the FileField or ImageField to your model, defining the upload_to option to specify a subdirectory of MEDIA_ROOT to use for uploaded files.

All that will be stored in your database is a path to the file (relative to MEDIA_ROOT). You’ll most likely want to use the convenience url attribute provided by Django. For example, if your ImageField is called mug_shot, you can get the absolute path to your image in a template with {{ object.mug_shot.url }}.

Sometimes your templates all need the same thing. A common example would be dynamically generated menus. At first glance, it seems logical to add a common dictionary to the template context.

The best way to do this in Django is to use a RequestContext. Details on how to do this are here: Using RequestContext.

---

## General Index | Django Documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/genindex/

**Contents:**
- General Index
- Symbols
- _
- A
- B
- C
- D
- E
- F
- G

Symbols | _ | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z

---

## Getting started | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/intro/

**Contents:**
- Getting started¶

New to Django? Or to web development in general? Well, you came to the right place: read this material to quickly get up and running.

If you’re new to Python, you might want to start by getting an idea of what the language is like. Django is 100% Python, so if you’ve got minimal comfort with Python you’ll probably get a lot more out of Django.

If you’re new to programming entirely, you might want to start with this list of Python resources for non-programmers

If you already know a few other languages and want to get up to speed with Python quickly, we recommend referring the official Python documentation, which provides comprehensive and authoritative information about the language, as well as links to other resources such as a list of books about Python.

---

## Glossary | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/glossary/

**Contents:**
- Glossary¶

A non-abstract (abstract=False) model.

An attribute on a model; a given field usually maps directly to a single database column.

A higher-order view function that provides an abstract/generic implementation of a common idiom or pattern found in view development.

See Class-based views.

Models store your application’s data.

“Model-template-view”; a software pattern, similar in style to MVC, but a better description of the way Django does things.

Model-view-controller; a software pattern. Django follows MVC to some extent.

A Python package – i.e. a directory of code – that contains all the settings for an instance of Django. This would include database configuration, Django-specific options and application-specific settings.

Also known as “managed attributes”, and a feature of Python since version 2.2. This is a neat way to implement attributes whose usage resembles attribute access, but whose implementation uses method calls.

An object representing some set of rows to be fetched from the database.

A short label for something, containing only letters, numbers, underscores or hyphens. They’re generally used in URLs. For example, in a typical blog entry URL:

the last bit (spring) is the slug.

A chunk of text that acts as formatting for representing data. A template helps to abstract the presentation of data from the data itself.

A function responsible for rendering a page.

---

## Meta-documentation and miscellany | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/misc/

**Contents:**
- Meta-documentation and miscellany¶

Documentation that we can’t find a more organized place for. Like that drawer in your kitchen with the scissors, batteries, duct tape, and other junk.

---

## Third-party distributions of Django | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/misc/distributions/

**Contents:**
- Third-party distributions of Django¶
- For distributors¶

Many third-party distributors are now providing versions of Django integrated with their package-management systems. These can make installation and upgrading much easier for users of Django since the integration includes the ability to automatically install dependencies (like database adapters) that Django requires.

Typically, these packages are based on the latest stable release of Django, so if you want to use the development version of Django you’ll need to follow the instructions for installing the development version from our Git repository.

If you’re using Linux or a Unix installation, such as OpenSolaris, check with your distributor to see if they already package Django. If you’re using a Linux distro and don’t know how to find out if a package is available, then now is a good time to learn. The Django Wiki contains a list of Third Party Distributions to help you out.

If you’d like to package Django for distribution, we’d be happy to help out! Please introduce yourself on the Django Forum.

We also encourage all distributors to subscribe to the django-announce mailing list, which is a (very) low-traffic list for announcing new releases of Django and important bugfixes.

---

## Troubleshooting | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/faq/troubleshooting/

**Contents:**
- Troubleshooting¶
- Problems running django-admin¶
  - command not found: django-admin¶
  - macOS permissions¶
- Miscellaneous¶
  - I’m getting a UnicodeDecodeError. What am I doing wrong?¶

This page contains some advice about errors and problems commonly encountered during the development of Django applications.

django-admin should be on your system path if you installed Django via pip. If it’s not in your path, ensure you have your virtual environment activated and you can try running the equivalent command python -m django.

If you’re using macOS, you may see the message “permission denied” when you try to run django-admin. This is because, on Unix-based systems like macOS, a file must be marked as “executable” before it can be run as a program. To do this, open Terminal.app and navigate (using the cd command) to the directory where django-admin is installed, then run the command sudo chmod +x django-admin.

This class of errors happen when a bytestring containing non-ASCII sequences is transformed into a Unicode string and the specified encoding is incorrect. The output generally looks like this:

The resolution mostly depends on the context, however here are two common pitfalls producing this error:

Your system locale may be a default ASCII locale, like the “C” locale on UNIX-like systems (can be checked by the locale command). If it’s the case, please refer to your system documentation to learn how you can change this to a UTF-8 locale.

https://wiki.python.org/moin/UnicodeDecodeError

---

## What to read next | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/intro/whatsnext/

**Contents:**
- What to read next¶
- Finding documentation¶
- How the documentation is organized¶
- How documentation is updated¶
- Where to get it¶
  - On the web¶
  - In plain text¶
  - As HTML, locally¶
- Differences between versions¶

So you’ve read all the introductory material and have decided you’d like to keep using Django. We’ve only just scratched the surface with this intro (in fact, if you’ve read every single word, you’ve read about 5% of the overall documentation).

Well, we’ve always been big fans of learning by doing. At this point you should know enough to start a project of your own and start fooling around. As you need to learn new tricks, come back to the documentation. There’s also a bigger Django ecosystem out there for you to explore that the community has created.

We’ve put a lot of effort into making Django’s documentation useful, clear and as complete as possible. The rest of this document explains more about how the documentation works so that you can get the most out of it.

(Yes, this is documentation about documentation. Rest assured we have no plans to write a document about how to read the document about documentation.)

Django’s got a lot of documentation – almost 450,000 words and counting – so finding what you need can sometimes be tricky. A good place to start is the Index. We also recommend using the builtin search feature.

Or you can just browse around!

Django’s main documentation is broken up into “chunks” designed to fill different needs:

The introductory material is designed for people new to Django – or to web development in general. It doesn’t cover anything in depth, but instead gives a high-level overview of how developing in Django “feels”.

The topic guides, on the other hand, dive deep into individual parts of Django. There are complete guides to Django’s model system, template engine, forms framework, and much more.

This is probably where you’ll want to spend most of your time; if you work your way through these guides you should come out knowing pretty much everything there is to know about Django.

Web development is often broad, not deep – problems span many domains. We’ve written a set of how-to guides that answer common “How do I …?” questions. Here you’ll find information about generating PDFs with Django, writing custom template tags, and more.

Answers to really common questions can also be found in the FAQ.

The guides and how-to’s don’t cover every single class, function, and method available in Django – that would be overwhelming when you’re trying to learn. Instead, details about individual classes, functions, methods, and modules are kept in the reference. This is where you’ll turn to find the details of a particular function or whatever you need.

If you are interested in deploying a project for public use, our docs have several guides for various deployment setups as well as a deployment checklist for some things you’ll need to think about.

Finally, there’s some “specialized” documentation not usually relevant to most developers. This includes the release notes and internals documentation for those who want to add code to Django itself, and a few other things that don’t fit elsewhere.

Just as the Django code base is developed and improved on a daily basis, our documentation is consistently improving. We improve documentation for several reasons:

To make content fixes, such as grammar/typo corrections.

To add information and/or examples to existing sections that need to be expanded.

To document Django features that aren’t yet documented. (The list of such features is shrinking but exists nonetheless.)

To add documentation for new features as new features get added, or as Django APIs or behaviors change.

Django’s documentation is kept in the same source control system as its code. It lives in the docs directory of our Git repository. Each document online is a separate text file in the repository.

You can read Django documentation in several ways. They are, in order of preference:

The most recent version of the Django documentation lives at https://docs.djangoproject.com/en/dev/. These HTML pages are generated automatically from the text files in source control. That means they reflect the “latest and greatest” in Django – they include the very latest corrections and additions, and they discuss the latest Django features, which may only be available to users of the Django development version. (See Differences between versions below.)

We encourage you to help improve the docs by submitting changes, corrections and suggestions in the ticket system. The Django developers actively monitor the ticket system and use your feedback to improve the documentation for everybody.

Note, however, that tickets should explicitly relate to the documentation, rather than asking broad tech-support questions. If you need help with your particular Django setup, try the Django Forum or the Django Discord server instead.

For offline reading, or just for convenience, you can read the Django documentation in plain text.

If you’re using an official release of Django, the zipped package (tarball) of the code includes a docs/ directory, which contains all the documentation for that release.

If you’re using the development version of Django (aka the main branch), the docs/ directory contains all of the documentation. You can update your Git checkout to get the latest changes.

One low-tech way of taking advantage of the text documentation is by using the Unix grep utility to search for a phrase in all of the documentation. For example, this will show you each mention of the phrase “max_length” in any Django document:

You can get a local copy of the HTML documentation following a few steps:

Django’s documentation uses a system called Sphinx to convert from plain text to HTML. You’ll need to install Sphinx by either downloading and installing the package from the Sphinx website, or with pip:

Then, use the included Makefile to turn the documentation into HTML:

You’ll need GNU Make installed for this.

If you’re on Windows you can alternatively use the included batch file:

The HTML documentation will be placed in docs/_build/html.

The text documentation in the main branch of the Git repository contains the “latest and greatest” changes and additions. These changes include documentation of new features targeted for Django’s next feature release. For that reason, it’s worth pointing out our policy to highlight recent changes and additions to Django.

We follow this policy:

The development documentation at https://docs.djangoproject.com/en/dev/ is from the main branch. These docs correspond to the latest feature release, plus whatever features have been added/changed in the framework since then.

As we add features to Django’s development version, we update the documentation in the same Git commit transaction.

To distinguish feature changes/additions in the docs, we use the phrase: “New in Django Development version” for the version of Django that hasn’t been released yet, or “New in version X.Y” for released versions.

Documentation fixes and improvements may be backported to the last release branch, at the discretion of the merger, however, once a version of Django is no longer supported, that version of the docs won’t get any further updates.

The main documentation web page includes links to documentation for previous versions. Be sure you are using the version of the docs corresponding to the version of Django you are using!

---
