import asyncio
import discord

from discord.ext import commands

class Verify(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Verify", style=discord.ButtonStyle.blurple, custom_id="verify:blurple")
    async def verify(self, interaction: discord.Interaction, button: discord.Button):
        verified_id = 1071779538725511178
        embedVerified = discord.Embed(description="Great! You have been verified.\n\nYou can now start talking to other members.", color=0x00ff00)
        channel = interaction.channel
        user = interaction.user
        verified = discord.utils.get(user.guild.roles, id=verified_id)
        
        await interaction.response.send_message(embed=embedVerified, ephemeral=True)
        await asyncio.sleep(1)
        await user.add_roles(verified)
