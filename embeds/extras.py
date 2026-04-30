# Funções utilitárias para embeds de log e aviso
import discord

def log(tipo, mensagem):
    return discord.Embed(
        title=f"📄 Log • {tipo.replace('_',' ').title()}",
        description=mensagem,
        color=0x2f3136
    )

#A princio esse embed não foi mudado então por enquanto pode deixa-lo fora do Slash Command.
def aviso_fechamento(membro):
    embed = discord.Embed(
        title="AVISO DE FECHAMENTO",
        description=(
            f"Olá {membro.mention},\n\n"
            f"ㅤㅤNossa equipe está empenhada em prestar o melhor suporte possível para você.\n"
            f"ㅤㅤPara dar continuidade ao atendimento, por favor, responda a este ticket com uma mensagem.\n\n"
            f"ㅤㅤÉ importante destacar que, caso não haja resposta em até 24 horas (1 dia), o ticket será automaticamente excluído.\n"
            f"ㅤㅤPortanto, fique atento(a) para que possamos ajudá-lo(a) de maneira eficiente.\n"
            f"ㅤㅤEstamos à disposição para qualquer dúvida ou necessidade que você possa ter.\n"
        ),
        color=0xFFD700
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1488691281193341100/1488700494007373844/ADESIVO_AMARELO_MARCONE_1.png?ex=69cdbbe0&is=69cc6a60&hm=53da9f9a292565f904cc04480edbe7a39e8402ccb831fd0a93460b277ac58879&")
    embed.set_footer(text="Criadores Marcone® | #2026 • © Todos os direitos reservados.", icon_url="https://cdn.discordapp.com/attachments/1444735189765849320/1487659680997179612/ADESIVO_AMARELO_MARCONE_1.png?ex=69c9f28b&is=69c8a10b&hm=e589b322c781d19b55a3fe235a04c1f93498e1f7e48fd463d9b8fd31261b95f6&")
    return embed

#A princio esse embed não foi mudado então por enquanto pode deixa-lo fora do Slash Command.
def aviso_ticket_respondido(membro):
    embed = discord.Embed(
        title="🔔 Seu ticket foi respondido",
        description=(
            f"Olá {membro.mention},\n\n"
            f"ㅤㅤSeu ticket foi respondido no servidor **Criadores Marcone®**.\n\n"
            f"ㅤㅤPara continuar como o ticket, favor responder com alguma mensagem no ticket.\n"
            f"ㅤㅤCaso contrário, seu ticket **será deletado** em 24 horas (1 dias).\n"
        ),
        color=0xFFD700
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1488691281193341100/1488700494007373844/ADESIVO_AMARELO_MARCONE_1.png?ex=69cdbbe0&is=69cc6a60&hm=53da9f9a292565f904cc04480edbe7a39e8402ccb831fd0a93460b277ac58879&")
    embed.set_footer(text="Criadores Marcone® | #2026 • © Todos os direitos reservados.", icon_url="https://cdn.discordapp.com/attachments/1444735189765849320/1487659680997179612/ADESIVO_AMARELO_MARCONE_1.png?ex=69c9f28b&is=69c8a10b&hm=e589b322c781d19b55a3fe235a04c1f93498e1f7e48fd463d9b8fd31261b95f6&")
    return embed
