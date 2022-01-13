import discord
from discord.ext import commands
from main import imgCrime, imgLost, imgRestrict
from api.compiler import Compiler



class Solve(commands.Cog):
    def __init__(self, bot: commands.Context) -> None:
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def run(self, ctx: commands.Context, *, msg):
        # trigger typing indicator
        await ctx.trigger_typing()

        languages = {'py', 'python', 'js', 'javascript'}

        # error handling
        message: list[str] = msg.splitlines()

        if '```' not in message[0] and '```' not in message[-1]:
            await ctx.reply( content='Make sure you add the code within `\`` code `\``' )
            raise commands.BadArgument

        if '```' == message[0]:
            await ctx.reply( content='please mention the language!' )
            raise commands.BadArgument

        if message[0][3:] not in languages:
            await ctx.reply( content='I don\'t know the above mentioned language 🥲\nAt the moment I know `python3` and `javascript` only. I\'ve still a lot to learn' )
            raise commands.BadArgument

        lang = message[0][3:]
        code = '\n'.join(message[1:-1])

        if message[-1] != '```':
            code += '\n' + message[-1].replace('```', '')

        result = Compiler(code, lang)
        send = result.run()

        # embed
        embed = discord.Embed( title='Ouput', description=f"""output of your code is as follow ```{send['output']}```""", color=0xFBBC04 )
        embed.add_field( name='Time', value=f"{send['cpuTime']} s")
        embed.add_field( name='Memory', value=f"{send['memory']} kb" )

        # reply
        await ctx.reply( embed=embed )

    
    @run.error
    async def run_error(self, ctx: commands.Context, error):
        # trigger typing indicator
        await ctx.trigger_typing()

        # code not formatted properly
        if isinstance(error, commands.BadArgument):
            # embed
            embed = discord.Embed( title='Wrong format', description='Make sure to pack the code with `\`` and don\'t forget to mention the language.', color=0xFBBC04 )
            embed.set_author( name=ctx.author.display_name, icon_url=ctx.author.avatar_url )
            embed.set_thumbnail( url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREdkKzEnffBZ0CI_n6Ief3-ft3OyONfEFIaQ&usqp=CAU" )

            embed.add_field( name='Command Library', value='Use `!help` command to view all of the commands.' )
            embed.set_image( url="https://lh3.googleusercontent.com/I22RdB47Sic_2lt8dVYwvDlyD9YohxuiMNQA8UuQHxM4_P5Bw6yr28ccsDzffxa-QvF4aKOYvVBhfB5RqM-7PEbkrbf61x4hUzSL4ljPFPj4i3zGH7wnAJa6N5xZCZRN7FHa-hjmxxr4t-P7DD9tl5Ixbn9XN5LgIGodWMwkCUc1ODIazqTJjFx2bO0eB_GKmD1cYQdEUlOj4AXVXEqJRkT4Nnxmu0U8RFZgSKq26MecLmpwNU6kE9xPkUNFZa3EWmJ108GrICN4LmoMDZPEJz8lnMqtSu0TmH7tDd0xUrUMjclx4YvKsCYmZnifbO_HQ7lr6p15yUyix1o4yjzp_IGP_9Eeq9gry0PFqVseuhMP0SUdDUwP1xYW7fe9Z71HRtXkPBMWoQyzEMqyS1b9O99MLf5lpg8wjR8X807MtJQn6CgLynv_SeYLsu9F_K6OvTyEzLawnwLFXGplEbYL61MCniyl7md9J-VPqTDZnfOFJmyYTDYGMot2p3TbdFWU3eeWJWeYwS0OlW2BuU1kcbpOemkZld9c_0BmJTcOWbvlgc2PcPlCLQ2qtTnSxFnfhmlIGh3TWGZv76nMIvKvXiACuHjYBEB3OlLhf0j0td6ecU7w-TPoTpCFvbjd6lAlCfxlYqsE36zIRlrkDM1kZDdO9xFFft3foD84ToR_BMW5IB3ObmiNBHGDR7GZr8_ZZBuK2VRN85pTy_ZQdUUrk2U=w400-h183-no?authuser=0" )

            # reply
            await ctx.reply( embed=embed )

        # missing code
        elif isinstance(error, commands.MissingRequiredArgument):
            # embed
            embed = discord.Embed( title='Code Missing!', description='You are missing few arguments. Make sure to pack the code within `\`` and don\'t forget to mention the language.', color=0xFBBC04 )
            embed.set_author( name=ctx.author.display_name, icon_url=ctx.author.avatar_url )

            embed.add_field( name='Command Library', value='Pass `!help` command to view all of the commands.' )
            embed.set_image( url="attachment://lost.jpg" )

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
    bot.add_cog(Solve(bot))
