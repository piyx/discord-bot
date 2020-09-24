import discord
from utils.rddit import Reddit
from discord.ext import commands


class Posts(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @commands.command()
    async def reddit(self, ctx, subreddit, category="hot"):
        '''Displays one post from the subreddit based on category'''
        rdt = Reddit(subreddit, category)
        data = rdt.get_post()
        if not data:
            embed = discord.Embed(
                title="Invalid subreddit or category!", color=0x4e7978)
        else:
            embed = discord.Embed(
                title=f"{data['name']}\n{data['title']}", description=f"{data['desc']}\n{data['url']}", color=0x4e7978)
            embed.set_image(url=data['url'])
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Posts(client))
