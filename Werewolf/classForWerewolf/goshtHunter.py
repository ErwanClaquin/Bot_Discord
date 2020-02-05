from Werewolf.classForWerewolf.player import *


# =-=-=-= GOSHTHUNTER CLASS =-=-=-= #
class GoshtHunter(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)
        self.firstChoice = None
        self.state = None

    async def play(self, members, centralDeck):
        await super().play(members, centralDeck)
        await self.user.send(
            "Vous êtes le chasseur de fantômes. Écrivez le nom d'une personne dont vous souhaitez observer la carte parmis ["
            + ", ".join(self.getMembersName()) +
            "]. Vous rejoindrez le camp d'un loup, d'un vampire ou d'un tanneur si vous le trouvez.")
        await self.wait()
        await self.user.send("Souhaitez vous regarder un deuxième rôles ? Répondez par ```Oui``` ou par ```Non```")
        await self.wait()
        return self.lastRole

    async def checkingMessage(self, msg):
        if self.state is None:
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
                await msg.author.send("Ce joueur est un(e) " + self.getMemberFromName(self.choice).lastRole + ".")
                self.state = "FirstLook"

        elif self.state == "FirstLook":
            if msg.content == "Non":
                # Failed to find user
                print("Succeed, don't want to look further role.")

            elif msg.content == "Oui":
                # Succeed to find user
                print("Succeed, want to look further role.")
                self.state = "SecondLook"
                await self.user.send("Écrivez le nom d'une personne dont vous souhaitez observer la carte parmis ["
                                     + ", ".join(self.getMembersName()) +
                                     "]. Vous rejoindrez le camp d'un loup, d'un vampire ou d'un tanneur si vous le trouvez.")
                await self.wait()

            else:
                print("Failed.")
                await self.user.send("Erreur, répondez par ```Oui``` ou par ```Non```")
                await self.wait()

        elif self.state == "SecondLook":
            # Failed to find user
            print("Failed")
            await self.user.send("Erreur, impossible de trouver la personne visée. Veuillez réessayer parmis ["
                                 + ", ".join(self.getMembersName()) + "].")
            await self.wait()
        else:
            # Succeed to find user
            print("Succeed")
            self.choice = msg.content
            await msg.author.send("Ce joueur est un(e) " + self.getMemberFromName(self.choice).lastRole + ".")
