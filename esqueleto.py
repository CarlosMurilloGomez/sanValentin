from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from diccionarioAUtilizar import personas


TOKEN = "8195976477:AAHJ1racJ2qMCwvXI8e3I_aT1t-A2nHOrAc"
PREGUNTAS = {
    "Sexo": ["Hombre", "Mujer"],
    "Grado": ["Informatica", "Deporte", "Mecanizado", "Comercio"],
    "Fin": ["Nada serio", "Duda", "Relacion estable"],
    "Hijos": ["No quiere", "Duda", "Si quiere"]

}
historico = []

async def start(update: Update, context: CallbackContext) -> None:
    print(f'User: {update.effective_user.first_name}, Comando: {update.message.text}')

    """Muestra un mensaje de bienvenida."""
    await update.message.reply_text(f"¡Hola, {update.effective_user.first_name}! 😊\nUsa /love para comenzar el cuestionario.")

async def stop(update: Update, context: CallbackContext) -> None:
    print(f'User: {update.effective_user.first_name}, Comando: {update.message.text}')

    if historico.__len__() > 0:
        historico.clear()
        await update.message.reply_text("Cuestionario cancelado, escribe /love para volver a empezar")
    else:
        await update.message.reply_text("Aun no se ha comenzado ningun cuestionario, escribe /love para empezar")


async def back(update: Update, context: CallbackContext) -> None:
    print(f'User: {update.effective_user.first_name}, Comando: {update.message.text}')

    if historico.__len__() == 0:
        await update.message.reply_text("Aun no se ha comenzado ningun cuestionario, escribe /love para empezar")
    elif historico.__len__() > 1:
        historico.pop()
        await update.message.reply_text("Ultima respuesta eliminada, vuelve a contestarla")
    else:
        await update.message.reply_text("Aun no se ha respondido nada, escribe tu nombre:")


async def love(update: Update, context: CallbackContext) -> None:
    print(f'User: {update.effective_user.first_name}, Comando: {update.message.text}')
    if historico.__len__() > 0:
        await update.message.reply_text("Ya hay un cuestionario en marcha:")
    else:
        historico.append("Empezar")
        await update.message.reply_text("Escribe tu nombre completo:")

async def option_selected(update: Update, context: CallbackContext) -> None:
    print(f'User: {update.effective_user.first_name}, Mensaje: {update.message.text}')

    if historico.__len__() == 1:
        historico.append(update.message.text)
        await update.message.reply_text("Introduce tu edad:")
    elif historico.__len__() == 2:
        if update.message.text.isdigit():
            historico.append(update.message.text)
            keyboard = [[option] for option in PREGUNTAS["Sexo"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text("Introduce tu sexo:", reply_markup=reply_markup)
        else:
            await update.message.reply_text("Introduce una edad valida:")
    elif historico.__len__() == 3:
        if update.message.text in PREGUNTAS["Sexo"]:
            keyboard = [[option] for option in PREGUNTAS["Grado"]]
            historico.append(update.message.text)
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text("Introduce tu grado:", reply_markup=reply_markup)
        else:
            keyboard = [[option] for option in PREGUNTAS["Sexo"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text("Introduce un sexo valido:", reply_markup=reply_markup)
    elif historico.__len__() == 4:
        if update.message.text in PREGUNTAS["Grado"]:
            keyboard = [[option] for option in PREGUNTAS["Fin"]]
            historico.append(update.message.text)
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text("Introduce tu finalidad:", reply_markup=reply_markup)
        else:
            keyboard = [[option] for option in PREGUNTAS["Grado"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text("Introduce un grado valido:", reply_markup=reply_markup)
    elif historico.__len__() == 5:
        if update.message.text in PREGUNTAS["Fin"]:
            keyboard = [[option] for option in PREGUNTAS["Hijos"]]
            historico.append(update.message.text)
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text("Introduce si quieres hijos:", reply_markup=reply_markup)
        else:
            keyboard = [[option] for option in PREGUNTAS["Fin"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text("Introduce una finalidad valida:", reply_markup=reply_markup)
    elif historico.__len__() == 6:
        if update.message.text in PREGUNTAS["Hijos"]:
            historico.append(update.message.text)
            personas = buscarPersonasAfines(historico)
            await update.message.reply_text("Estas son las personas mas afines contigo:"+personas)
        else:
            keyboard = [[option] for option in PREGUNTAS["Hijos"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text("Introduce una respuesta valida de si quieres hijos:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Para iniciar el cuestionario escribe /love")

def buscarPersonasAfines(historico):
    personasAfines = personas
    for key, per in personasAfines.items():
        per["Afinidad"] = 0
        if int(historico[2]) > per["Edad"]-5 and int(historico[2]) < per["Edad"]+5:
            per["Afinidad"] +=1
        elif int(historico[2]) > per["Edad"]-2 and int(historico[2]) < per["Edad"]+2:
            per["Afinidad"] +=2

        if historico[3] != per["Sexo"]:
            per["Afinidad"] +=2

        if historico[4] == per["Grado"]:
            per["Afinidad"] +=1

        if historico[5]=="Duda" or per["Fin"]=="Duda":
            per["Afinidad"] +=1
        elif historico[5] == per["Fin"]:
            per["Afinidad"] +=2

        if historico[6]=="Duda" or per["Hijos"]=="Duda":
            per["Afinidad"] +=1
        elif historico[6] == per["Fin"]:
            per["Afinidad"] +=2

    personas_ordenadas = dict(sorted(personasAfines.items(), key=lambda x: x[1]['Afinidad'], reverse=True))
    return "\n- " + personas_ordenadas.get(0)["NombreCompleto"] + "\n- " + personas_ordenadas.get(1)["NombreCompleto"] + "\n- " + personas_ordenadas.get(2)["NombreCompleto"]


def main():
    """Configura y ejecuta el bot."""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("love", love))
    app.add_handler(CommandHandler("back", back))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, option_selected))


    app.run_polling()

if __name__ == "__main__":
    main()