import discord
from discord.ext import commands
# import youtube_dl
from os import system



class Music(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    
    @commands.command()
    async def join(self, ctx: commands.Context):
        channel = ctx.author.voice.channel
        await channel.connect()


    @commands.command()
    async def leave(self, ctx: commands.Context):
        await ctx.voice_client.disconnect()


    @join.error
    async def join_error(self, ctx: commands.Context, error):
        print(error)
        pass


    @leave.error
    async def leave_error(self, ctx: commands.Context, error):
        pass



def setup(bot: commands.Bot) -> None:
    bot.add_cog(Music(bot))
