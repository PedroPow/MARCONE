import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import discord
from MarconeBOT.main import CONFIG_VISUAL, BENEFICIOS


# Esse embed será mandado após o Streamer colocar as informações pelo botão "Infos Streamers" lá no Embed 3, esse embed é para o contrato de promoção, ou seja, quando o streamer for promovido para um nível maior, esse embed será mandado para o canal de contrato junto de de todas as informações do Streamer, esse embed é o ultimo, onde terá todas as informações do Streamer. 
def contrato_promocao_embed(user, nivel, ingame=None, perfil=None):
    beneficios = BENEFICIOS.get(nivel.lower(), [])
    beneficios_texto = ""
    if beneficios:
        beneficios_texto = f"**Benefícios do Nível {nivel.upper()}:**\n" + "\n".join(f"• {b}" for b in beneficios) + "\n\n"
    desc = (
        f"👋{user.mention} Bem-vindo(a) à equipe de Streamers da Marcone!🎉🔥\n\n"
        f"---\n\n"
        f"**Informações atuais:**\n"
        f"Membro: {user.mention}\n"
        f"ID: {user.id}\n"
        f"ID IN-GAME: {ingame if ingame else 'Não informado'}\n"
        f"Frequência de Vídeos ou Lives: Não informado\n"
        f""
        f"Streamer: {nivel.upper()}\n"
        f"---\n\n"
        f"{beneficios_texto}"
        f"---\n\n"
        f"Perfil: {perfil if perfil else 'Não informado'}\n\n"
        f"---\n\n"
    )
    embed = discord.Embed(
        title=f"Contrato de Streamer {nivel.upper()}",
        description=desc,
        color=CONFIG_VISUAL["cores"].get(nivel.lower(), 0xFFD700)
    )
    embed.set_image(url=CONFIG_VISUAL["banners"]["gif"])
    return embed
