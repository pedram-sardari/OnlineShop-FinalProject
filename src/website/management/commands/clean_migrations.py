import os
import glob
from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
from django.db import connection, OperationalError


class Command(BaseCommand):
    help = 'Deletes all .py files (except __init__.py) from migrations directories and cleans corresponding records from django_migrations table.'

    def handle(self, *args, **kwargs):
        project_root = str(settings.BASE_DIR)
        self.stdout.write('Starting clean_migrations...')

        migrations_to_clean = []

        # Step 1: Delete migration files
        for app_config in apps.get_app_configs():
            app_path = str(app_config.path)
            if project_root not in app_path:
                continue

            migrations_path = os.path.join(app_path, 'migrations')
            if os.path.exists(migrations_path):
                migration_files = glob.glob(os.path.join(migrations_path, '*.py'))
                for migration_file in migration_files:
                    if os.path.basename(migration_file) == '__init__.py':
                        continue

                    migration_name = os.path.splitext(os.path.basename(migration_file))[0]
                    migrations_to_clean.append((app_config.label, migration_name))

                    # Delete the .py migration file
                    try:
                        os.remove(migration_file)
                        self.stdout.write(f'Successfully deleted file: {migration_file}')
                    except OSError as e:
                        self.stderr.write(f'Error deleting file {migration_file}: {e}')
                        continue

        # Step 2: Clean up the database
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM django_migrations LIMIT 1;")
        except OperationalError:
            self.stderr.write(
                'The django_migrations table does not exist. Run "python manage.py migrate" before using this command.')
            return

        for app_label, migration_name in migrations_to_clean:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM django_migrations WHERE app = %s AND name = %s",
                                   [app_label, migration_name])
                self.stdout.write(f'Successfully deleted migration record: {app_label} - {migration_name}')
            except OperationalError as e:
                self.stderr.write(f'Error deleting migration record {app_label} - {migration_name}: {e}')
                continue

        self.stdout.write('Completed clean_migrations.')
