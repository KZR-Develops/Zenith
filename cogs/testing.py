import discord
import json
from discord.ext import commands

with open('./config.json', 'r') as f:
    config = json.load(f)

class Testings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def send(self, ctx):
        modlogs = config['channels']['modlogs']
        
        channel = self.bot.get_channel(int(modlogs))
        await channel.send(ctx.message.content)
        
async def setup(bot):
    await bot.add_cog(Testings(bot))