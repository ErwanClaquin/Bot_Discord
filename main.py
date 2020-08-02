from gameWerwolf import *

# =-=-=-= BOT COMMANDS =-=-=-= #
bot.remove_command(name="help")


@bot.command()
async def help(ctx, *msg):
    """
    Will display all bot commands available
    :return:
    """
    args = " ".join(msg)

    if args == "":
        embedHelp = Embed(title="Liste des commandes")
        embedHelp.add_field(name=bot.command_prefix + "lg c", value="Créer une nouvelle partie", inline=False)
        embedHelp.add_field(name=bot.command_prefix + "lg v", value="Valide une partie précédemment créée.",
                            inline=False)
        await ctx.channel.send(content="Voici la liste des commandes disponibles. Vous pouvez obtenir de l'aide "
                                       "supplémentaire sur chaque commande en tapant `" + bot.command_prefix +
                                       "help <?>`",
                               embed=embedHelp)
    elif args == "lg c":
        await ctx.channel.send(content="Cette commande permet d'initialiser une partie. Chaque rôle est associé"
                                       "à un smiley. Les rôles seront pris en compte uniquement si il y'a plus "
                                       "de 2 vote par réaction associée.")

    elif args == "lg v":
        await ctx.channel.send(content="Cette commande permet de valider une partie précédemment créée par `"
                                       + bot.command_prefix + "lg c`. N'oubliez pas qu'il faut pour cela avoir 3 rôles "
                                                              "de plus que le nombre total de joueurs et 3 joueurs "
                                                              "minimum. Si trop de rôles sont choisis, une sélection "
                                                              "pseudo-aléatoire parmis ces rôles aura lieu.")

    else:
        await ctx.channel.send("Impossible de trouver la commande spécifiée.")


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
loop = asyncio.get_event_loop()
# loop.create_task(botMusic.start(TOKEN_MUSIC))
bot.loop.create_task(botAlone())
loop.create_task(bot.start(TOKEN))
loop.run_forever()

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

# TODO: Add waiting over : generate error currently
