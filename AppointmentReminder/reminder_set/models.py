from django.db import models

class Account(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    time_zone = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField(unique=True)
    password = models.CharField(max_length=100)