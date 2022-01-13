import discord
import youtube_dl
from discord.utils import get
from discord.ext import commands



class Music(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    
    @commands.command()
    @commands.guild_only()
    async def join(self, ctx: commands.Context):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_connected():
            await ctx.reply(f'I\'m already connected to {ctx.author.voice.channel.mention}')

        # getting user's voice channel
        channel = ctx.author.voice.channel

        # connecting to the voice channel
        await channel.connect()


    @commands.command()
    async def leave(self, ctx: commands.Context):
        await ctx.voice_client.disconnect()


    @join.error
    async def join_error(self, ctx: commands.Context, error):
        # AttributeError
        pass


    @leave.error
    async def leave_error(self, ctx: commands.Context, error):
        pass



def setup(bot: commands.Bot) -> None:
    bot.add_cog(Music(bot))
