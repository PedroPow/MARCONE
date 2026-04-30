# main.py
# SUBSTITUA SEU MAIN COMPLETO

import discord
from discord.ext import commands
from views.ticket_view import TicketView, PainelAbrirTicketView
from views.live_view import LiveVideoView
from discord.ext import commands
import os
from dotenv import load_dotenv 

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

CANAL_ABRIR_TICKET = 1498888608818397266
CANAL_LIVE_VIDEO = 1488723564247908462

# ============================
#        COMANDO /clearall
# ============================
@bot.tree.command(name="clearall", description="Apaga todas as mensagens do canal atual.", guild=discord.Object(id=GUILD_ID))
async def clearall(interaction: discord.Interaction):
    # validar cargo autorizado
    if not await require_authorized(interaction):
        return

    canal = interaction.channel
    guild = interaction.guild
    if canal is None or guild is None:
        return await interaction.response.send_message("❌ Contexto inválido.", ephemeral=True)

    # responder rápido
    await interaction.response.send_message(f"🧹 Limpando todas as mensagens do canal **{canal.name}**...", ephemeral=True)

    # limpa mensagens
    try:
        # limite=None as vezes falha em alguns builds, tenta em bloco
        await canal.purge(limit=100)
    except Exception:
        try:
            await canal.purge()
        except Exception:
            # se tudo falhar, informa o usuário
            pass

    # enviar confirmação no canal limpo (se permitido)
    try:
        embed_confirm = discord.Embed(
            title="🧹 Canal Limpo",
            description=f"As mensagens do canal `{canal.name}` foram apagadas com sucesso!",
            color=discord.Color.green()
        )
        await canal.send(embed=embed_confirm)
    except Exception:
        # sem permissão para enviar no canal limpo — ignora
        pass

    # preparar log detalhado e enviar para o canal de logs (LOG_CHANNEL_ID)
    embed_log = discord.Embed(
        title="🧹 Log - Canal Limpo",
        description=(
            f"**Usuário:** {interaction.user.mention}\n"
            f"**ID do usuário:** `{interaction.user.id}`\n"
            f"**Canal limpo:** {canal.mention}\n"
            f"**Servidor:** `{guild.name}`"
        ),
        color=discord.Color.orange(),
        timestamp=discord.utils.utcnow()
    )
    embed_log.set_footer(text=f"Ação: clearall")

    await enviar_log_embed(guild, embed_log)

# ============================
#         MODAL /mensagem
# ============================
class MensagemModal(Modal, title="📢 Enviar Mensagem"):
    conteudo = TextInput(
        label="Conteúdo da mensagem",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=2000
    )

    async def on_submit(self, interaction: discord.Interaction):
        # checar autorização rapidamente
        if not has_authorized_role(interaction.user):
            # interação ainda pode ser respondida
            await interaction.response.send_message("❌ Você não tem permissão para usar este modal.", ephemeral=True)
            return

        await interaction.response.send_message("⏳ Enviando...", ephemeral=True)

        try:
            msg_inicial = await interaction.channel.send(self.conteudo.value)
        except Exception:
            await interaction.followup.send("❌ Não consegui enviar a mensagem inicial (permissão).", ephemeral=True)
            return

        await interaction.followup.send(
            "📎 Responda aquela mensagem com anexos em até 5 minutos.",
            ephemeral=True
        )

        def check(m: discord.Message):
            return (
                m.reference and
                m.reference.message_id == msg_inicial.id and
                m.author == interaction.user and
                m.channel == interaction.channel
            )

        try:
            reply = await bot.wait_for("message", timeout=300.0, check=check)
            files = []
            async with aiohttp.ClientSession() as session:
                for a in reply.attachments:
                    try:
                        async with session.get(a.url) as resp:
                            dados = await resp.read()
                            files.append(discord.File(io.BytesIO(dados), filename=a.filename))
                    except Exception:
                        continue

            # tenta deletar mensagens do usuário e a de confirmação
            try:
                await msg_inicial.delete()
                await reply.delete()
            except Exception:
                pass

            try:
                await interaction.channel.send(content=self.conteudo.value, files=files)
            except Exception:
                await interaction.followup.send("❌ Não consegui reenviar a mensagem (permissão).", ephemeral=True)

        except asyncio.TimeoutError:
            # tempo esgotado — só ignora
            try:
                await interaction.followup.send("⏰ Tempo esgotado. Nenhum anexo recebido.", ephemeral=True)
            except Exception:
                pass

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

bot.run(os.getenv("TOKEN_MCN"))