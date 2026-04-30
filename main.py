# main.py
# SUBSTITUA SEU MAIN COMPLETO

import discord
from discord.ext import commands
from views.ticket_view import TicketView, PainelAbrirTicketView
from views.live_view import LiveVideoView
from os import getenv
from dotenv import load_dotenv  

load_dotenv()

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

TOKEN = os.getenv("TOKEN_MCN")  # Certifique-se de definir o TOKEN no .env ou variáveis de ambiente

# guard para não reenviar painel/verify em reconexões
bot._ready_sent = False

# ===============================
# IDS FIXOS
# ===============================

CANAL_ABRIR_TICKET = 1498888608818397266
CANAL_LIVE_VIDEO = 1488723564247908462

# ===============================
# READY
# ===============================

@bot.event
async def on_ready():
    print(f"✅ {bot.user} online")

    bot.add_view(PainelAbrirTicketView(bot))
    bot.add_view(TicketView(bot))
    bot.add_view(LiveVideoView())

    canal_ticket = bot.get_channel(CANAL_ABRIR_TICKET)
    canal_live = bot.get_channel(CANAL_LIVE_VIDEO)

    # limpa mensagens antigas do bot
    async for msg in canal_ticket.history(limit=20):
        if msg.author == bot.user:
            await msg.delete()

    async for msg in canal_live.history(limit=20):
        if msg.author == bot.user:
            await msg.delete()

    # painel ticket
    embed = discord.Embed(
        title="<:TICKET:1498895809645908021> CENTRAL DE CADASTRO",
        description=(
            "> `Deseja virar streamer da MarconeRP?`\n"
            "> `Clique no botão abaixo para abrir ticket.`"
        ),
        color=0xf1c40f
    )

    embed.set_image(url="https://cdn.discordapp.com/attachments/1444735189765849320/1487656538159190076/EMAIL_CRIADORES_AMARELO_KABRINHA.png?ex=69f2ce1e&is=69f17c9e&hm=07a19cd2c52ae288163fe3211d3d9f1d4e849403d4bbf79bd09950181319af20&")

    embed.set_footer(text="Criadores MarconeRP® - Todos os direitos reservados", icon_url="https://cdn.discordapp.com/emojis/1490521797454598224.webp?size=96")    

    await canal_ticket.send(
        embed=embed,
        view=PainelAbrirTicketView(bot)
    )

    # painel lives
    embed2 = discord.Embed(
        title="<:PLAY:1489111805602173058> PAINEL DE DIVULGAÇÃO",
        description="> `Quer divulgar sua live ou vídeo para a comunidade?`\n" \
        "> `Clique no botão abaixo para enviar seus conteúdos para todos.`",
        color=0xf1c40f
    )

    embed2.set_image(url="https://cdn.discordapp.com/attachments/1444735189765849320/1487656538159190076/EMAIL_CRIADORES_AMARELO_KABRINHA.png?ex=69f2ce1e&is=69f17c9e&hm=07a19cd2c52ae288163fe3211d3d9f1d4e849403d4bbf79bd09950181319af20&")

    embed2.set_footer(text="Criadores MarconeRP® - Todos os direitos reservados", icon_url="https://cdn.discordapp.com/emojis/1490521797454598224.webp?size=96")    

    await canal_live.send(
        embed=embed2,
        view=LiveVideoView()
    )

bot.run(getenv("TOKEN_MCR"))