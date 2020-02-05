from Werewolf.classForWerewolf.player import *


# =-=-=-= SEER CLASS =-=-=-= #
class BeginnerSeer(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    async def play(self, members, centralDeck):
        await super().play(members, centralDeck)
        await self.user.send(
            "Vous êtes l'apprentie voyante. Écrivez une position parmis [gauche, droite, milieu} pour voir une des carte.")
        await self.wait()
        return self.lastRole

    async def checkingMessage(self, msg):
        if self.getRoleFromDeck(position=msg.content) is not None:
            print("Succeed")
            await self.user.send(
                "Il y a " + self.getRoleFromDeck(position=msg.content) + " à la position choisie.")
        else:
            print("Failed")
            await self.user.send("Erreur, impossible de trouver le rôle visé. Veuillez réessayer.")
            await self.wait()
