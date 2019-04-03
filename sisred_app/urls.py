from django.urls import path
from . import views
from sisred_app.views import views_equipo3

urlpatterns = [

    path('post_proyecto_red/', views_equipo3.post_proyecto_red, name='agregar_proyecto_red'),
    path('detallered/', views_equipo3.get_detallered, name='detallered'),
    path('detallered/metadata/', views_equipo3.get_detallered_metadata, name='detallered'),
    path('detallered/personas/', views_equipo3.get_detallered_personas, name='detallered'),
    path('detallered/recursos/', views_equipo3.get_detallered_recursos, name='detallered'),
    path('detallered/proyectos/', views_equipo3.get_detallered_proyectosred, name='detallered'),
    path('reds/asignados/<int:id>', views_equipo3.get_reds_asignados, name='reds_asignados'),
    path('getProyectosRED/', views.getProyectosRED),
    path('getRecurso/', views.getRecurso),
    path('getRED/', views.getRED),
    path('asignaciones/', views.getAsignaciones),
]
