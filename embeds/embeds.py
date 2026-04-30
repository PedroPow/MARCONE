# Centralização dos Embeds do Bot
# Todas as funções de embed ficam aqui, mantendo compatibilidade com o restante do bot.

import discord

# Copiado de bot.py para evitar importação circular
CONFIG_VISUAL = {
    "cores": {
        "bronze": 0x8B0000,
        "prata": 0xC0C0C0,
        "ouro": 0xFFD700,
        "platina": 0x3498DB,
        "esmeralda": 0x2ECC71,
        "ruby": 0xE67E22,
        "diamante": 0x9B59B6,
        "oficial": 0x000000,
    },
    "badges": {
        "bronze": "🔴",
        "prata": "⚪",
        "ouro": "🟡",
        "platina": "🔵",
        "esmeralda": "🟢",
        "ruby": "🟠",
        "diamante": "🟣",
        "oficial": "⚫"
    },
    "banners":{
        "foto": "https://media.discordapp.net/attachments/1310324084487229481/1488274148001321051/CRIADORES.gif?ex=69cc2ecf&is=69cadd4f&hm=e58d3c536c8afbdbc4e1d55c796c3f56152e3e1337f29d14e4a8297dd6af93ee&=&width=967&height=544",
        "gif": "https://cdn.discordapp.com/attachments/1310324084487229481/1488275061105360966/STREAMERS.gif?ex=69cc2fa9&is=69cade29&hm=478801556d7da81dd625911e963b12adf5be4fac8e478f154ae7dd1c92a93be4&"
    }
}

BENEFICIOS = {
    "bronze": [
        "18 Gemas ( Todo dia 1 - Solicitar no Ticket Streamer )",
        "$18.000 em dinheiro",
        "Direito à aquisição de 01 (um) veículo, desde que disponível para compra com moeda do jogo, com valor máximo de até $175.000"
    ],
    "prata": [
        "25 Gemas ( Todo dia 1 - Solicitar no Ticket Streamer )",
        "$18.000 em dinheiro",
        "Acesso ao comando /cam",
        "Acesso ao comando /som",
        "Direito à aquisição de 01 (um) veículo, desde que disponível para compra com moeda do jogo, com valor máximo de até $350.000"
    ],
    "ouro": [
        "32 Gemas ( Todo dia 1 - Solicitar no Ticket Streamer )",
        "$25.000 em dinheiro",
        "Acesso ao comando /cam",
        "Acesso ao comando /som",
        "Acesso ao comando /remap",
        "Direito à aquisição de 01 (um) veículo, desde que disponível para compra com moeda do jogo, com valor máximo de até $525.000"
    ],
    "platina": [
        "39 Gemas ( Todo dia 1 - Solicitar no Ticket Streamer )",
        "$32.000 em dinheiro",
        "Acesso ao comando /cam",
        "Acesso ao comando /som",
        "Acesso ao comando /remap",
        "Verificação oficial no Instagram",
        "Direito à aquisição de 01 (um) veículo disponível na concessionária"
    ],
    "esmeralda": [
        "46 Gemas ( Todo dia 1 - Solicitar no Ticket Streamer )",
        "$39.000 em dinheiro",
        "Acesso ao comando /cam",
        "Acesso ao comando /som",
        "Acesso ao comando /remap",
        "Acesso ao /barber",
        "Verificação oficial no Instagram",
        "Direito à aquisição de 01 (um) veículo disponível na concessionária"
    ],
    "ruby": [
        "53 Gemas ( Todo dia 1 - Solicitar no Ticket Streamer )",
        "$46.000 em dinheiro",
        "Acesso ao comando /cam",
        "Acesso ao comando /som",
        "Acesso ao comando /remap",
        "Verificação oficial no Instagram",
        "Direito à aquisição de 02 (dois) veículos disponíveis na concessionária",
        "Direito a 01 (um) item de até $35 na loja do servidor",
        "Acesso ao /barber",
        "Acesso à /skin shop"
    ],
    "diamante": [
        "60 Gemas ( Todo dia 1 - Solicitar no Ticket Streamer )",
        "$46.000 em dinheiro",
        "Acesso ao comando /cam",
        "Acesso ao comando /som",
        "Acesso ao comando /remap",
        "Verificação oficial no Instagram",
        "Direito à aquisição de 02 (três) veículos disponíveis na concessionária",
        "Direito a 01 (um) item de até $53 na loja do servidor",
        "Acesso ao /barber",
        "Acesso à /skin shop"
    ],
    "oficial": [
        "67 Gemas ( Todo dia 1 - Solicitar no Ticket Streamer )",
        "$46.000 em dinheiro",
        "Acesso ao comando /cam",
        "Acesso ao comando /som",
        "Acesso ao comando /remap",
        "Verificação oficial no Instagram",
        "Direito à aquisição de 02 (quatro) veículos disponíveis na concessionária",
        "Direito a 01 (um) item de até $70 na loja do servidor",
        "Acesso ao /barber",
        "Acesso à /skin shop",
        "Redução do tempo de morte",
        "Acesso ao drone"
    ]
}

# Embeds que ficará no canal: 1489775233186402314
# Embed 1
def inicial():
    embed = discord.Embed(
        title="Bem vindo ao Discord dos criadores da Marcone!",
        description="Este é o servidor oficial para integração, suporte e organização dos Streamers e Criadores de Conteúdo da Marcone RP.\n\n"
        "**📌 Por aqui você vai encontrar:**\n\n"
        "• Regras e diretrizes 👮‍♂️\n"
        "• Beneficios e campanhas especiais 📦\n"
        "• Espaços para conversar e divulgar seu trabalho🔗\n"
        "• Suporte direto do Time de Streamers ✅\n\n"
        "🎥 Faça parte da nossa comunidade, produza, compartilhe e brilhe com a gente!\n\n"
        "_Clique abaixo e converse com um dos nossos colaboradores_\n\n"
        "Marcone Roleplay - 2026",
        color=0xFFD700
    )
    embed.set_footer(text="Criadores Marcone® | #2026 • © Todos os direitos reservados.", icon_url="https://discord.com/channels/@me/1310324084487229481/1489027668342079641")
    embed.set_image(url=CONFIG_VISUAL["banners"]["foto"])
    return embed


# Esse será em todos os tickets que ficaram na categoria: 1487237697083932784 ou seja todo ticket que for aberto no botão "Abrir Ticket"
#Embed 2
def ticket(user):
    embed = discord.Embed(
        title="_**Triagem Streamer - Informações Iniciais**_",
        description=(
            f"👋{user.mention} Bem-vindo(a) ao Discord de Streamers da Marcone!🎉🔥\n\n"
            "**📋 Para começarmos com tudo alinhado, preencha as informações abaixo:**\n\n"
            "📌 Qual o nome e id do seu personagem?\n"
            "📌 Quais plataformas você utiliza para produzir seu conteúdo?\n"
            "📌 Link dos seus perfis onde fará os conteúdos\n\n"
            "---\n\n"
            "**✨ Além dos benefícios de Streamer, queremos saber:**\n"
            "Existe algo que possamos fazer para ajudar ainda mais na sua produção de conteúdo?\n\n"
            "---\n\n"
            "Após preencher as informações acima, nossa equipe entrará em contato com você.\n\n"
        ),
        color=0xFFD700
    )
    embed.set_footer(text="Criadores Marcone® | #2026 • © Todos os direitos reservados.", icon_url="https://cdn.discordapp.com/attachments/1444735189765849320/1487659680997179612/ADESIVO_AMARELO_MARCONE_1.png?ex=69c9f28b&is=69c8a10b&hm=e589b322c781d19b55a3fe235a04c1f93498e1f7e48fd463d9b8fd31261b95f6&")
    embed.set_image(url=CONFIG_VISUAL["banners"]["gif"])
    return embed


# Esse embed será mandado para os canais de contrato após o Staff usar o botão "Contratar Streamer" após o staff usar o botão abrirá mais um ticket e esse embed será mandado lá. 
#Embed 3
def contrato(user, nome, user_id, ingame, perfil, nivel, staff):
    beneficios = BENEFICIOS.get(nivel.lower(), [])
    beneficios_texto = ""
    if beneficios:
        beneficios_texto = f"\n\n**Benefícios do Nível {nivel.upper()}:**\n" + "\n".join(f"• {b}" for b in beneficios)
    embed = discord.Embed(
        title="🎉 Bem-vindo(a) à Discord de Streamers da Marcone! 🔥",
        description=(
            f"👋{user.mention} Parabéns por se juntar à nossa comunidade! 🎉\n"
            f"Agora você é um Streamer {nivel.upper()} da Marcone! 🚀\n\n"
            "Utilize o botão **Infos Stremers** para preencher suas informações.\n\n"
            "---\n\n"
            f"**Informações dos seus Benefícios:**\n\n"
            f"{beneficios_texto}\n\n"
            f"---\n\n"
            f"Perfil: {perfil}\n\n"
        ),
        color=CONFIG_VISUAL["cores"].get(nivel.lower(), 0xFFD700)
    )
    embed.set_footer(text="Criadores Marcone® | #2026 • © Todos os direitos reservados.", icon_url="https://cdn.discordapp.com/attachments/1444735189765849320/1487659680997179612/ADESIVO_AMARELO_MARCONE_1.png?ex=69c9f28b&is=69c8a10b&hm=e589b322c781d19b55a3fe235a04c1f93498e1f7e48fd463d9b8fd31261b95f6&")
    embed.set_image(url=CONFIG_VISUAL["banners"]["gif"])
    return embed


# Embed para o painel de lives
def embed_live():
    embed = discord.Embed(
        title="🔴 Painel de Lives Marcone",
        description="Aqui você acompanha as transmissões ao vivo dos nossos criadores! Fique ligado para não perder nenhuma live e apoiar a comunidade.",
        color=0xFFD700
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1444735189765849320/1487659680997179612/ADESIVO_AMARELO_MARCONE_1.png?ex=69c9f28b&is=69c8a10b&hm=e589b322c781d19b55a3fe235a04c1f93498e1f7e48fd463d9b8fd31261b95f6&")
    embed.set_image(url=CONFIG_VISUAL["banners"]["gif"])
    embed.set_footer(text="Criadores Marcone® | #2026 • © Todos os direitos reservados.", icon_url="https://cdn.discordapp.com/attachments/1444735189765849320/1487659680997179612/ADESIVO_AMARELO_MARCONE_1.png?ex=69c9f28b&is=69c8a10b&hm=e589b322c781d19b55a3fe235a04c1f93498e1f7e48fd463d9b8fd31261b95f6&")
    return embed
