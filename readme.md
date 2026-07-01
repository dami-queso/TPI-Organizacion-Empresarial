# BOT DE GESTIÓN DE VACACIONES

## Trabajo Práctico Integrador – Organización Empresarial

### Tecnicatura Universitaria en Programación a Distancia (UTN)

---

# Descripción

Este proyecto consiste en el desarrollo de un chatbot para la gestión de solicitudes de vacaciones, implementado en Python e integrado con Telegram.

El sistema automatiza el proceso de solicitud de vacaciones siguiendo un modelo BPMN 2.0. El bot interactúa con los empleados, valida las reglas de negocio, registra las solicitudes, consulta una base de datos simulada mediante archivos CSV y permite que un jefe apruebe o rechace las solicitudes.

---

# Objetivo

Automatizar el proceso administrativo de gestión de vacaciones mediante un chatbot que permita:

* Solicitar vacaciones.
* Consultar saldo de días disponibles.
* Validar reglas de negocio.
* Detectar conflictos de fechas.
* Registrar solicitudes.
* Aprobar o rechazar solicitudes.
* Cancelar solicitudes pendientes.
* Actualizar automáticamente el saldo de vacaciones.

---

# Tecnologías utilizadas

* Python 3.13
* python-telegram-bot
* csv
* datetime
* enum

---

# Estructura del proyecto

```text
ProyectoBotVacaciones/

│── main.py
│── bd.py
│── vacaciones.py
│── estados.py
│── usuarios.csv
│── solicitudes.csv
│── README.md
```

---

# Base de datos

La información del sistema se almacena utilizando dos archivos CSV.

## usuarios.csv

Contiene los empleados registrados.

Campos:

* user_id
* nombre
* saldo_vacaciones

Ejemplo:

```csv
user_id,nombre,saldo_vacaciones
U1,Ana Perez,12
U2,Bruno Gomez,3
U3,Carla Ruiz,20
```

---

## solicitudes.csv

Registra todas las solicitudes realizadas.

Campos:

* solicitud_id
* user_id
* fecha_inicio
* fecha_fin
* dias
* estado
* aprobador_id
* comentario
* fecha_creacion

Estados posibles:

* EN_REVISION
* APROBADO
* RECHAZADO
* CANCELADO

---

# Funcionalidades

El chatbot permite:

* Solicitar vacaciones.
* Consultar saldo disponible.
* Consultar solicitudes realizadas.
* Cancelar solicitudes pendientes.
* Ver solicitudes pendientes de aprobación.
* Aprobar solicitudes.
* Rechazar solicitudes.
* Actualizar automáticamente el saldo de vacaciones.

---

# Flujo del proceso

1. El usuario inicia una solicitud mediante Telegram.
2. El bot solicita el ID del usuario.
3. El bot solicita las fechas de inicio y fin.
4. El usuario ingresa el motivo.
5. El sistema calcula la cantidad de días solicitados.
6. Se consulta el saldo disponible.
7. Se verifica si existen conflictos de fechas.
8. Si todas las validaciones son correctas, la solicitud queda registrada con estado **EN_REVISION**.
9. El jefe consulta las solicitudes pendientes.
10. El jefe aprueba o rechaza la solicitud.
11. Si la solicitud es aprobada, el sistema descuenta automáticamente los días del saldo del empleado.
12. El bot informa el resultado al usuario.

---

# Comandos disponibles

## Usuario

### /start

Muestra el menú de comandos disponibles.

### /solicitar_vacaciones

Inicia una nueva solicitud de vacaciones.

### /saldo

Consulta el saldo de días disponibles.

### /mis_solicitudes

Muestra todas las solicitudes realizadas por el usuario.

### /cancelar

Permite cancelar una solicitud que aún no haya sido aprobada.

---

## Jefe / Aprobador

### /pendientes

Muestra las solicitudes pendientes de aprobación.

### /aprobar

Aprueba una solicitud.

### /rechazar

Rechaza una solicitud indicando el motivo.

---

# Máquina de estados

El bot mantiene el estado de cada conversación para continuar el flujo correspondiente.

Estados principales:

* PEDIR_USUARIO
* PEDIR_FECHA_INICIO
* PEDIR_FECHA_FIN
* PEDIR_MOTIVO
* PEDIR_SOLICITUD
* PEDIR_APROBADOR

Esto permite que cada usuario continúe el proceso desde el punto en el que se encontraba.

---

# Validaciones implementadas

El sistema contempla distintos escenarios:

* Usuario inexistente.
* Formato incorrecto de fechas.
* Fecha final anterior a la fecha inicial.
* Saldo insuficiente.
* Conflicto de fechas.
* Solicitud inexistente.
* Cancelación de solicitudes aprobadas.

---

# Instalación

Instalar la dependencia necesaria:

```bash
py -m pip install python-telegram-bot
```

---

# Configuración

Crear un bot mediante **BotFather** en Telegram.

Obtener el token generado por BotFather y reemplazar la siguiente línea en `main.py`:

```python
TOKEN = "PEGAR_ACA_EL_TOKEN_DE_BOTFATHER"
```

por el token real:

```python
TOKEN = "123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

---

# Ejecución

Ubicarse en la carpeta del proyecto y ejecutar:

```bash
py main.py
```

Si el bot inicia correctamente aparecerá el siguiente mensaje:

```text
Bot iniciado correctamente...
```

A partir de ese momento se podrá interactuar con el bot desde Telegram utilizando los comandos disponibles.

---

# Relación con el BPMN

La implementación respeta el modelo BPMN diseñado para el proceso TO-BE.

* Usuario: inicia la solicitud e ingresa la información requerida.
* Sistema/Bot: valida los datos, consulta la base de datos, registra la solicitud y notifica los resultados.
* Jefe/Aprobador: revisa la solicitud y decide aprobarla o rechazarla.

Los gateways implementados son:

* Verificación de existencia del usuario.
* Validación de fechas.
* Verificación de saldo disponible.
* Detección de conflictos de fechas.
* Decisión de aprobación o rechazo.

---

# Autores

Lautaro Bustillo
Ana Clara Pennacchio
