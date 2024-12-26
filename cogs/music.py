from discord import Option
from discord import slash_command
from discord import Embed, Colour
from discord.ext import commands

import config
import sys
import yt_util
import asyncio

sys.path.append("..")
music_queue = []
KORN_TWIST = "korn - twist"

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = asyncio.Queue()
        self.is_playing = False
        self.current = None    
        self.is_join = False
        self.current_music_name = ''
    
    @slash_command(guild_ids=[config.GUILD_ID,], name="stop", description=config.STOP_DESCRIPTION)
    async def stop(self, ctx):
        global music_queue
        self.queue = asyncio.Queue()
        if ctx.voice_client and ctx.voice_client.is_playing():
            music_queue = []
            ctx.voice_client.stop()
        else:
            return await ctx.respond("🚫 봇이 Voice Channel에 없습니다")
        
        return await ctx.respond("👋 Bye~!")
    
    @slash_command(guild_ids=[config.GUILD_ID,], name="skip", description="skip current music")
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()

            embed = Embed(
                title=f'⏭️ **{self.current_music_name}을(를) Skip 했습니다**',
                color=Colour.yellow()
            )

            await ctx.respond(embed=embed)
        else:
            embed = Embed(
                title=f'❌ **현재 재생 중인 노래가 없습니다.**',
                color=Colour.red()
            )

            await ctx.respond(embed=embed)
    
    @slash_command(guild_ids=[config.GUILD_ID,], name="korn", description="OMG Korn")
    async def korn(self, ctx):
        global music_queue
        isUserinVoice = ctx.user.voice

        if isUserinVoice == None:   # user가 voice 채널에 있는지 확인
            return await ctx.respond(f"❌ {ctx.user.mention} is not in Voice Channel")
        
        if not self.is_join:    # 봇이 voice 채널에 있는지 확인
            await ctx.author.voice.channel.connect()
            self.is_join = True
        
        embed = Embed(
            title="🌽🌽🌽🌽 **Oh My God It's Korn** 🌽🌽🌽🌽",
            color=Colour.dark_gray()
        )

        await ctx.respond(embed=embed)
            
        player = await yt_util.YTDLSource.from_local("./local_music/korn_twist.mp3")       
        await self.queue.put(player)
        position = self.queue.qsize()
        music_queue.append(KORN_TWIST)

        if not self.is_playing and not ctx.voice_client.is_paused():
            await self.play_next(ctx)
    
    @slash_command(guild_ids=[config.GUILD_ID,], name="play", description="play music")
    async def play(self, ctx, url=Option(str, description="YouTube URL", required=True)):
        global music_queue
        isUserinVoice = ctx.user.voice
        user_avatar = ctx.user.avatar
        username = ctx.user.name

        if isUserinVoice == None:   # user가 voice 채널에 있는지 확인
            return await ctx.respond(f"❌ {ctx.user.mention} is not in Voice Channel")
        
        if not self.is_join:    # 봇이 voice 채널에 있는지 확인
            await ctx.author.voice.channel.connect()
            self.is_join = True
        
        res = await ctx.respond(f"🔄 Pull Music From Youtube...")
    
        player, title, duration, thumb_url = await yt_util.YTDLSource.from_url(url, loop=self.bot.loop, stream=True)       
        await self.queue.put(player)
        position = self.queue.qsize()

        music_queue.append(title)
        print(f'pos: {position}')
        print(user_avatar)

        embed = Embed(
            title=title,
            color=Colour.green()
        )

        embed.add_field(name="곡 길이", value=duration, inline=True)
        embed.add_field(name="대기열", value=f'대기열 {position}번', inline=True)
        embed.add_field(name="음원", value=f'[링크]({url})', inline=True)
        embed.set_image(url=thumb_url)
        embed.set_footer(text=f"{username}'s request", icon_url=user_avatar)

        await res.edit(content="", embed=embed)

        if not self.is_playing and not ctx.voice_client.is_paused():
            await self.play_next(ctx)
    
    async def play_next(self, ctx):
        global music_queue
        print(f'empty: {self.queue.empty()}')
        if not self.queue.empty():
            self.current = await self.queue.get()
            self.is_playing = True
            self.current_music_name = music_queue[0]
            music_queue = music_queue[1:]
            ctx.voice_client.play(self.current, after=lambda e: self.bot.loop.create_task(self.play_next_after(ctx, e)))
        else:
            await ctx.voice_client.disconnect()
            self.current = None
            self.is_playing = False
            self.is_join = False
    
    async def play_next_after(self, ctx, error):
        if error:
            print(f'Play Error: {error}')
        self.is_playing = False
        await self.play_next(ctx)

        
def setup(bot):
    bot.add_cog(Music(bot))