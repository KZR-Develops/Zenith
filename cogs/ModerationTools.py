from datetime import datetime
import discord
import json

from discord.ext import commands

# Get's the logging channel info
with open('config.json', 'r') as f:
    config = json.load(f)

class ModerationTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.limit = config['Limits']['Purge']
    
    @commands.command(aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int, member: discord.Member=None):
        
        if amount > int(self.limit):
            embedError = discord.Embed(description="The amount exceeds the limit. Do not exceed the limit to keep the bot running smoothly.")
            
            await ctx.send(embed=embedError)
        else:
            if member is not None:
                modlogsID = config['channels']['modlogs']
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Load the JSON file containing the cases
                with open('./extras/cases.json', 'r') as f:
                    cases = json.load(f)
                
                # Increment the case number
                case_number = cases['total_count'] + 1
                
                # Create a new case object
                new_case = {
                    'ID': case_number,
                    'Responsible Staff': ctx.author.name,
                    'Activity': 'Purge Member Message',
                    'Channel': ctx.channel.name,
                    'Member': member.name,
                    'Time': current_time
                }
                
                # Append the new case to the cases list
                cases['cases'].append(new_case)
                
                # Update the case number in the JSON file
                cases['total_count'] = case_number
                
                # Save the JSON file
                with open('./extras/cases.json', 'w') as f:
                    json.dump(cases, f, indent=4)
                
                # Deletes x amount of messages and sends a message on the channel
                await ctx.channel.purge(limit=amount + 1, check=lambda m: m.author == member)
                embedAction = discord.Embed(description=f"Deleted {amount} messages of {member.display_name} in this channel", color=0xf50000)
                await ctx.send(embed=embedAction, delete_after=5)
                
                # Log the moderation activity
                channel = self.bot.get_channel(modlogsID)
                embedLog = discord.Embed(description=f"Deleted {amount} messages of {member.display_name} in {ctx.channel.mention}", color=0x9acd32, timestamp=datetime.now())
                embedLog.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                embedLog.set_footer(text=f"Case ID: {case_number}")
                await channel.send(embed=embedLog)
            else:
                modlogsID = config['channels']['modlogs']
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Load the JSON file containing the cases
                with open('./extras/cases.json', 'r') as f:
                    cases = json.load(f)
                
                # Increment the case number
                case_number = cases['total_count'] + 1
                
                # Create a new case object
                new_case = {
                    'ID': case_number,
                    'Responsible Staff': ctx.author.name,
                    'Activity': 'Purge',
                    'Channel': ctx.channel.name,
                    'Time': current_time
                }
                
                # Append the new case to the cases list
                cases['cases'].append(new_case)
                
                # Update the case number in the JSON file
                cases['total_count'] = case_number
                
                # Save the JSON file
                with open('./extras/cases.json', 'w') as f:
                    json.dump(cases, f, indent=4)
                
                # Deletes x amount of messages and sends a message on the channel
                await ctx.channel.purge(limit=amount + 1)
                embedAction = discord.Embed(description=f"Deleted {amount} messages in this channel", color=0xf50000)
                await ctx.send(embed=embedAction, delete_after=5)
                
                # Log the moderation activity
                modlogs = self.bot.get_channel(int(modlogsID))
                embedLog = discord.Embed(description=f"Deleted {amount} messages in {ctx.channel.mention}", color=0x9acd32, timestamp=datetime.now())
                embedLog.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                embedLog.set_footer(text=f"Case ID: {case_number}")
                await modlogs.send(embed=embedLog)       
        
    ### Punishment System ###
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if member == ctx.author:
            embedError = discord.Embed(description="Error! You cannot kick yourself!", color=0xff0000)
            
            await ctx.send(embed=embedError, delete_after=3)
        else:
            modlogsID = config['channels']['modlogs']
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Load the JSON file containing the cases
            with open('./extras/cases.json', 'r') as f:
                cases = json.load(f)
            
            # Increment the case number
            case_number = cases['total_count'] + 1
            
            # Create a new case object
            new_case = {
                'ID': case_number,
                'Responsible Staff': ctx.author.name,
                'User': member.name,
                'Activity': 'Kicked',
                'Reason': reason,
                'Time': current_time
            }
            
            # Append the new case to the cases list
            cases['cases'].append(new_case)
            
            # Update the case number in the JSON file
            cases['total_count'] = case_number
            
            # Save the JSON file
            with open('./extras/cases.json', 'w') as f:
                json.dump(cases, f, indent=4)
                
            # Sends a message on the channel and kicks the member
            embedAction = discord.Embed(description=f"{member.name} has been removed from the server for violating our community guidelines.", color=0xf50000)
            await ctx.send(embed=embedAction, delete_after=5)
            # await member.kick(reason=reason)
            
            # Send a kick notice to the member
            embedNotice = discord.Embed(description=f"Hey there {member.name}!\n\nThis message is sent to make you aware of the action we've made.\nYou have been removed from the server for violating our community guidelines.\n\nWe take the safety and well-being of our community seriously. Please respect our rules and guidelines to ensure a positive and enjoyable experience for all members.\n\nIf you were removed from the server and believe it was unjust, you can [submit an appeal](https://forms.gle/M6yTr78DkMycVpSY7) for reinstatement. Provide a clear explanation and any supporting evidence. We take moderation actions seriously and will not entertain frivolous appeals. Our team will review and make a decision as soon as possible.", color=0xf50000, timestamp=datetime.now())
            embedNotice.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
            embedNotice.add_field(name="Reason For The Action:", value=reason)
            embedNotice.set_footer(text=f"Case ID: {case_number}")
            
            await member.send(embed=embedNotice)
            
            # Log the moderation activity
            modlogs = self.bot.get_channel(int(modlogsID))
            embedLog = discord.Embed(color=0xf50000, timestamp=datetime.now())
            embedLog.set_author(name=f"{member.name}#{member.discriminator} has been kicked", icon_url=member.avatar)
            embedLog.add_field(name="Responsible Staff", value=ctx.author, inline=True)
            embedLog.add_field(name="Reason", value=reason, inline=False)
            await modlogs.send(embed=embedLog)
        
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if member == ctx.author:
            embedError = discord.Embed(description="Error! You cannot ban yourself!", color=0xff0000)
            
            await ctx.send(embed=embedError, delete_after=3)
        else:
            modlogsID = config['channels']['modlogs']
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Load the JSON file containing the cases
            with open('./extras/cases.json', 'r') as f:
                cases = json.load(f)
            
            # Increment the case number
            case_number = cases['total_count'] + 1
            
            # Create a new case object
            new_case = {
                'ID': case_number,
                'Responsible Staff': ctx.author.name,
                'User': member.name,
                'Activity': 'Banned',
                'Reason': reason,
                'Time': current_time
            }
            
            # Append the new case to the cases list
            cases['cases'].append(new_case)
            
            # Update the case number in the JSON file
            cases['total_count'] = case_number
            
            # Save the JSON file
            with open('./extras/cases.json', 'w') as f:
                json.dump(cases, f, indent=4)
                
            # Sends a message on the channel and bans the member
            embedAction = discord.Embed(description=f"{member.name} has been banned from the server for violating our community guidelines.", color=0xf50000)
            await ctx.send(embed=embedAction)
            # await member.ban(reason=reason)
            
            # Send a ban notice to the member
            embedNotice = discord.Embed(description=f"Hey there {member.name}!\n\nThis message is sent to make you aware of the action we've made.\nYou have been banned from the server for violating our community guidelines.\n\nWe take the safety and well-being of our community seriously. Please respect our rules and guidelines to ensure a positive and enjoyable experience for all members.\n\nIf you were removed from the server and believe it was unjust, you can [submit an appeal](https://forms.gle/M6yTr78DkMycVpSY7) for reinstatement. Provide a clear explanation and any supporting evidence. We take moderation actions seriously and will not entertain frivolous appeals. Our team will review and make a decision as soon as possible.", color=0xf50000, timestamp=datetime.now())
            embedNotice.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
            embedNotice.add_field(name="Reason For The Action:", value=reason)
            embedNotice.set_footer(text=f"Case ID: {case_number}")
            
            await member.send(embed=embedNotice)
            
            # Log the moderation activity
            modlogs = self.bot.get_channel(int(modlogsID))
            embedLog = discord.Embed(color=0xf50000, timestamp=datetime.now())
            embedLog.set_author(name=f"{member.name}#{member.discriminator} has been banned", icon_url=member.avatar)
            embedLog.add_field(name="Responsible Staff", value=ctx.author, inline=True)
            embedLog.add_field(name="Reason", value=reason, inline=False)
            await modlogs.send(embed=embedLog)
        
    ### Warning System ###
    @commands.command()
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        if member == ctx.author:
            embedError = discord.Embed(description="Error! You cannot warn yourself!", color=0xff0000)
            
            await ctx.send(embed=embedError, delete_after=3)
        else:
            modlogsID = config['channels']['modlogs']
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Load the JSON file containing the cases
            with open('./extras/cases.json', 'r') as f:
                cases = json.load(f)
            
            # Increment the case number
            case_number = cases['total_count'] + 1
            
            # Create a new case object
            new_case = {
                'ID': case_number,
                'Responsible Staff': ctx.author.name,
                'User': member.name,
                'Status': 'Warning',
                'Reason': reason,
                'Time': current_time
            }
            
            # Append the new case to the cases list
            cases['cases'].append(new_case)
            
            # Update the case number in the JSON file
            cases['total_count'] = case_number
            
            # Save the JSON file
            with open('./extras/cases.json', 'w') as f:
                json.dump(cases, f, indent=4)
            
            # Load the JSON file containing the warnings
            with open("./extras/warnings.json", "r") as f:
                warnings = json.load(f)
            
            # Checks if the member has existing warning
            if str(member.id) not in warnings:
                warnings[str(member.id)] = {"WarningCount": "0",}

            warnings[str(member.id)]["WarningCount"] = str(int(warnings[str(member.id)]["WarningCount"]) + 1)
            warning_number = warnings[str(member.id)]["WarningCount"]
            warnings[str(member.id)][warning_number] = {
                "Reason": reason,
                "Staff Responsible": ctx.author.name,
                "Time": str(datetime.now())
            }
            
            # Save the JSON file
            with open("./extras/warnings.json", "w") as f:
                json.dump(warnings, f, indent=4)
                
            # Sends a message on the channel
            embedAction = discord.Embed(description=f"{member.mention} have been warned for the reason stated below\n\n**Reason**: {reason}", color=0xf50000)
            await ctx.send(embed=embedAction, delete_after=5)
            
            # Send a warning to the member
            embedNotice = discord.Embed(description=f"Hey there {member.name}!\n\nThis message is sent to make you aware of the action we've made.\nYou have been warned from the server for violating our community guidelines.\n\nWe take the safety and well-being of our community seriously. Please respect our rules and guidelines to ensure a positive and enjoyable experience for all members.", color=0xf50000, timestamp=datetime.now())
            embedNotice.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
            embedNotice.add_field(name="Reason For The Action:", value=reason)
            embedNotice.set_footer(text=f"Total # of Warnings {warning_number} • Case ID: {case_number}")
            
            await member.send(embed=embedNotice)
            
            # Log the moderation activity
            modlogs = self.bot.get_channel(int(modlogsID))
            embedLog = discord.Embed(color=0xf50000, timestamp=datetime.now())
            embedLog.set_author(name=f"Warning for {member.name}#{member.discriminator}", icon_url=member.avatar)
            embedLog.add_field(name=f"Total Warnings", value=warning_number, inline=True)
            embedLog.add_field(name="Responsible Staff", value=ctx.author, inline=True)
            embedLog.add_field(name="Reason", value=reason, inline=False)
            embedLog.set_footer(text=f"Member ID: {member.id} • Case ID: {case_number}")
            
            await modlogs.send(embed=embedLog)
    
    @commands.command()
    async def clearwarnings(self, ctx, member: discord.Member):
        if member == ctx.author:
            embedError = discord.Embed(description="Error! You cannot clear your warnings!", color=0xff0000)
            
            await ctx.send(embed=embedError, delete_after=3)
        else:
            modlogsID = config['channels']['modlogs']
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Load the JSON file containing the cases
            with open('./extras/cases.json', 'r') as f:
                cases = json.load(f)
            
            # Increment the case number
            case_number = cases['total_count'] + 1
            
            # Create a new case object
            new_case = {
                'ID': case_number,
                'Responsible Staff': ctx.author.name,
                'User': member.name,
                'Activity': 'Clear Warnings',
                'Time': current_time
            }
            
            # Append the new case to the cases list
            cases['cases'].append(new_case)
            
            # Update the case number in the JSON file
            cases['total_count'] = case_number
            
            # Save the JSON file
            with open('./extras/cases.json', 'w') as f:
                json.dump(cases, f, indent=4)
            
            # Load the JSON file containing the warnings
            with open('./extras/warnings.json', 'r') as f:
                warnings = json.load(f)


            # Sends a message on the channel and clear all the warnings of the member
            if str(member.id) not in warnings:
                await ctx.send("This user has no warnings.")
                return

            del warnings[str(member.id)]
            with open('./extras/warnings.json', 'w') as f:
                json.dump(warnings, f)

            embedAction = discord.Embed(description=f"All warnings of {member.mention} have been cleared.", timestamp=datetime.now())
            await ctx.send(embed=embedAction, delete_after=5)

            # Log the moderation activity
            modlogs = self.bot.get_channel(int(modlogsID))
            embedLog = discord.Embed(color=0x9acd32, timestamp=datetime.now())
            embedLog.set_author(name=f"Cleared all warnings for {member.name}#{member.discriminator}", icon_url=member.avatar)
            embedLog.set_footer(text=f"Case ID: {case_number}")
            
            await modlogs.send(embed=embedLog)
            
    @commands.command(aliases=["warnings", "checkwarns", "warns"])
    async def checkwarnings(self, ctx, member: discord.Member):
        with open('./extras/warnings.json', 'r') as f:
            warnings = json.load(f)
            
        if str(member.id) not in warnings:
            embedCount = discord.Embed(description=f"{member.name}#{member.discriminator} has a total of no warnings.", color=member.color)
            await ctx.send(embed=embedCount)
            return
            
        count = warnings[str(member.id)]["WarningCount"]
        
        embedCount = discord.Embed(description=f"{member.name}#{member.discriminator} has a total of {count} of warnings.", color=member.color)
        
        await ctx.send(embed=embedCount)
        
    ### Lockdown System ###
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def lockdown(self, ctx):
        
        modlogsID = config['channels']['modlogs']
        announcement = config['channels']['announcement']
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Load the JSON file containing the cases
        with open('./extras/cases.json', 'r') as f:
            cases = json.load(f)
        
        # Increment the case number
        case_number = cases['total_count'] + 1
        
        # Create a new case object
        new_case = {
            'ID': case_number,
            'Responsible Staff': ctx.author.name,
            'Status': 'Server Lockdown',
            'Time': current_time
        }
        
        # Append the new case to the cases list
        cases['cases'].append(new_case)
        
        # Update the case number in the JSON file
        cases['total_count'] = case_number
        
        # Save the JSON file
        with open('./extras/cases.json', 'w') as f:
            json.dump(cases, f, indent=4)
        
        # Load the config file and gets all the channel in ChannelsToLock key in a lockdown mode
        with open("config.json") as f:
            config = json.load(f)
        channels_to_lock = config["ChannelsToLock"]

        for channel_id in channels_to_lock:
            channel = ctx.guild.get_channel(int(channel_id))
            if channel is None:
                continue

            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

        # Sends a message on the announcement channel
        channel = self.bot.get_channel(announcement)
        embedAction = discord.Embed(description="**Attention** @everyone,\n\nOur server is currently in lockdown mode.\nAccess to certain channels and features may be restricted.\nThis is for the safety and security of the community.\n\nPlease follow any instructions from the server administrators and stay updated on the situation. \n\nThank you for your understanding and cooperation.\n\n- Management", color=0xff0000)
        await channel.send(embed=embedAction)
        
        # Log the moderation activity
        modlogs = self.bot.get_channel(int(modlogsID))
        embedLog = discord.Embed(color=0x000000, timestamp=datetime.now())
        embedLog.set_author(name="Lockdown mode has been enabled.", icon_url=ctx.guild.icon)
        embedLog.set_footer(text=f"Case ID: {case_number}")
        
        await modlogs.send(embed=embedLog)
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unlock(self, ctx):
        
        modlogsID = config['channels']['modlogs']
        announcement = config['channels']['announcement']
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Load the JSON file containing the cases
        with open('./extras/cases.json', 'r') as f:
            cases = json.load(f)
        
        # Increment the case number
        case_number = cases['total_count'] + 1
        
        # Create a new case object
        new_case = {
            'ID': case_number,
            'Responsible Staff': ctx.author.name,
            'Status': 'Lockdown Lifted',
            'Time': current_time
        }
        
        # Append the new case to the cases list
        cases['cases'].append(new_case)
        
        # Update the case number in the JSON file
        cases['total_count'] = case_number
        
        # Save the JSON file
        with open('./extras/cases.json', 'w') as f:
            json.dump(cases, f, indent=4)
        
        # Load the config file and gets all the channel in ChannelsToLock key in a lockdown mode
        with open("config.json") as f:
            config = json.load(f)
        channels_to_lock = config["ChannelsToLock"]

        for channel_id in channels_to_lock:
            channel = ctx.guild.get_channel(int(channel_id))
            if channel is None:
                continue

            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

        # Sends a message on the announcement channel
        channel = self.bot.get_channel(announcement)
        embedAction = discord.Embed(description="**Attention** @everyone,\n\nLockdown status has been lifted.\nYou may now access to certain channel and features.\nWe thank you for your understanding and cooperation.\nWe promise to get back to you as soon as possible.\n\n- Management", color=0xf00ff00)
        await channel.send(embed=embedAction)
        
        # Log the moderation activity
        modlogs = self.bot.get_channel(int(modlogsID))
        embedLog = discord.Embed(title="Moderation Activity: Lockdown Lifted", color=0x00ff00, timestamp=datetime.now())
        embedLog.set_footer(text=f"Case ID: {case_number}")
        
        await modlogs.send(embed=embedLog)

async def setup(bot):
    await bot.add_cog(ModerationTools(bot))