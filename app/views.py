

import requests

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.forms.models import model_to_dict

from utils.pulsar_client import publish_event

from .models import Usuario, Persona, Documento, EventoLog
from .forms import UsuarioForm, PersonaForm, DocumentoForm

from django.contrib.auth import authenticate, login as django_login



#API MINDICADOR

def obtener_indicadores():
    url = "https://mindicador.cl/api"
    datos = {
        "tpm_actual": None,
        "tc_clp_pen": None,
        "tc_clp_cop": None,
        "error_api": None,
    }

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()

            # TPM
            datos["tpm_actual"] = data.get("tpm", {}).get("valor")

            # Valores necesarios
            usd_clp = data.get("dolar", {}).get("valor")
            usd_pen = data.get("dolar_intercambio", {}).get("valor")
            usd_cop = data.get("dolar_intercambio", {}).get("valor")

            # Conversión CLP → PEN
            if usd_clp and usd_pen:
                datos["tc_clp_pen"] = round(usd_clp / usd_pen, 3)

            # Conversión CLP → COP
            if usd_clp and usd_cop:
                datos["tc_clp_cop"] = round(usd_clp / usd_cop, 3)

        else:
            datos["error_api"] = "Error al conectarse a la API externa."

    except Exception as e:
        datos["error_api"] = f"Error al consumir la API: {str(e)}"

    return datos



# HOME

def inicio(request):
    context = obtener_indicadores()
    return render(request, "app/inicio.html", context)



# CRUD: USUARIO + PERSONA

def lista_registros(request):
    personas = Persona.objects.select_related("usuario").all()
    return render(request, "registro/lista_registros.html", {"personas": personas})


def crear_registro(request):
    if request.method == "POST":
        usuario_form = UsuarioForm(request.POST)
        persona_form = PersonaForm(request.POST)

        if usuario_form.is_valid() and persona_form.is_valid():
            usuario = usuario_form.save()
            persona = persona_form.save(commit=False)
            persona.usuario = usuario
            persona.save()
            publish_event(
                f"Usuario creado: {usuario.id_usuario} - {usuario.nombre_usuario} | Usuario: {request.session.get('usuario_id')}"
            )
            EventoLog.objects.create(
                tipo="Usuario",
                mensaje=f"Usuario creado: {usuario.nombre_usuario} (ID {usuario.id_usuario})"
    )
            return redirect("lista_registros")

    else:
        usuario_form = UsuarioForm()
        persona_form = PersonaForm()

    return render(request, "registro/crear_registro.html", {
        "usuario_form": usuario_form,
        "persona_form": persona_form
    })


def editar_registro(request, usuario_id):
    usuario = get_object_or_404(Usuario, id_usuario=usuario_id)
    persona = get_object_or_404(Persona, usuario=usuario)

    if request.method == "POST":
        usuario_form = UsuarioForm(request.POST, instance=usuario)
        persona_form = PersonaForm(request.POST, instance=persona)

        if usuario_form.is_valid() and persona_form.is_valid():
            usuario_form.save()
            persona_form.save()
            publish_event(
                f"Usuario editado: {usuario.id_usuario} - {usuario.nombre_usuario} | Usuario: {request.session.get('usuario_id')}"
            )
            EventoLog.objects.create(
                tipo="Usuario",
                mensaje=f"Usuario editado: {usuario.nombre_usuario} (ID {usuario.id_usuario})"
    )
            return redirect("lista_registros")

    else:
        usuario_form = UsuarioForm(instance=usuario)
        persona_form = PersonaForm(instance=persona)

    return render(request, "registro/editar_registro.html", {
        "usuario_form": usuario_form,
        "persona_form": persona_form
    })


def eliminar_registro(request, usuario_id):
    usuario = get_object_or_404(Usuario, id_usuario=usuario_id)

    if request.method == "POST":
        usuario.delete()
        publish_event(
            f"Usuario eliminado: {usuario.id_usuario} - {usuario.nombre_usuario} | Usuario: {request.session.get('usuario_id')}"
        )
        EventoLog.objects.create(
            tipo="Usuario",
            mensaje=f"Usuario eliminado: {usuario.nombre_usuario} (ID {usuario.id_usuario})"
    )
        return redirect("lista_registros")

    return render(request, "registro/eliminar_registro.html", {"usuario": usuario})




# CRUD: DOCUMENTOS

def lista_documentos(request):
    query = request.GET.get('q')
    tipo = request.GET.get('tipo')

    documentos = Documento.objects.all()

    # Filtro texto
    if query:
        documentos = documentos.filter(
            Q(documento_nombre__icontains=query) |
            Q(usuario__nombre_usuario__icontains=query) |
            Q(documento_tipo__documento_tipo__icontains=query)
        )

    # Filtro tipo select
    if tipo and tipo != "":
        documentos = documentos.filter(documento_tipo__id_documento_tipo=tipo)

    return render(request, "documentos/lista_documentos.html", {
        "documentos": documentos,
        "query": query,
        "tipo": tipo,
    })


def crear_documento(request):
    if request.method == "POST":
        form = DocumentoForm(request.POST, request.FILES)

        if form.is_valid():
            doc = form.save()
            publish_event(f"Documento creado: {doc.id_documento} - {doc.documento_nombre}")
            return redirect("lista_documentos")

    else:
        form = DocumentoForm()

    return render(request, "documentos/crear_documento.html", {"form": form})


def editar_documento(request, documento_id):
    documento = get_object_or_404(Documento, id_documento=documento_id)

    if request.method == "POST":
        form = DocumentoForm(request.POST, request.FILES, instance=documento)

        if form.is_valid():
            doc = form.save()
            publish_event(f"Documento editado: {doc.id_documento} - {doc.documento_nombre}")
            return redirect("lista_documentos")

    else:
        form = DocumentoForm(instance=documento)

    return render(request, "documentos/editar_documento.html", {"form": form})


def eliminar_documento(request, documento_id):
    documento = get_object_or_404(Documento, id_documento=documento_id)

    if request.method == "POST":
        publish_event(f"Documento eliminado: {documento.id_documento} - {documento.documento_nombre}")
        documento.delete()
        return redirect("lista_documentos")

    return render(request, "documentos/eliminar_documento.html", {"documento": documento})




# LOGS DE EVENTOS (PULSAR)

def lista_logs(request):
    logs = EventoLog.objects.order_by('-fecha')
    return render(request, 'logs/lista_logs.html', {'logs': logs})


def api_logs(request):
    logs = EventoLog.objects.order_by('-fecha')[:20]
    data = [model_to_dict(log) for log in logs]
    return JsonResponse(data, safe=False)




# LOGIN + MENÚS

def login_view(request):
    indicadores = obtener_indicadores()

    if request.method == "POST":
        login_input = request.POST.get("login", "").strip()
        password = request.POST.get("password", "").strip()

        usuario = None


        # LOGIN TABLA Usuario
        try:
            usuario = Usuario.objects.get(
                nombre_usuario=login_input,
                contrasena=password
            )
        except Usuario.DoesNotExist:
            usuario = None


        # LOGIN POR EMAIL EN Persona
        if usuario is None:
            try:
                persona = Persona.objects.get(email=login_input)
                if persona.usuario.contrasena == password:
                    usuario = persona.usuario
            except Persona.DoesNotExist:
                usuario = None


        # LOGIN DEL ADMIN DE DJANGO
        if usuario is None:
            django_user = authenticate(request, username=login_input, password=password)
            if django_user:
                django_login(request, django_user)

                # Registrar LOG (Pulsar + DB)
                mensaje = f"Inicio de sesión exitoso (Admin Django): {django_user.username}"
                publish_event(mensaje)
                EventoLog.objects.create(tipo="Login", mensaje=mensaje)

                request.session["tipo"] = "Administrador"
                return redirect("menu_admin")


        # LOGIN FALLIDO
        if usuario is None:
            mensaje = f"Intento de inicio de sesión fallido: '{login_input}'"
            publish_event(mensaje)
            EventoLog.objects.create(tipo="Login", mensaje=mensaje)

            return render(request, "app/login.html", {
                "error": "Credenciales inválidas",
                **indicadores
            })


        # LOGIN EXITOSO → USUARIO PERSONALIZADO
        request.session["usuario_id"] = usuario.id_usuario
        request.session["tipo"] = usuario.usuario_tipo.usuario_tipo  #Usuario / Administrador

        # Registrar LOG (Pulsar + DB)
        mensaje = f"Inicio de sesión exitoso: {usuario.nombre_usuario} (ID {usuario.id_usuario})"
        publish_event(mensaje)
        EventoLog.objects.create(tipo="Login", mensaje=mensaje)

        # REDIRECCIONAR SEGÚN TIPO
        if usuario.usuario_tipo.usuario_tipo == "Administrador":
            return redirect("menu_admin")
        else:
            return redirect("menu_usuario")


    # GET → mostrar login con indicadores
    return render(request, "app/login.html", indicadores)





def menu_admin(request):
    if request.session.get("tipo") != "Administrador":
        return redirect("login")

    context = obtener_indicadores()
    return render(request, "app/menu_admin.html", context)



def menu_usuario(request):
    if "usuario_id" not in request.session:
        return redirect("login")

    context = obtener_indicadores()
    return render(request, "app/menu_usuario.html", context)



def logout_view(request):
    usuario_id = request.session.get("usuario_id")
    tipo = request.session.get("tipo")

    # Registrar logout ANTES de limpiar la sesión
    if usuario_id:
        try:
            usuario = Usuario.objects.get(id_usuario=usuario_id)
            nombre = usuario.nombre_usuario
        except Usuario.DoesNotExist:
            nombre = "Desconocido"
        
        EventoLog.objects.create(
            tipo="Logout",
            mensaje=f"Cierre de sesión: {nombre} (ID {usuario_id})"
        )
    else:
        # Caso de superusuario de Django(?)
        if request.user.is_authenticated:
            EventoLog.objects.create(
                tipo="Logout",
                mensaje=f"Cierre de sesión (Admin): {request.user.username}"
            )

    request.session.flush()
    return redirect("login")
