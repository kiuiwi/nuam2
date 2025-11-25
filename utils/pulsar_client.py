import pulsar

# Conecta con tu Pulsar standalone
client = pulsar.Client('pulsar://localhost:6650')
producer = client.create_producer('persistent://public/default/eventos-nuam')

def publish_event(data):
    """Envía un mensaje a Pulsar"""
    producer.send(data.encode('utf-8'))
