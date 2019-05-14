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

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ('nombre',)


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

class RolAsignadoSerializer(serializers.ModelSerializer):
    rol = RolSerializer()
    class Meta:
        model = RolAsignado
        fields = ('rol',)

class ProyectosSerializer(serializers.ModelSerializer):
    red_count = serializers.SerializerMethodField()
    red_alert = serializers.SerializerMethodField()
    red_active = serializers.SerializerMethodField()
    red_close = serializers.SerializerMethodField()
    class Meta:
        model = ProyectoConectate
        fields = ('nombre', 'red_count', 'red_alert', 'red_active','red_close')

    def get_red_count(self, obj):
        return RED.objects.filter(proyecto_conectate=obj.id).count()

    def get_red_alert(self, obj):
        d = datetime.today() - timedelta(days=7)
        return Comentario.objects.filter(version__red__proyecto_conectate=obj.id)\
            .filter(~Q(version__red__fase__nombre_fase='Cerrado')).filter(fecha_creacion__lte=d).count()

    def get_red_active(self, obj):
        d = datetime.today() - timedelta(days=7)
        return Comentario.objects.filter(version__red__proyecto_conectate=obj.id)\
            .filter(~Q(version__red__fase__nombre_fase='Cerrado')).filter(fecha_creacion__gte=d).count()

    def get_red_close(self, obj):
        return RED.objects.filter(proyecto_conectate=obj.id).filter(fase__nombre_fase='Cerrado').count()
