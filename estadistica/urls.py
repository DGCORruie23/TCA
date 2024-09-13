from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('generales/', views.general, name="estadistica_p"),
]