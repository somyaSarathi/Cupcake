import discord
import asyncio
from discord.ext import commands
from main import imgCount, imgCrime, imgLost, imgFetch



class Operation(commands.Cog):
    def __init__(self, bot: commands.Context) -> None:
        self.bot = bot

    
    #### clear message log ####
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, *, args=None):
        # delete all of the messages
        if args is None:
            await ctx.channel.purge()
            await asyncio.sleep(1.2)

        # delete specific number of messages
        else:
            num = int(eval(args))
            if num <= 0:
                raise commands.BadArgument

            await ctx.channel.purge(limit=num)
            await asyncio.sleep(1.2)


    @clear.error
    async def clear_error(self, ctx: commands.Context, error):
        # triggering typing instance
        await ctx.trigger_typing()

        # invalid airthmetic operation of conversion
        if isinstance(error, SyntaxError):
            # embed
            embed = discord.Embed( title='Not a valid number', description='Please pass an valid number.', color=0xFBBC04 )
            embed.set_author( name=ctx.author.display_name, icon_url=ctx.author.avatar_url )
            embed.set_image( url='attachment://count.jpg' )

            # reply
            await ctx.reply( file=imgCount, embed=embed )

        # for number below or equals to 0
        if isinstance(error, commands.BadArgument):
            # embed
            embed = discord.Embed( title='Not a valid number', description='Try any integer greater than 0', color=0xFBBC04 )
            embed.set_author( name=ctx.author.display_name, icon_url=ctx.author.avatar_url )
            embed.set_image( url='attachment://count.jpg' )

            # reply
            await ctx.reply( file=imgCount, embed=embed )

        # DM
        elif isinstance(error, commands.NoPrivateMessage):
            # embed
            embed = discord.Embed( title='DMs are restricted', description='Bot command on the DM are restricted' )
            embed.set_author( name=ctx.author.display_name, icon_url=ctx.author.avatar_url )

            embed.set_image( url='attachment://restrict.jpg' )

            # reply
            await ctx.reply( file=imgRestrict, embed=embed )

        
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(f"I'm sorry {ctx.author.mention} you don't have the permissions to delete the messages")


    #### ban member ####
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, message: str=None):
        # trigger typing instance
        await ctx.trigger_typing()

        # ban
        await member.send(f'you have been banned from the server for the following reason(s)\n{message}')
        await member.ban( reason=message )

        # reply
        await ctx.reply(f'{member.display_name} has been banned from the server')


    @ban.error
    async def ban_error(self, ctx: commands.Context, error):
        # triggering typing instance
        await ctx.trigger_typing()

        # error handling
        # permission
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(f'I\'m sorry {ctx.author.mention} you don\'t have the permission to ban the member\nYou can request the admins')

        # member mention
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed( title='Tag the member', description='Please tag the member you want to ban from the server')
            embed.set_author( name=ctx.author.display_name, icon_url=ctx.author.avatar_url )
            embed.set_image( url='attachment://lost.jpg' )

            # reply
            await ctx.reply( file=imgLost, embed=embed )

        # member doesn't exist
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed( title='Member doesn\'t exist', description='The mentioned member is not in the server' )
            embed.set_author( name=ctx.author.display_name, icon_url=ctx.author.avatar_url )
            embed.set_image( url='attachment://lost.jpg' )

            # reply
            await ctx.reply( file=imgLost, embed=embed )

        # DM
        elif isinstance(error, commands.NoPrivateMessage):
            # embed
            embed = discord.Embed( title='DMs are restricted', description='Bot command on the DM are restricted' )
            embed.set_author( name=ctx.author.display_name, icon_url=ctx.author.avatar_url )

            embed.set_image( url='attachment://restrict.jpg' )

            # reply
            await ctx.reply( file=imgRestrict, embed=embed )

        else:
            embed = discord.Embed( title='oops! I may have chewed up the power cord.', description='Looks like I did something missrable', color=0xFBBC04 )
            embed.set_image( url='attachment://crime.jpg' )

            # reply
            await ctx.reply( file=imgCrime, embed=embed )


    #### kick member ####
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, message):
        # trigger typing
        await ctx.trigger_typing()

        # kick
        await member.send(f'you have been kicked out of the server for the following reason(s)\n{message}')
        await member.kick( reason=message )

        # reply
        await ctx.reply(f'{member.display_name} has been kicked out of the server')


    @kick.error
    async def kick_error(self, ctx: commands.Context, error):
        # triggering typing instance
        await ctx.trigger_typing()

        # error handling
        # permission
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(f'I\'m sorry {ctx.author.mention} you don\'t have the permission to ban the member\nYou can request the admins')

        # member mention
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed( title='Tag the member', description='Please tag the member you wish to kick from the server')
            embed.set_author( name=ctx.author.display_name, icon_url=ctx.author.avatar_url )
            embed.set_image( url='attachment://fetching.jpg' )

            # reply
            await ctx.reply( file=imgFetch, embed=embed )

        # member doesn't exist
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed( title='Member doesn\'t exist', description='The mentioned member is not in the server' )
            embed.set_author( name=ctx.author.display_name, icon_url=ctx.author.avatar_url )
            embed.set_image( url='attachment://lost.jpg' )

            # reply
            await ctx.reply( file=imgLost, embed=embed )

        # DM
        elif isinstance(error, commands.NoPrivateMessage):
            # embed
            embed = discord.Embed( title='DMs are restricted', description='Bot command on the DM are restricted' )
            embed.set_author( name=ctx.author.display_name, icon_url=ctx.author.avatar_url )

            embed.set_image( url='attachment://restrict.jpg' )

            # reply
            await ctx.reply( file=imgRestrict, embed=embed )

        else:
            embed = discord.Embed( title='oops! I may have chewed up the power cord.', description='Looks like I did something missrable', color=0xFBBC04 )
            embed.set_image( url='attachment://crime.jpg' )

            # reply
            await ctx.reply( file=imgCrime, embed=embed )



def setup(bot: commands.Bot):
    bot.add_cog(Operation(bot))
