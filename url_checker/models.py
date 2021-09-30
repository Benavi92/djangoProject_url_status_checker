from django.db import models

# Create your models here.


class UrlStatus(models.Model):
    url = models.URLField(verbose_name="url")
    status_code = models.PositiveSmallIntegerField(verbose_name="status code")



