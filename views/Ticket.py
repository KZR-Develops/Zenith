import asyncio
import os
import discord
import datetime

from discord.ext import commands
from datetime import datetime

class Setup(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.ticket_category_id = 1071728273677090837
        self.ticket_role = 1071715597567664258
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 600, commands.BucketType.member)
        
    @discord.ui.button(label="Create a Ticket", style=discord.ButtonStyle.blurple, custom_id="create:blurple")
    async def gen(self, interaction: discord.Interaction, button: discord.ui.Button):
        interaction.message.author = interaction.user
        retry = self.cooldown.get_bucket(interaction.message).update_rate_limit()
        if retry:
            return await interaction.response.send_message(f"Slow down! You can create a ticket again in {round(retry, 1)} seconds.", ephemeral=True)
        
        author = interaction.user
        guild = interaction.guild
        category = discord.utils.get(guild.categories, id=self.ticket_category_id)
        self.total_ticket = category.channels
        self.ticket_count = len(self.total_ticket) - 1
        self.ticket_name = self.ticket_count + 1
        channel_name = f'ticket-{self.ticket_name}'
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel = False),
            interaction.user: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files = True, embed_links = True)
        }
        channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
        
        embedCreated = discord.Embed(title="Ticket Creation", description=f"{author.mention}, Your ticket has been created in {channel.mention}.")
        embedAssistance = discord.Embed(title=f"Hey there {author.name}!", description=f"A staff will assist you shortly, please wait.\n<@&{self.ticket_role}>", timestamp=datetime.now())
        embedAssistance.set_footer(text=f"Ticket ID: {self.ticket_name}")
        await channel.send(embed=embedAssistance)
        await interaction.response.send_message(embed=embedCreated, ephemeral=True)

class Settings(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, custom_id="close:red", emoji="🗑️")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        embedConfirmation = discord.Embed(description="Are you sure you want to close this ticket?", color=0xff0000)
        await interaction.response.send_message(embed=embedConfirmation, ephemeral=True, view=CloseConfirm())
    
    @discord.ui.button(label="Create Transcript", style=discord.ButtonStyle.blurple, custom_id='transcript:blurple', emoji="🖨️")
    async def transcript(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.channel
        await interaction.response.defer()
        
        if os.path.exists(f'./extras/transcripts/{interaction.channel.id}.md'):
            return await interaction.followup.send(f"A transcript has already been generated", ephemeral=True)
        with open(f'./extras/transcripts/{interaction.channel.id}.md', 'a', encoding="utf-8") as f:
            f.write(f"# Transcript of {interaction.channel.name}:\n\n")
            async for message in channel.history(limit=None, oldest_first=True):
                created = datetime.strftime(message.created_at, "%m/%d/%Y at %H:%M")
                if message.edited_at:
                    edited = datetime.strftime(message.edited_at, '%m/%d/%Y at %H:%M')
                    f.write(f"{message.author} on {created}: {message.clean_content} (Edited at {edited})\n")
                else:
                    f.write(f"{message.author} on {created}: {message.clean_content}\n")
                
            generated = datetime.now().strftime('%m/%d/%Y at %H:%M')
            f.write(f"\n*Generated at {generated}*, this transcript was requested by {interaction.user}*")
                
        with open(f'./extras/transcripts/{interaction.channel.id}.md', 'rb') as f:
            await interaction.followup.send(file=discord.File(f, f"./extras/transcripts/{interaction.channel.id}.md"))

        async def delete_transcript():
            await asyncio.sleep(120)
            os.remove(f"./extras/transcripts/{interaction.channel.id}.md")
        
        asyncio.ensure_future(delete_transcript())



class CloseConfirm(discord.ui.View):
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.danger, custom_id="confirmclose:danger")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        embedAction = discord.Embed(description="Ticket is being deleted.", color=0xff0000)
        await interaction.response.send_message(embed=embedAction, ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.delete()