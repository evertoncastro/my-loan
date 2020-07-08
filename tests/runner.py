import os
import sys
from unittest.loader import TestLoader
from unittest import TextTestRunner

def test_suite():
    suite = TestLoader().discover(
        'tests',
        pattern='test_*.py',
        top_level_dir=os.environ['PYTHONPATH'].split(os.pathsep)[0]
    )
    return TextTestRunner(verbosity=1).run(suite)


if __name__ == '__main__':
    result = test_suite()
    if not result.wasSuccessful():
        sys.exit(1)