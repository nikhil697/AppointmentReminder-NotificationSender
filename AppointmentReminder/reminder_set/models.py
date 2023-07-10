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
    
    # def save(self, *args, **kwargs):
    #     account_sid = os.environ['ACaf4571de8a4cdb52f6398c6acf8eed6a']
    #     auth_token = os.environ['b593cf441af57520a78ca5d87de42613']
    #     client = Client(account_sid, auth_token)

    #     message = client.messages.create(
    #                                 body='Hi there',
    #                                 from_='+14849929143',
    #                                 to=''
    #                             )

    #     print(message.sid)

    #     return super.save(*args,**kwargs)