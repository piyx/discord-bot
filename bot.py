import os
import discord
from utils.secret import TOKEN
from discord.utils import get
from youtube_dl import YoutubeDL
from discord.ext import commands
from discord import FFmpegPCMAudio

# Discord token
token = TOKEN
client = commands.Bot(command_prefix='.')


@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    try:
        client.load_extension(f"cogs.{extension}")
        await ctx.send(f":white_check_mark: cogs.{extension} has been loaded")
    except Exception as e:
        await ctx.send(f":x: **{e}**")


@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    try:
        client.unload_extension(f"cogs.{extension}")
        await ctx.send(f":white_check_mark: cogs.{extension} has been unloaded")
    except Exception as e:
        await ctx.send(f":x: **{e}**")


@client.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    try:
        client.unload_extension(f"cogs.{extension}")
        client.load_extension(f"cogs.{extension}")
        await ctx.send(f":white_check_mark: **cogs.{extension} has been reloaded**")
    except Exception as e:
        await ctx.send(f":x: **{e}**")


# Load all cog files
for filename in os.listdir('./cogs'):
    if filename.endswith('py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(":x:**Argument missing!**")
    else:
        print(error)

client.run(token)
