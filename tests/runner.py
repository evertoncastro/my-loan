import os
import sys
from unittest.loader import TestLoader
from unittest import TextTestRunner
from app import app
from app import db
from models import *


def test_suite():
    with app.app_context():
        try:
            os.remove('app/test.db')
        except IOError:
            pass
        db.create_all()
        suite = TestLoader().discover(
            'tests',
            pattern='test_*.py',
            top_level_dir=os.environ['PYTHONPATH'].split(os.pathsep)[0]
        )
        return TextTestRunner(verbosity=1).run(suite)


def clear_database(_db):
    db.session.rollback()
    for table in reversed(_db.metadata.sorted_tables):
        _db.session.execute(table.delete())
    _db.session.commit()


if __name__ == '__main__':
    result = test_suite()
    if not result.wasSuccessful():
        sys.exit(1)
