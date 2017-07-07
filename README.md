DIM3 Team K - PlayMaker
====

PlayMaker is an online platform where users who are looking for a sports partner can post announcements and offer to take part in games that require two players.

This was an exercise to design and build a Django web application as a team.

See the file Documents/Team-K-PlayMaker_updated.ppt for details.

Setup
----

1.  Install the requirements listed in Documents/requirements.txt

    The following commands should be executed from the playmaker_project subfolder (the outer one).

2.  To create the database, run

        python manage.py syncdb

    and you can say "no" to the superuser, because the population script will create one.

3.  To populate the database, run:

        python populate_playmaker.py

4.  To start the server, run:

        python manage.py runserver

After changing the models, delete playmaker_db.sqlite3 and start from step 2.

If changing the data in the population script, it suffices to rerun step 3,
because the population script deletes the rows before refilling them.

Accounts
----

Superuser: "admin"

Regular users: "vlad", "tomasz", "helen", "leif"...

Passwords are currently the same as the usernames.

External libraries and frameworks
----
- jQuery
- jQuery UI
- Bootstrap
- mmenu (http://mmenu.frebsite.nl/)

