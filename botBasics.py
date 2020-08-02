from discord.ext import commands
import asyncio
import discord
from TOKEN import *
import runpy


bot = commands.Bot(command_prefix='//')
lastTextChannel = {}


# =-=-=-= BOT LOOPING FUNCTION =-=-=-= #
async def botAlone():  # Will be check each minute
    """
    Check if bot is alone in a voice channel
    If true, will disconnect from it
    :return:
    """
    while not bot.is_closed():
        for voiceClient in bot.voice_clients:
            if len(voiceClient.channel.members) == 1:
                await voiceClient.disconnect()
        await asyncio.sleep(10)


# =-=-=-= OTHER FUNCTION =-=-=-= #
async def join(ctx):
    """
    Try to join user.
    If found one, connect.
    Else, send message to inform nobody is here?
    :param botToConnect: the bot to connect
    :param ctx: The context of discord call
    :return: channelId or None
    """
    print("Starting connection ...")
    lastTextChannel[ctx.guild.name] = ctx.message.channel
    if ctx.author.voice is None:
        await ctx.message.channel.send("Un utilisateur à besoin d'être connecté")
        return None
    else:
        print("Connected.")
        channel = ctx.author.voice.channel
        await channel.connect()
        return channel.id


async def playAudio(guild, audio):
    """
    Play audio in a channel with the specified audio files
    :param guild: The context.guild of discord call
    :param audio: the resource file to play
    :return:
    """
    for voiceClient in bot.voice_clients:
        if voiceClient.guild == guild:
            while voiceClient.is_playing():
                await asyncio.sleep(1)
            audioSource = discord.FFmpegPCMAudio(audio)
            voiceClient.play(source=audioSource, after=None)
            break


# =-=-=-= DISPLAY FUNCTION =-=-=-= #
def getAuthor(rawAuthor):
    """
    Simply return the display_name of each author as list or string depending of parameter type
    :param rawAuthor: List or string of members
    :return: list or string
    """
    return [x.display_name for x in rawAuthor] if type(rawAuthor) == list else rawAuthor.display_name


# =-=-=-= BOT EVENT =-=-=-= #
@bot.event
async def on_ready():
    """
    After execute bot, will just print in log he's ready
    :return: None
    """
    await bot.change_presence(
        activity=discord.Game(name="Werewolf | ``" + bot.command_prefix + "help``"))
    for voiceClient in bot.voice_clients:
        await voiceClient.disconnect()
    print("Bot is ready")

