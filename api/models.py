from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import os
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_num = models.TextField()
    address = models.TextField()
    
    def __str__(self):
        return self.user.first_name
