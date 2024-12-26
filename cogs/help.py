from discord import slash_command
from discord import Embed, Colour
from discord.ext import commands
import sys
import config
import help_info

sys.path.append("..")

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(guild_ids=[config.GUILD_ID,], name='help', description='명령어 도움말')
    async def help(self, ctx):
        author_avatar = ctx.author.avatar
        embed = Embed(
            title="명령어 도움말",
            color=Colour.blurple()
        )

        embed.add_field(name="/play", value=help_info.PLAY_INFO, inline=False)
        embed.add_field(name="/skip", value=help_info.SKIP_INFO, inline=False)
        embed.add_field(name="/stop", value=help_info.STOP_INFO, inline=False)
        embed.add_field(name="/korn", value=help_info.KORN_INFO, inline=False)
        embed.set_author(name="Sining in the Bratva", icon_url=author_avatar)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))