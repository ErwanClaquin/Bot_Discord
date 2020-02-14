from discord import Embed
# Importing class roles
from Werewolf.classForWerewolf.alphaWerewolf import *
from Werewolf.classForWerewolf.beginnerSeer import *
from Werewolf.classForWerewolf.bodyGuard import *
from Werewolf.classForWerewolf.diviner import *
from Werewolf.classForWerewolf.doppelganger import *
from Werewolf.classForWerewolf.drunkard import *
from Werewolf.classForWerewolf.freemasson import *
from Werewolf.classForWerewolf.goshtHunter import *
from Werewolf.classForWerewolf.hunter import *
from Werewolf.classForWerewolf.insomniac import *
from Werewolf.classForWerewolf.minion import *
from Werewolf.classForWerewolf.seer import *
from Werewolf.classForWerewolf.shamanWerewolf import *
from Werewolf.classForWerewolf.sleepingWerewolf import *
from Werewolf.classForWerewolf.tanner import *
from Werewolf.classForWerewolf.thief import *
from Werewolf.classForWerewolf.troublemaker import *
import time

messagesChoice = {}
lgGame = {}


class LG:
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
                                  value="```css\nReconnait ses pairs de la franc-maçonnerie.```",
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
        await self.delAllMsg(0)
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

    async def creatingGame(self, ctx):
        if self.progression == "":
            self.progression = "Création d'une partie"
            msg1 = await ctx.channel.send(
                content="Seules les réactions ayant plus de 2 voix seront comptabilisées."
                        "```css\nLes rôles en verts sont les membres du village.```"
                        "```Markdown\n#Les rôles en bleu dépendent de la partie.```"
                        "```diff\n-Les rôles en rouge sont les loups-garous.```"
                        "```Fix\n#Les rôles en orange doivent gagner seul.```"
                ,
                embed=self.embedPage1)
            self.msgChoiceRole.append(msg1.id)
            self.msgToDelete.append(msg1)
            await self.addRolesOnEmbed(msg1)
        else:
            await self.wait(ctx)

    async def validationGame(self, ctx):
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
                    await self.getRoleFromEmoji(ctx, reactions)
            self.players = ctx.author.voice.channel.members

            # =-=-=-= CHECKING INVALID PARTY =-=-=-= #
            print("TODO : REPLACE HERE BY 3 PLAYERS MIN, JUST DID THAT TO CHECK WHEN I'M ALONE")
            if len(self.players) < 1:
                self.msgToDelete.append(await ctx.channel.send(
                    "Nombre de joueurs insuffisant : 3 joueurs minimum. (" + str(
                        len(self.players)) + " actuellement.)"))
                await asyncio.sleep(3)
                await self.delete()
                return
            if len(self.roles) < len(self.players) + 3:
                self.msgToDelete.append(
                    await ctx.channel.send(
                        "Nombre de rôles insuffisants pour le nombre de joueurs : minimum " + str(
                            len(self.players) + 3) + " rôles (" + str(
                            len(self.players)) + " joueurs + 3 dans le tas central.)"))
                await asyncio.sleep(3)
                await self.delete()
                return

            if len(self.roles) > len(self.players) + 3:
                self.msgToDelete.append(await ctx.channel.send(
                    "Nombre de rôles supérieur au nombre de joueurs : " + str(len(self.roles)) + "rôles pour " + str(
                        len(self.players)) +
                    " joueurs + 3 dans le tas central. Certains rôles ne seront pas pris en compte."))

            await self.delAllMsg(waitingTime=3)
            print("Début de la partie avec les rôles suivants : " + ", ".join(self.roles))
            self.msgToDelete.append(await ctx.channel.send(
                "Début de la partie avec les rôles suivants : " + ", ".join(self.roles)))
            print("Les joueurs sont les suivants : " + ", ".join(getAuthor(self.players)))
            self.msgToDelete.append(await ctx.channel.send(
                "Les joueurs sont les suivants : " + ", ".join(getAuthor(self.players))))

            # =-=-=-= START GAME =-=-=-= #
            await self.startGame(ctx=ctx)
            await asyncio.sleep(5)
            # await self.endGame(ctx=ctx)

        else:
            await self.wait(ctx=ctx)

    @staticmethod
    async def addRolesOnEmbed(msg):
        for field in msg.embeds[0].fields:
            await msg.add_reaction(field.name[0])

    async def startGame(self, ctx):
        # =-=-=-= ATTRIBUTE ROLES FOR PLAYERS =-=-=-= #
        self.msgToDelete.append(await ctx.message.channel.send("Attribution des rôles ..."))
        self.rolesOrder = self.roles.copy()
        self.rolesOrder = list(dict.fromkeys(self.rolesOrder))  # Remove redundant roles for playGame()
        random.seed(time.time())
        random.shuffle(self.players)
        random.shuffle(self.roles)

        for numberPlayer in range(len(self.players)):
            # At least there is less player than role, so I need to get the number of players instead of roles.
            if self.roles[numberPlayer] == "Doppelgänger":
                self.playersAndRoles.append(
                    Doppelganger(user=self.players[numberPlayer], firstRole=self.roles[numberPlayer], botRef=bot))

            elif self.roles[numberPlayer] == "Sbire":
                self.playersAndRoles.append(
                    Minion(user=self.players[numberPlayer], firstRole=self.roles[numberPlayer], botRef=bot))

            elif self.roles[numberPlayer] == "Loup-Garou":
                self.playersAndRoles.append(
                    Werewolf(user=self.players[numberPlayer], firstRole=self.roles[numberPlayer], botRef=bot))

            elif self.roles[numberPlayer] == "Loup Alpha":
                self.playersAndRoles.append(
                    AlphaWerewolf(user=self.players[numberPlayer], firstRole=self.roles[numberPlayer], botRef=bot))

            elif self.roles[numberPlayer] == "Loup Shamane":
                self.playersAndRoles.append(
                    ShamanWerewolf(user=self.players[numberPlayer], firstRole=self.roles[numberPlayer], botRef=bot))

            elif self.roles[numberPlayer] == "Franc-Maçon":
                self.playersAndRoles.append(
                    Freemason(user=self.players[numberPlayer], firstRole=self.roles[numberPlayer], botRef=bot))

            elif self.roles[numberPlayer] == "Voyante":
                self.playersAndRoles.append(
                    Seer(user=self.players[numberPlayer], firstRole=self.roles[numberPlayer], botRef=bot))

            elif self.roles[numberPlayer] == "Chasseur de Fantômes":
                self.playersAndRoles.append(
                    GoshtHunter(user=self.players[numberPlayer], firstRole=self.roles[numberPlayer], botRef=bot))

            elif self.roles[numberPlayer] == "Apprentie voyante":
                self.playersAndRoles.append(
                    BeginnerSeer(user=self.players[numberPlayer], firstRole=self.roles[numberPlayer], botRef=bot))

            elif self.roles[numberPlayer] == "Voleur":
                self.playersAndRoles.append(
                    Thief(user=self.players[numberPlayer], firstRole=self.roles[numberPlayer], botRef=bot))

            elif self.roles[numberPlayer] == "Noiseuse":
                self.playersAndRoles.append(
                    Troublemaker(user=self.players[numberPlayer], firstRole=self.roles[numberPlayer], botRef=bot))

            elif self.roles[numberPlayer] == "Soûlard":
                self.playersAndRoles.append(
                    Drunkard(user=self.players[numberPlayer], firstRole=self.roles[numberPlayer], botRef=bot))

            elif self.roles[numberPlayer] == "Insomniaque":
                self.playersAndRoles.append(
                    Insomniac(user=self.players[numberPlayer], firstRole=self.roles[numberPlayer], botRef=bot))

            elif self.roles[numberPlayer] == "Divinateur":
                self.playersAndRoles.append(
                    Diviner(user=self.players[numberPlayer], firstRole=self.roles[numberPlayer], botRef=bot))

            elif self.roles[numberPlayer] == "Tanneur":
                self.playersAndRoles.append(
                    Tanner(user=self.players[numberPlayer], firstRole=self.roles[numberPlayer], botRef=bot))

            elif self.roles[numberPlayer] == "Chasseur":
                self.playersAndRoles.append(
                    Hunter(user=self.players[numberPlayer], firstRole=self.roles[numberPlayer], botRef=bot))

            elif self.roles[numberPlayer] == "Garde du corps":
                self.playersAndRoles.append(
                    BodyGuard(user=self.players[numberPlayer], firstRole=self.roles[numberPlayer], botRef=bot))

            elif self.roles[numberPlayer] == "Loup rêveur":
                self.playersAndRoles.append(
                    SleepingWerewolf(user=self.players[numberPlayer], firstRole=self.roles[numberPlayer], botRef=bot))
            else:
                print("GROS PROBLEME : ", self.roles[numberPlayer])

        # =-=-=-= ATTRIBUTE ROLES FOR DECK =-=-=-= #
        for numberCentralRole in range(len(self.players), len(self.players) + 3):
            if numberCentralRole == len(self.players) + 0:
                position = "gauche"
            elif numberCentralRole == len(self.players) + 1:
                position = "milieu"
            else:
                position = "droite"

            if self.roles[numberCentralRole] == "Doppelgänger":
                self.centralDeck.append(
                    Doppelganger(user=position, firstRole=self.roles[numberCentralRole], botRef=bot))

            elif self.roles[numberCentralRole] == "Sbire":
                self.centralDeck.append(Minion(user=position, firstRole=self.roles[numberCentralRole], botRef=bot))

            elif self.roles[numberCentralRole] == "Loup-Garou":
                self.centralDeck.append(Werewolf(user=position, firstRole=self.roles[numberCentralRole], botRef=bot))

            elif self.roles[numberCentralRole] == "Loup Alpha":
                self.centralDeck.append(
                    AlphaWerewolf(user=position, firstRole=self.roles[numberCentralRole], botRef=bot))

            elif self.roles[numberCentralRole] == "Loup Shamane":
                self.centralDeck.append(
                    ShamanWerewolf(user=position, firstRole=self.roles[numberCentralRole], botRef=bot))

            elif self.roles[numberCentralRole] == "Franc-Maçon":
                self.centralDeck.append(Freemason(user=position, firstRole=self.roles[numberCentralRole], botRef=bot))

            elif self.roles[numberCentralRole] == "Voyante":
                self.centralDeck.append(Seer(user=position, firstRole=self.roles[numberCentralRole], botRef=bot))

            elif self.roles[numberCentralRole] == "Chasseur de Fantômes":
                self.centralDeck.append(GoshtHunter(user=position, firstRole=self.roles[numberCentralRole], botRef=bot))

            elif self.roles[numberCentralRole] == "Apprentie voyante":
                self.centralDeck.append(
                    BeginnerSeer(user=position, firstRole=self.roles[numberCentralRole], botRef=bot))

            elif self.roles[numberCentralRole] == "Voleur":
                self.centralDeck.append(Thief(user=position, firstRole=self.roles[numberCentralRole], botRef=bot))

            elif self.roles[numberCentralRole] == "Noiseuse":
                self.centralDeck.append(
                    Troublemaker(user=position, firstRole=self.roles[numberCentralRole], botRef=bot))

            elif self.roles[numberCentralRole] == "Soûlard":
                self.centralDeck.append(Drunkard(user=position, firstRole=self.roles[numberCentralRole], botRef=bot))

            elif self.roles[numberCentralRole] == "Insomniaque":
                self.centralDeck.append(Insomniac(user=position, firstRole=self.roles[numberCentralRole], botRef=bot))

            elif self.roles[numberCentralRole] == "Divinateur":
                self.centralDeck.append(Diviner(user=position, firstRole=self.roles[numberCentralRole], botRef=bot))

            elif self.roles[numberCentralRole] == "Tanneur":
                self.centralDeck.append(Tanner(user=position, firstRole=self.roles[numberCentralRole], botRef=bot))

            elif self.roles[numberCentralRole] == "Chasseur":
                self.centralDeck.append(Hunter(user=position, firstRole=self.roles[numberCentralRole], botRef=bot))

            elif self.roles[numberCentralRole] == "Garde du corps":
                self.centralDeck.append(BodyGuard(user=position, firstRole=self.roles[numberCentralRole], botRef=bot))

            elif self.roles[numberCentralRole] == "Loup rêveur":
                self.centralDeck.append(
                    SleepingWerewolf(user=position, firstRole=self.roles[numberCentralRole], botRef=bot))
            else:
                print("GROS PROBLEME", self.roles[numberCentralRole])

        # =-=-=-= REMOVING REDUNDANT ROLES =-=-=-= #
        await self.createRole(ctx=ctx)

        # =-=-=-= REMOVING REDUNDANT CATEGORY =-=-=-= #
        await self.removeCategory(ctx=ctx)

        # =-=-=-= CREATING GAME SPACE =-=-=-= #
        await self.createGameSpace(ctx=ctx)

        # =-=-=-= MOVING PLAYERS =-=-=-= #

        self.msgToDelete.append(await ctx.message.channel.send("Début de la partie."))

        await ctx.channel.send("Cleaning all messages ...")
        await self.delAllMsg(2)
        await self.playGame(ctx=ctx)

    async def createRole(self, ctx):
        await self.deleteRole(ctx=ctx, reason="Début de partie.")
        await ctx.guild.create_role(name=self.categoryName)
        await asyncio.sleep(1)
        self.roleForPlayer = discord.utils.get(ctx.guild.roles, name=self.categoryName)
        print("Role created.")
        member = await ctx.guild.fetch_member(bot.user.id)
        print(self.roleForPlayer.__class__)
        print(member.__class__)
        await member.add_roles(self.roleForPlayer, reason="Début de partie.")

    async def removeCategory(self, ctx):

        self.msgToDelete.append(await ctx.message.channel.send("Création du village ..."))
        print("Create village ...")
        self.lastVoiceChannel = ctx.author.voice.channel
        await self.deleteCategory(ctx=ctx, reason="Pas de dualité de channel.")

    async def createGameSpace(self, ctx):
        self.category = await ctx.guild.create_category_channel(name=self.categoryName)
        print("Category created")
        await self.category.set_permissions(self.roleForPlayer, read_messages=True, connect=True)
        roleEveryone = discord.utils.get(ctx.guild.roles, name="@everyone")
        await self.category.set_permissions(roleEveryone, read_messages=False, connect=False)

        self.textChannel = await ctx.guild.create_text_channel(name="Partie", category=self.category)
        print("Text channel created")
        self.voiceChannel = await ctx.guild.create_voice_channel(name="Village", category=self.category)
        print("Voice channel created")
        await self.voiceChannel.edit(user_limit=len(self.players) + 1, sync_permissions=True)
        await self.textChannel.edit(nsfw=True, sync_permissions=True)

    async def movePlayer(self, ctx):
        self.msgToDelete.append(await ctx.message.channel.send("Déplacement des joueurs ..."))

        for member in ctx.author.voice.channel.members:
            await member.add_roles(self.roleForPlayer, reason="Début de partie.")
            # await member.move_to(channel=self.voiceChannel, reason="Début de partie.")
        print("Game started")

    def getMemberFromName(self, name):
        for member in self.playersAndRoles:
            if name in member.user.name:
                return member

    def getMembersName(self, forDisplay=False):
        listMemberName = []
        for member in self.playersAndRoles:
            if forDisplay:
                name = "```" + member.user.name + "```"

            else:
                name = member.user.name
            listMemberName.append(name)
        random.shuffle(listMemberName)
        return listMemberName

    async def endGame(self, ctx):
        print("Ending game ...")
        for member in self.voiceChannel.members:
            await member.move_to(channel=self.lastVoiceChannel, reason="Fin de partie.")
        await self.deleteCategory(ctx=ctx, reason="Fin de partie.")
        await self.deleteRole(ctx=ctx, reason="Fin de partie.")
        print("Game ended")
        await self.delete()

    async def playGame(self, ctx):
        print(len(self.playersAndRoles))
        for player in self.playersAndRoles:
            await player.user.send("Vous êtes " + player.firstRole + ", attendez votre tour.")
            print(player.user.name + " : " + player.firstRole)
        print(len(self.centralDeck))
        for deck in self.centralDeck:
            print(deck.user + " : " + deck.firstRole)
        print("\n\n")
        for role in self.rolesOrder:
            for player in self.playersAndRoles:
                if player.firstRole == role:
                    await player.play(members=self.playersAndRoles, centralDeck=self.centralDeck)
                    print(player.user.name, "played role :", player.firstRole)
                elif player.newRole == "Insomniaque":
                    player.play(members=self.playersAndRoles, centralDeck=self.centralDeck)

        for player in self.playersAndRoles:
            print(player.user.name + " : " + player.lastRole)
        for deck in self.centralDeck:
            print(deck.user + " : " + deck.lastRole)
        await self.letVote()
        await self.endGame(ctx=ctx)

    async def letVote(self):
        mStart = await self.textChannel.send(
            "Dès maintenant les votes sont pris en compte. Votez parmis :" + "".join(self.getMembersName(
                forDisplay=True)) + "en écrivant un des pseudos ci-dessus. Évitez de trop spammer si vous ne voulez pas que le décompte soit trop long.")
        await asyncio.sleep(7)
        await self.textChannel.send("Plus qu'une minute.")
        await asyncio.sleep(6)
        mEnd = await self.textChannel.send("Le décompte est terminé, obtention des votes ...")
        votes = await self.getVote(msgStart=mStart, msgEnd=mEnd)
        await self.applyVote(votes=votes)
        await self.textChannel.send("Fin de la partie. Suppression du channel dans 1 minute.")
        await asyncio.sleep(60)

    async def getVote(self, msgStart, msgEnd):
        votes = {player: None for player in self.getMembersName()}
        async for msg in self.textChannel.history(limit=None, before=msgEnd.created_at, after=msgStart.created_at):
            if msg.author.name in self.getMembersName() and msg.content in self.getMembersName() and msg.content != msg.author.name:
                if votes[msg.author.name] is None:
                    print(msg.author.name, "voted", msg.content)
                    votes[msg.author.name] = msg.content
                    if None not in votes.values():
                        break
        return votes

    async def applyVote(self, votes):
        voteCount = {vote: 0 for vote in self.getMembersName()}
        voteCount[None] = -len(self.players) - 10
        for vote in votes.values():
            voteCount[vote] += 1

        playerOrder = sorted(voteCount.items(), key=lambda x: x[1], reverse=True)
        print(playerOrder)
        for i in range(len(self.players)):
            player = self.getMemberFromName(name=playerOrder[i][0])
            print("player :", player)
            isDead = await player.isDead(channel=self.textChannel)
            if isDead:
                await player.death(channel=self.textChannel)
                break

    async def deleteCategory(self, ctx, reason="No reason available"):
        for category in ctx.guild.categories:
            if category.name == self.categoryName:
                for chan in category.channels:
                    await chan.delete()
                await category.delete(reason=reason)
        print("Deleted all category.")

    async def deleteRole(self, ctx, reason="No reason available"):
        for role in ctx.guild.roles:
            if role.name == self.categoryName:
                await role.delete(reason=reason)
        print("Deleted all roles.")

    async def getRoleFromEmoji(self, ctx, reactions):
        if reactions.count > 1:
            for msgId in self.msgChoiceRole:
                msg = await ctx.channel.fetch_message(msgId)
                for field in msg.embeds[0].fields:
                    if field.name[0] == str(reactions.emoji):
                        for i in range(reactions.count - 1):
                            self.roles.append(field.name[4:])
                            if field.name[4:] in ["Franc-Maçon"]:
                                self.roles.append(field.name[4:])

    async def wait(self, ctx):
        msg = await ctx.channel.send(self.progression + ", veuillez patientez.")
        self.msgToDelete.append(msg)

    async def delAllMsg(self, waitingTime=0):
        for msg in self.msgToDelete:
            await msg.delete(delay=waitingTime)


# =-=-=-= BOT COMMANDS =-=-=-= #
@bot.command()
async def lg(ctx, val=""):
    if ctx.author.voice is None:
        await ctx.message.channel.send("Un utilisateur à besoin d'être connecté")
    else:
        if val == "":
            await ctx.channel.send("tapez <<" + bot.command_prefix + "lg create>> pour créer une partie.")
            await ctx.channel.send("tapez <<" + bot.command_prefix + "lg val>> pour valider une partie.")

        elif val == "create" or val == "c":
            if lgGame.get(ctx.guild.name) is None:
                lgGame[ctx.guild.name] = LG()
            await lgGame[ctx.guild.name].creatingGame(ctx=ctx)

        elif val == "val" or val == "v":
            if lgGame.get(ctx.guild.name) is not None:
                await lgGame[ctx.guild.name].validationGame(ctx)
            else:
                await ctx.channel.send("Partie non créée.")
        else:
            await ctx.channel.send(
                "Commande inconnue. Tapez <<" + bot.command_prefix + "lg>> pour plus d'informations")
