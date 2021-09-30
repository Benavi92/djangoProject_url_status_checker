from django.contrib import admin
from .models import UrlStatus

# Register your models here.


class UrlStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'url', 'status_code']


admin.site.register(UrlStatus)
