from Werewolf.classForWerewolf.player import *


# =-=-=-= SEER CLASS =-=-=-= #
class Thief(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    async def checkingMessage(self, msg):
        if msg.content not in self.getMembersName():
            # Failed to find user
            print("Failed")
            await self.user.send("Erreur, impossible de trouver la personne visée. Veuillez réessayer parmis ["
                                 + ", ".join(self.getMembersName()) + "].")
            await self.wait()
        else:
            # Succeed to find user
            print("Succeed")
            self.choice = msg.content
            await msg.author.send("Joueur choisi : " + self.choice + ".")

    async def play(self, members, centralDeck):
        await super().play(members, centralDeck)
        if self.user not in ["gauche", "droite", "milieu"]:
            await self.user.send(
                "Vous êtes le Voleur. Écrivez le nom d'une personne dont vous souhaitez copier la carte parmis ["
                + ", ".join(self.getMembersName()) + "].")
            await self.wait()
            player = self.getMemberFromName(self.choice)
            await self.user.send(player.user.name + " était un(e) " + player.lastRole)
            saveRole = self.lastRole
            self.lastRole = player.lastRole
            player.lastRole = saveRole

        else:
            await asyncio.sleep(random.randint(a=4, b=7))
