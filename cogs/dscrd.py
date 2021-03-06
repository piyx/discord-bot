import discord
from discord.ext import tasks
from discord.utils import get
from discord.ext import commands
from utils.embeds import wcm, bcm, error


class Discord(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.status = "1101100"

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
    async def delete(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def join(self, ctx):
        if not ctx.author.voice:
            return await ctx.send(f"{error} **`You need to be in a voice channel`**")

        channel = ctx.author.voice.channel
        voice_client = ctx.voice_client

        if voice_client and voice_client.is_playing():
            return await ctx.send(f"{error} **`Can't use this command when playing music in a channel!`**")

        if voice_client:
            await ctx.send(f"{wcm} **`Joined {channel}`**")
            return await ctx.voice_client.move_to(channel)

        await channel.connect()
        await ctx.send(f"{wcm} **`Joined {channel}`**")

    @commands.command(aliases=['disconnect'])
    async def leave(self, ctx):
        voice_client = ctx.voice_client
        if not voice_client:  # Check if bot instance is connected to voice channel
            await ctx.send(f"{error} **`Not in any channel`**")
        else:
            await ctx.send(f"{wcm} **`Left {voice_client.channel}`**")
            await ctx.voice_client.disconnect()


def setup(client):
    client.add_cog(Discord(client))
