import os
import django
import pulsar

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nuam.settings')
django.setup()

from app.models import EventoLog

client = pulsar.Client('pulsar://localhost:6650')
consumer = client.subscribe(
    'persistent://public/default/eventos-nuam',
    subscription_name='nuam-log-service'
)

print("🔎 Escuchando eventos de Pulsar...")

while True:
    msg = consumer.receive()
    contenido = msg.data().decode('utf-8')

    print("EVENTO RECIBIDO:", contenido)

    # Guardar en la base de datos
    EventoLog.objects.create(
        tipo="documento",
        mensaje=contenido
    )

    consumer.acknowledge(msg)
