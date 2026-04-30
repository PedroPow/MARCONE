# views/ticket_view.py
# VERSÃO FINAL ATUALIZADA
# abrir ticket + staff painel + contratar + promover + rebaixar + encerrar
# notificar membro + embeds ephemeral + fechar ticket

import discord
from discord.ui import View, Button, Select, Modal, TextInput, UserSelect
from database import cursor, db
from utils.plataformas import detectar_plataforma, link_permitido

# ==========================================
# IDS
# ==========================================

STAFF_ROLE_ID = 1487237994711879731
CATEGORIA_TICKET = 1487237697083932784

CARGOS = {
    "bronze": 1487238047429820518,
    "prata": 1487238048591908924,
    "ouro": 1487238020389277797,
    "platina": 1487251376743518228,
    "esmeralda": 1487251422570348706,
    "ruby": 1487251454950506576,
    "diamante": 1487251477566324867,
    "oficial": 1487251526924636250
}

CATEGORIAS = {
    "bronze": 1487237950004531402,
    "prata": 1487237925195481229,
    "ouro": 1487237884468789399,
    "platina": 1487252252472119348,
    "esmeralda": 1487252281471799528,
    "ruby": 1487252300866130132,
    "diamante": 1487252321057505501,
    "oficial": 1487252387629633688
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

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True),
            staff: discord.PermissionOverwrite(view_channel=True)
        }

        canal = await interaction.guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
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
                f'🔸`Id Ingame.`\n'
                f"🔸`Idade Nárnia.`\n"
                f"🔸`Plataformas e Redes Sociais.`\n"
                f"🔸`Porque deseja ser streamer da MarconeRP?`"
            ),
            color=0xFFC000
        )


        embed.set_image(url="https://cdn.discordapp.com/attachments/1444735189765849320/1487656538159190076/EMAIL_CRIADORES_AMARELO_KABRINHA.png?ex=69f2ce1e&is=69f17c9e&hm=07a19cd2c52ae288163fe3211d3d9f1d4e849403d4bbf79bd09950181319af20&")

        embed.set_footer(text="Criadores MarconeRP® - Todos os direitos reservados", icon_url="https://cdn.discordapp.com/emojis/1490521797454598224.webp?size=96")

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
            discord.SelectOption(label="Promover Streamer", value="promover", emoji="<:ADD:1489110059123212368> "),
            discord.SelectOption(label="Rebaixar", value="rebaixar", emoji="<:x1:1489109039744028724>"),
            discord.SelectOption(label="Encerrar Contrato", value="encerrar", emoji="<:x1:1489109039744028724>"),
            discord.SelectOption(label="Contratar", value="contratar", emoji="<:AMARELO:1487636711860207747> "),
            discord.SelectOption(label="Renomear Ticket", value="renomear", emoji="<:EDITAR:1489108787745788014> "),
            discord.SelectOption(label="Notificar Membro", value="notificar", emoji="<:SINO:1489110783391694902>"),
            discord.SelectOption(label="Add Plataforma",value="plataforma",emoji=discord.PartialEmoji(name="ADD",id=1489110059123212368)
            ),            
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

        elif escolha == "renomear":
            return await interaction.response.send_modal(RenomearModal())

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

# COLE ESTA NOVA CLASS no ticket_view.py

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
            f"Olá {membro.mention},\n"
            f">ㅤ"
            f"> `Seu ticket foi respondido no servidor **Criadores Marcone®**.`\n"
            f"> `Para continuar como o ticket, favor responder com alguma mensagem no ticket.`\n"
            f"> `Caso contrário, seu ticket **será deletado** em 24 horas (1 dias).`\n"
            ),
            color=0xF1C40F
        )

        view = View()
        view.add_item(
            Button(
                label="Ver Ticket",
                style=discord.ButtonStyle.link,
                url=interaction.channel.jump_url,
                emoji="<:TICKET:1498895809645908021>"
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


# ==========================================
# CONTRATAR
# ==========================================

# SUBSTITUA a classe ContratarModal inteira no views/ticket_view.py

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

        await interaction.response.send_message(
            embed=embed_padrao("Escolha o nível do streamer."),
            view=NivelView(
                self.nome.value,
                self.user_id.value,
                self.ingame.value,
                self.redes.value
            ),
            ephemeral=True
        )


# SUBSTITUA a classe NivelView inteira

class NivelView(View):
    def __init__(self, nome, user_id, ingame, redes):
        super().__init__(timeout=180)

        self.add_item(
            NivelSelect(
                nome,
                user_id,
                ingame,
                redes
            )
        )


# SUBSTITUA a classe NivelSelect inteira

class NivelSelect(Select):
    def __init__(self, nome, user_id, ingame, redes):

        self.nome = nome
        self.user_id = int(user_id)
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

        await membro.add_roles(
            interaction.guild.get_role(
                CARGOS[nivel]
            )
        )

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
                f"🔸`Nível: {nivel.upper()}`\n"
                f"🔸`Plataformas:`\n 🔸{self.redes or 'Não informado'}"
            ),
            color=0xF1C40F
        )

        embed.set_image(url="https://cdn.discordapp.com/attachments/1444735189765849320/1487656538159190076/EMAIL_CRIADORES_AMARELO_KABRINHA.png?ex=69f2ce1e&is=69f17c9e&hm=07a19cd2c52ae288163fe3211d3d9f1d4e849403d4bbf79bd09950181319af20&")

        embed.set_footer(text="Criadores MarconeRP® - Todos os direitos reservados", icon_url="https://cdn.discordapp.com/emojis/1490521797454598224.webp?size=96")         

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
# PROMOVER / REBAIXAR / ENCERRAR
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


# SUBSTITUA APENAS A CLASS PromoverSelect no ticket_view.py

class PromoverSelect(Select):
    def __init__(self, user_id):
        self.user_id = user_id

        super().__init__(
            placeholder="Novo nível",
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

        # remove cargos antigos
        for cid in CARGOS.values():
            role = interaction.guild.get_role(cid)
            if role in membro.roles:
                await membro.remove_roles(role)

        # adiciona novo cargo
        novo_cargo = interaction.guild.get_role(
            CARGOS[nivel]
        )

        await membro.add_roles(novo_cargo)

        # pega nome atual sem badge
        nome_atual = interaction.channel.name

        if "・" in nome_atual:
            nome_base = nome_atual.split("・", 1)[1]
        else:
            nome_base = nome_atual

        # move categoria + troca nome
        await interaction.channel.edit(
            category=interaction.guild.get_channel(
                CATEGORIAS[nivel]
            ),
            name=f"{BADGES[nivel]}・{nome_base}"
        )

        # salva banco
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
                f"✅ {membro.mention} promovido para {nivel.upper()}"
            ),
            ephemeral=True
        )


class RebaixarModal(Modal, title="Rebaixar"):
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

        ordem = list(CARGOS.keys())

        atual = None
        for nome, cid in CARGOS.items():
            role = interaction.guild.get_role(cid)
            if role in membro.roles:
                atual = nome
                break

        if not atual:
            return await interaction.response.send_message(
                embed=embed_padrao("❌ Sem cargo streamer.", False),
                ephemeral=True
            )

        pos = ordem.index(atual)

        if pos == 0:
            return await interaction.response.send_message(
                embed=embed_padrao("❌ Já está no menor nível.", False),
                ephemeral=True
            )

        novo = ordem[pos - 1]

        await membro.remove_roles(
            interaction.guild.get_role(CARGOS[atual])
        )

        await membro.add_roles(
            interaction.guild.get_role(CARGOS[novo])
        )

        nome_base = interaction.channel.name.split("・",1)[1]

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


class EncerrarModal(Modal, title="Encerrar Contrato"):
    user_id = TextInput(label="ID Discord")

    async def on_submit(self, interaction):

        membro = interaction.guild.get_member(
            int(self.user_id.value)
        )

        for cid in CARGOS.values():
            role = interaction.guild.get_role(cid)
            if role in membro.roles:
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
# RENOMEAR
# ==========================================

class RenomearModal(Modal, title="Renomear"):
    nome = TextInput(label="Novo nome")

    async def on_submit(self, interaction):

        await interaction.channel.edit(
            name=self.nome.value
        )

        await interaction.response.send_message(
            embed=embed_padrao("✅ Ticket renomeado."),
            ephemeral=True
        )