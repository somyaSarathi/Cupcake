import discord
from discord.utils import get
from discord.ext import commands
from youtube_dl import YoutubeDL


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        self.YDL_OPTINOS = {
            'format': 'bestaudio/best',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'
        }


    @commands.command()
    @commands.guild_only()
    async def join(self, ctx: commands.Context):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        # user not in a vc
        if ctx.author.voice is None:
            await ctx.trigger_typing()
            await ctx.reply('You are not in any voice channel')
        
        #  already connected to a vc
        elif voice_client and voice_client.is_connected():
            await ctx.trigger_typing()
            await ctx.reply(f'Already streaming! Join the party at {voice_client.channel.mention}')
        
        # connecting to the vc
        else:
            channel = ctx.author.voice.channel
            await channel.connect()

        # playing music
        await ctx.invoke(self.bot.get_command('play'))


    @commands.command()
    @commands.guild_only()
    async def leave(self, ctx: commands.Context):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_connected():
            await ctx.voice_client.disconnect()


    @commands.command()
    @commands.guild_only()
    async def play(self, ctx: commands.Context, url='https://www.youtube.com/watch?v=gnZImHvA0ME'):
        # stop playing
        ctx.voice_client.stop()

        vc = ctx.voice_client
        with YoutubeDL(self.YDL_OPTINOS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **self.FFMPEG_OPTIONS)
            vc.play(source)


def setup(bot: commands.Bot):
    bot.add_cog(Music(bot))
