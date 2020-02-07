from Werewolf.classForWerewolf.player import *


# =-=-=-= DOPPELGANGER CLASS =-=-=-= #
class Diviner(Player):
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

    async def reveal(self, user):
        if user.lastRole in ["Loup-Garou", "Loup Alpha", "Loup Shamane", "Sbire", "Tanneur", "Loup rêveur"]:
            user.revealed = True
            await self.user.send(user.name + " est un " + user.lastRole + ", il sera donc révélé aux autres joueurs.")
        else:
            await self.user.send(
                user.name + " est un " + user.lastRole + ", il ne sera donc pas révélé aux autres joueurs.")

    async def play(self, members, centralDeck):
        await super().play(members, centralDeck)
        if self.user not in ["gauche", "droite", "milieu"]:

            await self.user.send(
                "Vous êtes le Divinateur. Écrivez le nom d'une personne dont vous souhaitez révéler le rôle parmis ["
                + ", ".join(self.getMembersName()) + "].")
            await self.wait()
            member = self.getMemberFromName(self.choice)
            member.revealed = True

        else:
            await asyncio.sleep(random.randint(a=4, b=7))
