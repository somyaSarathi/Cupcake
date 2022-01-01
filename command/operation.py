import discord
import asyncio
from discord.ext import commands
from main import imgCount
import logging



class Operation(commands.Cog):
    def __init__(self, bot: commands.Context) -> None:
        self.bot = bot

    
    @commands.command()
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
        ctx.trigger_typing()

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

        
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(f"I'm sorry {ctx.author.mention} you don't have the permissions to delete the messages")



def setup(bot: commands.Bot):
    bot.add_cog(Operation(bot))
