import asyncio
import time
import discord
import os
import sys
import json

from discord.ext import commands


# Fetch configuration datas
with open('config.json', 'r') as f:
    config = json.load(f)

class DeveloperTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group()
    async def cog(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(description=f"cog load [extension name], cog unload [extension name], cog reload [extension name], cog list")
            
            await ctx.send(embed=embed)
    
    @cog.command()
    async def load(self, ctx, extension_name : str):
        """Loads an extension."""
        try:
            await self.bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        
        embedAction = discord.Embed(description=f"{extension_name} has been loaded with no errors.", color=0x00ff00)
        await ctx.send(embed=embedAction)

    @cog.command()
    async def unload(self, ctx, extension_name : str):
        """Unloads an extension."""
        await self.bot.unload_extension(extension_name)
        embedAction = discord.Embed(description=f"{extension_name} has been loaded with no errors.", color=0x00ff00)
        await ctx.send(embed=embedAction)
        
    @cog.command()
    async def reload(self, ctx, *, extension_name: str):
        """Reloads an extension."""
        extension_path = f'cogs.{extension_name}'
        if extension_path in self.bot.extensions:
            await self.bot.unload_extension(extension_path)
            
        try:
            await self.bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        
        embedAction = discord.Embed(description=f"{extension_name} has been loaded with no errors.", color=0x00ff00)
        await ctx.send(embed=embedAction)

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await self.bot.close()
        print("Closed the connection between the bot and the gateway.")
        os._exit(0)


async def setup(bot):
    await bot.add_cog(DeveloperTools(bot))
