from django.contrib import admin
from nested_tree_app.models import Category
# Register your models here.
from mptt.admin import MPTTModelAdmin

admin.site.register(Category, MPTTModelAdmin)