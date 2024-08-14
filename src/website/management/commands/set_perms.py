from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from website.permissions import GROUPS, PERMISSIONS


class Command(BaseCommand):
    help = 'Creates'

    def handle(self, *args, **kwargs):
        for group_name, model_permissions in GROUPS.items():
            group_name, created = Group.objects.get_or_create(name=group_name)

            if created:
                self.stdout.write(self.style.SUCCESS(f'Group {group_name.name} was created.'))
            else:
                self.stdout.write(f"Group {group_name.name} already exists.")

            for model, permissions in model_permissions.items():
                content_type = ContentType.objects.get_for_model(model)

                for permission_code in permissions:
                    # Generate the permission codename from the model and the action
                    permission_codename = f"{PERMISSIONS[permission_code]}_{model._meta.model_name}"

                    try:
                        permission = Permission.objects.get(content_type=content_type, codename=permission_codename)
                        group_name.permissions.add(permission)
                        self.stdout.write(self.style.SUCCESS(f'Assigned `{permission_codename}` to {group_name}.'))
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f'Permission `{permission_codename}` does not exist.'))

            self.stdout.write(self.style.SUCCESS('Permissions assignment completed.'))
