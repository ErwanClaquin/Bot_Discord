from Werewolf.classForWerewolf.player import *


# =-=-=-= SEER CLASS =-=-=-= #
class Thief(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    async def play(self, members, centralDeck):
        await super().play(members, centralDeck)
        await self.user.send(
            "Vous êtes le Voleur. Écrivez le nom d'une personne dont vous souhaitez copier la carte parmis ["
            + ", ".join(self.getMembersName()) + "].")
        await self.wait()
        user = self.getMemberFromName(self.choice)
        await self.user.send(user.name + " était un(e) " + user.lastRole)
        saveRole = self.lastRole
        self.lastRole = user.lastRole
        user.lastRole = saveRole
        return self.lastRole

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
