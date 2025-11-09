from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('panel_paciente/', views.panel_paciente, name='panel_paciente'),
    path('panel_doctor/', views.panel_doctor, name='panel_doctor'),
    path('panel_recepcionista/', views.panel_recepcionista, name='panel_recepcionista'),
]
