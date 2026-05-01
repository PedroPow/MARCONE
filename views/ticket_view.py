# views/ticket_view.py
# VERSÃO FINAL ATUALIZADA
# abrir ticket + staff painel + contratar + promover + rebaixar + encerrar
# notificar membro + embeds ephemeral + fechar ticket

import discord
from discord.ui import View, Button, Select, Modal, TextInput, UserSelect
from database import cursor, db
from utils.plataformas import detectar_plataforma, link_permitido
from embeds.embeds import beneficios

# ==========================================
# IDS
# ==========================================

STAFF_ROLE_ID = 1425626604205379586
CATEGORIA_TICKET = 1425626605044236327

CARGOS = {
    "bronze": [1425626604192661534, 1425626603869704301],
    "prata": [1425626604192661535, 1425626603869704301],
    "ouro": [1425626604192661536, 1425626603869704301],
    "platina": [1425626604192661537, 1425626603869704301],
    "esmeralda": [1425626604192661538, 1425626603869704301],
    "ruby": [1425626604192661539, 1425626603869704301],
    "diamante": [1425626604192661540, 1425626603869704301],
    "oficial": [1425626604192661541, 1425626603869704301]
}

CATEGORIAS = {
    "bronze": 1425626605237178428,
    "prata": 1425626605237178429,
    "ouro": 1425626605237178430,
    "platina": 1425626605237178431,
    "esmeralda": 1425626605237178432,
    "ruby": 1425626605237178434,
    "diamante": 1425626605237178435,
    "oficial": 1425626605237178436
}

BADGES = {
    "bronze": "🔴",
    "prata": "⚪️",
    "ouro": "🟡",
    "platina": "🔵",
    "esmeralda": "🟢",
    "ruby": "🟠",
    "diamante": "🟣",
    "oficial": "⚫️"
}

# ==========================================
# UTILS
# ==========================================

def is_staff(member):
    return any(role.id == STAFF_ROLE_ID for role in member.roles)


def embed_padrao(msg, ok=True):
    cor = 0xF1C40F if ok else 0xE74C3C
    return discord.Embed(description=msg, color=cor)

def criar_embed_streamer(membro, nivel, ingame="Atualizar Manualmente", redes="Não informado"):
    embed = discord.Embed(
        title="<:PONTOELETRONICO:1498906803281334382> Streamer Atualizado",
        description=(
            f"Informações do Streamer:\n\n"
            f"🔸`Membro:` {membro.mention}\n"
            f"🔸`ID Discord:` {membro.id}\n"
            f"🔸`ID Ingame:` {ingame}\n"
            f"🔸`Nível:` {nivel.upper()}\n\n"
            f"--------------------------------------\n\n"
            f"{beneficios(nivel)}\n\n"
            f"--------------------------------------\n\n"
            f"🔸`Plataformas:`\n🔸{redes}"
        ),
        color=0xF1C40F
    )

    embed.set_image(
        url="https://cdn.discordapp.com/attachments/1444735189765849320/1487656538159190076/EMAIL_CRIADORES_AMARELO_KABRINHA.png"
    )

    embed.set_footer(
        text="Criadores MarconeRP® - Todos os direitos reservados"
    )

    return embed    


# ==========================================
# ABRIR TICKET
# ==========================================

class PainelAbrirTicketView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        label="Abrir Ticket",
        style=discord.ButtonStyle.gray,
        emoji="<:TICKET:1498895809645908021>",
        custom_id="abrir_ticket"
    )
    async def abrir(self, interaction: discord.Interaction, button):

        cursor.execute(
            "DELETE FROM tickets WHERE user_id=?",
            (interaction.user.id,)
        )
        db.commit()

        categoria = interaction.guild.get_channel(CATEGORIA_TICKET)
        staff = interaction.guild.get_role(STAFF_ROLE_ID)

        if categoria is None:
            return await interaction.response.send_message(
                "❌ Categoria de ticket não encontrada.",
                ephemeral=True
            )

        if staff is None:
            return await interaction.response.send_message(
                "❌ Cargo STAFF não encontrado.",
                ephemeral=True
            )

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True),
            staff: discord.PermissionOverwrite(view_channel=True)
        }

        canal = await interaction.guild.create_text_channel(
            name=f"🎫・{interaction.user.name}",
            category=categoria,
            overwrites=overwrites
        )

        cursor.execute(
            "INSERT INTO tickets(user_id, canal_id) VALUES (?,?)",
            (interaction.user.id, canal.id)
        )
        db.commit()

        embed = discord.Embed(
            title="<:TICKET:1498895809645908021> Ticket Aberto",
            description=(
                f"Seu cadastro foi aberto Sr(a) {interaction.user.mention}\n"
                f"Pedimos que aguarde o atendimento da nossa equipe.\n\n"
                f"Enquanto isso nos envie:\n\n"
                f"🔸`Nome do Pessonagem.`\n"
                f"🔸`Id Ingame.`\n"
                f"🔸`Idade Nárnia.`\n"
                f"🔸`Plataformas e Redes Sociais.`\n"
                f"🔸`Porque deseja ser streamer da MarconeRP?`"
            ),
            color=0xFFC000
        )

        embed.set_image(url="https://cdn.discordapp.com/attachments/1444735189765849320/1487656538159190076/EMAIL_CRIADORES_AMARELO_KABRINHA.png")
        embed.set_footer(text="Criadores MarconeRP® - Todos os direitos reservados")

        await canal.send(
            embed=embed,
            view=TicketView(self.bot)
        )

        view = View()
        view.add_item(
            Button(
                label="Ver Ticket",
                style=discord.ButtonStyle.link,
                url=canal.jump_url,
                emoji="<:TICKET:1498895809645908021>"
            )
        )

        await interaction.response.send_message(
            embed=embed_padrao(f"✅ Ticket criado: {canal.mention}"),
            view=view,
            ephemeral=True
        )


# ==========================================
# TICKET VIEW
# ==========================================

class TicketView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        label="Configurações",
        style=discord.ButtonStyle.secondary,
        emoji="<:CONFIG:1489297902118375544>",
        custom_id="ticket_config"
    )
    async def config(self, interaction, button):

        if not is_staff(interaction.user):
            return await interaction.response.send_message(
                embed=embed_padrao("❌ Apenas staff.", False),
                ephemeral=True
            )

        await interaction.response.send_message(
            embed=embed_padrao("⚙️ Painel administrativo"),
            view=ConfigView(self.bot),
            ephemeral=True
        )

    @discord.ui.button(
        label="Fechar Ticket",
        style=discord.ButtonStyle.gray,
        emoji="<:x1:1489109039744028724>",
        custom_id="ticket_close"
    )
    async def fechar(self, interaction, button):

        if not is_staff(interaction.user):
            return

        cursor.execute(
            "DELETE FROM tickets WHERE canal_id=?",
            (interaction.channel.id,)
        )
        db.commit()

        await interaction.response.send_message(
            embed=embed_padrao("🗑️ Ticket fechado.")
        )

        await interaction.channel.delete()


# ==========================================
# CONFIG MENU
# ==========================================

class ConfigView(View):
    def __init__(self, bot):
        super().__init__(timeout=180)
        self.add_item(ConfigSelect(bot))


class ConfigSelect(Select):
    def __init__(self, bot):
        self.bot = bot

        options = [
            discord.SelectOption(label="Promover Streamer", value="promover"),
            discord.SelectOption(label="Rebaixar", value="rebaixar"),
            discord.SelectOption(label="Encerrar Contrato", value="encerrar"),
            discord.SelectOption(label="Contratar", value="contratar"),
            discord.SelectOption(label="Renomear Ticket", value="renomear"),
            discord.SelectOption(label="Notificar Membro", value="notificar"),
            discord.SelectOption(label="Add Plataforma", value="plataforma"),
        ]

        super().__init__(
            placeholder="Selecione uma ação",
            options=options
        )

    async def callback(self, interaction):

        escolha = self.values[0]

        if escolha == "promover":
            return await interaction.response.send_modal(PromoverModal())

        elif escolha == "rebaixar":
            return await interaction.response.send_modal(RebaixarModal())

        elif escolha == "encerrar":
            return await interaction.response.send_modal(EncerrarModal())

        elif escolha == "contratar":
            return await interaction.response.send_modal(ContratarModal())

        elif escolha == "notificar":
            return await interaction.response.send_message(
                embed=embed_padrao("Selecione o membro."),
                view=NotificarMembroView(),
                ephemeral=True
            )

        elif escolha == "plataforma":
            return await interaction.response.send_modal(
                AddPlataformaModal()
            )


# ==========================================
# ADD PLATAFORMA
# ==========================================

class AddPlataformaModal(Modal, title="Adicionar Plataforma"):

    link = TextInput(
        label="Link da Plataforma",
        placeholder="https://tiktok.com/@usuario"
    )

    async def on_submit(self, interaction):

        link = self.link.value.strip()

        if not link_permitido(link):
            return await interaction.response.send_message(
                embed=embed_padrao("❌ Link inválido.", False),
                ephemeral=True
            )

        dados = detectar_plataforma(link)

        cursor.execute(
            "SELECT user_id FROM tickets WHERE canal_id=?",
            (interaction.channel.id,)
        )
        dados_ticket = cursor.fetchone()

        if not dados_ticket:
            return await interaction.response.send_message(
                embed=embed_padrao("❌ Ticket não encontrado.", False),
                ephemeral=True
            )

        user_id = dados_ticket[0]

        cursor.execute(
            "INSERT INTO plataformas(user_id, link) VALUES (?, ?)",
            (user_id, link)
        )
        db.commit()

        await interaction.response.send_message(
            embed=embed_padrao(
                f"✅ {dados['emoji']} Plataforma adicionada."
            ),
            ephemeral=True
        )


# ==========================================
# PROMOVER
# ==========================================

class PromoverModal(Modal, title="Promover"):
    user_id = TextInput(label="ID Discord")

    async def on_submit(self, interaction):
        await interaction.response.send_message(
            embed=embed_padrao("Escolha novo nível."),
            view=PromoverView(int(self.user_id.value)),
            ephemeral=True
        )


class PromoverView(View):
    def __init__(self, user_id):
        super().__init__(timeout=180)
        self.add_item(PromoverSelect(user_id))


class PromoverSelect(Select):
    def __init__(self, user_id):
        self.user_id = user_id

        super().__init__(
            placeholder="Novo nível",
            options=[
                discord.SelectOption(label=x.capitalize(), value=x)
                for x in CARGOS.keys()
            ]
        )

    async def callback(self, interaction):

        await interaction.response.defer(ephemeral=True)        

        nivel = self.values[0]
        membro = interaction.guild.get_member(self.user_id)

        if not membro:
            return await interaction.followup.send(
                embed=embed_padrao("❌ Usuário não encontrado.", False),
                ephemeral=True
            )
        
        # atualizar embed principal do streamer
        async for msg in interaction.channel.history(limit=50):
            if msg.author == interaction.client.user and msg.embeds:
                if "Streamer Contratado" in msg.embeds[0].title or "Streamer Atualizado" in msg.embeds[0].title:
                    novo_embed = criar_embed_streamer(membro, nivel)
                    await msg.edit(embed=novo_embed)
                    break     

        # remove cargos antigos
        for cargos in CARGOS.values():
            for cid in cargos:
                role = interaction.guild.get_role(cid)
                if role and role in membro.roles:
                    await membro.remove_roles(role)

        # adiciona novos cargos
        for cargo_id in CARGOS[nivel]:
            cargo = interaction.guild.get_role(cargo_id)
            if cargo:
                await membro.add_roles(cargo)

        nome_atual = interaction.channel.name

        if "・" in nome_atual:
            nome_base = nome_atual.split("・", 1)[1]
        else:
            nome_base = nome_atual

        await interaction.channel.edit(
            category=interaction.guild.get_channel(CATEGORIAS[nivel]),
            name=f"{BADGES[nivel]}・{nome_base}"
        )

        cursor.execute(
            """
            INSERT OR REPLACE INTO contratos
            (user_id, nivel)
            VALUES (?,?)
            """,
            (membro.id, nivel)
        )
        db.commit()

        await interaction.followup.send(
            embed=embed_padrao(
                f"✅ {membro.mention} promovido para {nivel.upper()}"
            ),
            ephemeral=True
        )

# ==========================================
# REBAIXAR
# ==========================================

class RebaixarModal(Modal, title="Rebaixar"):
    user_id = TextInput(label="ID Discord")

    async def on_submit(self, interaction):


        await interaction.response.defer(ephemeral=True)

        membro = interaction.guild.get_member(
            int(self.user_id.value)
        )

        if not membro:
            return await interaction.response.send_message(
                embed=embed_padrao("❌ Usuário não encontrado.", False),
                ephemeral=True
            )

        ordem = list(CARGOS.keys())

        atual = None
        for nome in reversed(list(CARGOS.keys())):
            cargos = CARGOS[nome]
            for cid in cargos:
                role = interaction.guild.get_role(cid)
                if role and role in membro.roles:
                    atual = nome
                    break
            if atual:
                break

        if not atual:
            return await interaction.response.send_message(
                embed=embed_padrao("❌ Sem cargo streamer.", False),
                ephemeral=True
            )

        pos = ordem.index(atual)

        if pos == 0:
            return await interaction.followup.send(
                embed=embed_padrao("❌ Este membro já está no menor nível.", False),
                ephemeral=True
            )

        novo = ordem[pos - 1]

        await interaction.followup.send(
            embed=embed_padrao(f"⬇️ Rebaixado para {novo.upper()}"),
            ephemeral=True
        )

        # remove cargos atuais
        for cid in CARGOS[atual]:
            role = interaction.guild.get_role(cid)
            if role and role in membro.roles:
                await membro.remove_roles(role)

        # adiciona cargos novos
        for cid in CARGOS[novo]:
            role = interaction.guild.get_role(cid)
            if role:
                await membro.add_roles(role)

        nome_atual = interaction.channel.name

        if "・" in nome_atual:
            nome_base = nome_atual.split("・", 1)[1]
        else:
            nome_base = nome_atual

        await interaction.channel.edit(
            category=interaction.guild.get_channel(CATEGORIAS[novo]),
            name=f"{BADGES[novo]}・{nome_base}"
        )

        cursor.execute(
            "UPDATE contratos SET nivel=? WHERE user_id=?",
            (novo, membro.id)
        )
        db.commit()

        await interaction.response.send_message(
            embed=embed_padrao(f"⬇️ Rebaixado para {novo.upper()}"),
            ephemeral=True
        )

        async for msg in interaction.channel.history(limit=50):
            if msg.author == interaction.client.user and msg.embeds:
                if "Streamer Contratado" in msg.embeds[0].title or "Streamer Atualizado" in msg.embeds[0].title:
                    novo_embed = criar_embed_streamer(membro, novo)
                    await msg.edit(embed=novo_embed)
                    break      


# ==========================================
# ENCERRAR CONTRATO
# ==========================================

class EncerrarModal(Modal, title="Encerrar Contrato"):
    user_id = TextInput(label="ID Discord")

    async def on_submit(self, interaction):

        membro = interaction.guild.get_member(
            int(self.user_id.value)
        )

        if not membro:
            return await interaction.response.send_message(
                embed=embed_padrao("❌ Usuário não encontrado.", False),
                ephemeral=True
            )

        # remove todos cargos streamer
        for cargos in CARGOS.values():
            for cid in cargos:
                role = interaction.guild.get_role(cid)
                if role and role in membro.roles:
                    await membro.remove_roles(role)

        cursor.execute(
            "DELETE FROM contratos WHERE user_id=?",
            (membro.id,)
        )
        db.commit()

        await interaction.response.send_message(
            embed=embed_padrao("❌ Contrato encerrado."),
            ephemeral=True
        )
 

# ==========================================
# CONTRATAR
# ==========================================

class ContratarModal(Modal, title="Contratar"):

    nome = TextInput(
        label="Nome",
        placeholder="Nome do streamer"
    )

    user_id = TextInput(
        label="ID Discord",
        placeholder="ID do membro"
    )

    ingame = TextInput(
        label="ID Ingame",
        placeholder="ID dentro da cidade"
    )

    redes = TextInput(
        label="Redes Sociais",
        placeholder="https://twitch.tv/... | https://instagram.com/...",
        style=discord.TextStyle.paragraph,
        required=False
    )

    async def on_submit(self, interaction):

        user_id = self.user_id.value.strip()

        if not user_id.isdigit():
            return await interaction.response.send_message(
                embed=embed_padrao("❌ ID Discord inválido.", False),
                ephemeral=True
            )

        await interaction.response.send_message(
            embed=embed_padrao("Escolha o nível do streamer."),
            view=NivelView(
                self.nome.value.strip(),
                int(user_id),
                self.ingame.value.strip(),
                self.redes.value.strip()
            ),
            ephemeral=True
        )


class NivelView(View):
    def __init__(self, nome, user_id, ingame, redes):
        super().__init__(timeout=180)

        self.add_item(
            NivelSelect(
                nome=nome,
                user_id=user_id,
                ingame=ingame,
                redes=redes
            )
        )

class NivelSelect(Select):
    def __init__(self, *, nome, user_id, ingame, redes):

        self.nome = nome
        self.user_id = user_id
        self.ingame = ingame
        self.redes = redes

        super().__init__(
            placeholder="Nível streamer",
            options=[
                discord.SelectOption(
                    label=x.capitalize(),
                    value=x
                )
                for x in CARGOS.keys()
            ]
        )

    async def callback(self, interaction):

        nivel = self.values[0]
        membro = interaction.guild.get_member(self.user_id)

        if not membro:
            return await interaction.response.send_message(
                embed=embed_padrao(
                    "❌ Usuário não encontrado.",
                    False
                ),
                ephemeral=True
            )

        # adiciona todos cargos do nível
        for cargo_id in CARGOS[nivel]:
            cargo = interaction.guild.get_role(cargo_id)
            if cargo:
                await membro.add_roles(cargo)

        await interaction.channel.edit(
            category=interaction.guild.get_channel(
                CATEGORIAS[nivel]
            ),
            name=f"{BADGES[nivel]}・{self.nome.lower()}"
        )

        embed = discord.Embed(
            title="<:PONTOELETRONICO:1498906803281334382> Streamer Contratado",
            description=(
                f"Bem-vindo(a) {membro.mention} à equipe de streamers da MarconeRP!\n\n"
                f"Desejamos muito sucesso na sua jornada como criador de conteúdo e estamos ansiosos para ver o incrível trabalho que você fará representando nossa comunidade.\n\n"
                f"Regras Importantes:\n\n"
                f"--------------------------------------\n\n"
                f"🔸 Mantenha sempre o respeito e a cordialidade em suas transmissões e interações com a comunidade.\n\n"
                f"--------------------------------------\n\n"
                f"🔸 Siga as diretrizes da plataforma de streaming que você utiliza, garantindo que seu conteúdo esteja em conformidade com as políticas de uso.\n\n"
                f"--------------------------------------\n\n"
                f"🔸 Promova um ambiente positivo e inclusivo, evitando qualquer tipo de discurso de ódio, discriminação ou comportamento tóxico.\n\n"
                f"--------------------------------------\n\n"
                f"🔸 Lembre-se que agora você representa a MarconeRP®.\n\n"
                f"--------------------------------------\n\n"
                f"Informações do Streamer:\n\n"
                f"🔸`Membro:` {membro.mention}\n"
                f"🔸`ID Discord: {membro.id}`\n"
                f"🔸`ID Ingame: {self.ingame}`\n"
                f"🔸`Nível: {nivel.upper()}`\n\n"
                f"--------------------------------------\n\n"
                f"{beneficios(nivel)}\n\n"
                f"--------------------------------------\n\n"
                f"🔸`Plataformas:`\n🔸{self.redes or 'Não informado'}"
            ),
            color=0xF1C40F
        )

        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1444735189765849320/1487656538159190076/EMAIL_CRIADORES_AMARELO_KABRINHA.png"
        )

        embed.set_footer(
            text="Criadores MarconeRP® - Todos os direitos reservados"
        )

        await interaction.channel.send(embed=embed)

        cursor.execute(
            """
            INSERT OR REPLACE INTO contratos
            (user_id, nivel)
            VALUES (?,?)
            """,
            (membro.id, nivel)
        )
        db.commit()

        await interaction.response.send_message(
            embed=embed_padrao(
                "✅ Streamer contratado com sucesso."
            ),
            ephemeral=True
        )        

# ==========================================
# NOTIFICAR MEMBRO
# ==========================================

class NotificarMembroView(View):
    def __init__(self):
        super().__init__(timeout=120)
        self.add_item(NotificarMembroSelect())


class NotificarMembroSelect(UserSelect):
    def __init__(self):
        super().__init__(
            placeholder="Selecionar membro",
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction):

        membro = self.values[0]

        embed_dm = discord.Embed(
            title="✅ Ticket Respondido",
            description=(
                f"Olá {membro.mention},\n\n"
                f"`Seu ticket foi respondido no servidor.`\n"
                f"`Clique no botão abaixo para visualizar.`"
            ),
            color=0xF1C40F
        )

        view = View()
        view.add_item(
            Button(
                label="Ver Ticket",
                style=discord.ButtonStyle.link,
                url=interaction.channel.jump_url
            )
        )

        try:
            await membro.send(embed=embed_dm, view=view)

            await interaction.response.send_message(
                embed=embed_padrao("✅ Membro notificado."),
                ephemeral=True
            )

        except:
            await interaction.response.send_message(
                embed=embed_padrao("❌ Não foi possível enviar DM.", False),
                ephemeral=True
            )        