# Djangoproject - Models

**Pages:** 1

---

## FAQ: Databases and models | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/faq/models/

**Contents:**
- FAQ: Databases and models¶
- How can I see the raw SQL queries Django is running?¶
- Can I use Django with a preexisting database?¶
- If I make changes to a model, how do I update the database?¶
- Do Django models support multiple-column primary keys?¶
- Does Django support NoSQL databases?¶
- How do I add database-specific options to my CREATE TABLE statements, such as specifying MyISAM as the table type?¶

Make sure your Django DEBUG setting is set to True. Then do this:

connection.queries is only available if DEBUG is True. It’s a list of dictionaries in order of query execution. Each dictionary has the following:

sql - The raw SQL statement

time - How long the statement took to execute, in seconds.

connection.queries includes all SQL statements – INSERTs, UPDATES, SELECTs, etc. Each time your app hits the database, the query will be recorded.

If you are using multiple databases, you can use the same interface on each member of the connections dictionary:

If you need to clear the query list manually at any point in your functions, call reset_queries(), like this:

Yes. See Integrating with a legacy database.

Take a look at Django’s support for schema migrations.

If you don’t mind clearing data, your project’s manage.py utility has a flush option to reset the database to the state it was in immediately after migrate was executed.

No. Only single-column primary keys are supported.

But this isn’t an issue in practice, because there’s nothing stopping you from adding other constraints (using the unique_together model option or creating the constraint directly in your database), and enforcing the uniqueness at that level. Single-column primary keys are needed for things such as the admin interface to work; e.g., you need a single value to specify an object to edit or delete.

NoSQL databases are not officially supported by Django itself. There are, however, a number of side projects and forks which allow NoSQL functionality in Django.

You can take a look on the wiki page which discusses some projects.

We try to avoid adding special cases in the Django code to accommodate all the database-specific options such as table type, etc. If you’d like to use any of these options, create a migration with a RunSQL operation that contains ALTER TABLE statements that do what you want to do.

For example, if you’re using MySQL and want your tables to use the MyISAM table type, use the following SQL:

---
