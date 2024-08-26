from django.db import models


class PortalUser(models.Model):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    date_register = models.DateField(auto_now_add=True)
    user_type = models.CharField(max_length=100)
