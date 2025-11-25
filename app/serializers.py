from rest_framework import serializers
from .models import Usuario, Persona, Documento, EventoLog

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'


class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = '__all__'


class EventoLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoLog
        fields =  '__all__'


