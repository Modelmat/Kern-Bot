from urllib.parse import urlparse
from os import listdir
from os.path import isfile, join
from datetime import datetime

import discord
from discord.ext import commands

async def bot_user_check(ctx):
    return not ctx.author.bot


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database = None
        self.prefix = "k"
        self.server_prefixes = {}
        self.time_format = '%H:%M:%S UTC on the %d of %B, %Y'
        self.bot_logs_id = 382780308610744331
        self.launch_time = datetime.utcnow()
        super().add_check(bot_user_check)
        self.todo = """TODO: ```
                    01. Finish contests cog
                    02. Use logging module
                    03. Fix the error with overload in define function (total = 15)
                    04. Finish and neaten up the help command (possibly use  HelpFormatter). Add docstrings to all commands
                    05. Hack Command - add fake attack
                    06. Server rules (database - rules) - custom titles
                    07. Custom context
                    08. Stackexchange search - https://api.stackexchange.com/docs
                    09. Make prefixes a list (for multiple)
                    ```
                    """
        self.extensions = {}
        for extension in [f.replace('.py', '') for f in listdir("cogs") if isfile(join("cogs", f))]:
            self.extensions[extension] = True

    class ResponseError(Exception):
        pass

class CustomContext(commands.Context):
    def clean_prefix(self):
        user = self.bot.user
        prefix = self.prefix.replace(user.mention, '@' + user.name)
        return prefix
    async def error(self, error, title="Error:", channel: discord.TextChannel = None, *args, **kwargs):
        error_embed = discord.Embed(title=title, colour=0xff0000, description=error)
        if channel is None:
            return await super().send(embed=error_embed, *args, **kwargs)
        return await channel.send(embed=error_embed, *args, **kwargs)

    async def success(self, success, title="Success", channel: discord.TextChannel = None, *args, **kwargs):
        success_embed = discord.Embed(title=title, colour=0x00ff00, description=success)
        if channel is None:
            return await super().send(embed=success_embed, *args, **kwargs)
        return await channel.send(embed=success_embed, *args, **kwargs)

    async def neutral(self, text, title, channel: discord.TextChannel = None, *args, **kwargs):
        neutral_embed = discord.Embed(title=title, colour=discord.Colour.blurple(), description=text)
        if channel is None:
            return await super().send(embed=neutral_embed, *args, **kwargs)
        return await channel.send(embed=neutral_embed, *args, **kwargs)

class FakeChannel:
    def __init__(self, name):
        self.name = name

class Url(commands.Converter):
    async def convert(self, ctx, argument):
        url = str(argument)
        if not url.startswith('http://'):
            url = "http://" + url
        if "." not in url:
            url += (".com")  # A bad assumption
        url = urlparse(url).geturl()

        return url
