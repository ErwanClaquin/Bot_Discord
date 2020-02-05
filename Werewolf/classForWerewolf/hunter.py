from Werewolf.classForWerewolf.player import *


# =-=-=-= SLEEPING WEREWOLF CLASS =-=-=-= #
class Hunter(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    async def play(self, members, centralDeck):
        await super().play(members=members, centralDeck=centralDeck)
        self.user.send(
            "Vous êtes le chasseur. Vous pourrez tuer quelqu'un à votre mort.")
        return self.lastRole

    async def on_death(self, members, channel):
        deadPlayer = []
        dead = await super().on_death(members=members, channel=channel)
        if dead is not None:
            deadPlayer.append(dead)
        else:
            await self.user.send(
                "La majoritée vous a visé ! Vengez-vous parmis " + ", ".join(self.getMembersName()) + ".")
            await self.wait()
            member = await self.getMemberFromName(name=self.choice)
            dead = member.on_death(members=members)
            if dead is not None:
                deadPlayer.append(dead)
        if len(deadPlayer) == 0:
            return None
        else:
            return deadPlayer

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
