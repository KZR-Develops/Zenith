import discord
from views.Verify import Verify

from discord.ext import commands

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def vsetup(self, ctx):
        embedVerification = discord.Embed(title="New here?", description="Click the verify button below to get verified.", color=0x5865f2)
        await ctx.send(embed=embedVerification, view=Verify())
        await ctx.message.delete()
        
async def setup(bot):
    await bot.add_cog(Verification(bot))