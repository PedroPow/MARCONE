import discord
from utils.perms import is_staff
from modals.rename_modal import RenameModal


class ConfigView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        label="Configurações",
        style=discord.ButtonStyle.gray,
        custom_id="ticket_config"
    )
    async def config(self, interaction: discord.Interaction, button):

        if not is_staff(interaction.user):
            return await interaction.response.send_message(
                "Apenas staff.",
                ephemeral=True
            )

        await interaction.response.send_message(
            view=ConfigSelect(),
            ephemeral=True
        )

    @discord.ui.button(
        label="Fechar Ticket",
        style=discord.ButtonStyle.red,
        custom_id="fechar_ticket"
    )
    async def fechar(self, interaction: discord.Interaction, button):

        if not is_staff(interaction.user):
            return await interaction.response.send_message(
                "Apenas staff.",
                ephemeral=True
            )

        await interaction.response.send_message(
            "Fechando ticket...",
            ephemeral=True
        )

        await interaction.channel.delete()


class ConfigSelect(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(ConfigMenu())


class ConfigMenu(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(
                label="Renomear Ticket"
            ),
            discord.SelectOption(
                label="Cancelar Ticket"
            )
        ]

        super().__init__(
            placeholder="Escolha uma opção",
            options=options
        )

    async def callback(self, interaction):

        escolha = self.values[0]

        if escolha == "Renomear Ticket":
            await interaction.response.send_modal(
                RenameModal()
            )

        elif escolha == "Cancelar Ticket":
            await interaction.response.send_message(
                "Ticket cancelado."
            )
            await interaction.channel.delete()