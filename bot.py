import discord
from discord.ext import commands, tasks
from get_weather import show
import random
from rddit import rddit
from itertools import cycle
from secret import TOKEN

# Discord token
token = TOKEN

client = commands.Bot(command_prefix='.')
status = cycle(['Happy', 'Sad', 'Angry'])


@client.event
async def on_ready():
    change_status.start()
    print("Bot is ready!")


@client.event
async def on_member_join(member):
    print(f"{member} has joined the best server lol.")


@client.event
async def on_member_remove(member):
    print(f"{member} has rage quit.")


@client.command()
async def ping(ctx):  # passing context
    embed = discord.Embed(
        title=f'Pong! {round(client.latency*1000)}ms', color=0x457832)
    await ctx.send(embed=embed)

@client.command(aliases=['owner', 'creator'])
async def boss(ctx):  # passing context
    embed = discord.Embed(
        title=f'Nyx made me! He is my boss', color=0x457832)
    await ctx.send(embed=embed)


@client.command(aliases=['weth', 'Weather'])
async def weather(ctx, city):
    ds = show(city)
    if 'message' in ds:
        embed = discord.Embed(
            title=f"{city} is not a city lol!", color=0x782322)
        await ctx.send(embed=embed)
        return
    embedVar = discord.Embed(
        title=f"Weather in {city}", color=0x4e7978)
    embedVar.add_field(name="Weather", value=ds['Weather'], inline=False)
    embedVar.add_field(name="Description",
                       value=ds['Description'], inline=False)
    embedVar.add_field(name="Min", value=ds['Min temp'], inline=False)
    embedVar.add_field(name="Max", value=ds['Max temp'], inline=False)
    embedVar.add_field(name="Sunrise", value=ds['Sunrise'], inline=False)
    embedVar.add_field(name="Sunset", value=ds['Sunset'], inline=False)
    await ctx.send(embed=embedVar)


@client.command(aliases=['8ball', '8b', 'question'])
async def ask(ctx, *, question):
    responses = ["It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely",
                 "You may rely on it", "As I see it, yes", "Most Likely", "Outlook Good",
                 "Yes", "Signs point to yes", "Reply hazy, try again", "Ask again later",
                 "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
                 "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very Doubtful"]
    embed = discord.Embed(
        title=f'Question: {question}', description=f"Answer: {random.choice(responses)}", color=0x36AFDF)
    await ctx.send(embed=embed)


@client.command()
async def reddit(ctx, subreddit):
    data = rddit(subreddit)
    embedVar = discord.Embed(
        title=f"{data['name']}\n{data['title']}", description=f"{data['desc']}\n{data['url']}", color=0x4e7978)
    embedVar.set_image(url=data['url'])
    await ctx.send(embed=embedVar)


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Argument missing!")


@client.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    pass


client.run(token)
