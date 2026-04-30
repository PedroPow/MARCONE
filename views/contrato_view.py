import discord

from utils.perms import is_staff
from config import CARGOS, CATEGORIAS
from database import cursor, db


class ContratoView(discord.ui.View):
    def __init__(self, bot, user_id):
        super().__init__(timeout=None)
        self.bot = bot
        self.user_id = user_id

    @discord.ui.button(
        label="Promover",
        style=discord.ButtonStyle.green,
        custom_id="promover_streamer"
    )
    async def promover(self, interaction, button):

        if not is_staff(interaction.user):
            return await interaction.response.send_message(
                "Apenas staff.",
                ephemeral=True
            )

        await interaction.response.send_message(
            view=PromocaoMenu(self.user_id),
            ephemeral=True
        )

    @discord.ui.button(
        label="Encerrar Contrato",
        style=discord.ButtonStyle.red,
        custom_id="encerrar_contrato"
    )
    async def encerrar(self, interaction, button):

        if not is_staff(interaction.user):
            return await interaction.response.send_message(
                "Apenas staff.",
                ephemeral=True
            )

        guild = interaction.guild
        membro = guild.get_member(self.user_id)

        if membro:
            for _, role_id in CARGOS.items():
                role = guild.get_role(role_id)
                if role in membro.roles:
                    await membro.remove_roles(role)

        cursor.execute(
            "DELETE FROM contratos WHERE user_id=?",
            (self.user_id,)
        )
        db.commit()

        await interaction.response.send_message(
            "Contrato encerrado.",
            ephemeral=True
        )


class PromocaoMenu(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=60)
        self.add_item(PromocaoSelect(user_id))


class PromocaoSelect(discord.ui.Select):
    def __init__(self, user_id):

        self.user_id = user_id

        options = [
            discord.SelectOption(label="Bronze", value="bronze"),
            discord.SelectOption(label="Prata", value="prata"),
            discord.SelectOption(label="Ouro", value="ouro"),
            discord.SelectOption(label="Platina", value="platina"),
            discord.SelectOption(label="Esmeralda", value="esmeralda"),
            discord.SelectOption(label="Ruby", value="ruby"),
            discord.SelectOption(label="Diamante", value="diamante"),
            discord.SelectOption(label="Oficial", value="oficial"),
        ]

        super().__init__(
            placeholder="Escolha o novo nível",
            options=options
        )

    async def callback(self, interaction):

        nivel = self.values[0]
        guild = interaction.guild
        membro = guild.get_member(self.user_id)

        if not membro:
            return await interaction.response.send_message(
                "Usuário não encontrado.",
                ephemeral=True
            )

        # remove cargos antigos
        for _, role_id in CARGOS.items():
            role = guild.get_role(role_id)
            if role in membro.roles:
                await membro.remove_roles(role)

        # add novo
        novo = guild.get_role(CARGOS[nivel])
        await membro.add_roles(novo)

        # move canal
        categoria = guild.get_channel(CATEGORIAS[nivel])
        await interaction.channel.edit(category=categoria)

        cursor.execute(
            "INSERT OR REPLACE INTO contratos(user_id,nivel) VALUES (?,?)",
            (self.user_id, nivel)
        )
        db.commit()

        await interaction.response.send_message(
            f"{membro.mention} promovido para **{nivel.upper()}**",
            ephemeral=True
        )