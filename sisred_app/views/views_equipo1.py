import json

from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse, HttpResponseNotFound
from rest_framework import  status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound

from rest_framework.response import Response
import json
import datetime
import requests
from datetime import datetime
from rest_framework.authtoken.models import Token

from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from sisred_app.models import Recurso, RED, Perfil, Fase, HistorialFases, Version, Comentario, ComentarioMultimedia
from sisred_app.serializer import RecursoSerializer, RecursoSerializer_post, RecursoSerializer_put, \
    REDSerializer, ComentarioCierreSerializer, comentariosHijosSerializer, comentarioMultimediaSerializer, \
    ComentariosPDFSerializer, VersionSerializer


#Autor: Francisco Perneth
#Fecha: 2019-03-30
#Parametros:
#    Request -> Datos de la solicitud
#Descripcion:
#   Permite registrar un recurso
@api_view(['POST'])
def recurso_post(request):
    serializer = RecursoSerializer_post(data=request.data)
    if serializer.is_valid():
        autor = Perfil.objects.get(id=int(request.data.get("autor")))

        rec = Recurso.objects.create(nombre=request.data.get('nombre'),
                                     archivo=request.data.get('archivo'),
                                     thumbnail=request.data.get('thumbnail'),
                                     descripcion=request.data.get('descripcion'),
                                     tipo=request.data.get('tipo'),
                                     autor=autor,
                                     usuario_ultima_modificacion=autor
                                     )
        rec.fecha_creacion=datetime.datetime.now()
        rec.fecha_ultima_modificacion = datetime.datetime.now()
        rec.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#Autor: Francisco Perneth
#Fecha: 2019-03-30
#Parametros:
#    Request -> Datos de la solicitud
#    id -> id del recurso para obtener
#Descripcion:
#   Permite consultar un recurso mediante su identificador (id)
@api_view(['GET'])
def recurso_get(request,id):
    recurso = Recurso.objects.filter(id=id).first()
    if(recurso==None):
        raise NotFound(detail="Error 404, recurso not found", code=404)
    serializer = RecursoSerializer(recurso)
    return Response(serializer.data)

#Autor: Francisco Perneth
#Fecha: 2019-03-30
#Parametros:
#    Request -> Datos de la solicitud
#Descripcion:
#   Permite modificar un recurso mediante.
#   los datos permitios a modificar son: nombre y descripción. la fecha y usaurio de la modificación son valores tomados de
#   el usuario que está realizando la operación (auntenticado en el sistema) y la fecha del sistema.
@api_view(['PUT'])
def recurso_put(request):
    serializer = RecursoSerializer_put(data=request.data)
    if serializer.is_valid():
        id=int(request.data.get("id"))
        ItemRecurso = Recurso.objects.filter(id=id).first()
        if (ItemRecurso==None):
            raise NotFound(detail="Error 404, recurso not found", code=404)
        ItemRecurso.nombre=request.data.get("nombre")
        ItemRecurso.descripcion=request.data.get("descripcion")
        Per=Perfil.objects.get(id=int(request.data.get("usuario_ultima_modificacion")))
        if (Per!=None):
            ItemRecurso.usuario_ultima_modificacion=Per
        ItemRecurso.fecha_ultima_modificacion=datetime.datetime.now()
        ItemRecurso.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#Autor: Ramiro Vargas
#Fecha: 2019-03-30
#Parametros:
#    Request -> Datos de la solicitud
#    id -> id del recurso para consultar
#Descripcion:
#   Permite consultar  la información de un RED, especialmente información del avance
@api_view(['GET', 'POST'])
def fase_byid(request,id):
    if request.method == 'GET':
        red = RED.objects.filter(id=id)
        if (red == None):
            raise NotFound(detail="Error 404, recurso not found", code=404)
        print(red)
        serializer = REDSerializer(red, many=True)
        return Response(serializer.data)


#Autor:         Adriana Vargas
#Fecha:         2019-04-11
#Parametros:    request -> Datos de la solicitud
#               numero_identificacion -> número de identificación del usuario
#Descripcion:   Permite consultar la información de un usuario con su número de identificación y actualizar el estado del mismo en sisred

@api_view(['GET', 'PUT'])
def getUserByIdentification(request, numero_identificacion):

    try:
        perfil = Perfil.objects.get(numero_identificacion=numero_identificacion)
    except Perfil.DoesNotExist:
        raise NotFound(detail="Error 404, User not found", code=404)

    usuario = User.objects.get(username=perfil.usuario)

    if request.method == 'GET':

        return Response(usuarioPerfilJson(perfil, usuario))

    elif request.method == 'PUT':

        perfil.estado_sisred = 1
        perfil.save()

        return Response(usuarioPerfilJson(perfil, usuario))

def usuarioPerfilJson(perfil, usuario):

    usuario_perfil = []

    usuario_perfil.append({"username": usuario.username, "email": usuario.email,
                           "first_name": usuario.first_name, "lastname": usuario.last_name,
                           "numero_identificacion": perfil.numero_identificacion,
                           "estado": perfil.estado, "estado_sisred": perfil.estado_sisred})

    return usuario_perfil


#Autor:         Ramiro Vargas
#Fecha:         2019-04-22
#Parametros:    id_conectate -> Id del RED
#Descripcion:   Funcionalidad para actualizar cuando un RED esta listo para revision

@api_view(['GET','PUT'])
def getREDByIdentification(request, id_conectate):
    reds=[]
    try:
        red = RED.objects.get(id_conectate=id_conectate)
    except RED.DoesNotExist:
        raise NotFound(detail="Error 404, User not found", code=404)

    if request.method == 'PUT':

        red.listo=True
        red.save()
        reds.append({"nombre": red.nombre, "nombre_corto": red.nombre_corto,
                    "descripcion": red.descripcion, "fecha_inicio": red.fecha_inicio,
                    "fecha_cierre": red.fecha_cierre,
                    "fecha_creacion": red.fecha_creacion, "porcentaje_avance": red.porcentaje_avance,
                    "tipo": red.tipo, "solicitante": red.solicitante,
                    "horas_estimadas": red.horas_estimadas, "horas_trabajadas": red.horas_trabajadas,
                    "proyecto_conectate_id": red.proyecto_conectate_id,
                    "listo": True})
        return Response(reds)
    if request.method == 'GET':
        return Response(makeReds(red))

def makeReds(red):

    reds = []

    reds.append({"listo": red.listo})

    return reds

#Autor:         Adriana Vargas
#Fecha:         2019-05-08
#Parametros:    idRed -> Id del RED en el sistema de PyS
#               idActual -> Id de la fase actual del RED
#               idFase -> Id de la nueva fase del RED
#Descripcion:   Funcionalidad para sincronizar el cambio de fase con el sistema de PyS

def sincronizarFases(idRed, idActual, idFase):
    url = 'http://sincronizar-red.mocklab.io/cambioFase'
    data = {"id_conectate": idRed, "fase_actual": idActual, "nueva_fase": idFase}
    response = requests.post(url, data=json.dumps(data))
    print(response)

    return Response(response)

#Autor:         Adriana Vargas
#Fecha:         2019-05-09
#Parametros:    contenido -> Comentario de cierre
#               version -> Versión a la que pertenece el comentario
#               usuario -> Usuario que realizó el comentario
#               comentario_multimedia -> Id de la tabla ComentarioMultimedia
#               fecha_creacion -> fecha en que se realizó el comentario
#               esCierre -> Bandera para identificar si el comentario es de cierre o no
#Descripcion:   Funcionalidad para almacenar el comentario de cierre en un archivo de PDF

@api_view(['POST'])
def comentario_cierre_post(request):
    '''token = request.META['HTTP_AUTHORIZATION']
    token = token.replace('Token ', '')
    try:
        TokenStatus = Token.objects.get(key=token).user.is_active
    except Token.DoesNotExist:
        TokenStatus = False
    if TokenStatus == True:
        reqUser = Token.objects.get(key=token).user.id'''

    reqUser = 1

    if request.method == 'POST':
        data = json.loads(request.body)

        contenido = data['contenido']
        version = Version.objects.get(id=data['version'])
        usuario = Perfil.objects.get(usuario__id=reqUser)
        comentario_multimedia = ComentarioMultimedia.objects.get(id=data['comentario_multimedia'])
        fecha_creacion = datetime.now()
        esCierre = data['esCierre']

        comentario = Comentario.objects.create(
            contenido=contenido,
            version=version,
            usuario=usuario,
            comentario_multimedia=comentario_multimedia,
            fecha_creacion=fecha_creacion,
            esCierre=esCierre
        )
        comentario.save()

        serializer=ComentarioCierreSerializer(comentario, many=False)

        return JsonResponse(serializer.data, safe=True)
    return HttpResponseNotFound()

#Autor:         Adriana Vargas
#Fecha:         2019-05-09
#Parametros:    id -> Id de comentario multimedia
#               cerrado -> Identificador para determinar si el comentario fue cerrado
#               resuelto -> Identificador para determinar si el comentario fue resuelto
#Descripcion:   Funcionalidad para actualizar los estados del comentario base una vez ha sido cerrado

@api_view(['PUT'])
def comentario_cierre_put(request, id):
        if request.method == 'PUT':

                comentario = json.loads(request.body)
                comentario_base = Comentario.objects.filter(comentario_multimedia=id).earliest('fecha_creacion')

                comentario_base.cerrado = comentario['cerrado']
                comentario_base.resuelto = comentario['resuelto']
                comentario_base.save()

                serializer = ComentarioCierreSerializer(comentario_base, many=False)

                return JsonResponse(serializer.data, safe=True)
        return HttpResponseNotFound()

# Autor:         Adriana Vargas
# Fecha:         2019-05-09
# Parametros:    id -> Identificador del comentario multimedia
# Descripcion:   Funcionalidad para obtener el comentario base a partir de un comentario del hilo

@api_view(['GET'])
def comentario_base_get(request,id):

    comentario_base = Comentario.objects.filter(comentario_multimedia=id).earliest('fecha_creacion')

    if(comentario_base==None):
        raise NotFound(detail="Error 404, Comment not found", code=404)
    serializer = ComentarioCierreSerializer(comentario_base)
    return Response(serializer.data)
  
#Autor: Francisco Perneth
#Fecha: 2019-05-09
#Parametros:
#    Request -> Datos de la solicitud
#    id -> id de la version
#Descripcion:
#   Permite consultar una version del RED mediante su identificador (id)

@api_view(['GET'])
def comentario_pdf_get(request,id):
    comentarios = Comentario.objects.filter(version=id).order_by("id")
    if(len(comentarios)==0):
        vers=Version.objects.filter(id=id)
        if (vers != None):
            Resp = VersionSerializer(vers[0])
            return Response(Resp.data)
        else:
            raise NotFound(detail="Error 404, recurso not found", code=404)
    else:
        filtered = [x for x in comentarios if x.EsPadre]
        serializer = ComentariosPDFSerializer(filtered, many=True)
        return Response(serializer.data)

#Autor:         Adriana Vargas
#Fecha:         2019-05-10
#Parametros:    contenido -> Comentario
#               version -> Versión a la que pertenece el comentario
#               usuario -> Usuario que realizó el comentario
#               comentario_multimedia -> Id de la tabla ComentarioMultimedia
#               fecha_creacion -> fecha en que se realizó el comentario
#Descripcion:   Funcionalidad para guardar un comentario en un archivo de PDF

@api_view(['POST'])
def comentario_pdf_post(request):
    '''token = request.META['HTTP_AUTHORIZATION']
    token = token.replace('Token ', '')
    try:
        TokenStatus = Token.objects.get(key=token).user.is_active
    except Token.DoesNotExist:
        TokenStatus = False
    if TokenStatus == True:
        reqUser = Token.objects.get(key=token).user.id'''

    reqUser = 1

    if request.method == 'POST':
        data = json.loads(request.body)

        contenido = data['contenido']
        version = Version.objects.get(id=data['version'])
        usuario = Perfil.objects.get(usuario__id=reqUser)
        fecha_creacion = datetime.now()

        try:
            comentario_multimedia = ComentarioMultimedia.objects.get(id=data['comentario_multimedia'])
        except ComentarioMultimedia.DoesNotExist:
            comentario_multimedia = None

        if comentario_multimedia == None:

            x1 = data['x1']
            x2 = data['x2']
            y1 = data['y1']
            y2 = data['y2']

            comentario_multimedia = ComentarioMultimedia.objects.create(x1=x1, y1=y1, x2=x2, y2=y2)

        comentario = Comentario.objects.create(
            contenido=contenido,
            version=version,
            usuario=usuario,
            comentario_multimedia=comentario_multimedia,
            fecha_creacion=fecha_creacion
        )
        comentario.save()

        serializer=comentariosHijosSerializer(comentario, many=False)

        return JsonResponse(serializer.data, safe=True)
    return HttpResponseNotFound()
