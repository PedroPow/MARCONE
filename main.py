# main.py
# SUBSTITUA SEU MAIN COMPLETO

import discord
from discord.ext import commands
from discord.ui import Modal, TextInput, View, Button, Select
from views.ticket_view import TicketView, PainelAbrirTicketView
from views.live_view import LiveVideoView
import os
import asyncio
import aiohttp
import io
from dotenv import load_dotenv

GUILD_ID = 1502777759863144518

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

load_dotenv()
TOKEN = os.getenv("TOKEN_MCN")  # Certifique-se de definir o TOKEN no .env ou variáveis de ambiente

# guard para não reenviar painel/verify em reconexões
bot._ready_sent = False

# ===============================
# IDS FIXOS
# ===============================

CANAL_ABRIR_TICKET = 1502777767610155126
CANAL_LIVE_VIDEO = 1502777768058814508


@bot.tree.command(name="mensagem", description="Enviar mensagem como o bot.", guild=discord.Object(id=GUILD_ID))
async def mensagem(interaction: discord.Interaction):
    if not await require_authorized(interaction):
        return
    # abrir modal
    await interaction.response.send_modal(MensagemModal())

# ===============================
# READY
# ===============================

@bot.event
async def on_ready():
    print(f"✅ {bot.user} online")
    print(f"Guilds: {[g.name for g in bot.guilds]}")
    print(f"Nome do Bot: {bot.user.name}#{bot.user.discriminator} (ID: {bot.user.id})")
    print(f"Comandos registrados: {len(bot.tree.get_commands())}")

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
            "> `Deseja virar streamer da JardimPeri?`\n"
            "> `Clique no botão abaixo para abrir ticket.`"
        ),
        color=0xf1c40f
    )

    embed.set_image(url="https://cdn.discordapp.com/attachments/1444735189765849320/1487656538159190076/EMAIL_CRIADORES_AMARELO_KABRINHA.png?ex=69f2ce1e&is=69f17c9e&hm=07a19cd2c52ae288163fe3211d3d9f1d4e849403d4bbf79bd09950181319af20&")

    embed.set_footer(text="Criadores JardimPeri® - Todos os direitos reservados", icon_url="https://cdn.discordapp.com/emojis/1490521797454598224.webp?size=96")    

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

    embed2.set_image(url="https://cdn.discordapp.com/attachments/1444735189765849320/1503019253782282362/bannerPeri.png?ex=6a0324c2&is=6a01d342&hm=054302c0966bc1fd56e0b0ab0eeb76386d9a499bc53458684a966cd2f4aa2088&")

    embed2.set_footer(text="Criadores JardimPeri® - Todos os direitos reservados", icon_url="https://cdn.discordapp.com/attachments/1444735189765849320/1503019230910746654/GIF_PERI.gif?ex=6a0324bd&is=6a01d33d&hm=f73a9ccccd7c7e3fb9336e7a6aa29ee58492f9061c262c7153597e5844a02ea2&")    

    await canal_live.send(
        embed=embed2,
        view=LiveVideoView()
    )

bot.run(os.getenv("TOKEN_MCN"))