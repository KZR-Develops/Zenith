import discord

from discord.ext import commands
from datetime import datetime
from views.Ticket import Setup, Settings, TicketTypeSelector, ReportTypeSelector, AppealTypeSelector

class TicketingSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name="ticket")
    @commands.has_permissions(manage_guild=True)
    async def ticket(self, ctx):
        try:
            if ctx.invoked_subcommand is None:
                pass
        except commands.errors.MissingPermissions:
            embedError = discord.Embed(description="You don't have enough permissions to run this command!", color=0xff0000)
            
            await ctx.message.delete()
            await ctx.send(embed=embedError, delete_after=5)

    @ticket.command()
    async def setup(self, ctx):
        embedSetup = discord.Embed(title="Do you need help?", description="To get help from our staffs, click the button below.\n\nIt will automatically generate a channel to discuss your problem with our support team.", color=0xb50000)
        await ctx.send(embed=embedSetup, view=Setup())
        await ctx.message.delete()
            
    @ticket.command()
    async def settings(self, ctx):
        embedSettings = discord.Embed(description="What do you want to do to this ticket?")
        await ctx.send(embed=embedSettings, view=Settings())
        await ctx.message.delete()
    
        
async def setup(bot):
    await bot.add_cog(TicketingSetup(bot))