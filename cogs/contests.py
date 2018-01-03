import discord
from discord.ext import commands

class Contests:
    """Contest functions"""
    def __init__(self, bot):
        self.bot = bot
        self.bot_logs = self.bot.get_channel(bot.bot_logs_id)

    #pylint: disable-msg=too-many-arguments
    def generateEmbed(self, messageAuthor: discord.User, title, description, footerText, image_url="", colour=0x00ff00):
        """Generates a discord embed object off the given parameters

        Arguments:
            messageAuthor {discord.User} -- Allows for the mention and user's logo to be added to the embed
            title {string} -- Title of the embed, the first heading
            description {string} -- The description of this object
            footerText {string} -- The text shown in the footer, usually for commands that operate upon this

        Keyword Arguments:
            colour {hex} -- Used for the bar on the left's colour (default: {0x00ff00} -- green)
            image_url {string} -- The image shown at the bottom of the embed. (default: {""} -- no image)

        Returns:
            [discord.Embed] -- The embed object generated.
        """
        embed = discord.Embed(title="Submission by:", description=messageAuthor.mention, colour=colour)
        embed.add_field(name="Title:", value=title, inline=False)
        embed.add_field(name="Description:", value=description, inline=False)
        embed.set_image(url=image_url)
        embed.set_footer(text=footerText)
        embed.set_thumbnail(url=messageAuthor.avatar_url)
        return embed
    #pylint: enable-msg=too-many-arguments

    @commands.command()
    async def submit(self, ctx, *, args):
        """Submits an item into a contest. ;submit <title> | <description> | [imageURL]. Note the spaces"""
        input_split = tuple(args.split(" | "))
        if len(input_split) != 2 and len(input_split) != 3:
            raise TypeError("Not all arguments passed")
        title, description = input_split[0:2]
        if len(input_split) == 3:
            image_url = input_split[3]
        else:
            image_url = ""
        submissionID = (await self.bot.database.generate_id())
        footerText = "Type {0}allow {1} True to allow this and {0}allow {1} False to prevent the moving on this to voting queue.".format(ctx.prefix, submissionID)
        embed = self.generateEmbed(ctx.author, title, description, footerText, image_url, 0x00ff00)
        server_channels = await self.bot.database.get_contest_channels(ctx.guild.id)
        print(server_channels)
        if ctx.channel.id == server_channels[0]:
            channel = ctx.guild.get_channel(server_channels[1])
            message = await channel.send(embed=embed)
            await self.bot.database.add_contest_submission(submissionID, embed, message.guild.id)
            await ctx.send(f"Submissions sent in {channel.mention}")

    @commands.command()
    async def list_submissions(self, ctx):
        submissions = (await self.bot.database.list_contest_submissions(ctx.guild.id))
        await ctx.send(submissions)

    @commands.command()
    async def allow(self, ctx, submissionID, allowed="True"):
        """Allows for moderators to approve/reject submissions."""
        #CHECK IF SAME SERVER
        embed = (await self.bot.database.get_submission(submissionID))
        if allowed.lower() == "true":
            embed.set_footer(text="Type {0}vote {1} 0 to hate it, type {0}vote {1} 5 to really like it.".format(ctx.prefix, submissionID))
            await ctx.send(embed=embed)
        elif allowed.lower() == "false":
            await ctx.send("​Submssions with submissionID of {} has been rejected.".format(submissionID))
            channel = ctx.guild.get_channel(await self.bot.database.get_server_channels(ctx.guild.id)[1])
            message = await channel.get_message(await self.bot.database.get_server_channels(ctx.guild.id)[1])
            embed.colour = 0xff0000
            await message.edit(embed=embed)
            await self.bot.database.remove_contest_submission(submissionID)
        else:
            await ctx.send("​A correct value of true/false was not passed ")

    @commands.command()
    async def vote(self, ctx, submissionsID):
        "Not implemented yet."
        pass

def setup(bot):
    bot.add_cog(Contests(bot))
