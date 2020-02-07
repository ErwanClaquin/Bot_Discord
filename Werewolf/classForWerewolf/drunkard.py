from Werewolf.classForWerewolf.player import *


# =-=-=-= SEER CLASS =-=-=-= #
class Drunkard(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    async def checkingMessage(self, msg):
        if msg.content not in ["gauche", "droite", "milieu"]:
            # Failed to find user
            print("Failed")
            await self.user.send("Erreur, impossible de trouver la personne visée. Veuillez réessayer parmis ["
                                 + ", ".join(self.getMembersName()) + "].")
            await self.wait()
        else:
            # Succeed to find user
            print("Succeed")
            self.choice = msg.content
            await msg.author.send("Position choisie : " + self.choice + ".")

    async def play(self, members, centralDeck):
        await super().play(members, centralDeck)
        if self.user not in ["gauche", "droite", "milieu"]:
            await self.user.send(
                "Vous êtes le Soûlard. Écrivez le nom d'une personne dont vous souhaitez copier la carte parmis [gauche, droite, milieu].")
            await self.wait()
            deck = self.getRoleFromDeck(self.choice)
            saveRole = self.lastRole
            self.lastRole = deck.lastRole
            deck.lastRole = saveRole

        else:
            await asyncio.sleep(random.randint(a=4, b=7))