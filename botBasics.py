from discord.ext import commands
import asyncio
import discord

bot = commands.Bot(command_prefix='//')

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}

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


# =-=-=-= CHECKING FUNCTION =-=-=-= #
async def particularWords(message, authorOutput):
    if "maman" in message.content or "mère" in message.content:
        msg = await message.channel.send("On avait dit pas les mamans " + authorOutput + ".")
        await msg.delete(delay=2)

    if "@everyone" in message.content or "@here" in message.content:
        msg = await message.channel.send("Ça t'amuses de mentionner tout le monde " + authorOutput + " ?")
        await msg.delete(delay=2)


def is_me(m):
    return m.author == bot.user


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


""""@bot.event
async def on_message(message):"""
"""
Detect all message send in channel bot can read.
:return: None
"""
"""if not is_me(message):
    authorOutput = getAuthor(message.author)
    print(authorOutput, ':', message.content)
    await particularWords(message, authorOutput)  # Checking everything

await bot.process_commands(message)"""
