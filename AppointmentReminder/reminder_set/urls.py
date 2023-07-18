from django.urls import path
from .views import *
from .views import loginpage

urlpatterns = [
    path('login/', loginpage, name='login'),
    path('create_account/', register, name='goto_create_account'),
    path('created_account/', done_account,name='created_account'),
    path('success_or_not/',success_or_not,name='success_or_not'),
    # path('personal/',personal,name='personal'),
    path('personal/', login, name='personal'),
    path('resetpage/',resetpass, name='reset_page'),
    path('resetpass1/',resetpassfunc, name='reset_pass'),
    path('reminderdone',create_reminder,name='createdone'),
    path('reminder_tile',personal,name='tilecreate'),
    path('all/',all_reminders, name='all_reminders'),
    path('delete/<int:reminder_id>/', delete_reminder, name='delete_reminder'),
    path('edit/<int:reminder_id>/', edit_reminder, name='edit_reminder'),
    # path('save/<int:reminder_id>/', save_reminder, name='save_reminder'),
    path('aboutus/', about_view, name='aboutus'),
]
