🟦 NUAM — Sistema de Gestión de Documentos y Usuarios con Django + Pulsar

📌 1. Introducción

NUAM es un sistema de gestión documental diseñado como proyecto TI.
Permite administrar usuarios, personas y documentos, integrando:

Django

Django REST Framework

Apache Pulsar (mensajería)

Docker

HTTPS (certificado local)

Logs de eventos

API interna + API externa (mindicador.cl)

El proyecto funciona sin base de datos externa, utilizando el modelo de datos propio de Django con SQLite por defecto.

📌 2. Arquitectura General
┌────────────────────┐       ┌─────────────────────┐
│        Django       │ <---> │   API REST (DRF)     │
│ CRUD + Auth + Logs │       └─────────────────────┘
│                    │
│ Produces eventos → │ Pulsar Producer
└────────────────────┘
         │
         ▼
   Pulsar (Docker)
         │
         ▼
┌─────────────────────┐
│   Consumer.py       │
│ Guarda logs en BD   │
└─────────────────────┘

📌 3. Tecnologías principales
Tecnología	Uso
Django	Lógica principal del sistema
Django REST Framework	API REST automática con ViewSets
Pulsar	Envío de eventos del sistema
Docker	Ejecución de broker Pulsar
HTTPS (cert.pem + key.pem)	Seguridad del proyecto
SQLite	Base de datos interna por defecto
requests	Consumo API mindicador.cl

📌 4. Estructura del Proyecto
nuam2/
│── nuam2/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
│── app/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── consumer.py
│   └── utils/
│       └── pulsar_client.py
│
│── templates/
│── static/
│── cert.pem
│── key.pem
│── manage.py

📌 5. Modelos del Sistema
Usuario

username

password

es_admin

fecha_registro

Persona

usuario (FK)

nombre

apellido

email

rut

Documento

titulo

descripcion

archivo

autor (FK Persona)

fecha_subida

EventoLog

tipo_evento

detalle

fecha

📌 6. CRUD Implementados
✔️ CRUD de Usuarios

Crear / Editar / Eliminar

Relación automática con Persona

Envío de evento a Pulsar

Registro de logs en BD

✔️ CRUD de Personas

Asociada 1:1 al Usuario

Validación de email y RUT

Actualización desde HTML y API

✔️ CRUD de Documentos

Subida de archivo

Filtros por texto y tipo

Tabla con acciones Editar / Eliminar

Evento Pulsar al crear o eliminar

Registro en EventoLog

📌 7. Autenticación del Sistema

El sistema soporta múltiples formas de acceso:

🔹 Login por Usuario

Login normal con username + password.

🔹 Login por Persona (email)

Se revisa la tabla Persona:
si coincide, se autentica contra el Usuario asociado.

🔹 Login desde Django Admin

Con usuario admin.

📌 8. API REST del Proyecto

Los endpoints se generan automáticamente gracias a ModelViewSet.

🔹 Usuarios
GET    /api/usuarios/
POST   /api/usuarios/
GET    /api/usuarios/{id}/
PUT    /api/usuarios/{id}/
DELETE /api/usuarios/{id}/

🔹 Personas
GET    /api/personas/
POST   /api/personas/
GET    /api/personas/{id}/
PUT    /api/personas/{id}/
DELETE /api/personas/{id}/

🔹 Documentos
GET    /api/documentos/
POST   /api/documentos/
GET    /api/documentos/{id}/
PUT    /api/documentos/{id}/
DELETE /api/documentos/{id}/

🔹 Logs
GET /api/logs/

📌 9. Pulsar — Productor y Consumidor
Productor (integrado en Django)

Cada vez que ocurre un evento:

Creación de Usuario

Eliminación

Subida de documento

Login

Error

Acción del CRUD

Se ejecuta:

publish_event("usuario_creado", {"id": usuario.id})

Consumer.py (independiente)

Se ejecuta en otra terminal:

python consumer.py


Su tarea:

Leer mensajes del tópico

Interpretarlos

Guardar en EventoLog

📌 10. Docker — Levantar Pulsar
Crear contenedor Pulsar (solo una vez):
docker run -d --name pulsar-standalone -p 6650:6650 -p 8080:8080 apachepulsar/pulsar-standalone

Iniciar si ya existe:
docker start pulsar-standalone

📌 11. HTTPS — Ejecución del Proyecto

Django se ejecuta con:

python manage.py runserver_plus --cert-file cert.pem --key-file key.pem


Esto permite:

Navegación con https://localhost:8000

Formularios seguros

Login seguro

Envío de archivos sin advertencias del navegador

📌 12. API Externa — mindicador.cl

Se consume la API oficial para mostrar:

UF

Dólar

Euro

IPC

UTM

El sistema maneja:

Errores de conexión

Datos inválidos

Retorno alternativo si la API cae

📌 13. Instalación y Ejecución
1️⃣ Clonar repositorio
git clone https://github.com/tu_usuario/NUAM.git
cd NUAM

2️⃣ Crear entorno virtual
python -m venv venv
source venv/bin/activate   # Linux
venv\Scripts\activate      # Windows

3️⃣ Instalar dependencias
pip install -r requirements.txt

4️⃣ Levantar Docker + Pulsar
docker start pulsar-standalone

5️⃣ Ejecutar Django con HTTPS
python manage.py runserver_plus --cert-file cert.pem --key-file key.pem

6️⃣ Ejecutar consumer (otra terminal)
python consumer.py

📌 14. Problemas comunes y soluciones
❗ “pulsar-client no responde”

Asegurarse que Docker está encendido

Verificar que el contenedor se inició correctamente

docker ps

❗ Error de certificados en Chrome

Volver a instalar cert.pem en la CA local

Reiniciar navegador

❗ Formulario no sube archivo

Revisar permisos en carpeta /media/

📌 15. Créditos

Proyecto desarrollado por:
Camila Cruz, Alejandra Miranda y Sol Toledo.
Carrera: Analista Programador
Institución: INACAP
