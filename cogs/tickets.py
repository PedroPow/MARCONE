import discord
from discord.ext import commands
from discord import app_commands

from config import (
    GUILD_ID,
    CANAL_PAINEL_TICKET,
    CATEGORIAS,
    CARGO_STAFF
)

from utils.embeds import padrao
from views.ticket_view import TicketView


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="embed",
        description="Criar painel de tickets"
    )
    async def embed(self, interaction: discord.Interaction):

        if not any(r.id == CARGO_STAFF for r in interaction.user.roles):
            return await interaction.response.send_message(
                "Sem permissão.",
                ephemeral=True
            )

        if interaction.channel.id != CANAL_PAINEL_TICKET:
            return await interaction.response.send_message(
                "Use no canal correto.",
                ephemeral=True
            )

        await interaction.channel.send(
            embed=padrao(
                "🎫 Tickets Marcone RP",
                "Clique no botão abaixo para abrir seu ticket."
            ),
            view=TicketView(self.bot)
        )

        await interaction.response.send_message(
            "Painel enviado.",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Tickets(bot), guild=discord.Object(id=GUILD_ID))