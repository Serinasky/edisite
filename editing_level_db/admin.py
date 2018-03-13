from django.contrib import admin
from .models import Sample, Editing_site, Editing_level
# Register your models here.

admin.site.register(Sample)
admin.site.register(Editing_level)
admin.site.register(Editing_site)