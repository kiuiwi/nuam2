EV3


info general:

SUPERUSER (django):
Usuario: inacap
Contraseña: inacap123

------------------------------------------------

LOGIN (usuarios para probar)

(usuario admin)
Usuario: inacap
Contraseña: 1234


(usuarios normales(?)
Usuario: pedro.perez o pedro@gmail.om
Contraseña: 1234

Usuario: juan.perez o juan@gmail.com
Contraseña: 1234


-----------------------------------------------
------------------------------------------------

REQUISITOS PREVIOS:

Python 3.12 o superior
pip (administrador de paquetes de Python)
Git
Virtualenv 
Docker Desktop (Windows) / Docker Engine (Linux)
Django 5.1.4 o superior (se instalará automáticamente desde requirements.txt)



-----------------------------------------------

CLONAR REPOSITORIO:

1. Crea una carpeta para el proyecto

Abre una terminal y accede a la carpeta creada, luego ejecuta:

git clone https://github.com/kiuiwi/nuam2
cd nuam



2. Crear y activar entorno virtual  (venv)
Desde la misma carpeta del proyecto "nuam", ejecuta:

Linux/Mac:
python3 -m venv venv
source venv/bin/activate

Windows:
python -m venv venv
venv\Scripts\activate


--------------------------------------------------

INSTALACION DE DEPENDENCIAS DE PYTHON:

pip install -r requirements.txt


---------------------------------------------------
---------------------------------------------------


LEVANTAR DOCKER Y PULSAR


1. Instalar Docker

Instala según tu sistema operativo:
Windows / Mac: Docker Desktop
Linux: Docker Engine



2. Abrir Docker Desktop
Asegurate de que Docker esté ejecutandose


3. Crear contenedor Pulsar (solo la primera vez)

(Abre una terminal)

Windows/Linux:
docker run -d --name pulsar-standalone -p 6650:6650 -p 8080:8080 apachepulsar/pulsar:latest bin/pulsar standalone



(
********************
Si el contenedor aparece como "Exited", eliminarlo:
docker rm pulsar-standalone


Y volver a ejecutar el comando anterior.

********************
)



4. Verificar contenedor

Listar contenedores:
docker ps -a 

Si está apagado:
docker start pulsar-standalone


Verificar:
docker ps

(debe mostrar "up")



(aquí ya se puede correr Django)



------------------------------------------

LEVANTAR DJANGO

en otra terminal, dentro de la carpeta nuam, ejecuta

Windows:
python manage.py runserver

Linux/Mac:
python3 manage.py runserver



------------------------------------------

EJECUTAR EL CONSUMIDOR (opcional):

En otra terminal, corre:

python consumer.py



(
-Debe ejecutarse en otra terminal para no detener el servidor Django.
-Los mensajes enviados desde publish_event() aparecerán en consola y en la base de datos.
)

Explicación: escucha el topic eventos-nuam y guarda eventos en Django (EventoLog)
Los mensajes se guardan en la tabla EventoLog.
Puedes verlos desde tu admin de Django (/admin) o con python manage.py shell:



------------------------------------

VERIFICAR MENSAJES MANUALES EN PULSAR

docker exec -it pulsar-standalone bin/pulsar-client consume -s prueba1 -n 0 persistent://public/default/eventos-nuam


-s prueba1  →  nombre de la suscripción
-n 0  →  consume todos los mensajes del topic
persistent://public/default/eventos-nuam  →  topic



Salida esperada:
"Subscribed to topic on localhost/127.0.0.1:6650 -- consumer: 0"


Indica que el consumidor está escuchando correctamente.



---------------------------------------------

Funcionamiento interno:

Productor: pulsar_client.py:

Se conecta al broker de Pulsar que corre en localhost:6650.
Crea un productor para el topic eventos-nuam.
La función publish_event(data) toma un string data y lo envía al topic.
Cada vez que llames a publish_event("mensaje"), ese mensaje se envía a Pulsar.


Consumidor: consumer.py:

Configura Django para poder usar tus modelos (EventoLog).
Se conecta a Pulsar y se suscribe al mismo topic eventos-nuam.
Entra en un bucle infinito, escuchando mensajes.
Cada vez que llega un mensaje:
Lo imprime en consola (print("EVENTO RECIBIDO:", contenido)).
Lo guarda en tu base de datos Django como un nuevo EventoLog.
Confirma a Pulsar que el mensaje fue recibido (acknowledge).



----------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------


API EXTERNA    ->   Mindicador

Esta función obtiene indicadores económicos desde la API pública de Mindicador, 
como la TPM (Tasa Política Monetaria) y tasas de conversión CLP → PEN / CLP → COP.



Endpoint utilizado

URL: https://mindicador.cl/api
Método: GET
Respuesta: JSON con los indicadores.



Salida de la función:

tpm_actual	Valor de la TPM actual.
tc_clp_pen	Tipo de cambio CLP → PEN calculado.
tc_clp_cop	Tipo de cambio CLP → COP calculado.
error_api	Mensaje de error si falla la consulta.




---------------------------------------------------------------------------
----------------------------------------------------------------------------

API INTERNA


Endpoints reales de la API interna como JSON 
(se puede acceder desde Menu admin):

http://localhost:8000/api/usuarios/
http://127.0.0.1:8000/api/personas/   
http://127.0.0.1:8000/api/documentos/
http://localhost:8000/api/logs/



Swagger UI: 
interfaz web interactiva para explorar API REST
http://localhost:8000/swagger/




-----------------------------------------------------------------------
-----------------------------------------------------------------------

CERTIFICADOS
pkcs12






-----------------------------------------------------------------------
-----------------------------------------------------------------------

HTTPS (?)









************************************************************************************************
************************************************************************************************


PAUTA:

APIs RESTful: APIs completas con documentación autogenerada ✅ 

Integración Kafka/Pulsar - Productores: Productores optimizados con monitoreo y métricas ✅

Integración Kafka/Pulsar - Consumidores: Consumidores avanzados con balanceo y scaling ✅

Seguridad HTTPS/SSL: Seguridad avanzada con HSTS y mejores prácticas

Certificados Digitales: Sistema completo de rotación y renovación automática 

Manejo de Errores: Sistema proactivo con alertas y recuperación automática 

Logging y Monitoreo: Monitoreo en tiempo real con dashboards ✅

































