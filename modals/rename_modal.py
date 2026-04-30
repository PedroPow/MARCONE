import discord


class RenameModal(discord.ui.Modal, title="Renomear Ticket"):

    nome = discord.ui.TextInput(
        label="Novo nome do ticket"
    )

    async def on_submit(self, interaction):

        await interaction.channel.edit(
            name=self.nome.value.lower().replace(" ", "-")
        )

        await interaction.response.send_message(
            "Ticket renomeado.",
            ephemeral=True
        )