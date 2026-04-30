import discord
from discord.ext import commands
from discord import app_commands

from config import GUILD_ID, CARGOS, CATEGORIAS, CARGO_STAFF
from utils.perms import is_staff
from utils.embeds import padrao
from database import cursor, db

from views.contrato_view import ContratoView


class Contratos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="contratar",
        description="Contratar streamer"
    )
    @app_commands.describe(
        usuario="Membro a contratar",
        nivel="bronze/prata/ouro/platina/esmeralda/ruby/diamante/oficial"
    )
    async def contratar(
        self,
        interaction: discord.Interaction,
        usuario: discord.Member,
        nivel: str
    ):

        if not is_staff(interaction.user):
            return await interaction.response.send_message(
                "Apenas staff.",
                ephemeral=True
            )

        nivel = nivel.lower()

        if nivel not in CARGOS:
            return await interaction.response.send_message(
                "Nível inválido.",
                ephemeral=True
            )

        cargo = interaction.guild.get_role(CARGOS[nivel])
        categoria = interaction.guild.get_channel(CATEGORIAS[nivel])

        await usuario.add_roles(cargo)

        canal = await interaction.guild.create_text_channel(
            name=f"{nivel}-{usuario.name}",
            category=categoria
        )

        embed = padrao(
            "📄 Contrato Ativo",
            f"{usuario.mention} contratado como **{nivel.upper()}**"
        )

        await canal.send(
            embed=embed,
            view=ContratoView(self.bot, usuario.id)
        )

        cursor.execute(
            "INSERT OR REPLACE INTO contratos(user_id, nivel) VALUES (?,?)",
            (usuario.id, nivel)
        )
        db.commit()

        await interaction.response.send_message(
            f"{usuario.mention} contratado com sucesso.",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(
        Contratos(bot),
        guild=discord.Object(id=GUILD_ID)
    )