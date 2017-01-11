from django.db import models
from django.contrib.auth.models import User

class Domain(models.Model):
    domain_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    owners = models.ManyToManyField(User)
