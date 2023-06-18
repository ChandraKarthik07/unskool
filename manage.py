import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unskool.settings')

    try:
        from django.core.management import execute_from_command_line
        from uvicorn import run

        # Run Django with Uvicorn
        if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
            run("unskool.asgi:application", host="0.0.0.0", port=8000)
        else:
            execute_from_command_line(sys.argv)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
