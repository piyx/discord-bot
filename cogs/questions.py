import discord
import random
from discord.ext import commands


class Question(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @commands.command(aliases=['roll'])
    async def dice(self, ctx):
        embed = discord.Embed(
            title=f":game_die: You rolled {random.randint(1, 6)}", color=0x00ff10)
        await ctx.send(embed=embed)

    @commands.command(aliases=['flip'])
    async def coin(self, ctx):
        embed = discord.Embed(
            title=f"You flipped {random.choice(['Heads', 'Tails'])}", color=0x3781ff)
        await ctx.send(embed=embed)

    @commands.command(aliases=['owner', 'creator'])
    async def boss(self, ctx):  # passing context
        embed = discord.Embed(
            title=f'Nyx made me! He is my boss', color=0x457832)
        await ctx.send(embed=embed)

    @commands.command(aliases=['8ball', '8b', 'question'])
    async def ask(self, ctx, *, question):
        responses = ["It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely",
                     "You may rely on it", "As I see it, yes", "Most Likely", "Outlook Good",
                     "Yes", "Signs point to yes", "Reply hazy, try again", "Ask again later",
                     "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
                     "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very Doubtful"]
        embed = discord.Embed(
            title=f'Question: {question}', description=f"Answer: {random.choice(responses)}", color=0x36AFDF)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Question(client))
