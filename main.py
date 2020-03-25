from gameWerwolf import *


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


# =-=-=-= MAIN =-=-=-= #
bot.loop.create_task(botAlone())
bot.run(TOKEN)
