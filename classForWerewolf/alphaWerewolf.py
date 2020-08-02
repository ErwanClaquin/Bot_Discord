from classForWerewolf.werewolf import *


# =-=-=-= ALPHA WEREWOLF CLASS =-=-=-= #
class AlphaWerewolf(Werewolf):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    async def checkingMessage(self, msg):
        if msg.content not in self.getMembersNameWithoutWolf():
            # Failed to find user
            print("Failed")
            await self.user.send("Erreur, impossible de trouver la personne visée. Veuillez réessayer parmis :```"
                                 + "``````".join(self.getMembersName()) + "```")
            await self.wait()
        else:
            # Succeed to find user
            print("Succeed")
            self.choice = msg.content
            member = self.getMemberFromName(self.choice)
            member.revealed = False
            member.lastRole = "Loup-Garou"
            print("Member", member.user.name, "is now a Werwolf.")
            await msg.author.send("Joueur choisi : " + self.choice + ".")
            self.courseOfTheGame += ["```diff\n-" + self.user.name + " a transformé " +
                                     self.choice + " en Loup-Garou.```"]

    async def play(self, members, centralDeck, courseOfTheGame):
        await super().play(members=members, centralDeck=centralDeck, courseOfTheGame=courseOfTheGame)

        if self.user not in ["gauche", "droite", "milieu"]:
            playersWithoutWolfs = self.getMembersNameWithoutWolf()
            if len(playersWithoutWolfs) != 0:
                await self.user.send(
                    "Vous êtes le loup Alpha. Sélectionnez un joueur parmis :```" + "``````".join(
                        playersWithoutWolfs) + "```pour le transformer en loup-garou.")
                await self.wait()

            else:
                await self.user.send(
                    "Vous êtes le loup Alpha. Actuellement, tous les joueurs sont des loups, vous ne pouvez donc pas "
                    "en transformer un.")

        else:
            await asyncio.sleep(random.randint(a=4, b=7))
