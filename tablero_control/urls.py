"""
URL configuration for tablero_control project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as viewsL
from . import views
from django.urls import path, include
from usuarios.views import index
import dashboard.views as vDash

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    
    path('', index, name="index"),
    path('log-in/', viewsL.LoginView.as_view(template_name= 'base/log_in.html'), name='log-in'),
    path('log-out/', viewsL.LogoutView.as_view(), name="logout"),
    path('dashboard/', vDash.dashboard ,name="dashboard" ),
    path('crear_registro/', vDash.crear_registro ,name="crear_registro" ),
    path('editar_registro/<int:registro_id>/', vDash.editar_registro , name='editar_registro'),
    path('detalles/<int:registro_id>/', vDash.detalles , name='detalles'),
]
