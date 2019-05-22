from django.shortcuts import get_object_or_404,get_list_or_404
from django.core import serializers
from django.core.serializers import serialize
from rest_framework import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, Http404, HttpResponseForbidden, HttpResponseBadRequest
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from sisred_app.models import ProyectoRED, Recurso, RED, RolAsignado, Perfil, Rol, ProyectoConectate, Version, Comentario, ComentarioMultimedia, HistorialFases
from django.contrib.auth.models import User
from sisred_app.serializer import RecursoSerializer
import datetime
import json
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from .views_equipo4 import createNotification
from rest_framework import status
from sisred_app.serializer import *


from sisred_app.views.views_equipo4 import createNotification


@csrf_exempt
def getProyectosRED(request):
    vLstObjects = list(ProyectoRED.objects.all())
    return HttpResponse(serialize('json', vLstObjects), content_type="application/json")

@csrf_exempt
def getRecurso(request):
    vLstObjects = list(Recurso.objects.all())
    return HttpResponse(serialize('json', vLstObjects), content_type="application/json")

@csrf_exempt
def getRED(request):
    vLstObjects = list(RED.objects.all())
    return HttpResponse(serialize('json', vLstObjects), content_type="application/json")

@csrf_exempt
def marcarVersion(request,id):
    NotificacionVersionFinal = 5

    if request.method == 'POST':
        tokenStatus = getTokenStatus(request)
        if(not tokenStatus):
            return HttpResponse('Invalid Token')
        version = get_object_or_404(Version, id=id)

        otherVersions = get_list_or_404(Version, red_id = version.red_id)
        for v in otherVersions:
            v.es_final=False
            v.save()

        version.es_final = True
        version.save()

        result = createNotification(version.red_id, NotificacionVersionFinal)  # para crear la notificacion
        print("notificacion:", result)

        if result != {"mensaje": 'La notificacion ha sido creada'}:
            return JsonResponse('No fue posible crear la notificacion', safe=False)

        return JsonResponse(str(id), safe=False)    
    return HttpResponseNotFound()     
    
def buscarRed(request):

    #verificar si el usuario esta logueado
    tokenStatus = getTokenStatus(request)
    if(not tokenStatus):
        return HttpResponseForbidden('Invalid Token')

    #traer el perfil del usuario que esta logueado
    token = request.META['HTTP_AUTHORIZATION']
    token = token.replace('Token ', '')
    userId = Token.objects.get(key=token).user.id

    if request.method == 'GET':
        fstart = request.GET.get("fstart")
        fend = request.GET.get("fend")
        text = request.GET.get("text")

        usuario = User.objects.get(pk=userId)
        perfil = Perfil.objects.get(usuario=usuario)
        roles_asignado = RolAsignado.objects.filter(usuario=perfil)

        redsAsignados = RED.objects.filter(rolasignado__in=roles_asignado).values() 
        
        #crear una querry vacia
        q = RED.objects.filter() 

        if text:
            q = q.filter(Q(nombre__contains=text) | Q(nombre_corto__contains=text)  | Q(descripcion__contains=text) | Q(metadata__tag=text))
        
        if fend:
            q = q.filter(fecha_cierre__lte = fend)
        
        if fstart:
            q = q.filter(fecha_inicio__gte = fstart)

        listOfReds = list(q.values())

        #asignar si esta asignado el red al usuario o no
        for red in listOfReds:
            if(any(redOfList['id'] == red['id'] for redOfList in redsAsignados)):
                red['asignado']=True
            else:
                red['asignado']=False
                
        return JsonResponse(listOfReds,safe=False)
    return HttpResponseNotFound()

@csrf_exempt
def getAsignaciones(request):
    data = list(RolAsignado.objects.all())
    serializer = RolAsignadoSerializer(data, many=True)
    return JsonResponse({'context': serializer.data}, safe=True)

@csrf_exempt
def versiones(request):
    #verificar si el usuario esta logueado
    tokenStatus = getTokenStatus(request)
    if(not tokenStatus):
        return HttpResponseForbidden('Invalid Token')

    #traer el perfil del usuario que esta logueado
    token = request.META['HTTP_AUTHORIZATION']
    token = token.replace('Token ', '')
    userId = Token.objects.get(key=token).user.id

    if request.method == 'POST':
        data = jsonUser = json.loads(request.body)
        es_final = False

        imagen = data['imagen']
        archivos = data['archivos']
        redId = data['redId']
        fecha_creacion = datetime.today().date()
        idRecursos = data['recursos']

        red = get_object_or_404(RED, id=redId)
        oldVersions = Version.objects.filter(red__id=redId)
        numero = 1

        if len(oldVersions) > 0:
            numero = max((v.numero for v in oldVersions)) + 1

        recursos = Recurso.objects.filter(id__in=idRecursos)
        creado_por=Perfil.objects.get(usuario__id=userId)

        version = createVersion(es_final, imagen, archivos, red, numero, creado_por, fecha_creacion)

        newrecursos=[]
        for i in recursos:
            aei = Recurso.objects.create(nombre=i.nombre, archivo=i.archivo,thumbnail=i.thumbnail, fecha_creacion=i.fecha_creacion, fecha_ultima_modificacion=i.fecha_ultima_modificacion, tipo=i.tipo, descripcion=i.descripcion, autor=i.autor, usuario_ultima_modificacion=i.usuario_ultima_modificacion)
            aei.metadata.set(i.metadata.all())
            newrecursos.append(aei)

        version.recursos.set(newrecursos)
        version.save()

        serializer=VersionSerializer(version, many=False)

        return JsonResponse(serializer.data, safe=True)
    return HttpResponseNotFound()

def createVersion(es_final, imagen, archivos, red, numero, creado_por, fecha_creacion):
    version = Version.objects.create(
        es_final=es_final,
        imagen=imagen,
        archivos=archivos,
        red=red,
        numero=numero,
        creado_por=creado_por,
        fecha_creacion=fecha_creacion,
    )
    return version

@csrf_exempt
def getRecursosRed(request, id):
    red = get_object_or_404(RED, id=id)

    serializer = RecursoSerializer(red.recursos, many=True)
    return JsonResponse({'context':serializer.data}, safe=True)

@csrf_exempt
def getVerVersion(request, id):
    tokenStatus = getTokenStatus(request)
    if(not tokenStatus):
        return HttpResponse('Invalid Token')
    version = get_object_or_404(Version, id=id)

    serializer = VersionSerializer_v(version, many=False)
    return JsonResponse(serializer.data, safe=True)

@csrf_exempt
def getVerVersionR(request, id):
    tokenStatus = getTokenStatus(request)
    if(not tokenStatus):
        return HttpResponse('Invalid Token')
    version = get_object_or_404(Version, id=id)

    serializer = RecursoSerializer(version.recursos, many=True)
    return JsonResponse({'context':serializer.data}, safe=True)


@csrf_exempt
def getVersionesRED(request, id):
    tokenStatus = getTokenStatus(request)
    if(not tokenStatus):
        return HttpResponse('Invalid Token')
    try:
        red = RED.objects.get(pk=id)
    except:
        raise Http404('No existe un RED con id '+str(id))
    data = Version.objects.filter(red=red).order_by('numero')
    serializer = VersionSerializer(data, many=True)
    return JsonResponse({'context': serializer.data}, safe=True)

@csrf_exempt
def comentarioExistente(request,id_v, id_r):
    tokenStatus = getTokenStatus(request)
    if(not tokenStatus):
        return HttpResponse('Invalid Token')

    if request.method == 'POST':
        data = jsonUser = json.loads(request.body)
        version = get_object_or_404(Version, id=id_v)
        recurso = get_object_or_404(Recurso, id=id_r)
        contenido = data['contenido']
        fecha_creacion = datetime.today()
        usuario=Perfil.objects.get(usuario__id=data['usuario'])
        idTabla = data['idTabla']

        comentario_multimedia=ComentarioMultimedia.objects.get(id=idTabla)

        comentario = Comentario.objects.create(
            contenido=contenido,
            usuario=usuario,
            fecha_creacion=fecha_creacion,
            recurso=recurso,
            version=version,
            comentario_multimedia=comentario_multimedia
        )
        comentario.save()

        serializer=ComentarioSerializer(comentario, many=False)

        return JsonResponse(serializer.data, safe=True)
    return HttpResponseNotFound()


@csrf_exempt
def comentarioNuevo(request,id_v, id_r):
    NotificacionComentario = 2

    tokenStatus = getTokenStatus(request)
    if(not tokenStatus):
        return HttpResponse('Invalid Token')

    #traer el perfil del usuario que esta logueado
    token = request.META['HTTP_AUTHORIZATION']
    token = token.replace('Token ', '')
    userId = Token.objects.get(key=token).user.id

    if request.method == 'POST':
        data = jsonUser = json.loads(request.body)
        version = get_object_or_404(Version, id=id_v)
        recurso = get_object_or_404(Recurso, id=id_r)
        contenido = data['contenido']
        fecha_creacion = datetime.date.today()
        usuario=Perfil.objects.get(usuario__id=userId)
        x1=data['x1']
        x2=data['x2']
        y1=data['y1']
        y2=data['y2']


        comentario_multimedia=ComentarioMultimedia.objects.create(x1=x1,y1=y1,x2=x2,y2=y2)

        comentario = Comentario.objects.create(
            contenido=contenido,
            usuario=usuario,
            fecha_creacion=fecha_creacion,
            recurso=recurso,
            version=version,
            comentario_multimedia=comentario_multimedia
        )
        comentario.save()

        serializer=ComentarioSerializer(comentario, many=False)

        result = createNotification(id_r, NotificacionComentario)  # para crear la notificacion
        print("notificacion:", result)

        if result != {"mensaje": 'La notificacion ha sido creada'}:
            return JsonResponse({"error":'No fue posible crear la notificacion'}, safe=True)

        return JsonResponse(serializer.data, safe=True)
    return HttpResponseNotFound()

@csrf_exempt
def getListaComentarios(request,id_v, id_r):
    tokenStatus = getTokenStatus(request)
    if(not tokenStatus):
        return HttpResponse('Invalid Token')

    version = get_object_or_404(Version, id=id_v)
    recurso = get_object_or_404(Recurso, id=id_r)

    data=Comentario.objects.filter(version=version, recurso=recurso).order_by('-fecha_creacion')
    serializer=ComentarioSerializer(data, many=True)
    return JsonResponse({'context': serializer.data}, safe=True)

@csrf_exempt
def verAvanceProyectoConectate(request,idProyecto):
    tokenStatus = getTokenStatus(request)
    if(not tokenStatus):
        return HttpResponse('Invalid Token')

    reds = RED.objects.filter(proyecto_conectate__id=idProyecto)

    alertaReds = []
    normalReds = []
    cerradosReds = []

    for red in reds:
        fases = HistorialFases.objects.filter(red__id=red.id).order_by("-fecha_cambio")

        if(len(fases)>0):
            historialFase = fases[0]
            fase=historialFase.fase.nombre_fase
            inicio_fase=historialFase.fecha_cambio
            ultima_modificacion=historialFase.fecha_cambio
        else:
            fase=""
            inicio_fase=""
            ultima_modificacion=""

        if fase.lower()=="cerrado":
            cerradosReds.append(
                {
                    "idRed":red.id,
                    "nombre":red.nombre,
                    "nombre_corto":red.nombre_corto,
                    "fecha_inicio":red.fecha_inicio,
                })
        elif esActivo(red):
            normalReds.append(
                {
                    "idRed":red.id,
                    "nombre":red.nombre,
                    "nombre_corto":red.nombre_corto,
                    "fecha_inicio":red.fecha_inicio,
                    "fase":fase,
                    "inicio_fase":inicio_fase,
                    "ultima_modificacion":ultima_modificacion
                })

        else:            
            alertaReds.append(
                {
                    "idRed":red.id,
                    "nombre":red.nombre,
                    "nombre_corto":red.nombre_corto,
                    "fecha_inicio":red.fecha_inicio,
                    "fase":fase,
                    "inicio_fase":inicio_fase,
                    "ultima_modificacion":ultima_modificacion
                })
    
    return JsonResponse(
        {
            'redsCount': len(reds),
            'alertaRedsCount':len(alertaReds),
            'normalRedsCount': len(normalReds),
            'cerradosRedsCount': len(cerradosReds),
            'alertaReds':list(alertaReds),
            'normalReds': list(normalReds),
            'cerradosReds':list(cerradosReds),
        }, safe=True)
        
#trae todos los asignados de un red
def getAllAsignados(request,redId):
    tokenStatus = getTokenStatus(request)
    if(not tokenStatus):
        return HttpResponse('Invalid Token')

    asignados = RolAsignado.objects.filter(red__id=redId)
    personasAsignadas = []

    for asignado in asignados:
        personasAsignadas.append(asignado.usuario.usuario.first_name + ' ' + asignado.usuario.usuario.last_name)

    return JsonResponse(list(personasAsignadas), safe=False)

def getTokenStatus(request):
    token = request.META['HTTP_AUTHORIZATION']
    token = token.replace('Token ', '')
    try:
        tokenStatus = Token.objects.get(key=token).user.is_active
    except Token.DoesNotExist:
        tokenStatus = False
    
    return tokenStatus

#verifica si el red esta activo
def esActivo(red):
    if not red.fecha_creacion:
        return False

    redCreacionDelta = datetime.now().date() - red.fecha_creacion

    if(redCreacionDelta.days > 7):
        return True

    comentarios = Comentario.objects.filter(version__red__id=red.id)

    for c in comentarios:
        comentarioCreacionDelta = datetime.now().date() - c.fecha_creacion.date()
        if(comentarioCreacionDelta.days < 7):
            return True
    
    return False

#Obtiene la lista de Proyectos RED asociados al RED
@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def getListaProyectosred(request, id):

    token = request.META['HTTP_AUTHORIZATION']
    token = token.replace('Token ', '')
    try:
        TokenStatus = Token.objects.get(key=token).user.is_active
    except Token.DoesNotExist:
        TokenStatus = False
    if not TokenStatus:
        return HttpResponseForbidden('Invalid Token')


    try:
        red = RED.objects.get(pk=id)
    except:
        raise Http404('No existe un RED con id '+str(id))
    data = ProyectoRED.objects.filter(red=red)
    serializer = ProyectoREDSerializer(data, many=True)
    return JsonResponse({'context': serializer.data}, safe=True)

def getTokenStatus(request):
    token = request.META['HTTP_AUTHORIZATION']
    token = token.replace('Token ', '')
    try:
        tokenStatus = Token.objects.get(key=token).user.is_active
    except Token.DoesNotExist:
        tokenStatus = False
    
    return tokenStatus


#Luego de subir RED se genera una notificación al proyecto
def generarNotificacionSubirRed(request, id_conectate):
    NotificacionSubirRed = 3
    result = createNotification(str(id_conectate), NotificacionSubirRed)
    print("notificacion", result)

    if result != {"mensaje": 'La notificacion ha sido creada'}:
        error = 'No fue posible crear la notificacion'
        return HttpResponseBadRequest(content=error, status=status.HTTP_400_BAD_REQUEST)

    return HttpResponse(json.dumps(result))

