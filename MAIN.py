from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from BD import (
    cargar_usuarios,
    cargar_solicitudes,
    guardar_usuarios,
    guardar_solicitudes
)

from VACACIONES import (
    obtener_usuario,
    consultar_saldo,
    validar_fechas,
    calcular_dias,
    saldo_suficiente,
    hay_conflicto,
    crear_solicitud,
    aprobar_solicitud,
    rechazar_solicitud,
    cancelar_solicitud,
    solicitudes_usuario,
    solicitudes_pendientes
)


TOKEN = "8821613432:AAEKC9QpJ4UvFe4DhIQ_vI6Hx0-7Pe3yLO8"

usuarios = cargar_usuarios()
solicitudes = cargar_solicitudes()

estados_usuario = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "BOT DE GESTIÓN DE VACACIONES\n\n"
        "Comandos disponibles:\n"
        "/solicitar_vacaciones\n"
        "/saldo actual\n"
        "/mis_solicitudes\n"
        "/cancelar solicitud\n"
        "/solicitudes pendientes\n"
        "Opciones de administrador:\n"
        "/aprobar solicitud\n"
        "/rechazar solicitud"
    )


async def solicitar_vacaciones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    estados_usuario[chat_id] = {
        "accion": "solicitar",
        "paso": "PEDIR_USUARIO"
    }

    await update.message.reply_text("Ingrese su ID de usuario:")


async def saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    estados_usuario[chat_id] = {
        "accion": "saldo",
        "paso": "PEDIR_USUARIO"
    }

    await update.message.reply_text("Ingrese su ID de usuario:")


async def mis_solicitudes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    estados_usuario[chat_id] = {
        "accion": "mis_solicitudes",
        "paso": "PEDIR_USUARIO"
    }

    await update.message.reply_text("Ingrese su ID de usuario:")


async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    estados_usuario[chat_id] = {
        "accion": "cancelar",
        "paso": "PEDIR_USUARIO"
    }

    await update.message.reply_text("Ingrese su ID de usuario:")


async def pendientes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = solicitudes_pendientes(solicitudes)

    if len(lista) == 0:
        await update.message.reply_text("No hay solicitudes pendientes.")
        return

    texto = "SOLICITUDES EN REVISIÓN:\n\n"

    for s in lista:
        texto += (
            f"ID: {s['solicitud_id']}\n"
            f"Usuario: {s['user_id']}\n"
            f"Desde: {s['fecha_inicio']}\n"
            f"Hasta: {s['fecha_fin']}\n"
            f"Días: {s['dias']}\n\n"
        )

    await update.message.reply_text(texto)


async def aprobar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    estados_usuario[chat_id] = {
        "accion": "aprobar",
        "paso": "PEDIR_SOLICITUD"
    }

    await update.message.reply_text("Ingrese el ID de la solicitud a aprobar:")


async def rechazar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    estados_usuario[chat_id] = {
        "accion": "rechazar",
        "paso": "PEDIR_SOLICITUD"
    }

    await update.message.reply_text("Ingrese el ID de la solicitud a rechazar:")


async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global usuarios, solicitudes

    chat_id = update.message.chat_id
    mensaje = update.message.text.strip()

    if chat_id not in estados_usuario:
        await update.message.reply_text(
            "No hay un proceso iniciado. Usá /start para ver los comandos."
        )
        return

    estado = estados_usuario[chat_id]
    accion = estado["accion"]
    paso = estado["paso"]

    # ==========================
    # SOLICITAR VACACIONES
    # ==========================

    if accion == "solicitar":

        if paso == "PEDIR_USUARIO":
            usuario = obtener_usuario(usuarios, mensaje)

            if usuario is None:
                await update.message.reply_text("Usuario inexistente. Volviendo al menú.")
                del estados_usuario[chat_id]
                return

            estado["user_id"] = mensaje
            estado["usuario"] = usuario
            estado["paso"] = "PEDIR_FECHA_INICIO"

            await update.message.reply_text("Ingrese fecha inicio AAAA-MM-DD:")

        elif paso == "PEDIR_FECHA_INICIO":
            estado["fecha_inicio"] = mensaje
            estado["paso"] = "PEDIR_FECHA_FIN"

            await update.message.reply_text("Ingrese fecha fin AAAA-MM-DD:")

        elif paso == "PEDIR_FECHA_FIN":
            estado["fecha_fin"] = mensaje

            try:
                if not validar_fechas(
                    estado["fecha_inicio"],
                    estado["fecha_fin"]
                ):
                    await update.message.reply_text(
                        "Fechas inválidas. La fecha final no puede ser anterior a la inicial."
                    )
                    del estados_usuario[chat_id]
                    return

            except ValueError:
                await update.message.reply_text(
                    "Formato de fecha incorrecto. Usá AAAA-MM-DD."
                )
                del estados_usuario[chat_id]
                return

            estado["paso"] = "PEDIR_MOTIVO"

            await update.message.reply_text("Ingrese el motivo de la solicitud:")

        elif paso == "PEDIR_MOTIVO":
            estado["motivo"] = mensaje

            dias = calcular_dias(
                estado["fecha_inicio"],
                estado["fecha_fin"]
            )

            if not saldo_suficiente(estado["usuario"], dias):
                await update.message.reply_text(
                    "Solicitud rechazada por saldo insuficiente."
                )
                del estados_usuario[chat_id]
                return

            if hay_conflicto(
                estado["user_id"],
                estado["fecha_inicio"],
                estado["fecha_fin"],
                solicitudes
            ):
                await update.message.reply_text(
                    "Existe conflicto con otra solicitud APROBADA o EN_REVISION."
                )
                del estados_usuario[chat_id]
                return

            nueva = crear_solicitud(
                solicitudes,
                estado["user_id"],
                estado["fecha_inicio"],
                estado["fecha_fin"],
                estado["motivo"]
            )

            guardar_solicitudes(solicitudes)

            await update.message.reply_text(
                "Solicitud registrada correctamente.\n\n"
                f"ID: {nueva['solicitud_id']}\n"
                f"Estado: {nueva['estado']}\n"
                f"Días solicitados: {nueva['dias']}\n\n"
                "Se notificó al jefe/aprobador."
            )

            del estados_usuario[chat_id]

    # ==========================
    # CONSULTAR SALDO
    # ==========================

    elif accion == "saldo":

        usuario = obtener_usuario(usuarios, mensaje)

        if usuario is None:
            await update.message.reply_text("Usuario inexistente.")
        else:
            await update.message.reply_text(
                f"Empleado: {usuario['nombre']}\n"
                f"Saldo disponible: {consultar_saldo(usuario)} días"
            )

        del estados_usuario[chat_id]

    # ==========================
    # VER MIS SOLICITUDES
    # ==========================

    elif accion == "mis_solicitudes":

        usuario = obtener_usuario(usuarios, mensaje)

        if usuario is None:
            await update.message.reply_text("Usuario inexistente.")
            del estados_usuario[chat_id]
            return

        lista = solicitudes_usuario(mensaje, solicitudes)

        if len(lista) == 0:
            await update.message.reply_text("No tiene solicitudes registradas.")
        else:
            texto = "MIS SOLICITUDES:\n\n"

            for s in lista:
                texto += (
                    f"ID: {s['solicitud_id']}\n"
                    f"Desde: {s['fecha_inicio']}\n"
                    f"Hasta: {s['fecha_fin']}\n"
                    f"Días: {s['dias']}\n"
                    f"Estado: {s['estado']}\n"
                    f"Comentario: {s['comentario']}\n\n"
                )

            await update.message.reply_text(texto)

        del estados_usuario[chat_id]

    # ==========================
    # CANCELAR SOLICITUD
    # ==========================

    elif accion == "cancelar":

        if paso == "PEDIR_USUARIO":
            usuario = obtener_usuario(usuarios, mensaje)

            if usuario is None:
                await update.message.reply_text("Usuario inexistente.")
                del estados_usuario[chat_id]
                return

            estado["user_id"] = mensaje
            estado["paso"] = "PEDIR_SOLICITUD"

            await update.message.reply_text("Ingrese el ID de la solicitud a cancelar:")

        elif paso == "PEDIR_SOLICITUD":
            ok = cancelar_solicitud(
                mensaje,
                estado["user_id"],
                solicitudes
            )

            if ok:
                guardar_solicitudes(solicitudes)
                await update.message.reply_text("Solicitud cancelada correctamente.")
            else:
                await update.message.reply_text(
                    "No fue posible cancelar la solicitud. Puede que no exista o ya esté aprobada."
                )

            del estados_usuario[chat_id]

    # ==========================
    # APROBAR SOLICITUD
    # ==========================

    elif accion == "aprobar":

        if paso == "PEDIR_SOLICITUD":
            estado["solicitud_id"] = mensaje
            estado["paso"] = "PEDIR_APROBADOR"

            await update.message.reply_text("Ingrese ID del aprobador:")

        elif paso == "PEDIR_APROBADOR":
            ok = aprobar_solicitud(
                estado["solicitud_id"],
                mensaje,
                solicitudes,
                usuarios
            )

            if ok:
                guardar_solicitudes(solicitudes)
                guardar_usuarios(usuarios)

                await update.message.reply_text("Solicitud aprobada correctamente.")
            else:
                await update.message.reply_text("Solicitud inexistente.")

            del estados_usuario[chat_id]

    # ==========================
    # RECHAZAR SOLICITUD
    # ==========================

    elif accion == "rechazar":

        if paso == "PEDIR_SOLICITUD":
            estado["solicitud_id"] = mensaje
            estado["paso"] = "PEDIR_APROBADOR"

            await update.message.reply_text("Ingrese ID del aprobador:")

        elif paso == "PEDIR_APROBADOR":
            estado["aprobador"] = mensaje
            estado["paso"] = "PEDIR_MOTIVO"

            await update.message.reply_text("Ingrese motivo del rechazo:")

        elif paso == "PEDIR_MOTIVO":
            ok = rechazar_solicitud(
                estado["solicitud_id"],
                estado["aprobador"],
                mensaje,
                solicitudes
            )

            if ok:
                guardar_solicitudes(solicitudes)

                await update.message.reply_text("Solicitud rechazada correctamente.")
            else:
                await update.message.reply_text("Solicitud inexistente.")

            del estados_usuario[chat_id]


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("solicitar_vacaciones", solicitar_vacaciones))
    app.add_handler(CommandHandler("saldo", saldo))
    app.add_handler(CommandHandler("mis_solicitudes", mis_solicitudes))
    app.add_handler(CommandHandler("cancelar", cancelar))
    app.add_handler(CommandHandler("pendientes", pendientes))
    app.add_handler(CommandHandler("aprobar", aprobar))
    app.add_handler(CommandHandler("rechazar", rechazar))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))

    print("Bot iniciado correctamente...")
    app.run_polling()


if __name__ == "__main__":
    main()