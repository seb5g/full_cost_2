#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fullcoster.full_cost.settings")
    import django
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    django.setup()
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    import sys
    #sys.argv = [r'C:\Users\weber\Labo\ProgrammesPython\Git_others\full_cost_2\src\fullcoster\manage.py', 'runserver', '--noreload']
    main()
