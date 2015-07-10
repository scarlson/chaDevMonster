#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask.ext.script import Server, Manager, Shell, Command, Option
from flask.ext.migrate import Migrate, MigrateCommand
from cdm.views import general
from cdm import models, db
from cdm import app

migrate = Migrate(app, db)
manager = Manager(app)


def _make_context():
    return dict(app=app, db=db, models=models)

manager.add_command("shell", Shell(make_context=_make_context, use_ipython=True))
manager.add_command('db', MigrateCommand)


port = int(os.environ.get("PORT", 5000))
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0',
    port=port)
)

@manager.command
def submit_link():
    """Submits a link to /r/chadev from db.

    submits the oldest link in the db that hasn't been submitted
    """

    query = models.submission.Submission.query.filter_by(submitted=False).order_by(models.submission.Submission.created_on).first()

    from cdm.lib.reddit import Reddit
    if query and Reddit().submit_link(query.title, query.link):
        query.submitted = True
        db.session.add(query)
        db.session.commit()


@manager.command
def test():
    """Run the unit tests
    Ran by: python manage.py test
    """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def cov():
    import coverage
    import unittest
    """Runs the unit tests with coverage.
    Ran by: python maange.py cov
    """
    cov = coverage.coverage(
        branch=True,
        include='app/*'
    )
    cov.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print 'Coverage Summary:'
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'coverage')
    cov.html_report(directory=covdir)
    cov.erase()


if __name__ == "__main__":
    manager.run()