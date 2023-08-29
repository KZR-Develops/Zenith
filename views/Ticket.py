import asyncio
import os
import discord
import datetime
import json

from discord.ext import commands
from datetime import datetime

with open('./config.json', 'r') as f:
    config = json.load(f)
    
async def generate(self, interaction: discord.Interaction, type):
    
        author = interaction.user
        guild = interaction.guild
        category = discord.utils.get(guild.categories, id=self.ticket_category_id)
        dashboard = discord.utils.get(guild.channels, id=self.ticket_dashboard_id)
        self.total_ticket = category.channels
        self.ticket_count = len(self.total_ticket) - 1
        self.ticket_name = self.ticket_count + 1
        channel_name = f'ticket-{self.ticket_name}'
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel = False),
            interaction.user: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files = True, embed_links = True)
        }
        channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
        
        if type == "question":
            embedAssistance = discord.Embed(title=f"Please standby!", description=f"Hey there{author.mention}!\nA staff will be here shortly, please wait.\n<@&{self.ticket_role}>", timestamp=datetime.now())
            embedAssistance.set_footer(text=f"Ticket ID: {self.ticket_name}")
            await channel.send(embed=embedAssistance)
            
            embedDashboard = discord.Embed(description=f"Type of Ticket: Question\nTicket Channel: {channel.mention}", color=interaction.user.color, timestamp=datetime.now())
            embedDashboard.set_author(name=f"A ticket was generated for {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar)
            embedDashboard.set_footer(text=f"Ticket ID: {self.ticket_name}")
            
            await dashboard.send(embed=embedDashboard)
        if type == "report":
            embedAssistance = discord.Embed(title=f"Please standby!", description=f"Hey there{author.mention}!\n\nA staff will be here shortly, please wait.\n<@&{self.ticket_role}>\n\nWhile waiting please select the category you want to report.", timestamp=datetime.now())
            embedAssistance.set_footer(text=f"Ticket ID: {self.ticket_name}")
            await channel.send(embed=embedAssistance, view=ReportTypeSelector())
            
            embedDashboard = discord.Embed(description=f"Type of Ticket: Report\nTicket Channel: {channel.mention}", color=interaction.user.color, timestamp=datetime.now())
            embedDashboard.set_author(name=f"A ticket was generated for {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar)
            embedDashboard.set_footer(text=f"Ticket ID: {self.ticket_name}")
            
            await dashboard.send(embed=embedDashboard)
        if type == "appeal":
            embedAssistance = discord.Embed(title=f"Please standby!", description=f"Hey there!\n\nWe sincerely apologize for the actions of our moderator that resulted in a misconduct.\nIf you have proven that our moderator made a mistake, we are willing to take full responsibility.", timestamp=datetime.now())
            embedAssistance.set_footer(text=f"Ticket ID: {self.ticket_name}")
            await channel.send(embed=embedAssistance)   
            
            embedDashboard = discord.Embed(description=f"Type of Ticket: Appeal\nTicket Channel: {channel.mention}", color=interaction.user.color, timestamp=datetime.now())
            embedDashboard.set_author(name=f"A ticket was generated for {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar)
            embedDashboard.set_footer(text=f"Ticket ID: {self.ticket_name}")
            
            await dashboard.send(embed=embedDashboard) 
        
        embedCreated = discord.Embed(title="Ticket Creation", description=f"{author.mention}, Your ticket has been created in {channel.mention}.", timestamp=datetime.now())    
        await interaction.response.send_message(embed=embedCreated, ephemeral=True)
class Setup(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.ticket_category_id = config['categories']['ticket']
        self.ticket_role = config['roles']['ticketer']
        self.ticket_dashboard_id = config['channels']['ticket_dashboard']
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 600, commands.BucketType.member)
    
    @discord.ui.button(label="Create a Ticket", style=discord.ButtonStyle.red, custom_id="create:blurple")
    async def create(self, interaction: discord.Interaction, button: discord.ui.Button):
        interaction.message.author = interaction.user
        retry = self.cooldown.get_bucket(interaction.message).update_rate_limit()
        if retry:
            return await interaction.response.send_message(f"Slow down! You can create a ticket again in {round(retry, 1)} seconds.", ephemeral=True)
        
        embedTypeSelector = discord.Embed(description="To assist you further, tell us why you are creating a ticket.", color=0xb50000)
        await interaction.response.send_message(embed=embedTypeSelector, view=TicketTypeSelector(), ephemeral=True)

class TicketTypeSelector(discord.ui.View):
    ticket_category_id = config['categories']['ticket']
    ticket_role = config['roles']['ticketer']
    ticket_dashboard_id = config['channels']['ticket_dashboard']
    
    types = [
        discord.SelectOption(label="Questions", value="question", description="Want to clarify something?", emoji="❔"),
        discord.SelectOption(label="Report", value="report", description="To report a misbehaving user or broken features.", emoji="❕"),
        discord.SelectOption(label="Appeal", value="appeal", description="If you want to file an appeal for a moderation activity.", emoji="📄")
    ]
    
    @discord.ui.select(placeholder="What's the ticket for?", options=types)
    async def menu_callback(self, interaction: discord.Interaction, select):
        
        if select.values[0] == "question":
            await generate(self, interaction, type="question")
        if select.values[0] == "report":
            await generate(self, interaction, type="report")
        if select.values[0] == "appeal":
            await generate(self, interaction, type="appeal")
            
        
class ReportTypeSelector(discord.ui.View):
    ticket_category_id = int(config['categories']['ticket'])
    ticket_role = int(config['roles']['ticketer'])
    ticket_dashboard_id = int(config['channels']['ticket_dashboard'])
    
    types = [
        discord.SelectOption(label="A member", value="member"),
        discord.SelectOption(label="A staff", value="staff"),
        discord.SelectOption(label="A broken feature", value="feature")
    ]
    
    @discord.ui.select(placeholder="Select the category that matches your report", options=types)
    async def menu_callback(self, interaction: discord.Interaction, select):
        select.disabled = True
        
        if select.values[0] == "member":
            embedFollowUp = discord.Embed(description="Who are you reporting? Also state the reason, so we can assist you further.")
            await interaction.response.send_message(embed=embedFollowUp)
        if select.values[0] == "staff":
            embedFollowUp = discord.Embed(description="Who are you reporting? Also state the reason, so we can assist you further.")
            await interaction.response.send_message(embed=embedFollowUp)
        if select.values[0] == "feature":
            embedFollowUp = discord.Embed(description="Tell us more about this broken feature.")
            await interaction.response.send_message(embed=embedFollowUp)
            
    
class AppealTypeSelector(discord.ui.View):
    ticket_category_id = int(config['categories']['ticket'])
    ticket_role = int(config['roles']['ticketer'])
    
    types = [
        discord.SelectOption(label="I have been warned", value="warned"),
        discord.SelectOption(label="I have been muted", value="muted"),
        discord.SelectOption(label="I have been kicked", value="kicked"),
        discord.SelectOption(label="I have been banned", value="banned")
    ]
    
    @discord.ui.select(placeholder="What is this appeal for?", options=types)
    async def menu_callback(self, interaction: discord.Interaction, select):
        select.disabled = True
        
        if select.values[0] == "warned":
            embedFollowUp = discord.Embed(description="Tell us more, if possible also state your Case ID (This is located at the footer of every notice sent directly to you.)")
            await interaction.response.send_message(embed=embedFollowUp)
        if select.values[0] == "muted":
            embedFollowUp = discord.Embed(description="Tell us more, if possible also state your Case ID (This is located at the footer of every notice sent directly to you.)")
            await interaction.response.send_message(embed=embedFollowUp)
        if select.values[0] == "kicked":
            embedFollowUp = discord.Embed(description="Tell us more, if possible also state your Case ID (This is located at the footer of every notice sent directly to you.)")
            await interaction.response.send_message(embed=embedFollowUp)
        if select.values[0] == "kicked":
            embedFollowUp = discord.Embed(description="Tell us more, if possible also state your Case ID (This is located at the footer of every notice sent directly to you.)")
            await interaction.response.send_message(embed=embedFollowUp)
                
class Settings(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, custom_id="close:red", emoji="🗑️")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        embedConfirmation = discord.Embed(description="Are you sure you want to close this ticket?", color=0xff0000)
        await interaction.response.send_message(embed=embedConfirmation, ephemeral=True, view=CloseConfirmation())
    
    @discord.ui.button(label="Create Transcript", style=discord.ButtonStyle.blurple, custom_id='transcript:blurple', emoji="🖨️")
    async def transcript(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.channel
        dashboard = discord.utils.get(interaction.guild.channels, id=self.ticket_dashboard_id)

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

class CloseConfirmation(discord.ui.View):
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.gray, custom_id="cancel:gray")
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()
        
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.danger, custom_id="confirmclose:danger")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        embedAction = discord.Embed(description="Ticket is being deleted.", color=0xff0000)
        await interaction.response.send_message(embed=embedAction, ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.delete()