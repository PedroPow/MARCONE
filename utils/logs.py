async def enviar_log(bot, canal_id, texto):
    canal = bot.get_channel(canal_id)
    if canal:
        await canal.send(texto)