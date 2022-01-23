import discord
from api.weather import weather as wthr
from discord import Embed
from discord.ext import commands
from main import imgMap
from timezonefinder import TimezoneFinder

obj = TimezoneFinder()



class Information(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.timezone = {}


    @commands.command()
    @commands.guild_only()
    async def weather(self, ctx: commands.Context, city: str):
        data = wthr(city)

        try:
            if data['message'] == 'city not found':
                raise commands.BadArgument
        except KeyError:
            pass

        # triggering typing instance
        await ctx.trigger_typing()

        # embed
        embed = Embed( title=f"{data['name']}, {data['sys']['country']} Weather Report", description=f"{data['weather'][0]['description'].capitalize()}", color=0xFBBC04 )
        embed.set_author( name=ctx.author.display_name, icon_url=ctx.author.avatar_url )

        embed.add_field( name='Unit', value=f"C", inline=True )
        embed.add_field( name='Temperature', value=f"{data['main']['temp']}", inline=True )
        embed.add_field( name='Humidity', value=f"{data['main']['humidity']}", inline=True )

        embed.add_field( name='Wind', value=f"{data['wind']['speed']} m/s", inline=True )
        embed.add_field( name='Feels Like', value=f"{data['main']['feels_like']}", inline=True )
        embed.add_field( name='Timezone', value=f"{obj.timezone_at(lng=data['coord']['lon'], lat=data['coord']['lat'])}", inline=True )

        # reply
        await ctx.reply(embed=embed)


    @weather.error
    async def weather_error(self, ctx: commands.Context, error):
        # triggering typing instance
        await ctx.trigger_typing()

        if isinstance(error, commands.MissingRequiredArgument):
            # embed
            embed = Embed(title='Provide location', description='Please mention a city name📍', color=0xFBBC04 )
            embed.set_author( name=ctx.author.display_name, icon_url=ctx.author.avatar_url )

            embed.set_image(url='attachment://map.jpg')

            # reply
            await ctx.reply(file=imgMap, embed=embed)

        elif isinstance(error, commands.BadArgument):
            # embed
            embed = Embed( title='Invalid Location', description='Please provide a valid city name📍', color=0xFBBC04 )
            embed.set_author( name=ctx.author.display_name, icon_url=ctx.author.avatar_url )

            embed.set_image(url='attachment://map.jpg')

            # reply
            await ctx.reply(file=imgMap, embed=embed)

        else:
            embed = discord.Embed( title='oops! I may have chewed up the power cord.', description='Looks like I did something missrable', color=0xFBBC04 )
            # embed.set_image( url='attachment://crime.jpg' )
            print(error)

            # reply
            await ctx.reply( embed=embed )



def setup(bot: commands.Bot):
    bot.add_cog(Information(bot))