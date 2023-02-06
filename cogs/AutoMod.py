import discord

from discord.ext import commands

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        # Invite blocker
        embedNotice = discord.Embed(description=f"{message.author.mention}, Sending discord invite links is not allowed in this server.", color=0xff0000)

        if "discord.gg" in message.content:
            await message.delete()
            await message.channel.send(embed=embedNotice, delete_after=3)
        elif "dsc.gg" in message.content:
            await message.delete()
            await message.channel.send(embed=embedNotice, delete_after=3)
        elif "invite.gg" in message.content:
            await message.delete()
            await message.channel.send(embed=embedNotice, delete_after=3)
        elif "discord.io" in message.content:
            await message.delete()
            await message.channel.send(embed=embedNotice, delete_after=3)
            
async def setup(bot):
    await bot.add_cog(AutoMod(bot))