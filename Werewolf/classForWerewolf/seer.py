from Werewolf.classForWerewolf.player import *


# =-=-=-= SEER CLASS =-=-=-= #
class Seer(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)
        self.state = None
        self.firstChoice = None

    async def play(self, members, centralDeck):
        await super().play(members, centralDeck)
        await self.user.send(
            "Vous êtes la voyante. Écrivez ```joueurs``` si vous souhaitez voir une carte d'un joueur ou ```deck``` si vous souhaitez voir deux cartes au centre.")

        await self.wait()
        return self.lastRole

    async def checkingMessage(self, msg):
        if self.state is None:
            if msg.content not in ["joueurs", "deck"]:
                # Failed to find category
                print("Failed")
                await self.user.send(
                    "Erreur, impossible de trouver la catégorie. Écrivez ```joueurs``` si vous souhaitez voir une carte d'un joueur ou ```deck``` si vous souhaitez voir deux cartes au centre.")
                await self.wait()
            else:
                # Succeed to find category
                print("Succeed")
                self.state = msg.content
                await msg.author.send("Catégorie choisie : " + msg.content + ".")
                await self.wait()

        elif self.state == "joueurs":
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
                member = self.getMemberFromName(self.choice)
                await self.user.send(member.user.name + " est un(e) " + member.lastRole)
                print("Member", member.name, "is a ", member.lastRole)

        elif self.state == "deck":
            if self.firstChoice == msg.content:
                print("Already seen this role.")
                await self.user.send("Vous avez déjà choisi de regarder ce rôle. Veuillez réessayer.")
                await self.wait()
            else:
                if self.getRoleFromDeck(position=msg.content) is not None:
                    print("Succeed")
                    await self.user.send(
                        "Il y a " + self.getRoleFromDeck(position=msg.content) + " à la position choisie.")
                    if self.firstChoice is None:
                        await self.user.send("Choisissez une autre position :")
                        await self.wait()
                    else:
                        print("End of look.")
                else:
                    print("Failed")
                    await self.user.send("Erreur, impossible de trouver le rôle visé. Veuillez réessayer.")
                    await self.wait()
