from discord import Color
from discord import Embed
from gettext import ngettext

wcm = ":white_check_mark:"
bcm = ":ballot_box_with_check:"
stop = ":octagonal_sign:"
pause = ":pause_button:"
resume = ":play_pause:"
error = ":x:"

empty = u'\u200b'


def np_embed(ctx, info):
    '''Embed for now playing'''
    embed = Embed(title=f"{info['title']}",
                  url=f"{info['url']}",
                  description=f"`Duration: {info['duration']}`",
                  color=Color.magenta(),
                  inline=True
                  )
    embed.set_thumbnail(url=info['thumbnail'])
    embed.set_author(
        name=f"Now playing", icon_url=ctx.author.avatar_url)
    return embed


def q_embed(ctx, info, q):
    '''Embed for queued songs'''
    n = len(q)
    embed = Embed(title=f"{info['title']}",
                  url=f"{info['url']}",
                  description=f"`Being played. Duration: {info['duration']}`\n",
                  inline=True,
                  color=Color.dark_green()
                  )
    embed.set_author(
        name=f"{n} {ngettext('song', 'songs', n)} queued",
        icon_url=ctx.author.avatar_url
    )

    for i, song in enumerate(q, 1):
        embed.add_field(name=empty,
                        value=f"`{i}.` [{song['title']}]({song['url']})\n `Duration: {song['duration']}`",
                        inline=False
                        )

    embed.set_thumbnail(url=info['thumbnail'])
    return embed
