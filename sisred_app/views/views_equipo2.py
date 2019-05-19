from django.shortcuts import get_object_or_404,get_list_or_404
from django.core import serializers
from django.core.serializers import serialize
from rest_framework import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, Http404
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from sisred_app.models import ProyectoRED, Recurso, RED, RolAsignado, Perfil, Rol, ProyectoConectate, Version, Comentario, ComentarioMultimedia
from django.contrib.auth.models import User
from sisred_app.serializer import RecursoSerializer
import datetime
import json

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
    if request.method == 'POST':
        version = get_object_or_404(Version, id=id)

        otherVersions = get_list_or_404(Version, red_id = version.red_id)
        for v in otherVersions:
            v.es_final=False
            v.save()

        version.es_final = True
        version.save()
        return JsonResponse(str(id), safe=False)    
    return HttpResponseNotFound()     
    
def buscarRed(request, idUsuario):
    if request.method == 'GET':
        fstart = request.GET.get("fstart")
        fend = request.GET.get("fend")
        text = request.GET.get("text")
        
        usuario = User.objects.get(pk=idUsuario);
        perfil = Perfil.objects.get(usuario=usuario);
        roles_asignado = RolAsignado.objects.filter(usuario=perfil)

        q = RED.objects.filter(rolasignado__in=roles_asignado) 

        if text:
            q = q.filter(Q(nombre__contains=text) | Q(nombre_corto__contains=text)  | Q(descripcion__contains=text) | Q(metadata__tag=text))
        
        if fend:
            q = q.filter(fecha_cierre__lte = fend)
        
        if fstart:
            q = q.filter(fecha_inicio__gte = fstart)

        return JsonResponse(list(q.values()),safe=False)
    return HttpResponseNotFound()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class PerfilSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    class Meta:
        model = Perfil
        fields = '__all__'


class RedSerializer(serializers.ModelSerializer):
    class Meta:
        model = RED
        fields = '__all__'


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'


class RolAsignadoSerializer(serializers.ModelSerializer):
    red = RedSerializer()
    usuario = PerfilSerializer()
    rol = RolSerializer()
    class Meta:
        model = RolAsignado
        fields = ('red', 'rol', 'usuario')

class VersionSerializer(serializers.ModelSerializer):
    creado_por = PerfilSerializer()
    class Meta:
        model = Version
        fields= '__all__'


class VersionSerializer(serializers.ModelSerializer):
    creado_por = PerfilSerializer()
    class Meta:
        model = Version
        fields= '__all__'


@csrf_exempt
def getAsignaciones(request):
    data = list(RolAsignado.objects.all())
    serializer = RolAsignadoSerializer(data, many=True)
    return JsonResponse({'context': serializer.data}, safe=True)


@csrf_exempt
def versiones(request):
    if request.method == 'POST':
        data = jsonUser = json.loads(request.body)
        es_final = False

        imagen = data['imagen']
        archivos = data['archivos']
        redId = data['redId']
        fecha_creacion = datetime.date.today()
        idRecursos = data['recursos']

        red = get_object_or_404(RED, id=redId)

        oldVersions = Version.objects.filter(red__id=redId)

        numero = 1

        if len(oldVersions) > 0:
            numero = max((v.numero for v in oldVersions)) + 1


        recursos = Recurso.objects.filter(id__in=idRecursos)


        creado_por=Perfil.objects.get(usuario__username=data['creado_por'])


        version = Version.objects.create(
            es_final=es_final,
            imagen=imagen,
            archivos=archivos,
            red=red,
            numero=numero,
            creado_por=creado_por,
            fecha_creacion=fecha_creacion,
        )

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

@csrf_exempt
def getRecursosRed(request, id):
    red = get_object_or_404(RED, id=id)

    serializer = RecursoSerializer(red.recursos, many=True)
    return JsonResponse({'context':serializer.data}, safe=True)


class ProyectoSerializer_v(serializers.ModelSerializer):
    class Meta:
        model = ProyectoConectate
        fields = ('nombre',)

class RedSerializer_v(serializers.ModelSerializer):
    proyecto_conectate = ProyectoSerializer_v()
    class Meta:
        model = RED
        fields = ('nombre', 'proyecto_conectate')

class VersionSerializer_v(serializers.ModelSerializer):
    red = RedSerializer_v()
    creado_por = PerfilSerializer()
    class Meta:
        model = Version
        fields = '__all__'


@csrf_exempt
def getVerVersion(request, id):
    version = get_object_or_404(Version, id=id)

    serializer = VersionSerializer_v(version, many=False)
    return JsonResponse(serializer.data, safe=True)


@csrf_exempt
def getVerVersionR(request, id):
    version = get_object_or_404(Version, id=id)

    serializer = RecursoSerializer(version.recursos, many=True)
    return JsonResponse({'context':serializer.data}, safe=True)


@csrf_exempt
def getVersionesRED(request, id):
    try:
        red = RED.objects.get(pk=id)
    except:
        raise Http404('No existe un RED con id '+str(id))
    data = Version.objects.filter(red=red).order_by('numero')
    serializer = VersionSerializer(data, many=True)
    return JsonResponse({'context': serializer.data}, safe=True)

class ComentarioMultimediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComentarioMultimedia
        fields = '__all__'

class ComentarioSerializer(serializers.ModelSerializer):
    version=VersionSerializer()
    recurso=RecursoSerializer()
    comentario_multimedia=ComentarioMultimediaSerializer()
    usuario=PerfilSerializer()
    class Meta:
        model = Comentario
        fields = '__all__'


@csrf_exempt
def comentarioExistente(request,id_v, id_r):
    if request.method == 'POST':
        data = jsonUser = json.loads(request.body)
        version = get_object_or_404(Version, id=id_v)
        recurso = get_object_or_404(Recurso, id=id_r)
        contenido = data['contenido']
        fecha_creacion = datetime.date.today()
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
    if request.method == 'POST':
        data = jsonUser = json.loads(request.body)
        version = get_object_or_404(Version, id=id_v)
        recurso = get_object_or_404(Recurso, id=id_r)
        contenido = data['contenido']
        fecha_creacion = datetime.date.today()
        usuario=Perfil.objects.get(usuario__id=data['usuario'])
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

        return JsonResponse(serializer.data, safe=True)
    return HttpResponseNotFound()

@csrf_exempt
def getListaComentarios(request,id_v, id_r):

    version = get_object_or_404(Version, id=id_v)
    recurso = get_object_or_404(Recurso, id=id_r)

    data=Comentario.objects.filter(version=version, recurso=recurso).order_by('-fecha_creacion')
    serializer=ComentarioSerializer(data, many=True)
    return JsonResponse({'context': serializer.data}, safe=True)

