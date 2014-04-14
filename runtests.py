#!/usr/bin/env python
import sys
from shutil import rmtree
from os.path import abspath, dirname, join

import django
from django.conf import settings

import invoices

sys.path.insert(0, abspath(dirname(__file__)))


media_root = join(abspath(dirname(__file__)), 'test_files')
rmtree(media_root, ignore_errors=True)

installed_apps = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.admin',
    'invoices',
)

DEFAULT_SETTINGS = dict(
    ROOT_URLCONF='invoice4django.tests.urls',
    MEDIA_ROOT=media_root,
    STATIC_URL='/static/',
    INSTALLED_APPS=installed_apps,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    AUTH_USER_MODEL='auth.user',
)


def main():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    if hasattr(django, 'setup'):
        django.setup()
    if django.VERSION < (1, 7): 
        from django.test.simple import DjangoTestSuiteRunner
        failures = DjangoTestSuiteRunner(verbosity=1, interactive=True, failfast=False).run_tests(test_labels=None)
        sys.exit(failures)
    else:
        from django.test.runner import DiscoverRunner
        failures = DiscoverRunner(
            pattern='test*.py', verbosity=1, interactive=True, failfast=False).run_tests(test_labels=None)
        sys.exit(failures)


if __name__ == "__main__":
    main()
