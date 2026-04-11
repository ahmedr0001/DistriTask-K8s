from django.urls import path
from . import views

app_name = "users"  

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),  
    path('change-password/', views.change_password, name='change_password'), 
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'), 
    
]