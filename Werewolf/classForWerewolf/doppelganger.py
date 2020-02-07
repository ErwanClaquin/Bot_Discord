from Werewolf.classForWerewolf.insomniac import *


# =-=-=-= DOPPELGANGER CLASS =-=-=-= #
class Doppelganger(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)
        self.newRole = None
        self.copyPlayer = None

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
            if self.newRole != "Insomniaque":
                await self.user.send(
                    "Vous êtes le Doppelgänger. Écrivez le nom d'une personne dont vous souhaitez copier la carte parmis "
                    + ", ".join(self.getMembersName()))

                await self.wait()
                member = self.getMemberFromName(self.choice)
                await self.user.send(member.user.name + " était un(e) " + member.firstRole)
                print(self.user.name, ":", self.newRole)
                self.copyPlayer = member.__class__(user=self.user, firstRole=self.firstRole, botRef=self.bot)
                if self.copyPlayer.__class__ == Insomniac:
                    self.newRole = "Insomniaque"
                    self.lastRole = "Insomniaque"
                else:
                    await self.copyPlayer.play(members=self.members, centralDeck=centralDeck)
                    self.lastRole = self.copyPlayer.lastRole
            else:
                self.copyPlayer.play(members=self.members, centralDeck=centralDeck)
        else:
            await asyncio.sleep(random.randint(a=4, b=7))
