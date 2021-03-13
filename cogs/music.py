import os
import pafy
import discord
from gettext import ngettext
from discord.utils import get
from collections import deque
from youtube_dl import YoutubeDL
from discord.ext import commands
from discord import FFmpegPCMAudio
from utils.yt_url import YoutubeUrl
from utils.embeds import np_embed, q_embed
from collections import defaultdict
from utils.embeds import wcm, bcm, error, pause, resume, stop


# Note: mp = music_player

'''
This music_rw.py is a rewrite of music.py.
This version supports multiple instances of bot music players.
'''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'verbose': True,
    'forceipv4': True,
    'cookies': True
}

ffmpeg_options = {
    'options': '-vn'
}


ytdl = YoutubeDL(ytdl_format_options)


class NoMusicPlayingException(Exception):
    pass


class MusicPlayer:
    def __init__(self, player, current):
        self.player = player
        self.current = current
        self.q = deque([])


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.players = {}
        self.path = "./media/"

    @commands.command()
    async def play(self, ctx, *, song_name):
        '''Plays song from first youtube search result'''

        # Extract the song info
        yt = YoutubeUrl(song_name)
        video_url = yt.get_video_url()
        data = yt.get_video_info(video_url)

        if not data:
            await ctx.send(f"{error} **`Song could not be found`**")
            return

        # Add music player to players
        server = ctx.guild.id
        voice = get(self.client.voice_clients, guild=ctx.guild)
        print(voice)
        if server not in self.players:
            self.players[server] = MusicPlayer(voice, data)

        print(self.players)

        # Music player
        mp = self.players[server]
        print(mp)
        folder = f"{self.path}{server}/"
        song = "song.mp3"

        # Func to Download the song
        def download(url):
            # Make folder
            if str(server) not in os.listdir(self.path):
                os.mkdir(folder)

            # Remove existing song
            for item in os.listdir(folder):
                os.remove(folder+item)

            # Download song
            try:
                ytdl_format_options['outtmpl'] = folder+song
                with YoutubeDL(ytdl_format_options) as ydl:
                    ydl.download([url])
            except Exception as e:
                return False
            return True

        def check_queue():
            # If q is empty, delete song and folder and the player
            if not mp.q:
                mp.current = None
                if os.listdir(folder):
                    os.remove(folder+song)
                    os.rmdir(folder)
                    del self.players[server]
                return

            # If q is not empty, remove song and download next
            os.remove(folder+song)
            mp.current = mp.q.popleft()
            download(mp.current['url'])
            mp.player.play(FFmpegPCMAudio(folder+song),
                           after=lambda x: check_queue())
            mp.player.source = discord.PCMVolumeTransformer(
                mp.player.source, volume=1.0)

        # If song is not playingm download it and play it
        if not mp.player.is_playing():
            async with ctx.typing():
                sucess = download(mp.current['url'])

                if not sucess:
                    return await ctx.send(f"{error} **`Song cannot be streamed`**")

                mp.player.play(FFmpegPCMAudio(folder+song),
                               after=lambda x: check_queue())
                mp.player.source = discord.PCMVolumeTransformer(
                    mp.player.source, volume=1.0)

            print(os.listdir(self.path))

            embed = np_embed(ctx, mp.current)
            return await ctx.send(embed=embed)

        # If song is already playing, add song to queue
        await ctx.send(f"{bcm} **`Song has been added to queue`**")
        mp.q.append(data)

    @commands.command()
    async def pause(self, ctx):
        '''Pauses the song'''
        mp = self.players.get(ctx.guild.id, None)
        mp.player.pause()
        await ctx.send(f"`Music paused` {pause}")

    @commands.command()
    async def resume(self, ctx):
        '''Resumes the song'''
        mp = self.players.get(ctx.guild.id, None)
        if not mp:
            return await ctx.send(f"{error} **`No song is being played`**")

        elif mp and mp.player.is_paused():
            mp.player.resume()
            return await ctx.send(f"{resume} **`Music resumed`**")

        return await ctx.send(f"{error} **`Song is already being played`**")

    @commands.command()
    async def stop(self, ctx):
        '''Stops the song'''
        mp = self.players.get(ctx.guild.id, None)
        mp.q.clear()
        mp.player.stop()
        await ctx.voice_client.disconnect()
        await ctx.send(f"`Music stopped` {stop}")

    @commands.command()
    async def np(self, ctx):
        '''Displays the now playing song info'''
        mp = self.players.get(ctx.guild.id, None)
        embed = np_embed(ctx, mp.current)
        return await ctx.send(embed=embed)

    @commands.command()
    async def queue(self, ctx):
        mp = self.players.get(ctx.guild.id, None)
        embed = q_embed(ctx, mp.current, mp.q)
        return await ctx.send(embed=embed)

    @commands.command()
    async def clear(self, ctx):
        '''Clears the queue'''
        mp = self.players.get(ctx.guild.id, None)
        if mp.q:
            mp.q.clear()
            return await ctx.send(f"{wcm} **`Queue cleared`**")

        return await ctx.send(f"{bcm} **`No songs queued`**")

    @commands.command()
    async def volume(self, ctx, volume: int):
        '''Sets the volume'''
        mp = self.players.get(ctx.guild.id, None)
        if 0 <= volume <= 100:
            mp.player.source.volume = volume/100
            return await ctx.send(f"**`Volume set to {volume}`**")

        return await ctx.send(f"{error} **`Volume should be in range [0, 100]`**")

    @commands.command()
    async def skip(self, ctx):
        '''Skips the current song'''
        mp = self.players.get(ctx.guild.id, None)
        if mp.q:
            mp.player.stop()
            return await ctx.send(f"{wcm} **`Music skipped`**")

        return await ctx.send(f"{error} `Queue empty`")

    @commands.command()
    async def repeat(self, ctx, times: int):
        '''Repeats the previous song'''
        mp = self.players.get(ctx.guild.id, None)

        for _ in range(times):
            mp.q.appendleft(mp.current)
        return await ctx.send(f"{wcm} **`Song will repeat for {times} times.`**")

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if not ctx.voice_client:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")

    @volume.before_invoke
    @pause.before_invoke
    @queue.before_invoke
    @clear.before_invoke
    @stop.before_invoke
    @skip.before_invoke
    @np.before_invoke
    @repeat.before_invoke
    async def song_playing(self, ctx):
        mp = self.players.get(ctx.guild.id, None)
        if mp and mp.player.is_playing():
            return

        await ctx.send(f"{error} **`No music being played!`**")
        raise NoMusicPlayingException("No music is being played!")


def setup(client):
    client.add_cog(Music(client))
