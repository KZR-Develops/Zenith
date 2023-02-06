import datetime

from datetime import datetime
import json
import platform
import time
import discord
import psutil

from discord.ext import commands

with open('config.json') as f:
    config = json.load(f)
class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.startTime = datetime.now()
    
    @commands.group()
    async def info(self, ctx):
        if ctx.invoked_subcommand is None:
            embedError = discord.Embed(description=f"Try {config['prefix']}bot, {config['prefix']}server, or {config['prefix']}user")
            await ctx.send(embed=embedError)
               
    @info.command()
    async def bot(self, ctx):
        with open('config.json', 'r') as f:
            config = json.load(f)
            
        with open('prodInfo.json', 'r') as f:
            prodInfo = json.load(f)
            
        
        lastBoot = self.startTime
        
        formattedLastBoot = self.startTime.strftime("%B %d, %Y @ %I:%M %p")
        ram = psutil.virtual_memory().total / (1024.0 ** 3)
        ramUsage = psutil.virtual_memory().percent
        dpyVersion = discord.__version__
        cpuUsage= psutil.cpu_percent()
        cpu = psutil.cpu_count()
        currentTime = datetime.now()
        uptime = currentTime - lastBoot
        createdTime = self.bot.user.created_at.strftime("%B %d, %Y @ %I:%M %p")
        pyVersion = platform.python_version()
        
        embedInfo = discord.Embed(color=0x00ff00, timestamp=currentTime)
        embedInfo.set_author(name=f"{self.bot.user.name}#{self.bot.user.discriminator}", icon_url=self.bot.user.avatar)
        embedInfo.add_field(name="General Informations", value=f"**Name:** {self.bot.user.name}\n**Bot ID:** {self.bot.user.id}\n**Created At:** {createdTime}\n**Bot Version** {prodInfo['Phase']} v{prodInfo['Version']}\n", inline=False)
        embedInfo.add_field(name="Developer Informations", value=f"**Developer:** KZR\n**Developer ID:** {config['owner_id']}\n", inline=False)
        embedInfo.add_field(name="Bot Usage and Statistics", value=f"**Last Boot:** {formattedLastBoot} \n**Ram Usage:** {ramUsage} % of {ram:.2f} GB\n**CPU Usage:** {cpuUsage}% of {cpu} Cores\n**Library Used:** Running on Discord.py {dpyVersion} and on Python {pyVersion}\n**Uptime:** {uptime.days} days, {uptime.seconds // 3600} hours, {(uptime.seconds // 60) % 60} minutes, and {uptime.seconds % 60} seconds\n", inline=False)
        embedInfo.set_footer(text="This is an official bot for KZR's Hangout Place")
        
        await ctx.send(embed=embedInfo)
    
    @info.command()
    async def server(self, ctx):
        guild = ctx.guild
        embedInfo = discord.Embed(description=guild.description, color=discord.Color.blue())

        embedInfo.set_author(name=guild.name, icon_url=guild.icon)
        embedInfo.set_thumbnail(url=guild.icon)
        embedInfo.add_field(name="Server ID", value=guild.id, inline=False)
        embedInfo.add_field(name="Members", value=guild.member_count, inline=False)
        embedInfo.add_field(name="Channels", value=f"Text Channels: {len([channel for channel in guild.channels if isinstance(channel, discord.TextChannel)])}\nVoice Channels: {len([channel for channel in guild.channels if isinstance(channel, discord.VoiceChannel)])}", inline=False)
        embedInfo.add_field(name="Boost Status", value=f"Boost Level: {guild.premium_tier}\nBoost Count: {guild.premium_subscription_count}", inline=False)
        embedInfo.add_field(name="Creation Date", value=guild.created_at.__format__("%B %d, %Y @ %I:%M %p"), inline=False)
        
        if guild.verification_level == discord.VerificationLevel.none:
            embedInfo.add_field(name="Verification Level", value="[None] This server is unrestricted.")
        elif guild.verification_level == discord.VerificationLevel.low:
            embedInfo.add_field(name="Verification Level", value="[Low] Must have a verified email on their account.")
        elif guild.verification_level == discord.VerificationLevel.medium:
            embedInfo.add_field(name="Verification Level", value="[Medium] Must be registered for longer than 5 minutes.")
        elif guild.verification_level == discord.VerificationLevel.high:
            embedInfo.add_field(name="Verification Level", value="[High] Must be a member for longer than 10 minutes.")
        elif guild.verification_level == discord.VerificationLevel.highest:
            embedInfo.add_field(name="Verification Level", value="[Highest] Must have a verified phone on their account.")
                

        await ctx.send(embed=embedInfo)
    
    @info.command()
    async def user(self, ctx, *, member: discord.Member=None):
        if member is None:
            member = ctx.author
        elif member is not None:
            member = member
        
        embedInfo = discord.Embed(color=member.color)
        
        embedInfo.set_thumbnail(url=member.avatar)
        embedInfo.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar)
        embedInfo.add_field(name="Member ID", value=member.id, inline=True)
        embedInfo.add_field(name="Nickname", value=member.nick, inline=True)
        embedInfo.add_field(name="Top Role", value=member.top_role, inline=False)
        embedInfo.add_field(name="Account Creation Date", value=member.created_at.__format__("%B %d, %Y @ %I:%M %p"), inline=False)
        embedInfo.add_field(name="Member Since", value=member.joined_at.__format__("%B %d, %Y @ %I:%M %p"), inline=False)
            
        await ctx.send(embed=embedInfo)
        
async def setup(bot):
    await bot.add_cog(Information(bot))