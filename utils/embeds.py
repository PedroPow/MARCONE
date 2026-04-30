import discord

def padrao(titulo, descricao):
    return discord.Embed(
        title=titulo,
        description=descricao,
        color=0xFFD700
    )

def ticket_embed(user):
    return discord.Embed(
        title="🎫 Ticket Criado",
        description=f"{user.mention}, aguarde atendimento.",
        color=0xFFD700
    )

def live_embed(user):
    return discord.Embed(
        title="🔴 LIVE INICIADA",
        description=f"{user.mention} iniciou live agora!",
        color=0xFF0000
    )