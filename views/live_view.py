# ==========================================
# views/live_view.py
# SISTEMA LIVE / VIDEO PROFISSIONAL
# link obrigatório
# descrição opcional
# plataforma automática
# emoji automático
# ==========================================

import discord
from discord.ui import View, Button, Modal, TextInput
from database import cursor, db
from utils.plataformas import detectar_plataforma, link_permitido

CANAL_LIVES = 1425626605455151154   # ID canal lives
CANAL_VIDEOS = 1425626605455151155 # ID canal videos

def embed_padrao(msg, ok=True):
    cor = 0xF1C40F if ok else 0xE74C3C
    return discord.Embed(description=msg, color=cor)


# ==========================================
# VIEW PRINCIPAL
# ==========================================

class LiveVideoView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Divulgar Live",
        emoji="<:PLAY:1489111805602173058>",
        style=discord.ButtonStyle.gray,
        custom_id="abrir_live"
    )
    async def abrir_live(self, interaction, button):
        await interaction.response.send_modal(LiveModal())

    @discord.ui.button(
        label="Divulgar Vídeo",
        emoji="<:PLAY:1489111805602173058>",
        style=discord.ButtonStyle.gray,
        custom_id="enviar_video"
    )
    async def enviar_video(self, interaction, button):
        await interaction.response.send_modal(VideoModal())


# ==========================================
# MODAL LIVE
# ==========================================

class LiveModal(Modal, title="Abrir Live"):

    link = TextInput(
        label="Link da Live",
        placeholder="https://twitch.tv/...",
        required=True
    )

    descricao = TextInput(
        label="Descrição",
        placeholder="Opcional",
        required=False,
        style=discord.TextStyle.paragraph
    )

    async def on_submit(self, interaction):

        link = self.link.value.strip()

        if not link_permitido(link):
            return await interaction.response.send_message(
                embed=embed_padrao("❌ Link inválido.", False),
                ephemeral=True
            )

        dados = detectar_plataforma(link)

        desc = self.descricao.value.strip()

        if not desc:
            desc = f"Vem pra live na cidade Marcone Roleplay® | #2026\n Segue, Curte, Comente e Compartilhe"

        embed = discord.Embed(
            title=f"{dados['emoji']} LIVE ON-LINE",
            description=f"{interaction.user.mention} está ao vivo em {dados['emoji']}\n\n {desc}",
            color=0xf1c40f
        )

        embed.add_field(
            name=f"{dados['emoji']} Assista:",
            value=link,
            inline=False
        )

        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1444735189765849320/1487659680997179612/ADESIVO_AMARELO_MARCONE_1.png?ex=69f379cb&is=69f2284b&hm=cfd03255779617aa67562773f06de7ae9d91beb38ae5a65ea698ef1fe9d25ae0&")

        embed.set_image(url="https://cdn.discordapp.com/attachments/1444735189765849320/1487656538159190076/EMAIL_CRIADORES_AMARELO_KABRINHA.png?ex=69f2ce1e&is=69f17c9e&hm=07a19cd2c52ae288163fe3211d3d9f1d4e849403d4bbf79bd09950181319af20&")

        embed.set_footer(text="Criadores MarconeRP® - Todos os direitos reservados", icon_url="https://cdn.discordapp.com/emojis/1490521797454598224.webp?size=96")        

        canal = interaction.guild.get_channel(CANAL_LIVES)

        if canal is None:
            canal = await interaction.guild.fetch_channel(CANAL_LIVES)

        msg = await canal.send(embed=embed)

        cursor.execute(
            "INSERT INTO lives(user_id, msg_id) VALUES (?,?)",
            (interaction.user.id, msg.id)
        )
        db.commit()

        await interaction.response.send_message(
            embed=embed_padrao("✅ Live enviada."),
            ephemeral=True
        )


# ==========================================
# MODAL VIDEO
# ==========================================

class VideoModal(Modal, title="Enviar Vídeo"):

    link = TextInput(
        label="Link do Vídeo",
        placeholder="https://youtube.com/...",
        required=True
    )

    descricao = TextInput(
        label="Descrição",
        placeholder="Opcional",
        required=False,
        style=discord.TextStyle.paragraph
    )

    async def on_submit(self, interaction):

        link = self.link.value.strip()

        if not link_permitido(link):
            return await interaction.response.send_message(
                embed=embed_padrao("❌ Link inválido.", False),
                ephemeral=True
            )

        dados = detectar_plataforma(link)

        desc = self.descricao.value.strip()

        if not desc:
            desc = f"Vídeo novo na cidade Marcone Roleplay® | #2026\n Segue, Curte, Comente e Compartilhe"

        embed = discord.Embed(
            title=f"{dados['emoji']} NOVO VÍDEO",
            description=f"{interaction.user.mention} postou um novo vídeo em {dados['emoji']}\n\n {desc}",
            color=0xf1c40f
        )

        embed.add_field(
            name=f"{dados['emoji']} Assista:",
            value=link,
            inline=False
        )

        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1444735189765849320/1487659680997179612/ADESIVO_AMARELO_MARCONE_1.png?ex=69f379cb&is=69f2284b&hm=cfd03255779617aa67562773f06de7ae9d91beb38ae5a65ea698ef1fe9d25ae0&")

        embed.set_image(url="https://cdn.discordapp.com/attachments/1444735189765849320/1487656538159190076/EMAIL_CRIADORES_AMARELO_KABRINHA.png?ex=69f2ce1e&is=69f17c9e&hm=07a19cd2c52ae288163fe3211d3d9f1d4e849403d4bbf79bd09950181319af20&")

        embed.set_footer(text="Criadores MarconeRP® - Todos os direitos reservados", icon_url="https://cdn.discordapp.com/emojis/1490521797454598224.webp?size=96")        

        canal = interaction.guild.get_channel(CANAL_VIDEOS)

        if canal is None:
            canal = await interaction.guild.fetch_channel(CANAL_VIDEOS)

        await canal.send(embed=embed)

        await interaction.response.send_message(
            embed=embed_padrao("✅ Vídeo enviado."),
            ephemeral=True
        )