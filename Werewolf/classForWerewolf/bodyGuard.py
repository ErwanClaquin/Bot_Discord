from Werewolf.classForWerewolf.player import *


# =-=-=-= BODYGUARD CLASS =-=-=-= #
class BodyGuard(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    async def play(self, members, centralDeck):
        await super().play(members, centralDeck)
        self.user.send("Vous êtes le garde du corps. Sélectionner un joueur parmis " + ", ".join(
            self.getMembersName()) + ". Cette personne ne pourra pas mourir lors du vote.")
        await self.wait()
        member = self.getMemberFromName(self.choice)
        print(self.user.name, " had been protected.")
        member.user.protected = True
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
            await msg.author.send("Le joueur : " + self.choice + ".")
