from django.urls import path
from .views import *
from .views import loginpage

urlpatterns = [
    path('login/', loginpage, name='login'),
    path('create_account/', register, name='goto_create_account'),
    path('created_account/', done_account,name='created_account'),
    path('success_or_not/',success_or_not,name='success_or_not'),
    path('personal/',personal,name='personal'),
    path('resetpage/',resetpass, name='reset_page'),
    path('resetpass1/',resetpassfunc, name='reset_pass'),
    path('reminderdone',create_reminder,name='createdone'),
]
