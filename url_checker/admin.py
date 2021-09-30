from django.contrib import admin

# Register your models here.


class UrlStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'url', 'status_code']

admin.sites.