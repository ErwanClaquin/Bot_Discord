from Werewolf.classForWerewolf.player import *


# =-=-=-= WEREWOLF CLASS =-=-=-= #
class Werewolf(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    def getWolf(self):
        wolfs = []
        for member in self.members:
            if member.lastRole in ["Loup-Garou", "Loup Alpha", "Loup Shamane"] and member != self:
                wolfs.append(member.user.name)
            print("Wolfs are", str(wolfs))
            return wolfs

    async def getSleepingWolf(self):
        sleepingWolf = False
        for member in self.members:
            if member.lastRole is not None:
                if member.lastRole is "Loup rêveur":
                    await self.user.send(member.user.name + " est un loup rêveur.")
                    sleepingWolf = True
        if not sleepingWolf:
            await self.user.send("Il n'y a pas de loup rêveur parmis les joueurs.")

    async def play(self, members, centralDeck):
        await super().play(members, centralDeck)
        wolfs = self.getWolf()
        await self.user.send("Vous êtes un des loups-Garous. Les autres loups sont :" + str(", ".join(wolfs)))

        if len(wolfs) == 0:
            await self.user.send(
                "Vous êtes le seul des loups-Garous. Vous pouvez choisir une carte parmis celle de gauche, droite, ou au centre.")
            await self.wait()
        else:
            await self.user.send("Vous êtes un des loups-Garous. Les autres loups sont :" + str(", ".join(wolfs)))

        await self.getSleepingWolf()
        return self.lastRole()

    async def checkingMessage(self, msg):
        if msg.content not in ["gauche", "droite", "centre"]:
            # Failed to find user
            print("Failed")
            await self.user.send("Erreur, impossible de trouver la personne visée. Veuillez réessayer parmis ["
                                 + ", ".join(self.getMembersName()) + "].")
            await self.wait()
        else:
            # Succeed to find user
            print("Succeed")
            self.choice = msg.content
            await msg.author.send("Le rôle de " + self.choice + " est un(e) " + self.getRoleFromDeck().lastRole + ".")
