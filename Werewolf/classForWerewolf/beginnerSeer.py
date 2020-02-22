from Werewolf.classForWerewolf.player import *


# =-=-=-= SEER CLASS =-=-=-= #
class BeginnerSeer(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    async def checkingMessage(self, msg):
        if self.getRoleFromDeck(position=msg.content) is not None:
            print("Succeed")
            await self.user.send(
                "Il y a " + self.getRoleFromDeck(position=msg.content).lastRole + " à la position choisie.")
        else:
            print("Failed")
            await self.user.send("Erreur, impossible de trouver le rôle visé. Veuillez réessayer.")
            await self.wait()

    async def play(self, members, centralDeck):
        await super().play(members, centralDeck)

        if self.user not in ["gauche", "droite", "milieu"]:
            await self.user.send(
                "Vous êtes l'apprentie voyante. Écrivez une position parmis :```gauche``````droite``````milieu```pour voir une des cartes.")
            await self.wait()

        else:
            await asyncio.sleep(random.randint(a=4, b=7))
