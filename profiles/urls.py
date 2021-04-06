from django.urls import path
from profiles import views

app_name = 'profiles'

urlpatterns = [
    path('my-profile', views.my_profile, name='my-profile'),
]