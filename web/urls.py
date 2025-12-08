from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('panel_paciente/', views.panel_paciente, name='panel_paciente'),
    path('panel_doctor/', views.panel_doctor, name='panel_doctor'),
    path('panel_recepcionista/', views.panel_recepcionista, name='panel_recepcionista'),
    path('agendar_cita/', views.agendar_cita, name='agendar_cita'),
    path('obtener_doctores/<int:especialidad_id>/', views.obtener_doctores, name='obtener_doctores'),
    path('citas_agendadas/', views.citas_agendadas, name='citas_agendadas'),
    path('registro_paciente/', views.registro_paciente, name='registro_paciente'),
    path('validar_correo/', views.validar_correo, name='validar_correo'),
    path('datos_personales/', views.datos_personales, name='datos_personales'),

]
