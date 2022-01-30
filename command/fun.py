import discord
from random import choice
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.coin = {
            'head': discord.File('./img/head.png', filename='head.png'),
            'tail': discord.File('./img/tail.png', filename='tail.png')
        }


    @commands.command()
    @commands.guild_only()
    async def flip(self, ctx: commands.Context):
        result = choice(['head', 'tail'])

        # trigger typing
        await ctx.trigger_typing()

        # embed
        embed = discord.Embed(title=result.capitalize()+'s', description='What were you expecting?')
        embed.set_author( name=ctx.author.display_name, icon_url=ctx.author.avatar_url )
        embed.set_thumbnail( url=f'attachment://{result}.png' )

        # reply
        await ctx.send( file=self.coin[result], embed=embed )



def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))