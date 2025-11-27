**🧩 Descripción del Proyecto**

* NUAM es un sistema de gestión documental y de usuarios que integra:
* CRUD de Usuarios
* CRUD de Personas asociadas
* CRUD de Documentos (con subida de archivos)
* Sistema de Login con roles (Administrador / Usuario)
* Registro detallado de eventos
* Envío de eventos en tiempo real mediante Apache Pulsar
* API REST completa mediante Django REST Framework
* Visualización de indicadores económicos (API mindicador.cl)
* Soporte para HTTPS local mediante certificado generado
* Este proyecto está desarrollado en Django, sin base de datos externa adicional (solo modelo Django).







**🏗 Arquitectura General**
┌──────────────────────────┐
│        Usuario           │
└───────────────┬──────────┘
		│
		 Peticiones HTTPS
		│
┌───────────────▼──────────────┐
│            Django            │
│ - CRUD Usuarios/Personas     │
│ - CRUD Documentos            │
│ - Login y Roles              │
│ - API REST                   │
└───────────────┬──────────────┘
		│
		 publish\_event() (Producer)
		│
┌───────────────▼──────────────┐
│       Apache Pulsar          │
│        (Docker)              │
└───────────────┬──────────────┘
		│

&nbsp;    	   Consumer.py        

&nbsp;    	Guarda logs en BD     







**⚙️ Tecnologías Utilizadas**


Tecnología	Uso
Python 3.12	Lenguaje principal
Django 5	Backend, views, modelos, sesiones
Django REST Framework	API REST
Apache Pulsar	Mensajería en tiempo real
Docker	Contenedor de Pulsar
Bootstrap	Estilos del frontend
HTTPS	Certificados locales (cert.pem, key.pem)
API mindicador.cl	Datos económicos actualizados







**⚙️ Requisitos previos:**



Python 3.12 o superior

pip (administrador de paquetes de Python)

Git

Virtualenv 

Docker Desktop (Windows) / Docker Engine (Linux)

Django 5.1.4 o superior (se instalará automáticamente desde requirements.txt)





------------------------------------------------------------------




**🛠️ Instalación del Proyecto**



1\. Crea una carpeta para el proyecto





2\. Abre una terminal y accede a la carpeta creada, luego ejecuta:



git clone https://github.com/kiuiwi/nuam2

cd nuam2




3. Crear y activar entorno virtual (venv):

Desde la misma carpeta del proyecto "nuam2", ejecuta:



Windows:

python -m venv venv

venv\\Scripts\\activate



Linux/Mac:

python3 -m venv venv

source venv/bin/actívate





4\. Instala las dependencias de Python:

Windows:

pip install -r requirements.txt



Linux:

pip3 install -r requirements.txt







**🔐 Ejecución del Servidor Django con HTTPS**

El proyecto se ejecuta usando:

python manage.py runserver\_plus --cert-file cert.pem --key-file key.pem



Si no existen, generar certificados:

openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes







**🐳 Levantamiento de Apache Pulsar con Docker**



1\. Instalar Docker

Instala según tu sistema operativo:

Windows / Mac: Docker Desktop 

Linux: Docker Engine



(en Windows abre Docker Desktop y asegúrate de que esté ejecutándose.





2\. Crear contenedor Pulsar (solo la primera vez):

(Abre una terminal)



Windows/Linux:

docker run -d --name pulsar-standalone -p 6650:6650 -p 8080:8080 apachepulsar/pulsar:latest bin/pulsar standalone



\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

Si el contenedor aparece como "Exited", eliminarlo:

docker rm pulsar-standalone



Y volver a ejecutar el comando anterior (paso 3).

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*





4\. Verificar contenedor

Listar contenedores:

docker ps -a 



Si está apagado:

docker start pulsar-standalone



Verificar:

docker ps



(debe mostrar "up")





(aquí ya se puede correr Django)







**🐊 Levantar Django**



en otra terminal, dentro de la carpeta nuam, ejecuta



Windows:

python manage.py runserver



Linux/Mac:

python3 manage.py runserver







**👤 Login**



**Usuario Admin**

Usuario: inacap

Contraseña: 1234



**Usuario**
Usuario: juan.perez / juan@gmail.com
Contraseña: 1234





**Superusuario Django**
Usuario: inacap
Contraseña: inacap123







**🐳 Ejecutar Consumidor:**



En otra terminal, corre:



python consumer.py





-Debe ejecutarse en otra terminal para no detener el servidor Django.

-Los mensajes enviados desde publish\_event() aparecerán en consola y en la base de datos.



Explicación: escucha el topic eventos-nuam y guarda eventos en Django (EventoLog)

Los mensajes se guardan en la tabla EventoLog.

Puedes verlos desde tu admin de Django (/admin) o con python manage.py shell:







**🐳 Verificar mensajes manuales en Pulsar**

En una terminal distinta a donde se esté ejecutando consumer.py, ejecuta:



docker exec -it pulsar-standalone bin/pulsar-client consume -s prueba1 -n 0 persistent://public/default/eventos-nuam





-s prueba1  →  nombre de la suscripción

-n 0  →  consume todos los mensajes del topic

persistent://public/default/eventos-nuam  →  topic





**Salida esperada:**

"Subscribed to topic on localhost/127.0.0.1:6650 -- consumer: 0"



Indica que el consumidor está escuchando correctamente.





**Funcionamiento interno:**



**Productor: pulsar\_client.py:**

Se conecta al broker de Pulsar que corre en localhost:6650.

Crea un productor para el topic eventos-nuam.

La función publish\_event(data) toma un string data y lo envía al topic.

Cada vez que llames a publish\_event("mensaje"), ese mensaje se envía a Pulsar.





**Consumidor: consumer.py:**

Configura Django para poder usar tus modelos (EventoLog).

Se conecta a Pulsar y se suscribe al mismo topic eventos-nuam.

Entra en un bucle infinito, escuchando mensajes.

Cada vez que llega un mensaje:

Lo imprime en consola (print("EVENTO RECIBIDO:", contenido)).

Lo guarda en tu base de datos Django como un nuevo EventoLog.

Confirma a Pulsar que el mensaje fue recibido (acknowledge).







**🔐 Certificados**



**Certificados utilizados en el proyecto**:

Certificado: nuam.crt

Clave privada: nuam.key

Ubicación: Carpeta certificados/ dentro del proyecto.

Tipo: Auto-firmado (self-signed) para entorno de desarrollo.

Generación: Se creó con OpenSSL



Nota: Este certificado no está emitido por una autoridad confiable, por lo que los navegadores mostrarán advertencias de seguridad.



**Archivos adicionales:**

certificate.crt

private.key

request.csr (solicitud de firma de certificado)







**🔐 HTTPS**

Para levantar el servidor de Django usando HTTPS, se utiliza el comando:



Windows:

python manage.py runserver\_plus --cert-file certificados/nuam.crt --key-file certificados/nuam.key



Linux / Mac:

python3 manage.py runserver\_plus --cert-file certificados/nuam.crt --key-file certificados/nuam.key





Esto levanta el servidor en https://127.0.0.1:8000/.



Se recomienda usar Chrome o Firefox para pruebas; ambos mostrarán advertencias debido al certificado auto-firmado.



El comando utiliza django-extensions (runserver\_plus) para habilitar HTTPS en desarrollo.







---------------------------------------------------------------







**📡 Sistema de Logs + Pulsar**

Cada acción del sistema genera un evento:

Login correcto

Login fallido

Crear usuario

Editar usuario

Eliminar usuario

Crear documento

Editar documento

Eliminar documento

Cierre de sesión



1. Envían a Pulsar (publish\_event())

2\. El consumer.py los escucha

3\. Se guardan en EventoLog en la base de datos







**🌐 API REST (Django REST Framework)**



Expuesta mediante ViewSets:

class UsuarioViewSet(viewsets.ModelViewSet)
class PersonaViewSet(viewsets.ModelViewSet)
class DocumentoViewSet(viewsets.ModelViewSet)
class EventoLogViewSet(viewsets.ModelViewSet)





Endpoints reales de la API interna como JSON

(se puede acceder desde Menu admin):



http://localhost:8000/api/usuarios/

http://127.0.0.1:8000/api/personas/

http://127.0.0.1:8000/api/documentos/

http://localhost:8000/api/logs/





**Endpoints disponibles:**
Endpoint	Métodos	Descripción
/api/usuarios/	GET, POST	CRUD usuarios
/api/usuarios/<id>/	GET, PUT, DELETE	Operaciones sobre un usuario
/api/personas/	CRUD	Personas
/api/documentos/	CRUD	Documentos
/api/eventolog/	CRUD	Logs generados





**Swagger UI:** 

interfaz web interactiva para explorar API REST

http://localhost:8000/swagger/







**🌐 Integración con API Externa (mindicador.cl)**



Esta función obtiene indicadores económicos desde la API pública de Mindicador, 

como la TPM (Tasa Política Monetaria) y tasas de conversión.

La función obtener\_indicadores() consulta:

TPM actual

Tipo de cambio CLP → PEN

Tipo de cambio CLP → COP



**Se maneja:**

Timeout

Errores de conexión

Datos faltantes



**Los valores se muestran en:**

inicio.html

menu\_admin.html

menu\_usuario.html

login.html



**Salida de la función:**

tpm\_actual	Valor de la TPM actual.

tc\_clp\_pen	Tipo de cambio CLP → PEN calculado.

tc\_clp\_cop	Tipo de cambio CLP → COP calculado.

error\_api	Mensaje de error si falla la consulta.





---------------------------------------------------------------





**📁 Estructura del Proyecto**


/nuam.

|

├── app

│   ├── admin.py

│   ├── api\_views.py

│   ├── apps.py

│   ├── forms.py

│   ├── models.py

│   ├── serializers.py

│   ├── static

│   │   └── app

│   │       ├── nuam\_HD2.png

│   │       ├── nuam\_HD.png

│   │       └── styles.css

│   ├── templates

│   │   ├── app

│   │   │   ├── inicio.html

│   │   │   ├── login.html

│   │   │   ├── menu\_admin.html

│   │   │   └── menu\_usuario.html

│   │   ├── base.html

│   │   ├── documentos

│   │   │   ├── crear\_documento.html

│   │   │   ├── editar\_documento.html

│   │   │   ├── eliminar\_documento.html

│   │   │   └── lista\_documentos.html

│   │   ├── logs

│   │   │   └── lista\_logs.html

│   │   ├── registro

│   │   │   ├── crear\_registro.html

│   │   │   ├── editar\_registro.html

│   │   │   ├── eliminar\_registro.html

│   │   │   └── lista\_registros.html

│   │   └── usuarios

│   │       ├── crear\_usuario.html

│   │       ├── eliminar\_usuario.html

│   │       └── lista\_usuarios.html

│   ├── tests.py

│   ├── urls.py

│   └── views.py

│

├── certificados

│   ├── cert.crt

│   ├── certificate.crt

│   ├── cert.key

│   ├── nuam.crt

│   ├── nuam.key

│   ├── private.key

│   └── request.csr

│

├── consumer.py

│

├── db.sqlite3

│

├── documentos

│   └── comprobante\_depositos.txt

│

├── manage.py

│

├── nuam

│   ├── asgi.py

│   ├── settings.py

│   ├── urls.py

│   └── wsgi.py

│

├── README.txt

├── requirements.txt

│

└── utils

&nbsp;   └── pulsar\_client.py





**🗂 Estructura de Modelos (Modelo de Datos)**

**El proyecto incluye:**

Usuario

Persona

Documento

DocumentoTipo

UsuarioTipo

EventoLog (logs generados por Pulsar)



**El CRUD depende de estas relaciones:**

UsuarioTipo 1 ──── N Usuario
Usuario 1 ──── 1 Persona
DocumentoTipo 1 ──── N Documento
Usuario 1 ──── N Documento







**👥 CRUD de Usuarios y Personas**
✔ Crear
✔ Editar
✔ Eliminar
✔ Listar

**Al crear o editar un usuario:**

Se guarda el usuario con su Persona asociada.

Se genera un evento Pulsar (publish\_event()).

Se registra un EventoLog en la base de datos.



**Flujo de creación**

Usuario + Persona enviados por POST

Validación de formularios

Guardado en DB

Pulsar produce evento

EventoLog guarda en DB

Redirige a la lista

Vistas incluidas:

lista\_registros

crear\_registro

editar\_registro

eliminar\_registro







**📄 CRUD de Documentos**
Funcionalidades:

Subir archivo (request.FILES)

Editar metadatos

Eliminar documento

Filtros (texto y tipo)

Logs + eventos Pulsar



**Vistas:**

lista\_documentos

crear\_documento

editar\_documento

eliminar\_documento



**Cada operación:**

✔ Envía evento al broker
✔ Guarda EventoLog en la base de datos







**🔑 Autenticación y Perfiles de Usuario**

**Sistema de login flexible:**

1. Login desde tabla Usuario (username + password)
2. Login por email (tabla Persona)
3. Login del Administrador Django (authenticate())



**Roles:**

Administrador → acceso a menú admin

Usuario → acceso a menú usuario



**Ambos almacenados en:**

request.session\["tipo"]
request.session\["usuario\_id"]









✨ Autores:

Nombres: Sol Toledo, Camila Cruz, Alejandra Miranda

Carrera: Analista Programador

Institución: Inacap

Año: 2025





