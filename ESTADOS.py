from enum import Enum


class Estado(Enum):
    MENU = 0

    # Flujo de solicitud
    INGRESAR_USUARIO = 1
    INGRESAR_FECHA_INICIO = 2
    INGRESAR_FECHA_FIN = 3
    INGRESAR_MOTIVO = 4

    # Validaciones
    VALIDAR_SALDO = 5
    VALIDAR_CONFLICTO = 6

    # Resultado
    ENVIADA_A_JEFE = 7
    APROBADA = 8
    RECHAZADA = 9
    CANCELADA = 10

    # Consultas
    CONSULTAR_SALDO = 11
    VER_SOLICITUDES = 12

    # Jefe
    APROBAR_RECHAZAR = 13

    # Salida
    FIN = 99
