from music import *
from Werewolf.gameWerwolf import *
from TOKEN import *


# =-=-=-= BOT COMMANDS =-=-=-= #
@bot.command()
async def helpAll(message):
    """
    Will display all bot commands available
    :return:
    """
    await message.channel.send("command help all not ready yet")


@bot.command()
async def disconnect(ctx):
    for voiceClient in bot.voice_clients:
        if voiceClient.guild == ctx.guild:
            await ctx.message.channel.send("Je me suis fait virer de <" + voiceClient.channel.name + ">")
            await voiceClient.disconnect()


@bot.command()
async def hug(ctx):
    sentences = ["Viens donc me faire un câlin",
                 "Tu te sens seul ? Viens donc te réchauffer auprès de moi",
                 "J'vais te tenir compagnie un jour",
                 "T'es à ce point en manque d'amour pour demander ça un bot ?"]

    authorOutput = getAuthor(ctx.message.author)
    await ctx.message.channel.send(random.choice(sentences) + " " + authorOutput)


# =-=-=-= MAIN =-=-=-= #
bot.loop.create_task(botAlone())
bot.loop.create_task(endedSong())
bot.run(TOKEN)
