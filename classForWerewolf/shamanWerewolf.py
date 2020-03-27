from classForWerewolf.werewolf import *


# =-=-=-= SHAMAN WEREWOLF CLASS =-=-=-= #
class ShamanWerewolf(Werewolf):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)
        self.playersWithoutWolfs = None

    async def checkingMessage(self, msg):
        if msg.content not in self.getMembersNameWithoutWolf():
            # Failed to find user
            print("Failed")
            await self.user.send("Erreur, impossible de trouver la personne visée. Veuillez réessayer parmis :```"
                                 + "``````".join(self.playersWithoutWolfs) + "```")
            await self.wait()
        else:
            # Succeed to find user
            print("Succeed")
            self.choice = msg.content
            await msg.author.send("Joueur choisi : " + self.choice + ".")

    async def play(self, members, centralDeck, courseOfTheGame):
        await super().play(members=members, centralDeck=centralDeck, courseOfTheGame=courseOfTheGame)
        if self.user not in ["gauche", "droite", "milieu"]:
            self.playersWithoutWolfs = self.getMembersNameWithoutWolf()
            if len(self.playersWithoutWolfs) != 0:
                await self.user.send(
                    "Vous êtes le loup Shaman. Sélectionnez un joueur parmis ```" + "``````".join(
                        self.playersWithoutWolfs) + "```pour voir son rôle.")
                await self.wait()
                member = self.getMemberFromName(self.choice)
                await self.user.send(member.user.name + " est un(e) " + member.lastRole)
                self.courseOfTheGame += ["```diff\n-" + self.user.name + " a observé " +
                                         member.user.name + " qui était un(e)" + member.lastRole + ".```"]
                print("Member", member.user.name, "is a ", member.lastRole)
                return self.lastRole
            else:
                await self.user.send(
                    "Vous êtes le loup Shamane. Actuellement, tous les joueurs sont des loups, vous ne pouvez donc pas en observer un.")

        else:
            await asyncio.sleep(random.randint(a=4, b=7))
