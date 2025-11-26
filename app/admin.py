from django.contrib import admin
from .models import (
    UsuarioTipo, Pais, Region,
    Usuario, Persona,
    DocumentoTipo, Documento,
    EventoLog

)


# ADMIN UsuarioTipo
@admin.register(UsuarioTipo)
class UsuarioTipoAdmin(admin.ModelAdmin):
    list_display = ('id_usuario_tipo', 'usuario_tipo')
    search_fields = ('usuario_tipo',)
    ordering = ('usuario_tipo',)



# ADMIN Pais
@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('id_pais', 'pais')
    search_fields = ('pais',)
    ordering = ('pais',)



# ADMIN Region
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id_region', 'region')
    search_fields = ('region',)
    ordering = ('region',)



# ADMIN Usuario
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'nombre_usuario', 'get_usuario_tipo')
    search_fields = ('nombre_usuario', 'usuario_tipo__usuario_tipo')
    list_filter = ('usuario_tipo',)
    ordering = ('nombre_usuario',)

    def get_usuario_tipo(self, obj):
        return obj.usuario_tipo.usuario_tipo if obj.usuario_tipo else ""
    get_usuario_tipo.short_description = "Tipo de Usuario"



# ADMIN Persona
@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = (
        'id_persona',
        'usuario',
        'nombres',
        'apellidos',
        'telefono',
        'email',
        'direccion',
        'get_region',
        'get_pais',
    )
    search_fields = (
        'nombres',
        'apellidos',
        'email',
        'usuario__nombre_usuario',
    )
    list_filter = ('pais', 'region')
    ordering = ('nombres',)

    def get_region(self, obj):
        return obj.region.region if obj.region else ''
    get_region.short_description = 'Región'

    def get_pais(self, obj):
        return obj.pais.pais if obj.pais else ''
    get_pais.short_description = 'País'



# ADMIN DocumentoTipo
@admin.register(DocumentoTipo)
class DocumentoTipoAdmin(admin.ModelAdmin):
    list_display = ('id_documento_tipo', 'documento_tipo')
    search_fields = ('documento_tipo',)
    ordering = ('documento_tipo',)



# ADMIN Documento
@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = (
        'id_documento',
        'documento_nombre',
        'usuario',
        'documento_tipo',
        'fecha_ingreso'
    )
    search_fields = (
        'documento_nombre',
        'usuario__nombre_usuario',
    )
    list_filter = ('documento_tipo', 'fecha_ingreso')
    ordering = ('fecha_ingreso',)


# ADMIN EventoLog
@admin.register(EventoLog)
class EventoLogAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'tipo', 'mensaje', 'get_icon', 'get_color')
    search_fields = ('mensaje', 'tipo')
    list_filter = ('tipo', 'fecha')
    ordering = ('-fecha',)

    # Para mostrar los íconos en la lista del admin
    def get_icon(self, obj):
        return obj.get_icon()
    get_icon.short_description = 'Icono'

    def get_color(self, obj):
        return obj.get_color()
    get_color.short_description = 'Color'