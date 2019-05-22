# Generated by Django 2.1.5 on 2019-05-22 01:51

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.TextField()),
                ('id_video_libreria', models.CharField(blank=True, max_length=200, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('cerrado', models.BooleanField(blank=True, default=False)),
                ('resuelto', models.BooleanField(blank=True, default=False)),
                ('esCierre', models.BooleanField(blank=True, default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ComentarioMultimedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x1', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('y1', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('x2', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('y2', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ComentarioVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seg_ini', models.IntegerField(blank=True, null=True)),
                ('seg_fin', models.IntegerField(blank=True, null=True)),
                ('comentario_multimedia', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sisred_app.ComentarioMultimedia')),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_conectate', models.CharField(max_length=50, unique=True)),
                ('nombre_estado', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Fase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_conectate', models.CharField(max_length=50)),
                ('nombre_fase', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='HistorialFases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_cambio', models.DateField(default=datetime.date.today)),
                ('comentario', models.CharField(max_length=500)),
                ('fase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial_fases_red', to='sisred_app.Fase')),
            ],
        ),
        migrations.CreateModel(
            name='Metadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensaje', models.TextField()),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('visto', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='NotificacionTipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_conectate', models.CharField(max_length=50, unique=True)),
                ('tipo_identificacion', models.CharField(blank=True, max_length=50, null=True)),
                ('numero_identificacion', models.CharField(blank=True, max_length=50, null=True)),
                ('estado', models.IntegerField()),
                ('estado_sisred', models.IntegerField(default=0)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Propiedad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('llave', models.CharField(max_length=200)),
                ('valor', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ProyectoConectate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_conectate', models.CharField(max_length=50, unique=True)),
                ('nombre', models.CharField(max_length=200)),
                ('nombre_corto', models.CharField(blank=True, max_length=50, null=True)),
                ('codigo', models.CharField(max_length=50)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ProyectoRED',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('tipo', models.CharField(max_length=50)),
                ('autor', models.CharField(max_length=50)),
                ('carpeta', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Recurso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('archivo', models.CharField(max_length=200)),
                ('thumbnail', models.CharField(max_length=200)),
                ('fecha_creacion', models.DateField(default=datetime.date.today)),
                ('fecha_ultima_modificacion', models.DateField(default=datetime.date.today)),
                ('tipo', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_autor', to='sisred_app.Perfil')),
                ('metadata', models.ManyToManyField(blank=True, to='sisred_app.Metadata')),
                ('usuario_ultima_modificacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_ultima_modificacion', to='sisred_app.Perfil')),
            ],
        ),
        migrations.CreateModel(
            name='RED',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_conectate', models.CharField(max_length=50, unique=True)),
                ('nombre', models.CharField(max_length=200)),
                ('nombre_corto', models.CharField(blank=True, max_length=50, null=True)),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateField(blank=True, null=True)),
                ('fecha_cierre', models.DateField(blank=True, null=True)),
                ('fecha_creacion', models.DateField(default=datetime.date.today, null=True)),
                ('porcentaje_avance', models.IntegerField(blank=True, null=True)),
                ('tipo', models.CharField(max_length=50)),
                ('solicitante', models.CharField(max_length=50)),
                ('horas_estimadas', models.IntegerField(blank=True, null=True)),
                ('horas_trabajadas', models.IntegerField(blank=True, null=True)),
                ('listo_para_revision', models.BooleanField(blank=True, default=False)),
                ('fase', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sisred_app.Fase')),
                ('metadata', models.ManyToManyField(blank=True, to='sisred_app.Metadata')),
                ('proyecto_conectate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sisred_app.ProyectoConectate')),
                ('recursos', models.ManyToManyField(blank=True, to='sisred_app.Recurso')),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_conectate', models.CharField(max_length=50, unique=True)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RolAsignado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_conectate', models.CharField(max_length=50, unique=True)),
                ('estado', models.IntegerField()),
                ('notificaciones', models.ManyToManyField(blank=True, to='sisred_app.Notificacion')),
                ('red', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sisred_app.RED')),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sisred_app.Rol')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sisred_app.Perfil')),
            ],
        ),
        migrations.CreateModel(
            name='SubproductoRED',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('red', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subproductos_del_red', to='sisred_app.RED')),
                ('subproducto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reds_del_subproducto', to='sisred_app.RED')),
            ],
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('es_final', models.BooleanField(default=False)),
                ('es_lista', models.BooleanField(default=False)),
                ('numero', models.IntegerField()),
                ('imagen', models.CharField(max_length=200, null=True)),
                ('archivos', models.CharField(max_length=200)),
                ('fecha_creacion', models.DateField(default=datetime.date.today, null=True)),
                ('creado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sisred_app.Perfil')),
                ('recursos', models.ManyToManyField(blank=True, to='sisred_app.Recurso')),
                ('red', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sisred_app.RED')),
            ],
        ),
        migrations.AddField(
            model_name='proyectored',
            name='red',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sisred_app.RED'),
        ),
        migrations.AddField(
            model_name='propiedad',
            name='recurso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sisred_app.Recurso'),
        ),
        migrations.AddField(
            model_name='notificacion',
            name='tipo_notificacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificacion_tipo', to='sisred_app.NotificacionTipo'),
        ),
        migrations.AddField(
            model_name='historialfases',
            name='red',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sisred_app.RED'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='comentario_multimedia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sisred_app.ComentarioMultimedia'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='recurso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sisred_app.Recurso'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sisred_app.Perfil'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sisred_app.Version'),
        ),
    ]
