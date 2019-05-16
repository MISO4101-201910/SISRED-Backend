from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json, decimal
from django.http import JsonResponse
from sisred_app.models import RED, ProyectoRED, RolAsignado, Perfil, Metadata, Recurso, ProyectoConectate, Version, Comentario, ComentarioMultimedia, ComentarioVideo
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.models import User

from datetime import datetime, timedelta

from django.utils.formats import get_format
from django.utils.dateparse import parse_date

# Create your views here.

# Metodo para agregar un proyecto RED
@csrf_exempt
def post_proyecto_red(request):
    if request.method == 'POST':
        json_proyecto_red = json.loads(request.body)
        red = RED.objects.get(id=json_proyecto_red['RED'])
        nuevo_proyecto_red = ProyectoRED(
            nombre=json_proyecto_red['nombre'],
            tipo=json_proyecto_red['tipo'],
            carpeta=json_proyecto_red['carpeta'],
            descripcion=json_proyecto_red['descripcion'],
            autor=json_proyecto_red['autor'],
            red=red)
        nuevo_proyecto_red.save()
        return HttpResponse(serializers.serialize("json", [nuevo_proyecto_red]))

# Metodo para obtener detalle de las personas asignadas al RED
@csrf_exempt
def get_detallered_personas(request):
    if request.method == 'GET':
        red = RED.objects.get(id=request.GET['RED'])
        personas = RolAsignado.objects.filter(red=red)
        respuesta = []
        for persona in personas:
            usuario = persona.usuario.usuario
            nombre= usuario.first_name + " " + usuario.last_name
            rol = persona.rol.nombre
            respuesta.append({"name": nombre, "rol": rol})
        return HttpResponse(json.dumps(respuesta), content_type="application/json")

# Metodo para obtener detalle de proyectos RED
@csrf_exempt
def get_detallered_proyectosred(request):

    if request.method == 'GET':
        red = RED.objects.get(id=request.GET['RED'])
        proyectos = ProyectoRED.objects.filter(red=red)
        respuesta = []
        for pro in proyectos:
            respuesta.append({"id": pro.pk, "name": pro.nombre, "autor": pro.autor, "typeFile": pro.tipo, "createdDate": red.fecha_creacion.strftime('%Y/%m/%d'),"description":pro.descripcion})
        return HttpResponse(json.dumps(respuesta), content_type="application/json")


# Metodo para obtener detalle de los metadatas del RED
@csrf_exempt
def get_detallered_metadata(request):
    if request.method == 'GET':
        red = RED.objects.get(id=request.GET['RED'])
        metas = Metadata.objects.filter(red=red)
        respuesta = []
        for met in metas:
            respuesta.append({"id": met.pk, "tag": met.tag})
        return HttpResponse(json.dumps(respuesta), content_type="application/json")

# Metodo para obtener detalle de los recursos asociados al RED
@csrf_exempt
def get_detallered_recursos(request):
    if request.method == 'GET':
        red = RED.objects.get(id=request.GET['RED'])
        recursos = Recurso.objects.filter(red=red)
        respuesta = []
        for re in recursos:
            respuesta.append({"id": re.pk, "name": re.nombre, "typeFormat": re.tipo})
        return HttpResponse(json.dumps(respuesta), content_type="application/json")

# Metodo para obtener detalle del RED
@csrf_exempt
def get_detallered(request):
    if request.method == 'GET':
        red = request.GET['RED']
        red = RED.objects.get(id=red)
        nombreRed = red.nombre
        url = 'conectatePrueba.com/'+nombreRed
        status = 'No tiene'
        nombreProject = red.proyecto_conectate.nombre
        fase = red.fase
        """historiales = HistorialEstados.objects.filter(red=red.pk)

        if len(historiales) > 1:
            ultimo = historiales[0]
            ultimoDate = datetime.date(datetime(1800,1,1))
            for hist in historiales :
                datAct = hist.fecha_cambio
                actDate = hist.fecha_cambio
                if datAct > ultimoDate:
                    ultimo = hist
                    ultimoDate = actDate
            status = ultimo.estado.nombre_estado"""
        fase_json = {"idConectate": fase.id_conectate, "nombreFase": fase.nombre_fase}
        respuesta = {"nombreRed": nombreRed, "nombreProject":nombreProject, "status":status, "url": url, "fase": fase_json}

    return HttpResponse(json.dumps(respuesta), content_type="application/json")

@csrf_exempt
def get_reds_asignados(request, id):
    if request.method == 'GET':
        perfil = Perfil.objects.get(id_conectate=id)
        reds_asignados = []
        rolesAsignado = RolAsignado.objects.filter(usuario=perfil)
        for rolAsignado in rolesAsignado:
            red = rolAsignado.red
            rol = rolAsignado.rol.nombre
            reds_asignados.append(
                {"idRed": red.pk, "nombreRed": red.nombre_corto, "rol": rol})
        respuesta = {
            "redsAsignados": reds_asignados}
        return JsonResponse(respuesta, safe=False)


#Metodo para obtener los datos de una version dado su id y el RED asociado
@csrf_exempt
def get_version(request):
    if request.method == 'GET':
        id = request.GET['id']
        version = Version.objects.get(pk=id)
        red = version.red
        return HttpResponse(serializers.serialize("json", [red, version]))


#Metodo para obtener dado el id de una version, sus recursos
@csrf_exempt
def get_recursos_by_version(request):
    if request.method == 'GET':
        id = request.GET['id']
        version = Version.objects.get(pk=id)
        recursos = Recurso.objects.filter(version=version)
        return HttpResponse(serializers.serialize("json", recursos))


# Metodo para obtener comentarios del recurso video
@csrf_exempt
def get_comentarios_video(request, id):
    if request.method == 'GET':
        print("Obteniendo comentarios del ID " + str(id))
        respuesta = []
        multimedias=[]
        try:
            recurso = Recurso.objects.get(pk=id)
            comentarios = Comentario.objects.filter(recurso=recurso)
            for comentario in comentarios:
                if comentario.comentario_multimedia not in multimedias:
                    multimedias.append(comentario.comentario_multimedia)
            for multimedia in multimedias:
                comentarios = Comentario.objects.filter(comentario_multimedia=multimedia)
                comentariosVideo = ComentarioVideo.objects.get(comentario_multimedia=multimedia.pk)
                rangeEsp = {"start": comentariosVideo.seg_ini, "end": comentariosVideo.seg_fin}

                shape = None if (multimedia.x1 or multimedia.x2 or multimedia.y1 or multimedia.y2) is None else {
                             "x1": decimal.Decimal(multimedia.x1),
                             "y1": decimal.Decimal(multimedia.y1),
                             "x2": decimal.Decimal(multimedia.x2),
                             "y2": decimal.Decimal(multimedia.y2)}

                comentEsp = []
                for comEsp in comentarios:
                    usuario = comEsp.usuario.usuario
                    nombreUsuario = usuario.first_name + " " + usuario.last_name
                    idUsuario = usuario.pk
                    metaVideo = {"datetime": comEsp.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'), "user_id": idUsuario,
                                 "user_name": nombreUsuario}
                    comentEsp.append({"id": str(comEsp.pk), "meta": metaVideo, "body": comEsp.contenido})
                respuesta.append({"id": multimedia.pk, "range": rangeEsp, "shape": shape, "comments": comentEsp})
                print(respuesta)
            return HttpResponse(json.dumps(respuesta, default=decimal_default), content_type="application/json")
        except Exception as ex:
            print(ex)
            print("ERROR OBTENIENDO LOS COMENTARIOS DEL VIDEO " + str(ex))
        return HttpResponse(json.dumps(respuesta, default=decimal_default), content_type="application/json")

# Metodo para agregar comentarios del recurso video
@csrf_exempt
def post_comentarios_video(request, idVersion, idRecurso):
    if request.method == 'POST':
        print("Persistiendo Comentarios Video en BD")
        commentsDetails = json.loads(request.body)
        print(commentsDetails)
        for commentData in commentsDetails:
            idMultimedia = commentData['id']
            comentarioMultimedia = None
            commentShape = commentData['shape']
            x1 = None
            y1 = None
            x2 = None
            y2 = None
            if (commentShape != None):
                x1 = commentData['shape']['x1']
                y1 = commentData['shape']['y1']
                x2 = commentData['shape']['x2']
                y2 = commentData['shape']['y2']

            # Validar si el ID ya existe (Pues se envian todos los comentarios) - En caso de que si, no se guarda.

            #########  COMENTARIO MULTIMEDIA ###########
            if (type(idMultimedia) is int): #Ya que la libreria envia unas cadenas
                comentarioMultimedia = ComentarioMultimedia.objects.filter(pk=idMultimedia)
                if comentarioMultimedia:
                    comentarioMultimedia = comentarioMultimedia[0]
            else:
                comentarioMultimedia = ComentarioMultimedia(
                    x1=x1,
                    y1=y1,
                    x2=x2,
                    y2=y2
                )
                comentarioMultimedia.save()
            print("ComentarioMultimediaData->")
            print(comentarioMultimedia)

            rangeStart = commentData['range']['start']
            rangeStop = None
            try:
                rangeStop = commentData['range']['stop']
            except Exception as ex:
                rangeStop = commentData['range']['end']

            #########  COMENTARIO VIDEO ###########

            comentarioVideo = ComentarioVideo.objects.filter(seg_ini=rangeStart).filter(seg_fin=rangeStop).filter(comentario_multimedia=comentarioMultimedia)
            print(comentarioVideo)
            if not comentarioVideo:
                comentarioVideo = ComentarioVideo(
                    seg_ini=rangeStart,
                    seg_fin=rangeStop + 1,
                    comentario_multimedia=comentarioMultimedia
                )
                print("Creando Comentario Video")
                comentarioVideo.save()

            #########  COMENTARIO  ###########
            comentarios = commentData['comments']
            print("Comentarios->")
            for comment in comentarios:
                idComentario = comment['id']
                commentBody = comment['body']
                userID = comment['meta']['user_id']
                dateTime = comment['meta']['datetime']
                print("Validando comentario ID: "+str(idComentario))
                try:
                    if (isNum(idComentario)):  # Ya que la libreria envia unas cadenas
                        comentario = Comentario.objects.get(pk=idComentario)
                        print("Se ignora ya que existe -> "+comentario.contenido)
                        continue
                    else:
                        try:
                            comentario = Comentario.objects.get(id_video_libreria=idComentario)
                        except Exception as ex:
                            comentario = None
                            print("No existe")
                        if(comentario == None):
                            print("Creando Nuevo objeto")
                            version = Version.objects.get(pk=idVersion)
                            recurso = Recurso.objects.get(pk=idRecurso)
                            usuario = Perfil.objects.get(pk=userID)

                            comentario = Comentario(
                                id_video_libreria=idComentario,
                                contenido=commentBody,
                                version=version,
                                recurso=recurso,
                                usuario=usuario,
                                comentario_multimedia=comentarioMultimedia
                            )
                            print(comment)
                            print(comentario)
                            comentario.save()
                except Exception as ex:
                    print(ex)

        return HttpResponse()

# Metodo para obtener la url del recurso video
@csrf_exempt
def get_url_recurso_video(request, id):
    if request.method == 'GET':
        print("Obteniendo url del recurso con ID " + str(id))
        respuesta = []
        try:
            recurso = Recurso.objects.get(pk=id)
            respuesta.append({"url": recurso.archivo})
            return HttpResponse(json.dumps(respuesta), content_type="application/json")
        except Exception as ex:
            print(ex)
            print("ERROR OBTENIENDO LA URL DEL VIDEO " + str(ex))
        return HttpResponse(json.dumps(respuesta), content_type="application/json")


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def isNum(data):
    try:
        int(data)
        return True
    except ValueError:
        return False


# Metodo para obtener las versiones asignadas a un usuario
@csrf_exempt
def get_versiones_revision(request, id):
    if request.method == 'GET':
        usuario = User.objects.get(pk=id);
        perfil = Perfil.objects.get(usuario=usuario);
        rolesAsignados = RolAsignado.objects.filter(usuario=perfil);
        respuesta = []
        for rol in rolesAsignados:
            versiones = Version.objects.filter(red=rol.red)
            for ver in versiones:
                respuesta.append({"versionId": ver.pk,"redId": rol.red.pk, "rol": rol.rol.nombre, "red": rol.red.nombre, "fecha": ver.date.strftime("%d/%m/%Y")})
    return HttpResponse(json.dumps(respuesta), content_type="application/json")
