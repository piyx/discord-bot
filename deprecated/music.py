# import os
# import pafy
# import discord
# from gettext import ngettext
# from discord.utils import get
# from youtube_dl import YoutubeDL
# from discord.ext import commands
# from discord import FFmpegPCMAudio
# from utils.yt_url import YoutubeUrl
# from utils.embeds import np_embed, q_embed
# from collections import defaultdict
# from utils.embeds import wcm, bcm, error, pause, resume

# class Player:
#     def __init__(self, player):
#         self.player = player
#         self.q = []
#         self.curr = None



# class Music(commands.Cog):
#     def __init__(self, client) -> None:
#         self.client = client
#         self.players = {}
#         self.server = None
#         self.path = "./media/"
#         self.q = []
#         self.voice = None
#         self.current = None
#         self.server = None
#         print(self.players)

#     @commands.command()
#     async def play(self, ctx, *, song_name):
#         '''Plays song from first youtube search result'''
#         server = ctx.guild.id
#         voice = get(self.client.voice_clients, guild=ctx.guild)
#         if server not in self.players:
#             self.players[server] = Player(voice)
        
#         player = self.players[server]

#         yt = YoutubeUrl(song_name)
#         video_url = yt.get_video_url()
#         data = yt.get_video_info(video_url)

#         if not data:
#             await ctx.send(f"{error} **`Song could not be found`**")
#             return

#         def download(url):
#             video = pafy.new(url)
#             if str(server) not in os.listdir("./media"):
#                 print("debug1")
#                 os.mkdir(f"{self.path}{server}/")
#             if ("song.mp3") in os.listdir(f"{self.path}{server}/"):
#                 print("debug2")
#                 os.remove(f"{self.path}{server}/song.mp3")
#             try:
#                 video.getbestaudio().download(f"{self.path}{server}/")
#             except Exception as e:
#                 return False

#             for song in os.listdir(f"{self.path}{server}/"):
#                 os.rename(f"{self.path}{server}/{song}", f"{self.path}{server}/song.mp3")
#             return True

#         def check_queue():
#             if not self.q:
#                 self.current = None
#                 if os.listdir(f"{self.path}{server}/"):
#                     os.remove(f"{self.path}{server}/song.mp3")
#                 return
#             os.remove(f"{self.path}{server}/song.mp3")
#             self.current = self.q.pop(0)
#             song = self.current['url']
#             download(song)
#             self.players[server].player.play(FFmpegPCMAudio(f"{self.path}{server}/song.mp3"),
#                             after=lambda x: check_queue())
#             self.players[server].source = discord.PCMVolumeTransformer(self.players[server].player.source, volume=1.0)

#         if not self.players[server].player.is_playing():
#             success = download(data['url'])
#             if not success:
#                 await ctx.send(f"{error} **`Song cannot be streamed`**")
#                 return

#             self.players[server].player.play(FFmpegPCMAudio(f"{self.path}{server}/song.mp3"),
#                             after=lambda x: check_queue())
#             self.players[server].player.source = discord.PCMVolumeTransformer(
#             self.players[server].player.source, volume=1.0)
#             self.players[server].curr = data
#             embed = np_embed(ctx, self.players[server].curr)
#             await ctx.send(embed=embed)
#         else:
#             await ctx.send(f"{bcm} **`Song has been added to queue`**")
#             self.players[server].q.append(data)
#             return

#     @commands.command()
#     async def pause(self, ctx):
#         '''Pauses the song'''
#         if self.voice and self.voice.is_playing():
#             self.voice.pause()
#             await ctx.send(f"`Music paused` {pause}")
#         else:
#             await ctx.send(f"{error} **`No song is being played`**")

#     @commands.command()
#     async def resume(self, ctx):
#         '''Resumes the song'''
#         if not self.voice:
#             await ctx.send(f"{error} **`No song is being played`**")
#         elif self.voice.is_paused():
#             self.voice.resume()
#             await ctx.send(f"{resume} **`Music resumed`**")
#         else:
#             await ctx.send(f"{error} **`Song is already being played`**")

#     @commands.command()
#     async def stop(self, ctx):
#         '''Stops the song'''
#         if self.voice and self.voice.is_playing():
#             self.q.clear()
#             self.voice.stop()
#             await ctx.voice_client.disconnect()
#             await ctx.send(f"`Music stopped` {stop}")
#         else:
#             await ctx.send(f"{error} **`No song is being played`**")

#     @commands.command()
#     async def np(self, ctx):
#         '''Displays now playing song info'''
#         server = ctx.guild.id
#         if not self.players[server].player:
#             await ctx.send(f"{error} **`No song is being played`**")
#             return

#         embed = np_embed(ctx, self.current)
#         await ctx.send(embed=embed)

#     @commands.command()
#     async def queue(self, ctx):
#         '''Displays the songs in queue'''
#         if not self.q or not self.current:
#             await ctx.send(f"{bcm} **`No songs queued`**")
#             return

#         embed = q_embed(ctx, self.current, self.q)
#         await ctx.send(embed=embed)

#     @commands.command()
#     async def clear(self, ctx):
#         '''Clears the queue'''
#         if self.q:
#             self.q.clear()
#             await ctx.send(f"{wcm} **`Queue cleared`**")
#         else:
#             await ctx.send(f"{bcm} **`No songs queued`**")

#     @commands.command()
#     async def volume(self, ctx, volume: int):
#         '''Sets the volume'''
#         if 0 <= volume <= 100:
#             self.voice.source.volume = volume/100
#             await ctx.send(f"**`Volume set to {volume}`**")
#             return
#         await ctx.send(f"{error} **`Volume should be in range [0, 100]`**")

#     @commands.command()
#     async def skip(self, ctx):
#         '''Skips the current song'''
#         if self.voice and self.q:
#             self.voice.stop()
#             await ctx.send(f"{wcm} **`Music skipped`**")
#         elif self.voice and not self.q:
#             await ctx.send(f"{error} `Queue empty`")
#         else:
#             await ctx.send(f"{error} **`No song is being played`**")

#     @play.before_invoke
#     async def ensure_voice(self, ctx):
#         if not ctx.voice_client:
#             if ctx.author.voice:
#                 await ctx.author.voice.channel.connect()
#             else:
#                 await ctx.send("You are not connected to a voice channel.")

#     @volume.before_invoke
#     async def song_playing(self, ctx):
#         if not ctx.voice_client or not ctx.voice_client.is_playing():
#             return await ctx.send(f"{error} **`No music being played!`**")
#             raise Exception
        


# def setup(client):
#     client.add_cog(Music(client))
