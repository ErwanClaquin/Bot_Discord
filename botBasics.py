from discord.ext import commands
import asyncio
import discord
from TOKEN import *

bot = commands.Bot(command_prefix='//')
lastTextChannel = {}


# =-=-=-= BOT LOOPING FUNCTION =-=-=-= #
async def botAlone():  # Will be check each minute
    while not bot.is_closed():
        for voiceClient in bot.voice_clients:
            if len(voiceClient.channel.members) == 1:
                await voiceClient.channel.send("Le bot, seul, se casse de " + voiceClient.channel.name)
                await voiceClient.disconnect()
        await asyncio.sleep(10)


# =-=-=-= OTHER FUNCTION =-=-=-= #
async def join(ctx):
    print("Starting connection ...")
    lastTextChannel[ctx.guild.name] = ctx.message.channel
    if ctx.author.voice is None:
        await ctx.message.channel.send("Un utilisateur à besoin d'être connecté")
    else:
        print("Connected.")
        channel = ctx.author.voice.channel
        await channel.connect()


# =-=-=-= DISPLAY FUNCTION =-=-=-= #
def getAuthor(rawAuthor):
    if type(rawAuthor) == list:
        rawReturn = []
        for author in rawAuthor:
            if author.nick:
                rawReturn.append(author.nick)
            else:
                authorSplit = str(author).split('#')[:-1]  # get the author name without last '#number'
                rawReturn.append("#".join(authorSplit))
        return rawReturn
    else:
        if rawAuthor.nick:
            return rawAuthor.nick

        else:
            author = str(rawAuthor).split('#')[:-1]  # get the author name without last '#number'
            authorOutput = "#".join(author)
            return authorOutput


# =-=-=-= BOT EVENT =-=-=-= #
@bot.event
async def on_ready():
    """
    After execute bot, will just print in log he's ready
    :return: None
    """
    await bot.change_presence(activity=discord.Activity(name="les ordres", type=discord.ActivityType.listening))
    for voiceClient in bot.voice_clients:
        await voiceClient.disconnect()
    print("Bot is ready")
    print(bot.voice_clients)
