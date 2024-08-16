from django.db import models


class SoftDeleteManager(models.Manager):
    def all_objects(self):
        """ Returns all objects, including all 'is_deleted=True' abjects"""
        return super().get_queryset()

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
