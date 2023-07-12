from django.db import models
import os
from twilio.rest import Client
from django.core.validators import MinLengthValidator
class Account(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    time_zone = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField(unique=True)
    password = models.CharField(max_length=100, validators=[MinLengthValidator(8)])

    def __str__(self):
        return self.email_address
    

class collectdata(models.Model):
    email_address = models.EmailField()
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()

    def __str__(self):
        return self.title
    