from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('table/', work_button, name='work_button'),
    path('table/field/', work_field, name='work_field'),
]