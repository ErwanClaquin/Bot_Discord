from discord import Embed
# Importing class roles
from classForWerewolf.alphaWerewolf import *
from classForWerewolf.beginnerSeer import *
from classForWerewolf.bodyGuard import *
from classForWerewolf.diviner import *
from classForWerewolf.doppelganger import *
from classForWerewolf.drunkard import *
from classForWerewolf.freemasson import *
from classForWerewolf.ghostHunter import *
from classForWerewolf.hunter import *
from classForWerewolf.insomniac import *
from classForWerewolf.minion import *
from classForWerewolf.seer import *
from classForWerewolf.shamanWerewolf import *
from classForWerewolf.sleepingWerewolf import *
from classForWerewolf.tanner import *
from classForWerewolf.thief import *
from classForWerewolf.troublemaker import *
import time
import subprocess

messagesChoice = {}
lgGame = {}


class LG:
    """
    Class for handling game Werewolf, function all described below
    """

    def __init__(self):
        self.rolesOrder = list()
        self.categoryName = "Loup-Garou"  # Changeable category for guild which already have this name.
        self.lastVoiceChannel = None  # To move back people after the game.
        self.msgChoiceRole = list()  # To delete them after validation of the game.
        self.progression = ""
        self.msgToDelete = list()
        self.category = None
        self.playersAndRoles = list()
        self.roles = list()
        self.players = list()
        self.centralDeck = list()
        self.voiceChannel = None
        self.textChannel = None
        self.roleForPlayer = None
        self.courseOfTheGame = ["Voici le déroulé de la partie :"]

        # =-=-=-= EMBEDS =-=-=-= #
        self.embedPage1 = Embed(title="Choix de rôles numéro 1")
        self.embedPage1.add_field(name="😀 : Doppelgänger",
                                  value="```Markdown\n#Regarde la carte d'un autre joueur et copie son rôle.```",
                                  inline=False)
        self.embedPage1.add_field(name="😄 : Sbire",
                                  value="```diff\n-Incite les villageois à le tuer pour faire gagner les loups.```",
                                  inline=False)
        self.embedPage1.add_field(name="😃 : Loup-Garou",
                                  value="```diff\n-Complote à la pleine lune contre les villageois.```",
                                  inline=False)
        self.embedPage1.add_field(name="🥰 : Loup Alpha",
                                  value="```diff\n-Sa puissance lui permet de créer un nouveau loup.```",
                                  inline=False)
        self.embedPage1.add_field(name="😍 : Loup Shamane",
                                  value="```diff\n-Lisant dans les ossements de ses victimes, il peut voir un rôle d'un des joueurs.```",
                                  inline=False)
        self.embedPage1.add_field(name="😁 : Franc-Maçon",
                                  value="```css\nReconnait son camarade de la franc-maçonnerie. (Maximum 2, ajout par paire)```",
                                  inline=False)
        self.embedPage1.add_field(name="😆 : Voyante",
                                  value="```css\nObserve le rôle d'un autre joueur ou deux rôles centraux.```",
                                  inline=False)
        self.embedPage1.add_field(name="😇 : Chasseur de Fantômes",
                                  value="```Markdown\n#Regarde un à deux rôles des joueurs et devient tanneur, loup ou vampire s'il en découvre un.```",
                                  inline=False)
        self.embedPage1.add_field(name="😗 : Apprentie voyante",
                                  value="```css\nDébutant dans la divination, elle ne peut observer qu'une carte d'un rôle central.```",
                                  inline=False)
        self.embedPage1.add_field(name="😅 : Voleur",
                                  value="```css\nÉchange son rôle.```",
                                  inline=False)
        self.embedPage1.add_field(name="🤣 : Noiseuse",
                                  value="```css\nÉchange deux autres rôle que le sien.```",
                                  inline=False)
        self.embedPage1.add_field(name="😂 : Soûlard",
                                  value="```css\nÉchange son rôle avec un rôle central.```",
                                  inline=False)
        self.embedPage1.add_field(name="🙂 : Insomniaque",
                                  value="```css\nNe pouvant dormir, il connaît son rôle avant la fin de la nuit.```",
                                  inline=False)
        self.embedPage1.add_field(name="😊 : Divinateur",
                                  value="```css\nPar le pouvoir de son Dieu, il révèle le rôle d'un villageois.```",
                                  inline=False)
        self.embedPage1.add_field(name="🙃 : Tanneur",
                                  value="```Fix\n#Le pauvre bougre veut se faire tuer.```",
                                  inline=False)
        self.embedPage1.add_field(name="😉 : Chasseur",
                                  value="```css\nIl se vengera en tirant une dernière balle avant son dernier souffle.```",
                                  inline=False)
        self.embedPage1.add_field(name="😘 : Garde du corps",
                                  value="```css\nSon vote permet de protéger un joueur de la potence.```",
                                  inline=False)
        self.embedPage1.add_field(name="🤩 : Loup rêveur",
                                  value="```diff\n-Ce pauvre loup n'a pas fini sa nuit et n'a pas pu voir qui était les loups.```",
                                  inline=False)
        """self.embedPage1.add_field(name="", value=".", inline=False)
        self.embedPage1.add_field(name="", value=".", inline=False)"""

        self.embedPage2 = None

    async def delete(self):
        await self.delAllMsg()
        self.lastVoiceChannel = None  # To move back people after the game.
        self.msgChoiceRole = list()  # To delete them after validation of the game.
        self.progression = ""
        self.msgToDelete = list()
        self.category = None
        self.playersAndRoles = list()
        self.roles = list()
        self.players = list()
        self.centralDeck = list()
        self.voiceChannel = None
        self.textChannel = None
        self.roleForPlayer = None
        self.courseOfTheGame = ["Voici le déroulé de la partie :"]

    async def creatingGame(self, ctx):
        """
        Send a message with all roles available in the game
        If calling while game is running, will just send the default progression
        :param ctx: The context of discord call
        :return: None
        """
        if self.progression == "":
            self.progression = "Création d'une partie"
            msg1 = await ctx.channel.send(
                content="Seules les réactions ayant plus de 2 voix seront comptabilisées."
                        "```css\nLes rôles en verts sont les membres du village.```"
                        "```Markdown\n#Les rôles en bleu dépendent de la partie.```"
                        "```diff\n-Les rôles en rouge sont les loups-garous.```"
                        "```Fix\n#Les rôles en orange doivent gagner seul.```",
                embed=self.embedPage1)
            self.msgChoiceRole.append(msg1.id)
            self.msgToDelete.append(msg1)
            await self.addRolesOnEmbed(msg1)
        else:
            await self.wait(ctx)

    async def validateGame(self, ctx):
        """
        Check if conditions are fulfill to launch the game
        :param ctx: The context of discord call
        :return: None
        """
        if self.progression == "Création d'une partie":  # Game created

            # =-=-=-= CHECKING TOO FAST START =-=-=-= #
            for msgID in self.msgChoiceRole:
                msg = await ctx.channel.fetch_message(msgID)
                if len(msg.embeds[0].fields) != len(msg.reactions):
                    await self.wait(ctx)
                    return

            # =-=-=-= CALCULATING ROLES =-=-=-= #
            self.progression = "Préparation de la partie"
            await self.wait(ctx)
            for msgId in self.msgChoiceRole:
                msg = await ctx.channel.fetch_message(msgId)
                for reactions in msg.reactions:
                    await self.getRoleFromReaction(ctx, reactions)
            self.players = [member for member in ctx.author.voice.channel.members if not member.bot]

            # =-=-=-= CHECKING INVALID PARTY =-=-=-= #
            # TODO : REPLACE HERE BY 3 PLAYERS MIN, JUST DID THAT TO CHECK WHEN I'M ALONE
            if len(self.players) < 1:
                self.msgToDelete.append(await ctx.channel.send(
                    "Nombre de joueurs insuffisant : 3 joueurs minimum. (" + str(
                        len(self.players)) + " actuellement.)"))
                await asyncio.sleep(5)
                await self.delete()
                return
            elif len(self.roles) < len(self.players) + 3:
                self.msgToDelete.append(
                    await ctx.channel.send(
                        str(len(self.roles)) + "rôles choisis : insuffisants pour le nombre de joueurs. (" +
                        str(len(self.players) + 3) + " rôles  minimum," + str(len(self.players)) +
                        " joueurs + 3 dans le tas central.)"))
                await asyncio.sleep(5)
                await self.delete()
                return

            elif len(self.roles) > len(self.players) + 3:
                self.msgToDelete.append(await ctx.channel.send(
                    "Nombre de rôles supérieur au nombre de joueurs : " + str(len(self.roles)) + "rôles pour " + str(
                        len(self.players)) +
                    " joueurs + 3 dans le tas central. Certains rôles ne seront pas pris en compte."))

            await self.delAllMsg(waitingTime=5)
            print("Start with roles : " + ", ".join(self.roles))
            self.msgToDelete.append(await ctx.channel.send(
                "Début de la partie avec les rôles suivants : " + ", ".join(self.roles)))
            print("Start with players : " + ", ".join(getAuthor(self.players)))
            self.msgToDelete.append(await ctx.channel.send(
                "Les joueurs sont les suivants : " + ", ".join(getAuthor(self.players))))

            # =-=-=-= START GAME =-=-=-= #
            await self.startingGame(ctx=ctx)

        else:
            await self.wait(ctx=ctx)

    async def startingGame(self, ctx):
        """
        Prepare everything to launch the game (roles, game space, ...)
        :param ctx: The context of discord call
        :return: None
        """
        # =-=-=-= ATTRIBUTE ROLES FOR PLAYERS =-=-=-= #
        self.msgToDelete.append(await ctx.message.channel.send("Attribution des rôles ..."))
        self.rolesOrder = self.roles.copy()
        self.rolesOrder = list(dict.fromkeys(self.rolesOrder))  # Remove redundant roles for playGame()
        random.seed(time.time())
        random.shuffle(self.players)
        random.shuffle(self.roles)
        self.roles = self.roles[:len(self.players) + 3]
        if self.roles.count("Franc-Maçon") % 2 != 0:  # Only One Freemason in
            for i in range(len(self.roles)):
                if self.roles[i] == "Franc-Maçon":
                    self.roles[(i + 1) % len(self.roles)] = "Franc-Maçon"
                    random.seed(time.time())
                    random.shuffle(self.players)
                    random.shuffle(self.roles)
                    break

        for numberPlayer in range(len(self.players)):
            # At least there is less player than role, so I need to get the number of players instead of roles.

            self.syncRole(user=self.players[numberPlayer], roleToAdd=self.roles[numberPlayer],
                          listToAdd=self.playersAndRoles)

        # =-=-=-= ATTRIBUTE ROLES FOR DECK =-=-=-= #
        for numberCentralRole in range(len(self.players), len(self.players) + 3):
            if numberCentralRole == len(self.players) + 0:
                position = "gauche"
            elif numberCentralRole == len(self.players) + 1:
                position = "milieu"
            else:
                position = "droite"
            self.syncRole(user=position, roleToAdd=self.roles[numberCentralRole], listToAdd=self.centralDeck)

        # =-=-=-= Preparing requires =-=-=-= #
        await self.createRole(ctx=ctx)
        self.msgToDelete.append(await ctx.message.channel.send("Création du village ..."))
        print("Create village ...")
        self.lastVoiceChannel = ctx.author.voice.channel
        await self.deleteCategory(ctx=ctx, reason="Pas de dualité de channel.")
        await self.createGameSpace(ctx=ctx)
        # await self.movePlayer(ctx=ctx, voiceChannel=self.voiceChannel, reason="Début de partie.")

        print("Game started")
        self.msgToDelete.append(await ctx.message.channel.send("Début de la partie."))

        await ctx.channel.send("Cleaning all messages ...")
        await self.delAllMsg(waitingTime=5)
        await self.playGame(ctx=ctx)

    async def playGame(self, ctx):
        """
        Launch the game
        :param ctx: The context of discord call
        :return:
        """
        await asyncio.sleep(1)
        await join(ctx=ctx)
        subprocess.Popen(["python.exe", "mainMusic.py", str(self.voiceChannel.id), str(ctx.guild.id), "Music.mp3"])
        await self.delAllMsg(waitingTime=0)
        await playAudio(guild=ctx.guild, audio="beginPlay.mp3")
        for player in self.playersAndRoles:
            await player.user.send(
                "```diff\n-NOUVELLE PARTIE-```Vous êtes " + player.firstRole + ", attendez votre tour pour plus d'informations.")
        for role in self.rolesOrder:
            for player in self.playersAndRoles + self.centralDeck:
                if player.firstRole == role or player.newRole == "Insomniaque":
                    await player.playAudio(guild=ctx.guild, start=True)
                    await player.play(members=self.playersAndRoles, centralDeck=self.centralDeck,
                                      courseOfTheGame=self.courseOfTheGame)
                    await player.playAudio(guild=ctx.guild, start=False)

        await playAudio(guild=ctx.guild, audio="beginVote.mp3")
        await self.letVote(ctx=ctx)

    async def letVote(self, ctx):
        """
        Let player vote for other players
        :return: None
        """
        msgStart = await self.textChannel.send(
            self.roleForPlayer.mention + " \nDès maintenant les votes sont pris en compte. Votez parmis :```" +
            "``````".join(
                self.getMembersName()) + "```en écrivant un des pseudos ci-dessus en **_message privé_**.\nÉvitez"
                                         " de trop spammer si vous ne voulez pas que le décompte soit trop "
                                         "long.\nN'oubliez pas que vous ne pouvez pas voter pour vous même.")
        for player in self.playersAndRoles:
            await player.user.send("Votez ici parmis :```" + "``````".join(player.getMembersName()) +
                                   "```Seul le dernier pseudo valide sera pris en compte.")

        await asyncio.sleep(5)
        await self.textChannel.send("Plus que 30s.")
        await asyncio.sleep(5)
        msgEnd = await self.textChannel.send("Le décompte est terminé, obtention des votes ...")
        votes = await self.getVote(msgStart=msgStart, msgEnd=msgEnd)
        await self.applyVote(votes=votes)
        await self.displayCourseOfTheGame()
        await self.textChannel.send("Fin de la partie. Suppression du channel dans 2 minutes.")

        await asyncio.sleep(20)
        await self.endGame(ctx=ctx)

    async def getVote(self, msgStart, msgEnd):
        """
        Get every vote for each player
        :param msgStart: The first message before anyone can vote
        :param msgEnd: The last message after anyone can vote
        :return: dict of 'playerName' : "playerVotFor'
        """
        votes = {player: None for player in self.getMembersName()}

        for user in self.players:
            async for msg in user.dm_channel.history(limit=None, before=msgEnd.created_at, after=msgStart.created_at):
                if msg.author.name in self.getMembersName() and msg.content in self.getMembersName() and msg.content != msg.author.name:
                    player = self.getMemberFromName(name=msg.author.name)
                    player.vote(self.getMemberFromName(name=msg.content))
                    print(msg.author.name, "voted for", msg.content)
                    self.courseOfTheGame += ["```" + msg.author.name + " a voté pour " + msg.content + "```"]
                    votes[msg.author.name] = msg.content
                    break
            if votes[user.name] is None:
                self.courseOfTheGame += ["```" + user.name + " n'a pas voté." + "```"]
        return votes

    async def applyVote(self, votes):
        """
         Get count of all the votes on each players. None vote (No valid vote done) will be destroy.
        :param votes: dict of 'playerName' : "playerVotFor'
        :return: None
        """
        voteCount = {vote: 0 for vote in self.getMembersName()}
        voteCount[None] = 0
        for vote in votes.values():
            voteCount[vote] += 1

        if voteCount[None] != 0:
            await self.textChannel.send(
                "Attention, des joueurs n'ont pas voté / ont mal écrit, les votes peuvent être faussés.")
        del voteCount[None]

        playerOrder = sorted(voteCount.items(), key=lambda x: x[1], reverse=True)
        print("playerOrder", playerOrder)
        if playerOrder[0][1] == 0:  # Nobody vote
            await self.textChannel.send("`Partie non valide`, personne n'a voté.")

        elif playerOrder[0][1] == 1:  # People think nobody is a werewolf
            await self.textChannel.send("Le village pense qu'il n'y a pas de loups-garou ? Vérification ...")
            werewolves = self.getWolves()
            if len(werewolves) == 0:
                await self.textChannel.send("Le village a raison, il n'y a pas de loups-garous parmis eux.")
                await self.textChannel.send("```css\nLES VILLAGEOIS ONT GAGNÉ```")
            else:
                await self.textChannel.send("Malheuresement, il y avait```" + ", ".join(werewolves) + "```")
                await self.textChannel.send("```diff\n-LES LOUPS-GAROUS ONT GAGNÉ-```")

        else:  # Classic vote
            werewolves = self.getWolves()
            deaths = []
            for i in range(len(playerOrder)):
                player = self.getMemberFromName(name=playerOrder[i][0])
                isDead = await player.isDead(channel=self.textChannel)
                if isDead:
                    deaths += await player.death(channel=self.textChannel, members=self.players)
                    print("voteCount :", voteCount)

                    # Get player name with same number of vote against them
                    playerEqualVote = []
                    for p in playerOrder:
                        if p[1] == playerOrder[i][1] and p[0] != playerOrder[i][0]:
                            playerEqualVote.append(self.getMemberFromName(name=p[0]))
                    print("Other players with equals number of vote :", playerEqualVote)
                    for otherPlayer in playerEqualVote:
                        isDead = await otherPlayer.isDead(channel=self.textChannel)
                        if isDead:
                            deaths += await otherPlayer.death(channel=self.textChannel, members=self.players)
                    break

            for i in range(len(deaths)):
                if deaths[i] is None:
                    del deaths[i]

            if len(deaths) == 0:  # No one die
                if len(werewolves) == 0:  # No Werewolves
                    await self.textChannel.send("Il n'ya pas eu de mort et il n'y a aucun Loup-Garou !")
                    await self.textChannel.send("```css\nLES VILLAGEOIS ONT GAGNÉ```")
                else:  # Werewolves among players
                    await self.textChannel.send(
                        "Il n'y a pas eu de mort mais```" + ", ".join(werewolves) + "```")
                    await self.textChannel.send("```diff\n-LES LOUPS-GAROUS ONT GAGNÉ-```")

            elif len(deaths) == 1:
                if deaths[0].lastRole in ["Loup-Garou", "Loup Alpha", "Loup Shamane", "Loup rêveur"]:  # Werewolf die
                    await self.textChannel.send("```css\nLES VILLAGEOIS ONT GAGNÉ```")
                elif deaths[0].lastRole in ["Tanneur"]:  # Tanner died
                    await self.textChannel.send("```Fix\n#LE TANNEUR A GAGNÉ#```")
                    if len(werewolves) > 0:  # Wolves in game
                        await self.textChannel.send("```diff\n-LES LOUPS-GAROUS ONT ÉGALEMENT GAGNÉ```")
                else:  # Villager died
                    await self.textChannel.send("```diff\n-LES LOUPS-GAROUS ONT GAGNÉ-```")

            else:  # more than 2 deaths
                rolesDead = []
                for dead in deaths:
                    if dead.lastRole in ["Loup-Garou", "Loup Alpha", "Loup Shamane", "Loup rêveur"]:
                        rolesDead.append("Loup-Garou")
                    elif dead.lastRole in ["Tanneur"]:
                        await self.textChannel.send("```Fix\n#LE TANNEUR A GAGNÉ#```")
                    else:
                        rolesDead.append("Villageois")
                print("rolesDead :", rolesDead)
                rolesDead = list(dict.fromkeys(rolesDead))
                print("rolesDead unique :", rolesDead)
                if "Loup-Garou" in rolesDead:
                    await self.textChannel.send("```css\nLES VILLAGEOIS ONT GAGNÉ```")
                else:
                    await self.textChannel.send("```diff\n-LES LOUPS-GAROUS ONT GAGNÉ-```")

    async def displayCourseOfTheGame(self):
        """
        Display how the game was, action by action
        :return:
        """
        print("display course of the game...")
        course = ""
        for message in self.courseOfTheGame:
            if len(course + message) >= 2000:  # Limit by discord
                await self.textChannel.send(course)
                course = ""
            course += message
        if course != "":
            await self.textChannel.send(course)
        print("displayed.")

    async def endGame(self, ctx):
        """
        Deleting all needs for game
        :param ctx: The context of discord call
        :return:
        """
        print("Ending game ...")
        await self.movePlayer(ctx=ctx, voiceChannel=self.lastVoiceChannel, reason="Fin de partie.")
        await self.deleteCategory(ctx=ctx, reason="Fin de partie.")
        await self.deleteRole(ctx=ctx, reason="Fin de partie.")
        print("Game ended")
        await self.delete()

    async def createRole(self, ctx):
        """
        Create self.categoryName role to not ping other non-player
        :param ctx: The context of discord call
        :return:
        """
        await self.deleteRole(ctx=ctx, reason="Début de partie.")
        await ctx.guild.create_role(name=self.categoryName)
        await asyncio.sleep(1)
        self.roleForPlayer = discord.utils.get(ctx.guild.roles, name=self.categoryName)
        print("Role created.")
        member = await ctx.guild.fetch_member(bot.user.id)
        await member.add_roles(self.roleForPlayer, reason="Début de partie.")
        for member in ctx.author.voice.channel.members:
            await member.add_roles(self.roleForPlayer, reason="Début de partie.")

    async def createGameSpace(self, ctx):
        """
        Create everything related to text & vocal information if non-DM message
        :param ctx: The context of discord call
        :return:
        """
        self.category = await ctx.guild.create_category_channel(name=self.categoryName)
        print("Category created")
        await self.category.set_permissions(self.roleForPlayer, read_messages=True, connect=True)
        roleEveryone = discord.utils.get(ctx.guild.roles, name="@everyone")
        await self.category.set_permissions(roleEveryone, read_messages=False, connect=False)

        self.textChannel = await ctx.guild.create_text_channel(name="Partie", category=self.category)
        print("Text channel created")
        self.voiceChannel = await ctx.guild.create_voice_channel(name="Village", category=self.category)
        print("Voice channel created")
        await self.voiceChannel.edit(user_limit=len(self.players) + 2, sync_permissions=True)
        await self.textChannel.edit(nsfw=True, sync_permissions=True)

    async def movePlayer(self, ctx, voiceChannel, reason):
        """
        move player to a specified voiceChannel
        :param reason: Reason of the move
        :param voiceChannel: the VoiceChannel() players will be move
        :param ctx: The context of discord call
        :return:
        """
        self.msgToDelete.append(await ctx.message.channel.send("Déplacement des joueurs ..."))
        for member in ctx.author.voice.channel.members:
            await member.move_to(channel=voiceChannel, reason=reason)

    async def getRoleFromReaction(self, ctx, reaction):
        """
        Get role from reaction : if > 1 it count
        :param ctx: The context of discord call
        :param reaction: a str() of emoji tag on Discord
        :return: Non
        """
        if reaction.count > 1:
            for msgId in self.msgChoiceRole:
                msg = await ctx.channel.fetch_message(msgId)
                for field in msg.embeds[0].fields:
                    if field.name[0] == str(reaction.emoji):
                        if field.name[4:] in ["Franc-Maçon"]:  # 2 Freemasson max
                            self.roles.append(field.name[4:])
                            self.roles.append(field.name[4:])
                        else:
                            for i in range(reaction.count - 1):
                                self.roles.append(field.name[4:])

    def getMemberFromName(self, name):
        """
        Return the Member() class corresponding with the name
        :param name: String of a player name
        :return: Member() class
        """
        for member in self.playersAndRoles:
            if name in member.user.name:
                return member

    def getMembersName(self):
        """
        Give and randomize all player in the game
        :return: list(Member())
        """
        listMemberName = []
        for member in self.playersAndRoles:
            listMemberName.append(member.user.name)
        random.shuffle(listMemberName)
        return listMemberName

    def getWolves(self):
        """
        Give every werewolves in the game
        :return: list() of str()
        """
        w = []
        for player in self.playersAndRoles:
            if player.lastRole in ["Loup-Garou", "Loup Alpha", "Loup Shamane", "Loup rêveur"]:
                w.append(str(player.user.name) + " est un " + str(player.lastRole))
        if len(w) == 0:  # No werewolf among players : maybe minions are among them
            for player in self.playersAndRoles:
                if player.lastRole in ["Sbire"]:
                    w.append(str(player.user.name) + " est un " + str(player.lastRole) +
                             " mais comme il n'y a pas de Loups-Garous, ce sbire devient un Loup-Garou.")
        return w

    async def deleteCategory(self, ctx, reason="No reason available"):
        """
        Delete category if exist & if permission enable
        :param ctx: The context of discord call
        :param reason: str() of the reason for deleting the channel
        :return: None
        """
        for category in ctx.guild.categories:
            if category.name == self.categoryName:
                try:
                    for chan in category.channels:
                        await chan.delete()
                    await category.delete(reason=reason)
                except discord.errors.Forbidden:
                    self.msgToDelete.append(await ctx.message.channel.send(
                        "Erreur, permission non accordée, la suppression des catégories n'est pas complète."))
        print("Deleted all category.")

    async def deleteRole(self, ctx, reason="No reason available"):
        """
        Delete Role if exist & if permission enable
        :param ctx: The context of discord call
        :param reason: str() of the reason for deleting the channel
        :return: None
        """
        for role in ctx.guild.roles:
            if role.name == self.categoryName:
                try:
                    await role.delete(reason=reason)
                except discord.errors.Forbidden:
                    self.msgToDelete.append(await ctx.message.channel.send(
                        "Erreur, permission non accordée, la suppression des rôles n'est pas complète."))
        print("Deleted all roles.")

    async def wait(self, ctx):
        """
        Display the message which contain the reason why user need to wait
        :param ctx: The context of discord call
        :return: None
        """
        msg = await ctx.channel.send(self.progression + ", veuillez patientez.")
        self.msgToDelete.append(msg)

    async def delAllMsg(self, waitingTime=0):
        """
        Delete every message in message buffer
        :param waitingTime: time after we delete <int> secondes
        :return: None
        """
        for msg in self.msgToDelete:
            await msg.delete(delay=waitingTime)

    @staticmethod
    async def addRolesOnEmbed(msg):
        """
        Add roles depending on role
        :param msg: message of embed
        :return: None
        """
        for field in msg.embeds[0].fields:
            await msg.add_reaction(field.name[0])

    @staticmethod
    def syncRole(user, roleToAdd, listToAdd):
        """
        Set user from role provided, with different class for each
        :param user: The Member() or string to associate role
        :param roleToAdd: The role which will be link
        :param listToAdd: On which list will be add this
        :return: None
        """
        print(user, ":", roleToAdd)
        if roleToAdd == "Doppelgänger":
            listToAdd.append(
                Doppelganger(user=user, firstRole=roleToAdd, botRef=bot))

        elif roleToAdd == "Sbire":
            listToAdd.append(Minion(user=user, firstRole=roleToAdd, botRef=bot))

        elif roleToAdd == "Loup-Garou":
            listToAdd.append(Werewolf(user=user, firstRole=roleToAdd, botRef=bot))

        elif roleToAdd == "Loup Alpha":
            listToAdd.append(
                AlphaWerewolf(user=user, firstRole=roleToAdd, botRef=bot))

        elif roleToAdd == "Loup Shamane":
            listToAdd.append(
                ShamanWerewolf(user=user, firstRole=roleToAdd, botRef=bot))

        elif roleToAdd == "Franc-Maçon":
            listToAdd.append(Freemason(user=user, firstRole=roleToAdd, botRef=bot))

        elif roleToAdd == "Voyante":
            listToAdd.append(Seer(user=user, firstRole=roleToAdd, botRef=bot))

        elif roleToAdd == "Chasseur de Fantômes":
            listToAdd.append(GhostHunter(user=user, firstRole=roleToAdd, botRef=bot))

        elif roleToAdd == "Apprentie voyante":
            listToAdd.append(
                BeginnerSeer(user=user, firstRole=roleToAdd, botRef=bot))

        elif roleToAdd == "Voleur":
            listToAdd.append(Thief(user=user, firstRole=roleToAdd, botRef=bot))

        elif roleToAdd == "Noiseuse":
            listToAdd.append(
                Troublemaker(user=user, firstRole=roleToAdd, botRef=bot))

        elif roleToAdd == "Soûlard":
            listToAdd.append(Drunkard(user=user, firstRole=roleToAdd, botRef=bot))

        elif roleToAdd == "Insomniaque":
            listToAdd.append(Insomniac(user=user, firstRole=roleToAdd, botRef=bot))

        elif roleToAdd == "Divinateur":
            listToAdd.append(Diviner(user=user, firstRole=roleToAdd, botRef=bot))

        elif roleToAdd == "Tanneur":
            listToAdd.append(Tanner(user=user, firstRole=roleToAdd, botRef=bot))

        elif roleToAdd == "Chasseur":
            listToAdd.append(Hunter(user=user, firstRole=roleToAdd, botRef=bot))

        elif roleToAdd == "Garde du corps":
            listToAdd.append(BodyGuard(user=user, firstRole=roleToAdd, botRef=bot))

        elif roleToAdd == "Loup rêveur":
            listToAdd.append(
                SleepingWerewolf(user=user, firstRole=roleToAdd, botRef=bot))
        else:
            print("GROS PROBLEME", roleToAdd)
            exit()


# =-=-=-= BOT COMMANDS =-=-=-= #
@bot.command()
async def lg(ctx, value=""):
    """
    Check the value to redirect to methods
    :param ctx: The context of discord call
    :param value: parameters for launching different step of the game
    :return:
    """

    if ctx.author.voice is None:
        await ctx.message.channel.send("Un utilisateur à besoin d'être connecté")
    else:
        if value == "create" or value == "c":
            if lgGame.get(ctx.guild.name) is None:
                lgGame[ctx.guild.name] = LG()
            await lgGame[ctx.guild.name].creatingGame(ctx=ctx)

        elif value == "validate" or value == "v":
            if lgGame.get(ctx.guild.name) is not None:
                await lgGame[ctx.guild.name].validateGame(ctx)
            else:
                await ctx.channel.send("Partie non créée.")
        else:
            await ctx.channel.send(
                "Commande inconnue. Tapez <<" + bot.command_prefix + "help>> pour plus d'informations")
    """
    try:
        if ctx.author.voice is None:
            await ctx.message.channel.send("Un utilisateur à besoin d'être connecté")
        else:
            if value == "create" or value == "c":
                if lgGame.get(ctx.guild.name) is None:
                    lgGame[ctx.guild.name] = LG()
                await lgGame[ctx.guild.name].creatingGame(ctx=ctx)

            elif value == "validate" or value == "v":
                if lgGame.get(ctx.guild.name) is not None:
                    await lgGame[ctx.guild.name].validateGame(ctx)
                else:
                    await ctx.channel.send("Partie non créée.")
            else:
                await ctx.channel.send(
                    "Commande inconnue. Tapez <<" + bot.command_prefix + "help>> pour plus d'informations")
    except AttributeError:
        await ctx.message.channel.send("Commande non supportée en Message Privé.")
"""
