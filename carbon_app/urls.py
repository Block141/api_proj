from django.urls import path, include
from . import views
# http://localhost:8000/api/v1/students/

urlpatterns = [
    path('estimate/', views.get_estimate_form, name='estimate_form'),
    path('estimate/result/', views.get_estimate_result, name='estimate_result'),
]