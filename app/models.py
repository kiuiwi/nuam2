from django.db import models


class UsuarioTipo(models.Model):
    id_usuario_tipo = models.AutoField(primary_key=True, db_column='ID_USUARIO_TIPO')
    usuario_tipo = models.CharField(max_length=30, blank=True, db_column='USUARIO_TIPO')

    def __str__(self):
        return self.usuario_tipo or "Tipo sin nombre"

    class Meta:
        verbose_name = 'Tipo de Usuario'
        verbose_name_plural = 'Tipos de Usuario'


class Pais(models.Model):
    id_pais = models.AutoField(primary_key=True, db_column='ID_PAIS')
    pais = models.CharField(max_length=50, blank=True, db_column='PAIS')

    def __str__(self):
        return self.pais or "País sin nombre"

    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'


class Region(models.Model):
    id_region = models.AutoField(primary_key=True, db_column='ID_REGION')
    region = models.CharField(max_length=50, blank=True, db_column='REGION')

    def __str__(self):
        return self.region or "Región sin nombre"

    class Meta:
        verbose_name = 'Región'
        verbose_name_plural = 'Regiones'


# --------------------------------------------------------
# NUEVA TABLA USUARIOS (autenticación)
# --------------------------------------------------------
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True, db_column='ID_USUARIO')
    usuario_tipo = models.ForeignKey(
        UsuarioTipo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='ID_USUARIO_TIPO'
    )
    nombre_usuario = models.CharField(max_length=50, db_column='NOMBRE_USUARIO')
    contrasena = models.CharField(max_length=100, null=True, blank=True)
 # En producción se debe encriptar

    def __str__(self):
        return self.nombre_usuario

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


# --------------------------------------------------------
# NUEVA TABLA PERSONAS (datos personales)
# --------------------------------------------------------
class Persona(models.Model):
    id_persona = models.AutoField(primary_key=True, db_column='ID_PERSONA')
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        db_column='ID_USUARIO'
    )
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True, blank=True, db_column='ID_PAIS')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, db_column='ID_REGION')
    nombres = models.CharField(max_length=50, db_column='NOMBRES', blank=True)
    apellidos = models.CharField(max_length=50, db_column='APELLIDOS', blank=True)
    telefono = models.CharField(max_length=20, db_column='TELEFONO', blank=True)
    email = models.EmailField(db_column='EMAIL', blank=True)
    direccion = models.CharField(max_length=100, db_column='DIRECCION', blank=True)

    def __str__(self):
        nombre = f"{self.nombres} {self.apellidos}".strip()
        return nombre or f"Persona {self.id_persona}"

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'


class DocumentoTipo(models.Model):
    id_documento_tipo = models.AutoField(primary_key=True, db_column='ID_DOCUMENTO_TIPO')
    documento_tipo = models.CharField(max_length=50, blank=True, db_column='DOCUMENTO_TIPO')

    def __str__(self):
        return self.documento_tipo or "Tipo sin nombre"

    class Meta:
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documento'


class Documento(models.Model):
    id_documento = models.AutoField(primary_key=True, db_column='ID_DOCUMENTO')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='ID_USUARIO')
    documento_nombre = models.CharField(max_length=100, blank=True, db_column='DOCUMENTO_NOMBRE')
    documento_tipo = models.ForeignKey(DocumentoTipo, on_delete=models.SET_NULL, null=True, blank=True, db_column='ID_DOCUMENTO_TIPO')
    archivo = models.FileField(upload_to='documentos/', blank=True, null=True, db_column='ARCHIVO')
    fecha_ingreso = models.DateTimeField(auto_now_add=True, db_column='FECHA_INGRESO')

    def __str__(self):
        return self.documento_nombre or f"Documento {self.id_documento}"




class EventoLog(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=20)
    mensaje = models.TextField()


    def get_color(self):
        if "creado" in self.mensaje.lower():
            return "green"
        if "editado" in self.mensaje.lower():
            return "orange"
        if "eliminado" in self.mensaje.lower():
            return "red"
        return "gray"

    def get_icon(self):
        if "creado" in self.mensaje.lower():
            return "🟢"
        if "editado" in self.mensaje.lower():
            return "🟠"
        if "eliminado" in self.mensaje.lower():
            return "🔴"
        return "⚪"