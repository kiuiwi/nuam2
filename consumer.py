import os
import django
import pulsar
import traceback

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nuam.settings')
django.setup()

from app.models import EventoLog

# Conectar con Pulsar
client = pulsar.Client('pulsar://localhost:6650')
consumer = client.subscribe(
    'persistent://public/default/eventos-nuam',
    subscription_name='nuam-log-service'
)

print("🔎 Escuchando eventos de Pulsar...")

while True:
    try:
        msg = consumer.receive()
        contenido = msg.data().decode('utf-8')
        print("EVENTO RECIBIDO:", contenido)

        # Determinar tipo según contenido
        msg_lower = contenido.lower()
        if "inicio de sesión" in msg_lower or "login" in msg_lower:
            tipo = "Login"
        elif "cierre de sesión" in msg_lower or "logout" in msg_lower:
            tipo = "Logout"
        elif "documento" in msg_lower:
            tipo = "Documento"
        elif "usuario" in msg_lower:
            tipo = "Usuario"
        else:
            tipo = "desconocido"

        # Guardar en la base de datos
        EventoLog.objects.create(
            tipo=tipo,
            mensaje=contenido
        )

        # Confirmar recepción a Pulsar
        consumer.acknowledge(msg)

    except Exception as e:
        print("❌ Error procesando mensaje:", e)
        traceback.print_exc()
        # opcional: no ack si falla para intentar procesar después
