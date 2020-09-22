import discord
from discord.ext import tasks
from discord.ext import commands


class Discord(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.status = "Kupla: Valentine"

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(self.status))
        print("Bot is ready!")

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(
            title=f'Pong! {round(self.client.latency*1000)}ms', color=0x457832)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member} has joined the best server lol.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"{member} has rage quit.")

    async def change_status(self):
        pass

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def join(self, ctx):
        voice = ctx.message.author.voice
        voice_client = ctx.voice_client
        if voice_client:
            await ctx.send(f":white_check_mark: **Already connected to voice channel!**")
        elif voice:  # Check if member is connected to voice channel
            await voice.channel.connect()
            await ctx.send(f":white_check_mark: **Joined {ctx.author.voice.channel}**")
        else:
            await ctx.send(":x: **You need to be in a voice channel!**")

    @commands.command()
    async def leave(self, ctx):
        voice_client = ctx.voice_client
        if not voice_client:  # Check if bot instance is connected to voice channel
            await ctx.send(":x: **You need to add me to voice channel first!**")
        else:
            await ctx.voice_client.disconnect()
            await ctx.send(f":white_check_mark: **Left {ctx.author.voice.channel}**")


def setup(client):
    client.add_cog(Discord(client))
