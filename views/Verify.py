import asyncio
import discord

from discord.ext import commands

class Verify(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Verify", style=discord.ButtonStyle.blurple, custom_id="verify:blurple")
    async def verify(self, interaction: discord.Interaction, button: discord.Button):
        community_member = discord.utils.get(user.guild.roles, id=1071779538725511178)
        defaults = discord.utils.get(user.guild.roles, id=1145298529183604778)
        embedVerified = discord.Embed(description="Great! You have been verified.\n\nYou can now start talking to other members.", color=0x00ff00)
        channel = interaction.channel
        user = interaction.user
        
        await interaction.response.send_message(embed=embedVerified, ephemeral=True)
        await asyncio.sleep(1)
        await user.add_roles(defaults)
        await user.add_roles(community_member)
