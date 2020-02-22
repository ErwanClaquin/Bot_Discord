from Werewolf.classForWerewolf.player import *


# =-=-=-= SEER CLASS =-=-=-= #
class Troublemaker(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)
        self.firstChoice = None
        self.newMembers = None

    async def checkingMessage(self, msg):
        if msg.content not in self.getMembersName():
            # Failed to find player
            print("Failed")
            await self.user.send("Erreur, impossible de trouver la personne visée. Veuillez réessayer parmis :```"
                                 + "``````".join(self.getMembersName()) + "```")
            await self.wait()
        else:
            if self.firstChoice is None:
                # Succeed to find category
                print("Succeed, first choice")
                await msg.author.send("Le premier joueur est : " + msg.content + ".")
                self.firstChoice = self.getMemberFromName(name=msg.content)
                self.newMembers = self.getMembersName().copy()
                self.newMembers.remove(self.firstChoice.user.name)
                await self.user.send("Écrivez le nom de l'autre joueur dont vous voulez échanger le rôle parmis :```" +
                                     "``````".join(self.newMembers) + "```")
                await self.wait()
            else:
                # Succeed to find category
                print("Succeed, second choice")
                await msg.author.send("Le deuxième joueur est : " + msg.content + ".")
                user = self.getMemberFromName(name=msg.content)
                saveRole = user.lastRole
                user.lastRole = self.firstChoice.lastRole
                self.firstChoice.lastRole = saveRole

    async def play(self, members, centralDeck):
        await super().play(members, centralDeck)
        if self.user not in ["gauche", "droite", "milieu"]:
            await self.user.send(
                "Vous êtes la Noiseuse. Écrivez le nom d'un des joueurs dont vous voulez échanger le rôle parmis :```"
                + "``````".join(self.getMembersName()) + "```")
            await self.wait()
            return self.lastRole

        else:
            await asyncio.sleep(random.randint(a=4, b=7))
