from rest_framework import viewsets
from .models import Usuario, Persona, Documento, EventoLog
from .serializers import UsuarioSerializer, PersonaSerializer, DocumentoSerializer, EventoLogSerializer


# API Usuario
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


# API Persona
class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


# API Documento
class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer

# API EventoLog
class EventoLogViewSet(viewsets.ModelViewSet):
    queryset = EventoLog.objects.all().order_by('-id')
    serializer_class = EventoLogSerializer
