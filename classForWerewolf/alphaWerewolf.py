from classForWerewolf.werewolf import *


# =-=-=-= ALPHA WEREWOLF CLASS =-=-=-= #
class AlphaWerewolf(Werewolf):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    def getMembersNameWithoutWolf(self):
        listMemberName = []
        for member in self.members:
            if member.user is not self.user and member.firstRole not in ["Loup-Garou", "Loup Alpha",
                                                                         "Loup Shamane", "Loup rêveur"]:
                listMemberName.append(member.user.name)
        random.shuffle(listMemberName)
        return listMemberName

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
            await msg.author.send("Joueur choisi : " + self.choice + ".")
            self.courseOfTheGame += ["```diff\n-" + self.user.name + " a transformé " +
                                     self.choice + " en Loup-Garou.```"]

    async def play(self, members, centralDeck, courseOfTheGame):
        await super().play(members=members, centralDeck=centralDeck, courseOfTheGame=courseOfTheGame)

        if self.user not in ["gauche", "droite", "milieu"]:
            playersWithourWolfs = self.getMembersNameWithoutWolf()
            if len(playersWithourWolfs) != 0:
                await self.user.send(
                    "Vous êtes le loup Alpha. Sélectionnez un joueur parmis :```" + "``````".join(
                        playersWithourWolfs) + "```pour le transformer en loup-garou.")
                await self.wait()
                member = self.getMemberFromName(self.choice)
                member.revealed = False
                member.lastRole = "Loup-Garou"
                print("Member", member.user.name, "is now a Werwolf.")
            else:
                await self.user.send(
                    "Actuellement, tous les joueurs sont des loups, vous ne pouvez donc pas en transformer un.")

        else:
            await asyncio.sleep(random.randint(a=4, b=7))
