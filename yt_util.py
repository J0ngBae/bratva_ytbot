from __future__ import unicode_literals
import yt_dlp
import uuid
import config
import discord
import asyncio
import requests

EXT = 'mp3'
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}
THUMBNAIL_PARSE = 'https://i.ytimg.com/vi/'

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': EXT,
        'preferredquality': '320',
    }],
    'outtmpl': config.TEMP_PATH + uuid.uuid1().hex + '_%(id)s.%(ext)s',
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": (
        "0.0.0.0"
    ),
    #'quiet': True,
}

ytdl = yt_dlp.YoutubeDL(ydl_opts)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source: discord.AudioSource, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream)
        )
        print(url)
        res = requests.get(url)
        idx = res.text.find(THUMBNAIL_PARSE)

        parse = res.text[idx:]
        thumb_url = parse[:parse.find('"')]

        if "entries" in data:
            # Takes the first item from a playlist
            data = data["entries"][0]

        #print(data)
        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data), data['title'], data['duration_string'], thumb_url