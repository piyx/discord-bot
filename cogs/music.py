import os
import pafy
import discord
from discord.utils import get
from youtube_dl import YoutubeDL
from discord.ext import commands
from utils.youtube import Youtube
from discord import FFmpegPCMAudio


class Music(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.path = "./music/"
        self.q = []
        self.voice = None
        self.current = None

    @commands.command()
    async def play(self, ctx, *, song_name):
        self.voice = get(self.client.voice_clients, guild=ctx.guild)
        yt = Youtube(song_name)
        data = yt.search()
        if not data:
            await ctx.send(f":x: **{song_name} could not be found!**")
            return

        def download(url):
            video = pafy.new(url)
            if song := f"{self.path}song.mp3" in os.listdir(self.path):
                os.remove(song)
            video.getbestaudio().download(self.path)
            for song in os.listdir(self.path):
                os.rename(f"{self.path}{song}", f"{self.path}song.mp3")

        def check_queue():
            if not self.q:
                if os.listdir(self.path):
                    os.remove(f"{self.path}song.mp3")
                return
            os.remove(f"{self.path}song.mp3")
            self.current = self.q.pop(0)
            song = self.current['url']
            download(song)
            self.voice.play(FFmpegPCMAudio(f"{self.path}song.mp3"),
                            after=lambda x: check_queue())

        async def now_playing():
            embed = discord.Embed(title="Now playing...", color=0xffffff)
            embed.set_thumbnail(url=data['thumbnail'])
            embed.add_field(name=f"{data['title']}", value=f"{data['url']}")
            await ctx.send(embed=embed)

        if not self.voice.is_playing():
            download(data['url'])
            self.voice.play(FFmpegPCMAudio(f"{self.path}song.mp3"),
                            after=lambda x: check_queue())
            self.current = data
            await now_playing()
        else:
            await ctx.send(f":ballot_box_with_check: **The song has been added to queue**")
            self.q.append(data)
            return

    @commands.command()
    async def pause(self, ctx):
        if self.voice and self.voice.is_playing():
            self.voice.pause()
            await ctx.send("**Music paused** :pause_button:")
        else:
            await ctx.send(":x: **No song is played!**")

    @commands.command()
    async def resume(self, ctx):
        if not self.voice:
            await ctx.send(":x: **No song is played!**")
        elif self.voice.is_paused():
            self.voice.resume()
            await ctx.send("**Music resumed** :play_pause:")
        else:
            await ctx.send(":x: **Song is already being played!**")

    @commands.command()
    async def stop(self, ctx):
        if self.voice and self.voice.is_playing():
            self.voice.stop()
            await ctx.send("**Music stopped** :octagonal_sign:")
        else:
            await ctx.send(":x: **No song is played!**")

    @commands.command()
    async def queue(self, ctx):
        if not self.q:
            await ctx.send(f"**No songs queued.**")

    @commands.command()
    async def np(self, ctx):
        if not self.current:
            await ctx.send(":x: **No song is being played!**")
            return
        embed = discord.Embed(title="Now playing...", color=0xffffff)
        embed.set_thumbnail(url=self.current['thumbnail'])
        embed.add_field(
            name=f"{self.current['title']}", value=f"{self.current['url']}")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Music(client))
