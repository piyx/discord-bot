import os
import pafy
import discord
from gettext import ngettext
from discord.utils import get
from youtube_dl import YoutubeDL
from discord.ext import commands
from discord import FFmpegPCMAudio
from utils.yt_url import YoutubeUrl
from utils.embeds import np_embed, q_embed
from utils.embeds import wcm, bcm, error, pause, resume, stop


class Music(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.path = "./music/"
        self.q = []
        self.voice = None
        self.current = None

    @commands.command()
    async def play(self, ctx, *, song_name):
        '''Plays song from first youtube search result'''
        voice_client = ctx.voice_client
        voice = ctx.author.voice
        if not voice:
            await ctx.send(f"{error} **`You need to be in a voice channel`**")
            return
        if not voice_client:
            await voice.channel.connect()

        self.voice = get(self.client.voice_clients, guild=ctx.guild)

        yt = YoutubeUrl(song_name)
        video_url = yt.get_video_url()
        data = yt.get_video_info(video_url)

        if not data:
            await ctx.send(f"{error} **`Song could not be found`**")
            return

        def download(url):
            video = pafy.new(url)
            if (song := "song.mp3") in os.listdir(self.path):
                os.remove(f"{self.path}{song}")
            try:
                video.getbestaudio().download(self.path)
            except Exception as e:
                return False

            for song in os.listdir(self.path):
                os.rename(f"{self.path}{song}", f"{self.path}song.mp3")
            return True

        def check_queue():
            if not self.q:
                self.current = None
                if os.listdir(self.path):
                    os.remove(f"{self.path}song.mp3")
                return
            os.remove(f"{self.path}song.mp3")
            self.current = self.q.pop(0)
            song = self.current['url']
            download(song)
            self.voice.play(FFmpegPCMAudio(f"{self.path}song.mp3"),
                            after=lambda x: check_queue())
            self.voice.source = discord.PCMVolumeTransformer(
                self.voice.source, volume=1.0)

        if not self.voice.is_playing():
            success = download(data['url'])
            if not success:
                await ctx.send(f"{error} **`Song cannot be streamed`**")
                return

            self.voice.play(FFmpegPCMAudio(f"{self.path}song.mp3"),
                            after=lambda x: check_queue())
            self.voice.source = discord.PCMVolumeTransformer(
                self.voice.source, volume=1.0)
            self.current = data
            embed = np_embed(ctx, self.current)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{bcm} **`Song has been added to queue`**")
            self.q.append(data)
            return

    @commands.command()
    async def pause(self, ctx):
        '''Pauses the song'''
        if self.voice and self.voice.is_playing():
            self.voice.pause()
            await ctx.send(f"`Music paused` {pause}")
        else:
            await ctx.send(f"{error} **`No song is being played`**")

    @commands.command()
    async def resume(self, ctx):
        '''Resumes the song'''
        if not self.voice:
            await ctx.send(f"{error} **`No song is being played`**")
        elif self.voice.is_paused():
            self.voice.resume()
            await ctx.send(f"{resume} **`Music resumed`**")
        else:
            await ctx.send(f"{error} **`Song is already being played`**")

    @commands.command()
    async def stop(self, ctx):
        '''Stops the song'''
        if self.voice and self.voice.is_playing():
            self.q.clear()
            self.voice.stop()
            await ctx.voice_client.disconnect()
            await ctx.send(f"`Music stopped` {stop}")
        else:
            await ctx.send(f"{error} **`No song is being played`**")

    @commands.command()
    async def np(self, ctx):
        '''Displays now playing song info'''
        if not self.current:
            await ctx.send(f"{error} **`No song is being played`**")
            return

        embed = np_embed(ctx, self.current)
        await ctx.send(embed=embed)

    @commands.command()
    async def queue(self, ctx):
        '''Displays the songs in queue'''
        if not self.q or not self.current:
            await ctx.send(f"{bcm} **`No songs queued`**")
            return

        embed = q_embed(ctx, self.current, self.q)
        await ctx.send(embed=embed)

    @commands.command()
    async def clear(self, ctx):
        '''Clears the queue'''
        if self.q:
            self.q.clear()
            await ctx.send(f"{wcm} **`Queue cleared`**")
        else:
            await ctx.send(f"{bcm} **`No songs queued`**")

    @commands.command()
    async def volume(self, ctx, volume: int):
        '''Sets the volume'''
        if 0 <= volume <= 100:
            self.voice.source.volume = volume/100
            await ctx.send(f"**`Volume set to {volume}`**")
            return
        await ctx.send(f"{error} **`Volume should be in range [0, 100]`**")

    @commands.command()
    async def skip(self, ctx):
        '''Skips the current song'''
        if self.voice and self.q:
            self.voice.stop()
            await ctx.send(f"{wcm} **`Music skipped`**")
        elif self.voice and not self.q:
            await ctx.send(f"{error} `Queue empty`")
        else:
            await ctx.send(f"{error} **`No song is being played`**")


def setup(client):
    client.add_cog(Music(client))
