from django.core.management.base import CommandError
from django.core.management.templates import TemplateCommand
from django.utils.crypto import get_random_string
from django.utils.importlib import import_module


class Command(TemplateCommand):
    help = ("Creates a Django project directory structure for the given "
            "project name in the current directory or optionally in the "
            "given directory.")

    def handle(self, invoice4django=None, target=None, *args, **options):
        self.validate_name(invoice4django, "project")

        # Check that the invoice4django cannot be imported.
        try:
            import_module(invoice4django)
        except ImportError:
            pass
        else:
            raise CommandError("%r conflicts with the name of an existing "
                               "Python module and cannot be used as a "
                               "project name. Please try another name." %
                               invoice4django)

        # Create a random SECRET_KEY hash to put it in the main settings.
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        options['secret_key'] = get_random_string(50, chars)

        super(Command, self).handle('project', invoice4django, target, **options)
