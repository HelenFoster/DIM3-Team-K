DIM3 Team K - PlayMaker
====

Setup
----

1.  Install the requirements listed in Documents/requirements.txt

2.  To create the database, run

        python manage.py syncdb

    and you can say "no" to the superuser, because the population script will create one.

3.  To populate the database, run:

        python populate_playmaker.py

4.  To start the server, run:

        python manage.py runserver

After changing the models, delete playmaker_project/playmaker_db.sqlite3 and start from step 2.

If changing the data in the population script, it suffices to rerun step 3,
because the population script deletes the rows before refilling them.

Notes
----

SQLite administration on Windows: http://sqliteadmin.orbmu2k.de/

