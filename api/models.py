from datetime import datetime
from django.db import models
from django.utils import timezone

class School(models.Model):
    status = models.BooleanField(default=True)
    name = models.CharField(max_length=64)
    updated = models.DateTimeField(default=timezone.now)
    licenses = models.IntegerField(default=3)

    def __str__(self):
        return self.name

class Account(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

class License(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    token = models.CharField(max_length=16)
    status = models.BooleanField(default=True)
    reserved = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [ models.Index(fields=['token']) ]

    def __str__(self):
        return self.school.name + ' - ' + self.account.username + ' - ' + self.token
