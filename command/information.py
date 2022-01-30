import discord
from api.weather import weather as wthr
from discord import Embed
from discord.ext import commands
from main import imgMap, imgNap, imgHack, imgCrime
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
            embed.set_image( url='attachment://crime.jpg' )
            print(error)

            # reply
            await ctx.reply( file=imgCrime, embed=embed )

    
    @commands.command()
    @commands.guild_only()
    async def about(self, ctx: commands.Context, member: discord.Member=None):
        if member is None:
            member = ctx.author

        if not isinstance(member, discord.Member):
            raise commands.BadArgument

        # triggering typing instance
        await ctx.trigger_typing()

        roles = [ role for role in member.roles ]
        
        # embed
        embed = Embed( title=f'{member.name}#{member.discriminator}', description='User Information', color=member.color )

        embed.set_author( name=ctx.author.display_name, icon_url=ctx.author.avatar_url )

        embed.set_thumbnail( url=member.avatar_url )

        # information
        embed.add_field(name='User ID:', value=member.id, inline=False)

        embed.add_field(name='Nickname:', value=member.display_name)
        embed.add_field(name='Top role:', value=member.top_role.mention)
        embed.add_field(name='Status:', value=str(member.status))

        embed.add_field(name=f'Roles {len(roles)}:', value=' '.join([role.mention for role in roles]), inline=False)

        # add badges
        embed.add_field(name='Badges: ', value='', inline=False)

        embed.add_field(name='Created at:', value=f"`member.created_at.strftime('%#d %B %Y, %-H:%M UTC')`", inline=False)

        embed.add_field(name='Joined at:', value=f"`member.joined_at.strftime('%#d %B %Y, %-H:%M UTC')`", inline=False)

        # add activity
        
        embed.add_field(name='Bot?', value=member.bot)

        # reply
        await ctx.reply( embed=embed )

    
    @about.error
    async def about_error(self, ctx: commands.Context, error):
        # triggering typing instance
        await ctx.trigger_typing()
        print(error)

        if isinstance(error, commands.BadArgument):
            # embed
            embed = Embed( title='Mention the member', description='Tag the member you want to interogate. e.g. @cupcake', color=0xFBBC04 )
            embed.set_author( name=ctx.author.display_name, icon_url=ctx.author.avatar_url )

            embed.set_image(url='attachment://hack.gif')
            
            # reply
            await ctx.reply( file=imgHack, embed=embed )

        else:
            # embed
            embed = discord.Embed( title='Something went wrong', description='It\'s nap time huumman. Will figure it out later...', color=0xFBBC04 )
            embed.set_author( name=ctx.author.display_name, icon_url=ctx.author.avatar_url )
            embed.set_image( url='attachment://nap.png' )

            # reply
            await ctx.reply( file=imgNap, embed=embed )

    
    @commands.command()
    @commands.guild_only()
    async def server(self, ctx: commands.Context):
        # triggering typing indicator
        await ctx.trigger_typing()

        roles = ctx.message.guild.roles[1:]
        online = 0
        for user in ctx.guild.members:
            if user.status != discord.Status.offline:
                online += 1

        features = ctx.guild.features

        # embed
        embed = Embed( title=f'{ctx.message.guild.name}', description='Server Information', color=0xFBBC04)
        embed.set_author( name=ctx.author.display_name, icon_url=ctx.author.avatar_url )
        embed.set_thumbnail( url=ctx.guild.icon_url )
        embed.set_image( url=ctx.guild.banner_url )

        embed.add_field( name='Owner: ', value=ctx.guild.owner.mention )
        embed.add_field( name='Members: ', value=len(ctx.guild.members) )
        embed.add_field( name='Online: ', value=online )

        embed.add_field( name=f'Roles ({len(ctx.message.guild.roles)-1}): ', value=' '.join([role.mention for role in roles]), inline=False )

        embed.add_field( name='Partnered?', value=len(features)>4 )
        embed.add_field( name='Verified?', value=len(features)>3 )
        embed.add_field( name='Boost:', value=ctx.guild.premium_tier )

        
        embed.add_field( name='Emojis:', value=len(ctx.guild.emojis) )
        embed.add_field( name='categories', value=len(ctx.guild.categories) )
        embed.add_field( name='Language:', value=ctx.guild.preferred_locale )
        
        embed.add_field( name='Location:', value=ctx.guild.region )

        embed.add_field( name='Creation date:', value=ctx.guild.created_at.strftime('%#d %B %Y, %-H:%M UTC'), inline=False )
        embed.add_field( name='Channels:', value=f'Text: {len(ctx.guild.text_channels)} | voice: {len(ctx.guild.voice_channels)} | stage: {len(ctx.guild.stage_channels)}', inline=False )

        # reply
        await ctx.reply( embed=embed )

    @server.error
    async def server_error(self, ctx: commands.Context, error):
        # triggering typing instance
        await ctx.trigger_typing()

        # embed
        embed = discord.Embed( title='Something went wrong', description='It\'s nap time huumman. Will figure it out later...', color=0xFBBC04 )
        embed.set_author( name=ctx.author.display_name, icon_url=ctx.author.avatar_url )
        embed.set_image( url='attachment://nap.png' )

        # reply
        await ctx.reply( file=imgNap, embed=embed )



def setup(bot: commands.Bot):
    bot.add_cog(Information(bot))