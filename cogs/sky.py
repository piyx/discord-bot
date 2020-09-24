import discord
from utils.nasa import apod
from utils.weather import Weather
from discord.ext import commands
from utils.secret import WEATHER_API


class Sky(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @commands.command(aliases=['current', 'weth'])
    async def weather(self, ctx, city):
        '''Displays the city's weather'''
        weather = Weather(WEATHER_API, city)
        data = weather.current_weather()

        if not data:
            embed = discord.Embed(
                title=f"{city} is not a city lol!", color=0x782322)
            await ctx.send(embed=embed)
            return

        # Location
        embedVar = discord.Embed(
            title=f"{data['location']}", color=0x4e7978)
        embedVar.set_thumbnail(url=data['icon'])

        # Weather
        embedVar.add_field(
            name="Weather", value=data['desc'], inline=False)

        # Numbers
        embedVar.add_field(
            name="Current", value=data['curr'], inline=False)
        embedVar.add_field(
            name="Feels Like", value=data['feels'], inline=False)
        embedVar.add_field(
            name="Wind Speed", value=data['wind'], inline=False)
        embedVar.add_field(
            name="Pressure", value=data['pressure'], inline=False)
        await ctx.send(embed=embedVar)

    @commands.command(aliases=['astronomy', 'sun', 'moon'])
    async def astro(self, ctx, city):
        '''Displays the city's astronomy information'''
        astro = Weather(WEATHER_API, city)
        data = astro.astronomy()

        if not data:
            embed = discord.Embed(
                title=f"{city} is not a city lol!", color=0x782322)
            await ctx.send(embed=embed)
            return

        embedVar = discord.Embed(
            title=f"Astronomy in {city}", color=0x4e7978)

        embedVar.add_field(
            name="Sunrise", value=data['sunrise'], inline=False)
        embedVar.add_field(
            name="Sunset", value=data['sunset'], inline=False)
        embedVar.add_field(
            name="Moonrise", value=data['moonrise'], inline=False)
        embedVar.add_field(
            name="Moonset", value=data['moonset'], inline=False)

        await ctx.send(embed=embedVar)

    @commands.command(aliases=['space', 'apod'])
    async def nasa(self, ctx):
        '''Displays astronomy picture of the day'''
        data = apod()
        if data:
            info, img = data
            embed = discord.Embed(
                title=f"Astronomy picture of day", description=f"{info}", color=0x36AFDF)
            embed.set_image(url=img)
        else:
            embed = discord.Embed(
                title=f"Error", color=0x36AFDF)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Sky(client))
