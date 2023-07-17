# from django.core.management.base import BaseCommand
# from django.core.mail import send_mail
# from reminder_set.models import collectdata
# from datetime import datetime, timedelta
# from time import sleep


# class Command(BaseCommand):
#     help = 'Checks reminders every second and sends email for reminders within the specified time range.'

#     def handle(self, *args, **options):
#         while True:
#             current_time = datetime.now()
#             reminders = collectdata.objects.all()
#             for reminder in reminders:
#                 reminder_datetime = datetime.combine(reminder.date, reminder.time)
#                 time_diff = reminder_datetime - current_time
#                 if timedelta(hours=48, seconds=1) <= time_diff <= timedelta(hours=48, seconds=3):
#                     # Send email to the reminder owner
#                     subject = 'Reminder'
#                     message = f'Hello {reminder.email_address},\n\nThis is a reminder for your appointment: {reminder.title}.\n\nPlease make sure to attend on time.\n\nRegards,\nThe Reminder Team'
#                     from_email = 'nchadha_be21@thapar.edu'
#                     to_email = [reminder.email_address]
#                     send_mail(subject, message, from_email, to_email, fail_silently=False)
#                     self.stdout.write(f'Sending email for reminder: {reminder.title}')
#             # Sleep for 1 second before checking again
#             sleep(1)


from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils.timezone import datetime
from time import sleep
from reminder_set.models import collectdata, Account
from datetime import timedelta

class Command(BaseCommand):
    help = 'Sends reminders to users'

    def handle(self, *args, **options):
        while True:
            current_time = datetime.now()
            reminders = collectdata.objects.all()
            for reminder in reminders:
                reminder_datetime = datetime.combine(reminder.date, reminder.time)
                time_diff = reminder_datetime - current_time
                
                if (timedelta(hours=48, seconds=0) <= time_diff <= timedelta(hours=48, seconds=1)
                    or timedelta(hours=24, seconds=0) <= time_diff <= timedelta(hours=24, seconds=1)
                    or timedelta(hours=1, seconds=0) <= time_diff <= timedelta(hours=1, seconds=1)
                    or timedelta(hours=0, seconds=0) < time_diff <= timedelta(hours=0, seconds=1)):
                    
                    # Get the person's name from the Account model
                    try:
                        account = Account.objects.get(email_address=reminder.email_address)
                        person_name = f'{account.first_name} {account.last_name}'
                    except Account.DoesNotExist:
                        person_name = 'User'
                    
                    # Calculate the time left for the reminder
                    time_left = reminder_datetime - current_time
                    
                    # Format the time left as hh:mm:ss
                    total_seconds = time_left.total_seconds()
                    hours = int(total_seconds // 3600)
                    minutes = int((total_seconds % 3600) // 60)
                    seconds = int(total_seconds % 60)
                    
                    # Send email to the reminder owner
                    subject = 'Reminder'
                    message = f'Hello {person_name},\n\nThis is an appointment reminder for your appointment: {reminder.title}.\n\nDate and Time: {reminder_datetime.strftime("%Y-%m-%d %H:%M:%S")}\nTime Left: {hours:02d}:{minutes:02d}:{seconds:02d}\n\nDescription: {reminder.description}\n\nPlease make sure to attend it on time.\n\nRegards,\nTeam Appointment Reminder'
                    from_email = 'nchadha_be21@thapar.edu'
                    to_email = [reminder.email_address]
                    send_mail(subject, message, from_email, to_email, fail_silently=False)
                    self.stdout.write(f'Sending email for reminder: {reminder.title} {current_time}')
                    
                elif time_diff <= timedelta(seconds=0):
                    # Delete the reminder if the current time has reached or passed the reminder datetime
                    reminder.delete()
                    self.stdout.write(f'Reminder deleted: {reminder.title}')
            
            # Sleep for 1 second before checking again
            sleep(1)


