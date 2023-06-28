from django.urls import path
from .views import *


urlpatterns = [
    path('login/', loginpage, name='login'),
    path('create_account/', register, name='goto_create_account'),
    path('created_account/', done_account,name='created_account'),
]
