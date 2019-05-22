from .models import *
from datetime import datetime, timedelta
from django.db.models import Q
from rest_framework import  serializers

class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Metadata
        fields=('id','tag')

class RecursoSerializer(serializers.ModelSerializer):
    metadata = MetadataSerializer(many=True, read_only=True)
    class Meta:
        model=Recurso
        fields=('nombre','id', 'archivo','thumbnail','fecha_creacion','fecha_ultima_modificacion','tipo','descripcion','metadata','autor','usuario_ultima_modificacion','getAutor','getResponsableModificacion')

class RecursoSerializer_post(serializers.ModelSerializer):
    class Meta:
        model=Recurso
        fields=('nombre','archivo','thumbnail','tipo','descripcion','autor','idRed')

class RecursoSerializer_put(serializers.ModelSerializer):
    class Meta:
        model=Recurso
        fields=('nombre','descripcion','usuario_ultima_modificacion')

class FaseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Fase
        fields=('id_conectate','nombre_fase')

class REDSerializer(serializers.ModelSerializer):
    fase = MetadataSerializer(many=True, read_only=True)
    class Meta:
        model = RED
        fields = ('id_conectate', 'nombre', 'nombre_corto', 'descripcion', 'fecha_inicio',
                  'fecha_cierre', 'fecha_creacion', 'porcentaje_avance', 'tipo', 'solicitante', 'proyecto_conectate', 'horas_estimadas',
                  'horas_trabajadas','fase','listo')

class UserAutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurso
        fields = '__all__'

#class RolSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Rol
#        fields = ('nombre',)

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'


class RedRolSerializer(serializers.ModelSerializer):
    class Meta:
        model = RED
        fields = ('id','nombre')

class PerfilRolSerializer(serializers.ModelSerializer):
    usuario = UserAutSerializer()
    class Meta:
        model = Perfil
        fields = ('usuario',)

class RedDetSerializer(serializers.ModelSerializer):
    recursos = ResourceSerializer(many=True)
    class Meta:
        model = RED
        fields = ('id_conectate', 'nombre', 'descripcion', 'recursos')

class ProyectoSerializer_v(serializers.ModelSerializer):
    class Meta:
        model = ProyectoConectate
        fields = ('nombre',)

class RedSerializer_v(serializers.ModelSerializer):
    proyecto_conectate = ProyectoSerializer_v()
    class Meta:
        model = RED
        fields = ('nombre', 'proyecto_conectate')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class PerfilSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    class Meta:
        model = Perfil
        fields = '__all__'

class VersionSerializer_v(serializers.ModelSerializer):
    red = RedSerializer_v()
    creado_por = PerfilSerializer()
    class Meta:
        model = Version
        fields = '__all__'

class RedSerializer(serializers.ModelSerializer):
    class Meta:
        model = RED
        fields = '__all__'

#class RolAsignadoSerializer(serializers.ModelSerializer):
#    rol = RolSerializer()
#    class Meta:
#        model = RolAsignado
#        fields = ('rol',)

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

class ProyectoREDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProyectoRED
        fields= '__all__'
        
class ProyectosSerializer(serializers.ModelSerializer):
    red_count = serializers.SerializerMethodField()
    red_alert = serializers.SerializerMethodField()
    red_active = serializers.SerializerMethodField()
    red_close = serializers.SerializerMethodField()
    class Meta:
        model = ProyectoConectate
        fields = ('id', 'nombre', 'red_count', 'red_alert', 'red_active','red_close')

    def get_red_count(self, obj):
        return RED.objects.filter(proyecto_conectate=obj.id).count()

    def get_red_alert(self, obj):
        d = datetime.today() - timedelta(days=7)
        a = RED.objects.filter(proyecto_conectate=obj.id).filter(fecha_creacion__lte=d)\
            .filter(~Q(fase__nombre_fase='Cerrado')).filter(version__numero__isnull=True).count()
        b = Comentario.objects.filter(version__red__proyecto_conectate=obj.id).filter(fecha_creacion__lte=d)\
            .filter(~Q(version__red__fase__nombre_fase='Cerrado')).count()
        alert = a + b
        return alert

    def get_red_active(self, obj):
        d = datetime.today() - timedelta(days=7)
        a = Comentario.objects.filter(version__red__proyecto_conectate=obj.id).filter(fecha_creacion__gte=d)\
            .filter(~Q(version__red__fase__nombre_fase='Cerrado')).count()
        b = RED.objects.filter(proyecto_conectate=obj.id).filter(fecha_creacion__gte=d)\
            .filter(~Q(fase__nombre_fase='Cerrado')).filter(version__numero__isnull=True).count()
        active = a + b
        return active

    def get_red_close(self, obj):
        return RED.objects.filter(proyecto_conectate=obj.id).filter(fase__nombre_fase='Cerrado').count()

class comentarioMultimediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComentarioMultimedia
        fields = '__all__'

class comentariosHijosSerializer(serializers.ModelSerializer):
    comentarioMultimedia=comentarioMultimediaSerializer(many=False)
    class Meta:
        model = Comentario
        fields = ('id','contenido','fecha_creacion','esCierre','resuelto','cerrado','usuario','version','UsuarioComentario','comentarioMultimedia')

class ComentariosPDFSerializer(serializers.ModelSerializer):
    comentariosHijos=comentariosHijosSerializer(many=True)
    comentarioMultimedia=comentarioMultimediaSerializer(many=False)
    class Meta:
        model = Comentario
        fields = ('id','contenido','fecha_creacion','esCierre','resuelto','cerrado','usuario','version','Width','Height','VersionArchivo','UsuarioComentario','comentarioMultimedia','comentariosHijos')

class ComentarioCierreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comentario
        fields = '__all__'

#class VersionSerializer(serializers.ModelSerializer):

    #class Meta:
    #    model = Version
    #    fields = '__all__'
