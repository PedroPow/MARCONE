import discord
from discord.ext import commands
from discord import app_commands

from config import (
    GUILD_ID,
    CANAL_PAINEL_LIVE,
    CARGO_STAFF
)

from utils.perms import is_staff
from utils.embeds import padrao
from views.live_view import LiveView


class Live(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="painellive",
        description="Criar painel de lives"
    )
    async def painellive(self, interaction: discord.Interaction):

        if not is_staff(interaction.user):
            return await interaction.response.send_message(
                "Apenas staff.",
                ephemeral=True
            )

        if interaction.channel.id != CANAL_PAINEL_LIVE:
            return await interaction.response.send_message(
                "Use no canal correto.",
                ephemeral=True
            )

        await interaction.channel.send(
            embed=padrao(
                "🔴 Painel de Lives",
                "Use os botões abaixo para iniciar ou finalizar live."
            ),
            view=LiveView(self.bot)
        )

        await interaction.response.send_message(
            "Painel enviado.",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(
        Live(bot),
        guild=discord.Object(id=GUILD_ID)
    )