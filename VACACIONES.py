from datetime import datetime


# ==========================
# USUARIOS
# ==========================

def obtener_usuario(usuarios, user_id):
    """Busca un usuario por su ID."""

    for usuario in usuarios:
        if usuario["user_id"] == user_id:
            return usuario

    return None


def consultar_saldo(usuario):
    """Devuelve el saldo de vacaciones."""

    return usuario["saldo_vacaciones"]


def saldo_suficiente(usuario, dias):
    """Verifica si posee días suficientes."""

    return usuario["saldo_vacaciones"] >= dias


# ==========================
# VALIDACIONES
# ==========================

def calcular_dias(fecha_inicio, fecha_fin):
    """Calcula la cantidad de días solicitados."""

    inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fin = datetime.strptime(fecha_fin, "%Y-%m-%d")

    return (fin - inicio).days + 1


def validar_fechas(fecha_inicio, fecha_fin):
    """Verifica que la fecha final sea mayor o igual a la inicial."""

    inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fin = datetime.strptime(fecha_fin, "%Y-%m-%d")

    return fin >= inicio


# ==========================
# GATEWAY 2
# CONFLICTO DE FECHAS
# ==========================

def hay_conflicto(user_id, inicio, fin, solicitudes):
    """
    Verifica si el usuario ya posee una solicitud
    aprobada o en revisión para esas fechas.
    """

    for solicitud in solicitudes:

        if solicitud["user_id"] != user_id:
            continue

        if solicitud["estado"] not in ["APROBADO", "EN_REVISION"]:
            continue

        if (
            inicio <= solicitud["fecha_fin"] and
            fin >= solicitud["fecha_inicio"]
        ):
            return True

    return False


# ==========================
# SOLICITUDES
# ==========================

def generar_id(solicitudes):
    """Genera un nuevo ID de solicitud."""

    if len(solicitudes) == 0:
        return "S1"

    ultimo = solicitudes[-1]["solicitud_id"]

    numero = int(ultimo[1:])

    return f"S{numero + 1}"


def crear_solicitud(
        solicitudes,
        user_id,
        inicio,
        fin,
        motivo):

    dias = calcular_dias(inicio, fin)

    nueva = {

        "solicitud_id": generar_id(solicitudes),

        "user_id": user_id,

        "fecha_inicio": inicio,

        "fecha_fin": fin,

        "dias": dias,

        "estado": "EN_REVISION",

        "aprobador_id": "",

        "comentario": motivo,

        "fecha_creacion":
            datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    }

    solicitudes.append(nueva)

    return nueva


# ==========================
# APROBAR
# ==========================

def aprobar_solicitud(
        solicitud_id,
        aprobador,
        solicitudes,
        usuarios):

    for solicitud in solicitudes:

        if solicitud["solicitud_id"] == solicitud_id:

            solicitud["estado"] = "APROBADO"

            solicitud["aprobador_id"] = aprobador

            solicitud["comentario"] = "Solicitud aprobada"

            dias = solicitud["dias"]

            for usuario in usuarios:

                if usuario["user_id"] == solicitud["user_id"]:

                    usuario["saldo_vacaciones"] -= dias

            return True

    return False


# ==========================
# RECHAZAR
# ==========================

def rechazar_solicitud(
        solicitud_id,
        aprobador,
        comentario,
        solicitudes):

    for solicitud in solicitudes:

        if solicitud["solicitud_id"] == solicitud_id:

            solicitud["estado"] = "RECHAZADO"

            solicitud["aprobador_id"] = aprobador

            solicitud["comentario"] = comentario

            return True

    return False


# ==========================
# CANCELAR
# ==========================

def cancelar_solicitud(
        solicitud_id,
        user_id,
        solicitudes):

    for solicitud in solicitudes:

        if (
            solicitud["solicitud_id"] == solicitud_id and
            solicitud["user_id"] == user_id
        ):

            if solicitud["estado"] == "APROBADO":
                return False

            solicitud["estado"] = "CANCELADO"

            solicitud["comentario"] = "Cancelada por usuario"

            return True

    return False


# ==========================
# CONSULTAS
# ==========================

def solicitudes_usuario(user_id, solicitudes):

    resultado = []

    for solicitud in solicitudes:

        if solicitud["user_id"] == user_id:
            resultado.append(solicitud)

    return resultado


def solicitudes_pendientes(solicitudes):

    pendientes = []

    for solicitud in solicitudes:

        if solicitud["estado"] == "EN_REVISION":
            pendientes.append(solicitud)

    return pendientes
