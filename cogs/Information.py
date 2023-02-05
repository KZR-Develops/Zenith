import datetime

from datetime import datetime
import json
import platform
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
        ram = psutil.virtual_memory().total / (1024.0 ** 3)
        ramUsage = psutil.virtual_memory().percent
        dpyVersion = discord.__version__
        cpuUsage= psutil.cpu_percent()
        cpu = psutil.cpu_count()
        currentTime = datetime.now()
        uptime = currentTime - lastBoot
        createdTime = self.bot.user.created_at.strftime("%A, %B %d %Y")
        pyVersion = platform.python_version()
        
        embedInfo = discord.Embed(title="About the Bot", color=0x00ff00, timestamp=currentTime)
        embedInfo.add_field(name="General Informations", value=f"**Name:** {self.bot.user.name}\n**Bot ID:** {self.bot.user.id}\n**Created At:** {createdTime}\n**Bot Version** {prodInfo['Phase']} v{prodInfo['Version']}\n", inline=False)
        embedInfo.add_field(name="Developer Informations", value=f"**Developer:** KZR\n**Developer ID:** {config['owner_id']}\n", inline=False)
        embedInfo.add_field(name="Bot Usage and Statistics", value=f"**Last Boot:** {lastBoot.month}/{lastBoot.day} @ {lastBoot.hour}:{lastBoot.minute}\n**Ram Usage:** {ramUsage} % of {ram:.2f} GB\n**CPU Usage:** {cpuUsage}% of {cpu} Cores\n**Library Used:** Running on Discord.py {dpyVersion} and on Python {pyVersion}\n**Uptime:** {uptime.days} days, {uptime.seconds // 3600} hours, {(uptime.seconds // 60) % 60} minutes, and {uptime.seconds % 60} seconds\n", inline=False)
        embedInfo.set_footer(text="This is an official bot for KZR's Hangout Place")
        
        await ctx.send(embed=embedInfo)
    
    @info.command()
    async def server(self, ctx):
        guild = ctx.guild
        embedInfo = discord.Embed(title=f"Server Information - {guild.name}", color=discord.Color.blue())

        embedInfo.add_field(name="Server Owner", value=guild.owner)
        embedInfo.add_field(name="Members", value=guild.member_count)
        embedInfo.add_field(name="Channels", value=len(guild.channels))
        embedInfo.add_field(name="Voice Channels", value=len([channel for channel in guild.channels if isinstance(channel, discord.VoiceChannel)]))
        embedInfo.add_field(name="Text Channels", value=len([channel for channel in guild.channels if isinstance(channel, discord.TextChannel)]))
        embedInfo.add_field(name="Server Creation Date", value=guild.created_at.strftime("%A, %B %d %Y"))
        embedInfo.add_field(name="Server Boost Status", value=guild.premium_tier)
        invite = await ctx.channel.create_invite(max_age=3600, max_uses=None)
        embedInfo.add_field(name="Invite Link", value=invite.url)

        await ctx.send(embed=embedInfo)
    
    @info.command()
    async def user(self, ctx, *, member: discord.Member=None):
        if member is None:
            member = ctx.author
        elif member is not None:
            member = member
        
        embedInfo = discord.Embed(title=f"{member.display_name}'s Information", description=f"Everything about {member.name}", color=member.color)
        
        embedInfo.set_thumbnail(url=member.avatar)
        embedInfo.add_field(name="Name:", value=member.name, inline=False)
        embedInfo.add_field(name="Discriminator:", value=member.discriminator, inline=False)
        embedInfo.add_field(name="ID:", value=member.id, inline=False)
        embedInfo.add_field(name="Top Role:", value=member.top_role, inline=False)
        embedInfo.add_field(name="Created Date:", value=member.created_at.__format__("%B %d, %Y @ %H:%M"), inline=False)
        embedInfo.add_field(name="Status:", value=member.status, inline=False)
            
        await ctx.send(embed=embedInfo)
        
async def setup(bot):
    await bot.add_cog(Information(bot))