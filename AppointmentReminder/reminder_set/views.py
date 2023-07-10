from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import *
import mysql.connector
from django.db import connection,IntegrityError,transaction
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
from mysql.connector import Error
from .forms import CollectDataForm
from django.contrib import messages



# Create your views here.

def loginpage(request):
    return render(request,'reminder_set/login_register.html')


def register(request):
    if request.method == "POST":
        return render(request, 'reminder_set/create_account.html')
    else:
        return redirect('login')  # Redirect to the login page if not a POST request

    

def success_or_not(request):
    message = request.GET.get('message')
    return render(request, 'reminder_set/success_or_not.html', {'message': message})
    

def done_account(request):
    if request.method == "POST":
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        time_zone = request.POST.get('time-zone')
        country_code = request.POST.get('country-code')
        phone_number = request.POST.get('phone-number')
        email_address = request.POST.get('email-address')
        password = request.POST.get('password')
        
        try:
            Regis = Account(first_name=first_name,
                    last_name=last_name,
                    time_zone=time_zone,
                    country_code=country_code,
                    phone_number=phone_number,
                    email_address=email_address,
                    password=password)
            Regis.full_clean()
            Regis.save()            
            print("Account saved successfully")

            subject = 'Account Created'
            message = f'Hello {first_name} {last_name},\n\nYour account has been successfully created. You can now login to your Account using your credentials.'
            from_email = 'nchadha_be21@thapar.edu'
            recipient_list = [email_address]
            send_mail(subject, message, from_email, recipient_list)

            success_message = "Account Registered successfully"
            return render(request, 'reminder_set/success_or_not.html', {'message': success_message})
        except IntegrityError:
            error_msg = "Email is already registered"
        except Exception as e:
            error_msg = "An error occurred: {}".format(str(e))
        
        return render(request, 'reminder_set/success_or_not.html', {'message': error_msg})
        
    else:
        return render(request, 'reminder_set/create_account.html')


def personal(request):
    if request.method == 'POST':
        email_address = request.POST.get('email-address')
        password = request.POST.get('password')
        
        try:
            conne = mysql.connector.connect(user='root', password='nikhil2002', host='localhost', database='Appointment')
            cursor = conne.cursor()
            
            query = f"SELECT * FROM reminder_set_account WHERE email_address = '{email_address}' AND password = '{password}'"
            cursor.execute(query)
            user = cursor.fetchone()
            
            if user:
                request.session['email_address'] = user[0] # assuming user_id is the first column in the table
                conne.close()
                
                return render(request, 'reminder_set/personal.html')
            else:
                conne.close()
                error_message = 'Invalid login credentials. Please try again.'
                return render(request, 'reminder_set/success_or_not.html', {'message': error_message})
        
        except Error as e:
            # Handle database connection or query errors
            error_message = 'An error occurred while accessing the database: {}'.format(str(e))
            return render(request, 'reminder_set/success_or_not.html', {'message': error_message})
        
    else:
        # If request method is GET, show the login page
        return render(request, 'reminder_set/login_register.html')
    

def resetpass(request):
    return render(request, 'reminder_set/resetpass.html', {})

def success(request):
    return render(request, 'reminder_set/success_or_not.html', {'message': 'Password has been successfully reset'})

def resetpassfunc(request):
    if request.method == 'POST':
        email_address = request.POST.get('email-address')
        prevpass = request.POST.get('prevp')
        newpass = request.POST.get('newpass')
        conne = mysql.connector.connect(user='root', password='nikhil2002', host='localhost', database='Appointment')
        cursor = conne.cursor()
        query = f"UPDATE reminder_set_account SET password = '{newpass}' WHERE email_address = '{email_address}' AND password = '{prevpass}'"
        cursor.execute(query)
        if cursor.rowcount > 0:
            # Password was successfully updated in the database
            conne.commit()
            conne.close()
            message = 'Password Reset Successful'
            return render(request, 'reminder_set/success_or_not.html', {'message': message})
            
        # render(request, 'sports_goods/resetsuccess.html', {})
        else:
            # Password could not be updated in the database
            conne.rollback()
            conne.close()
            error_message = 'Invalid credentials. Please try again.'
            return render(request, 'reminder_set/success_or_not.html', {'message': error_message})
    else:
        # if request method is GET, show the reset password page
        return render(request, 'reminder_set/resetpass.html', {})
    



def create_reminder(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        date = request.POST.get('date')
        time = request.POST.get('time')
        description = request.POST.get('description')
        
        email = request.session.get('email_address')
        conne = mysql.connector.connect(user='root', password='nikhil2002', host='localhost', database='Appointment')
        cursor = conne.cursor()
        query = f"SELECT email_address FROM reminder_set_account WHERE id = {email}"
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result:
            email_address = result[0]
            
            try:
                # Create a new instance of CollectData
                collect_data = collectdata(email_address=email_address, title=title, date=date, time=time, description=description)
                
                # Save the new instance to the database
                collect_data.save()
                
                # Fetch reminders
                reminders = collectdata.objects.filter(email_address=email_address)[:4]
                
                # Display success message and reminders
                success_message = "Reminder Created Successfully"
                return render(request, 'reminder_set/personal.html', {'message': success_message, 'reminders': reminders})
            
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                return render(request, 'reminder_set/personal.html', {'message': error_message})
        
        else:
            error_message = "Invalid account. Please login again."
            return render(request, 'reminder_set/personal.html', {'message': error_message})
    
    else:
        email_address = request.session.get('email_address')
        conne = mysql.connector.connect(user='root', password='nikhil2002', host='localhost', database='Appointment')
        cursor = conne.cursor()
        query = f"SELECT email_address FROM reminder_set_account WHERE id = {email_address}"
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            email_address = result[0]
            reminders = collectdata.objects.filter(email_address=email_address)[:4]
            return render(request, 'reminder_set/personal.html', {'reminders': reminders})
        else:
            # Handle case when user is not logged in
            return render(request, 'reminder_set/personal.html', {'reminders': []})

    

def personal(request, message=None):
    email_address = request.session.get('email_address')
    conne = mysql.connector.connect(user='root', password='nikhil2002', host='localhost', database='Appointment')
    cursor = conne.cursor()
    query = f"SELECT email_address FROM reminder_set_account WHERE id = {email_address}"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        email_address = result[0]
        reminders = collectdata.objects.filter(email_address=email_address)[:4]
        return render(request, 'reminder_set/personal.html', {'reminders': reminders, 'message': message})
    else:
        # Handle case when user is not logged in
        return render(request, 'reminder_set/personal.html', {'reminders': [], 'message': message})



def all_reminders(request):
    email_address = request.session.get('email_address')
    conne = mysql.connector.connect(user='root', password='nikhil2002', host='localhost', database='Appointment')
    cursor = conne.cursor()
    query = f"SELECT email_address FROM reminder_set_account WHERE id = {email_address}"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        email_address = result[0]
        reminders = collectdata.objects.filter(email_address=email_address)
        return render(request, 'reminder_set/all.html', {'reminders': reminders})
    else:
        # Handle case when user is not logged in or has no reminders
        return render(request, 'reminder_set/personal.html', {'reminders': []})
    

def delete_reminder(request, reminder_id):
    try:
        reminder = collectdata.objects.get(id=reminder_id)
        reminder.delete()
        return redirect('all_reminders')
    except collectdata.DoesNotExist:
        # Handle case when the reminder doesn't exist
        return redirect('all_reminders')
    

# def edit_reminder(request, reminder_id):
#     try:
#         # Retrieve the existing reminder from the database
#         reminder = collectdata.objects.get(id=reminder_id)

#         if request.method == 'POST':
#             title = request.POST.get('edit-title')
#             date = request.POST.get('edit-date')
#             time = request.POST.get('edit-time')
#             description = request.POST.get('edit-description')

#             # Update the reminder fields with the new values
#             # reminder.title = title
#             # reminder.date = date
#             # reminder.time = time
#             # reminder.description = description
#             conne=mysql.connector.connect(user='root', password='nikhil2002', host='localhost', database='Appointment')
#             cursor = conne.cursor()
#             query=f"update reminder_set_collectdata set title={title},date={date},time={time},description={description} where id={reminder_id}"
#             cursor.execute(query)
#             conne.commit()
#             conne.close()

#             # Save the updated reminder
#             reminder.save()

#             # Redirect to the personal page with a success message
#             success_message = "Reminder updated successfully"
#             return redirect('personal', message=success_message)

#         else:
#             return render(request, 'reminder_set/edit_reminder.html', {'reminder': reminder})

#     except collectdata.DoesNotExist:
#         # Handle case when the reminder does not exist
#         error_message = "Reminder not found"
#         return redirect('personal', message=error_message)
def edit_reminder(request, reminder_id):
    try:
        reminder = collectdata.objects.get(id=reminder_id)

        if request.method == 'POST':
            form = CollectDataForm(request.POST, instance=reminder)
            if form.is_valid():
                form.save()
                success_message = "Reminder updated successfully"
                return redirect('personal', message=success_message)
        else:
            form = CollectDataForm(instance=reminder)

        return render(request, 'reminder_set/edit_reminder.html', {'form': form, 'reminder': reminder})

    except collectdata.DoesNotExist:
        error_message = "Reminder not found"
        return redirect('personal', message=error_message)



from datetime import datetime

from django.shortcuts import render, redirect
from .forms import CollectDataForm
from .models import collectdata

def save_reminder(request, reminder_id):
    try:
        reminder = collectdata.objects.get(id=reminder_id)
        
        if request.method == 'POST':
            form = CollectDataForm(request.POST, instance=reminder)
            
            if form.is_valid():
                form.save()
                success_message = "Reminder updated successfully"
                return redirect('personal')
            else:
                # Print form errors for debugging purposes
                print(form.errors)
        
        else:
            form = CollectDataForm(instance=reminder)
        
        return render(request, 'reminder_set/edit_reminder.html', {'form': form, 'reminder': reminder})

    except collectdata.DoesNotExist:
        error_message = "Reminder not found"
        return redirect('personal', message=error_message)









# def save_reminder(request, reminder_id):
#     try:
#         # Retrieve the existing reminder from the database
#         reminder = collectdata.objects.get(id=reminder_id)

#         if request.method == 'POST':
#             title = request.POST.get('edit-title')
#             date = request.POST.get('edit-date')
#             time = request.POST.get('edit-time')
#             description = request.POST.get('edit-description')

#             # Update the reminder fields with the new values
#             # reminder.title = title
#             # reminder.date = date
#             # reminder.time = time
#             # reminder.description = description
#             conne=mysql.connector.connect(user='root', password='nikhil2002', host='localhost', database='Appointment')
#             cursor = conne.cursor()
#             query=f"update reminder_set_collectdata set title={title},date={date},time={time},description={description} where id={reminder_id}"
#             cursor.execute(query)
#             conne.commit()
#             conne.close()

#             # Save the updated reminder
#             reminder.save()

#             # Redirect to the personal page with a success message
#             success_message = "Reminder updated successfully"
#             return redirect('personal', message=success_message)

#         else:
#             return render(request, 'reminder_set/edit_reminder.html', {'reminder': reminder})

#     except collectdata.DoesNotExist:
#         # Handle case when the reminder does not exist
#         error_message = "Reminder not found"
#         return redirect('personal', message=error_message)
