from gameWerwolf import *


# =-=-=-= BOT COMMANDS =-=-=-= #
@bot.command()
async def helpAll(message):
    """
    Will display all bot commands available
    :return:
    """
    await message.channel.send("command helpAll not ready yet")


@bot.command()
async def disconnect(ctx):
    print("Trying to disconnect ...")
    for voiceClient in bot.voice_clients:
        if voiceClient.guild == ctx.guild:
            await ctx.message.channel.send("Je me suis fait virer de <" + voiceClient.channel.name + ">")
            await voiceClient.disconnect()
    print("Disconnected.")


@bot.command()
async def getCo(ctx):
    print("Displaying connections ...")
    for voiceClient in bot.voice_clients:
        await ctx.message.channel.send(voiceClient.channel)
    print("Displayed.")

# =-=-=-= MAIN =-=-=-= #
bot.loop.create_task(botAlone())
bot.run(TOKEN)

# TODO: Add sentences to THIS bot to have a nicer immersion
#       "Tout le monde fermez les yeux",
#       alphaWerewolf,
#       beginnerSeer,
#       diviner,
#       doppelganger,
#       drunkard,
#       goshtHunter,
#       seer,
#       shamanWerewolf,
#       thief,
#       troublemaker,
#       werewolf,
#       "Vous avez {x} minutes pour voter. (...)",
#       "Les {role(s)} ont gagnés !"

# TODO: Add music to AN OTHER bot to have a nicer immersion. Music can't be change first

# TODO: Add options (change the musics, the time of discussion, reminder of time left (1min & 30s))
