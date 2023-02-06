import datetime
import json
import discord

from datetime import datetime
from discord.ext import commands

with open('config.json') as f:
    config = json.load(f)
    
class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.startTime = datetime.now()
               
    @commands.command(aliases=["botinfo", "infobot"])
    async def info(self, ctx):
        with open('config.json', 'r') as f:
            config = json.load(f)
            
        with open('prodInfo.json', 'r') as f:
            prodInfo = json.load(f)
            
        
        lastBoot = self.startTime
        
        formattedLastBoot = self.startTime.strftime("%B %d, %Y @ %I:%M %p")
        dpyVersion = discord.__version__
        currentTime = datetime.now()
        uptime = currentTime - lastBoot
        createdTime = self.bot.user.created_at.strftime("%B %d, %Y @ %I:%M %p")
        
        embedInfo = discord.Embed(color=self.bot.user.color, timestamp=currentTime)
        embedInfo.set_author(name=f"{self.bot.user.name}#{self.bot.user.discriminator}", icon_url=self.bot.user.avatar)
        embedInfo.add_field(name="Version", value=prodInfo['Version'], inline=True)
        embedInfo.add_field(name="Library", value=f"Discord.py {dpyVersion}", inline=True)
        embedInfo.add_field(name="Uptime", value=f"{uptime.days} days, {uptime.seconds // 3600} hours, {(uptime.seconds // 60) % 60} minutes, and {uptime.seconds % 60} seconds", inline=False)
        embedInfo.add_field(name="Last System Startup Date", value=formattedLastBoot, inline=False)
        
        await ctx.send(embed=embedInfo)
    
    @commands.command(aliases=["sinfo", "infoserver"])
    async def serverinfo(self, ctx):
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
    
    @commands.command(aliases=["whois", "memberinfo", "infomember", "infouser"])
    async def userinfo(self, ctx, *, member: discord.Member=None):
        if member is None:
            member = ctx.author
        elif member is not None:
            member = member
            
        roles = sorted(member.roles, key=lambda x: x.position, reverse=True)
        for role in roles:
            if role.hoist:
                highest_role = role
                break
            else:
                highest_role = member.top_role
        
        embedInfo = discord.Embed(color=member.color)
        
        embedInfo.set_thumbnail(url=member.avatar)
        embedInfo.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar)
        embedInfo.add_field(name="Member ID", value=member.id, inline=True)
        embedInfo.add_field(name="Nickname", value=member.nick, inline=True)
        embedInfo.add_field(name="Top Role", value=highest_role, inline=False)
        embedInfo.add_field(name="Account Creation Date", value=member.created_at.__format__("%B %d, %Y @ %I:%M %p"), inline=False)
        embedInfo.add_field(name="Member Since", value=member.joined_at.__format__("%B %d, %Y @ %I:%M %p"), inline=False)
            
        await ctx.send(embed=embedInfo)
        
    @commands.command()
    async def ping(self, ctx):
        embedLatency = discord.Embed(description=f"It took me approximately {round(self.bot.latency * 100)}ms to respond back.",color=self.bot.user.color)
        embedLatency.set_author(name=f"Latency Checker")
        
        await ctx.send(embed=embedLatency)
    
    
    @commands.command()
    async def uptime(self, ctx):
        
        lastBoot = self.startTime
        currentTime = datetime.now()
        uptime = currentTime - lastBoot
        
        embedUptime = discord.Embed(description=f"{uptime.days} days, {uptime.seconds // 3600} hours, {(uptime.seconds // 60) % 60} minutes, and {uptime.seconds % 60} seconds", color=self.bot.user.color)
        embedUptime.set_author(name="Uptime Checker")
        
        await ctx.send(embed=embedUptime)
        
        
async def setup(bot):
    await bot.add_cog(Information(bot))