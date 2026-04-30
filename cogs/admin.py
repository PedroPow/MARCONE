import discord
from discord.ext import commands
from discord import app_commands

from config import (
    GUILD_ID,
    CARGO_STAFF,
    CANAL_PAINEL_TICKET,
    CANAL_PAINEL_LIVE
)

from utils.perms import is_staff
from utils.embeds import padrao
from views.ticket_view import TicketView
from views.live_view import LiveView


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # PREFIX COMMANDS
    # =========================

    @commands.command()
    async def sync(self, ctx):

        if not is_staff(ctx.author):
            return

        synced = await self.bot.tree.sync(
            guild=discord.Object(id=GUILD_ID)
        )

        await ctx.send(
            f"✅ {len(synced)} comandos sincronizados."
        )

    @commands.command()
    async def reload(self, ctx):

        if not is_staff(ctx.author):
            return

        mods = [
            "cogs.tickets",
            "cogs.live",
            "cogs.contratos",
            "cogs.admin"
        ]

        for m in mods:
            try:
                await self.bot.reload_extension(m)
            except:
                pass

        await ctx.send("♻️ Módulos recarregados.")

    @commands.command()
    async def painel(self, ctx):

        if not is_staff(ctx.author):
            return

        if ctx.channel.id != CANAL_PAINEL_TICKET:
            return await ctx.send("Use no canal ticket.")

        await ctx.send(
            embed=padrao(
                "🎫 Tickets Marcone RP",
                "Clique abaixo para abrir ticket."
            ),
            view=TicketView(self.bot)
        )

    @commands.command()
    async def painellive(self, ctx):

        if not is_staff(ctx.author):
            return

        if ctx.channel.id != CANAL_PAINEL_LIVE:
            return await ctx.send("Use no canal live.")

        await ctx.send(
            embed=padrao(
                "🔴 Painel Lives",
                "Use os botões abaixo."
            ),
            view=LiveView(self.bot)
        )

    # =========================
    # READY STATUS
    # =========================

    @commands.Cog.listener()
    async def on_ready(self):

        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="Marcone RP"
            )
        )

        print("Admin system carregado.")


async def setup(bot):
    await bot.add_cog(
        Admin(bot),
        guild=discord.Object(id=GUILD_ID)
    )