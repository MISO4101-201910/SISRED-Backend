from .models import *

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
