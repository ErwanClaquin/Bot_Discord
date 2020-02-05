from Werewolf.classForWerewolf.player import *


# =-=-=-= DOPPELGANGER CLASS =-=-=-= #
class Doppelganger(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)
        self.newRole = None

    async def play(self, members, centralDeck):
        await super().play(members, centralDeck)
        await self.user.send(
            "Vous êtes le Doppelgänger. Écrivez le nom d'une personne dont vous souhaitez copier la carte parmis ["
            + ", ".join(self.getMembersName()) + "].")

        await self.wait()
        member = self.getMemberFromName(self.choice)
        await self.user.send(member.user.name + " était un(e) " + member.firstRole)
        print(self.user.name, ":", self.newRole)
        self.lastRole = await member.__class__(user=self.user, firstRole=self.firstRole, botRef=self.bot).play(
            self.members)
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
