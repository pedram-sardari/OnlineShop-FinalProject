from django.db import models


class OwnerStaffManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=self.model.Roles.OWNER)


class ManagerStaffManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=self.model.Roles.MANAGER)


class OperatorStaffManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=self.model.Roles.OPERATOR)
