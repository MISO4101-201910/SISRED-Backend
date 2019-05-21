from django.urls import path
from sisred_app.views import  views_equipo1,views_equipo2,views_equipo3,views_equipo4

urlpatterns = [

    #path('recurso_list/', views_equipo1.recurso_list, name='recurso_list'),
    path('recurso_get/<int:id>', views_equipo1.recurso_get, name='recurso_get'),
    path('recurso_put/', views_equipo1.recurso_put, name='recurso_put'),
    path('recurso_post/', views_equipo1.recurso_post, name='recurso_post'),
    path('fase_byid/<int:id>', views_equipo1.fase_byid, name='fase_byid'),
    path('habilitar-usuario/<str:numero_identificacion>', views_equipo1.getUserByIdentification, name='habilitar-usuario'),
    path('habilitar-red/<str:id_conectate>', views_equipo1.getREDByIdentification, name='habilitar-red'),
    path('comentario-cierre/', views_equipo1.comentario_cierre_post, name='comentario-cierre'),
    path('comentario-cierre/base/<int:pk>', views_equipo1.comentario_cierre_put, name='comentario-cierre-put'),
    path('comentario-base/<int:pk>', views_equipo1.comentario_base_get, name='comentario-base'),
    path('comentario-pdf/<int:pk>/', views_equipo1.comentario_pdf_get, name='comentario_pdf_get'),
    path('comentario-pdf/', views_equipo1.comentario_pdf_post, name='comentario-pdf-post'),

    path('post_proyecto_red/', views_equipo3.post_proyecto_red, name='agregar_proyecto_red'),
    path('detallered/', views_equipo3.get_detallered, name='detallered'),
    path('detallered/metadata/', views_equipo3.get_detallered_metadata, name='detallered'),
    path('detallered/personas/', views_equipo3.get_detallered_personas, name='detallered'),
    path('detallered/recursos/', views_equipo3.get_detallered_recursos, name='detallered'),
    path('detallered/proyectos/', views_equipo3.get_detallered_proyectosred, name='detallered'),
    path('reds/asignados/<int:id>', views_equipo3.get_reds_asignados, name='reds_asignados'),
    path('get_version/', views_equipo3.get_version, name='version_red'),
    path('get_recursos_by_version/', views_equipo3.get_recursos_by_version, name='version_red'),
    path('comentarios/video/<int:id>', views_equipo3.get_comentarios_video, name='comentarios'),
    path('comentarios/video/<int:idVersion>/<int:idRecurso>', views_equipo3.post_comentarios_video, name='agregarComentarios'),
    path('comentarios/video/url/<int:id>', views_equipo3.get_url_recurso_video, name='urlRecursoVideo'),
    path('revisiones/<int:id>', views_equipo3.get_versiones_revision, name='revisiones'),

    path('getProyectosRED/', views_equipo2.getProyectosRED),
    path('getRecurso/', views_equipo2.getRecurso),
    path('getRED/', views_equipo2.getRED),
    path('asignaciones/', views_equipo2.getAsignaciones),
    path('red/<int:id>/recursos/', views_equipo2.getRecursosRed),
    path('versiones/<int:id>/', views_equipo2.getVerVersion),
    path('versiones/<int:id>/recursos/', views_equipo2.getVerVersionR),
    path('reds/<int:id>/versiones/', views_equipo2.getVersionesRED),
    path('versiones/<int:id>/marcar', views_equipo2.marcarVersion, name='marcarVersion'),
    path('buscarReds/<int:idUsuario>/', views_equipo2.buscarRed, name='reds'),
    path('versiones/', views_equipo2.versiones, name='versiones'),
    path('versiones/<int:id_v>/recursos/<int:id_r>/comentarios/', views_equipo2.comentarioExistente, name='comentarioExistente'),
    path('versiones/<int:id_v>/recursos/<int:id_r>/comentariosnuevos/', views_equipo2.comentarioNuevo, name='comentarioNuevo'),
    path('versiones/<int:id_v>/recursos/<int:id_r>/listacomentarios/', views_equipo2.getListaComentarios, name='getListaComentarios'),

    path('users/', views_equipo4.getAllUser, name='allUsers'),
    path('users/<int:id>/', views_equipo4.getUser, name='getUserId'),
    path('login/', views_equipo4.login, name='login'),
    path('logout/', views_equipo4.logout, name='logout'),
    path('users/add/', views_equipo4.postUser, name='addUser'),
    path('users/update/<int:id>/', views_equipo4.putUser, name='updateUser'),
    path('users/delete/<int:id>/', views_equipo4.deleteUser, name='deleteUser'),
    path('reds/relacionados/<int:id>/', views_equipo4.get_reds_relacionados, name='reds_relacionados'),
    path('getRecurso/<int:id>/', views_equipo4.getRecurso, name='getRecurso'),
    path('getTokenVal/', views_equipo4.getTokenVal, name='getTokenVal'),
    path('getRedDetailRecursos/<int:id>/', views_equipo4.getRedDetailRecursos, name='getRedDetailRecursos'),
    path('getUserAut/', views_equipo4.getUserAut, name='getUserAut'),
    path('getRolAsignadoRED/<int:id>/', views_equipo4.getRolAsignadoRED, name='getRolAsignadoRED'),
    path('update_sisred/', views_equipo4.update_sisred, name='update_sisred'),
    path('reds/', views_equipo4.get_red, name='reds'),
    path('sisred_create/', views_equipo4.sisred_create, name='sisred_create'),
    path('sisred_remove/', views_equipo4.sisred_remove, name='sisred_remove'),
    path('asignaciones/add/', views_equipo4.postRolAsignado, name='addRolAsignado'),
    path('asignaciones/update/<int:id>/', views_equipo4.putRolAsignado, name='putRolAsignado'),
    path('asignaciones/delete/<int:id>/', views_equipo4.deleteRolAsignado, name='deleteRolAsignado'),
    path('red/<int:idRed>/cambiarfase/<int:idFase>/', views_equipo4.putCambiarFaseRed, name='putCambiarFaseRed'),
    path('getMetrics/', views_equipo4.getMetrics, name='getMetrics'),

    path('fases/', views_equipo4.get_fases, name='fases'),
    path('addMetadataRecurso/<int:id>/', views_equipo4.add_metadata_recurso, name='addMetadataRecurso'),
    path('buscarRecurso/', views_equipo4.buscar_recurso, name='recursos'),
    path('notificaciones/<int:idUsuario>/', views_equipo4.getNotificacionesPorUsuario, name='getNotificacionesPorUsuario'),
    path('notificaciones/<int:idUsuario>/novistos/', views_equipo4.getNotificacionesNoVistosPorUsuario, name='getNotificacionesNoVistosPorUsuario'),
    path('putNotification/<int:id_notification>/', views_equipo4.putNotification, name='putNotification'),
    path('getHistoricoAsignadosRed/<int:id>/', views_equipo4.getHistoricoAsignadosRed, name='getHistoricoAsignadosRed')
]
