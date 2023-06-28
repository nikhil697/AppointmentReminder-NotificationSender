from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
import mysql.connector
from django.core.mail import send_mail

# Create your views here.

def loginpage(request):
    return render(request,'reminder_set/login_register.html')


def register(request):
    if request.method == "POST":
        return render(request,'reminder_set/create_account.html')


def done_account(request):
    if request.method == "POST":
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        time_zone = request.POST.get('time-zone')
        country_code = request.POST.get('country-code')
        phone_number = request.POST.get('phone-number')
        email_address = request.POST.get('email-address')
        password = request.POST.get('password')

        # Create an Account object and save the values in the database
        account = Account(
            first_name=first_name,
            last_name=last_name,
            time_zone=time_zone,
            country_code=country_code,
            phone_number=phone_number,
            email_address=email_address,
            password=password
        )
        account.save(using='Appointment')

        if account.pk:
            print("Account saved successfully")
            subject = 'Account Created'
            message = 'Your account has been successfully created. You can now login to your Account'
            from_email = 'nchadha_be21@thapar.edu'
            recipient_list = [email_address]
            send_mail(subject, message, from_email, recipient_list)

            return redirect('login')
        else:
            # Account not saved
            print("Account not saved successfully")
            return redirect('create_account')  # Redirect to the create_account page

    return render(request, 'reminder_set/create_account.html')
