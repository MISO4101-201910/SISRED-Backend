from django.urls import path

from . import views

urlpatterns = [
    path('recurso_list/', views.recurso_list, name='recurso_list'),
    path('recurso_addget/<int:id>', views.recurso_addget, name='recurso_addget'),
    path('fase_byid/<int:id>', views.fase_byid, name='fase_byid'),
]
