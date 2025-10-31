# myapp/urls.py
from django.urls import path
from . import views

app_name = "myapp"

urlpatterns = [
    path('check-age/', views.check_age, name='check_age'),
    path('regions/', views.regions, name='regions'),
]
