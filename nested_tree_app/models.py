from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    description = models.TextField(max_length=100, unique=True)

    class MPTTMeta:
        order_insertion_by = ['name']
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
