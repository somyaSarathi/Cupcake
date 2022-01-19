import discord
import youtube_dl
import spotdl
from time import sleep
from discord.utils import get
from discord.ext import commands



class Music(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    
    @commands.command(aliases=['play', 'voice', 'vc'])
    @commands.guild_only()
    async def join(self, ctx: commands.Context):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        # checking if connected already
        if voice_client and voice_client.is_connected():
            await ctx.reply(f'I\'m already connected to {ctx.author.voice.channel.mention}')

        # if user not connected
        if ctx.author.voice is None:
            await ctx.reply(f'You\'re not in a voice channel')

        # getting user's voice channel
        channel = ctx.author.voice.channel

        # connecting to the voice channel
        await channel.connect()


    @commands.command(aliases=['disconnect'])
    @commands.guild_only()
    async def leave(self, ctx: commands.Context):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        # if connected to any voice channel then leave
        if voice_client and voice_client.is_connected():
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
