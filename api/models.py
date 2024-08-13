from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import os
from django.core.validators import FileExtensionValidator
# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile_num = models.TextField()
    address = models.TextField()
    
    def __str__(self):
        return self.user.first_name

class Pension(models.Model):
    seniors = models.ForeignKey(User, on_delete=models.CASCADE)
    requirement = models.FileField(upload_to='pensions/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])],)
    date_submitted = models.DateTimeField(auto_now_add=True)
    status = models.TextField()
    qr = models.FileField(upload_to='qrs/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])], blank=True)
    notification_status = models.TextField()
    
class Schedule(models.Model):
    description = models.TextField()
    month = models.DateField()
    startDatetime = models.TimeField()
    endDatetime = models.TimeField()
    

class Notification(models.Model):
    seniors = models.ForeignKey(User, on_delete=models.CASCADE)
