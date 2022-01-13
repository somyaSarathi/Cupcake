import os
import sys
import discord
import logging
from discord.embeds import Embed
from discord.ext import commands
from dotenv import load_dotenv


# logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='./log/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# gateway intents
intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.reactions = True
intents.members = True


# load data from .env file
load_dotenv()
TOKEN: str = os.getenv('TOKEN')


# bot prefix
bot = commands.Bot(command_prefix='!', description='Good Boy Cupcake!', intents=intents)

# loading images
imgProfile  = discord.File('./img/cupcake.png' , filename='cupcake.png')
imgFetch    = discord.File('./img/fetching.jpg', filename='fetching.jpg')
imgBook     = discord.File('./img/book.jpg'    , filename='book.jpg')
imgChew     = discord.File('./img/chew.jpg'    , filename='chew.jpg')
imgCrime    = discord.File('./img/crime.jpg'   , filename='crime.jpg')
imgLost     = discord.File('./img/lost.jpg'    , filename='lost.jpg')
imgFormat   = discord.File('./img/format.png'  , filename='format.png')
imgCount    = discord.File('./img/count.jpg'   , filename='count.jpg')
imgRestrict = discord.File('./img/restrict.jpg', filename='restrict.jpg')



class MyClient(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        '''
            prints message on the console after connecting.
        '''
        print(f'[CONNECTED] connected as {self.bot.user.name} successfully')
        print(f'user id: {self.bot.user.id}', end = '\n\n')


    @commands.Cog.listener()
    async def on_resumed(self):
        '''
            prints message on the console after reconnecting.
        '''
        print(f'[RECONNCETED] reconnected as {self.user.name} successfully!')
        print(f'user id: {self.bot.user.id}', end = '\n\n')


    @commands.Cog.listener()
    async def help(self, ctx: commands.Context):
        '''
            Replies with list of bot commands.
        '''
        pass


    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        '''
            informs user if a wrong command is passed.
        '''
        if isinstance(error, commands.errors.CommandNotFound):
            # triggering typing indicator
            await ctx.trigger_typing()

            # embed
            embed = discord.Embed( title='Command doesn\'t exists', description='I\'ve no idea what you want.', color=0xFBBC04 )
            embed.set_author( name=ctx.author.display_name, icon_url=ctx.author.avatar_url )
            embed.set_image( url='attachment://book.jpg' )

            # reply
            await ctx.reply(file=imgBook, embed=embed)



if __name__ == '__main__':
    # Load extention
    print('\nloading extention(s)...')

    for filename in os.listdir('./command'):
        if filename.endswith('.py'):
            bot.load_extension(f'command.{filename[: -3]}')
            print(f'  ✔️ Loaded {filename}')

    print('✅ Extention(s) loaded successfully!\n')
    
    # client
    bot.add_cog(MyClient(bot))
    bot.run(TOKEN)
