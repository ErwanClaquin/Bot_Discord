from classForWerewolf.player import *


# =-=-=-= GOSHTHUNTER CLASS =-=-=-= #
class GoshtHunter(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)
        self.state = None
        self.newChoice = None

    async def checkingMessage(self, msg):
        if self.state is None:
            if msg.content not in self.getMembersName():
                # Failed to find user
                print("Failed")
                await self.user.send("Erreur, impossible de trouver la personne visée. Veuillez réessayer parmis :```"
                                     + "``````".join(self.getMembersName()) + "```")
                await self.wait()
            else:
                # Succeed to find user
                print("Succeed")
                self.choice = self.getMemberFromName(name=msg.content)
                await msg.author.send("Ce joueur est un(e) " + self.choice.lastRole + ".")
                self.state = "FirstLook"
                self.courseOfTheGame += ["```Markdown\n#" + self.user + " était le chasseur de fantôme et a vu " +
                                         self.choice + " qui était un(e) " +
                                         self.getMemberFromName(self.choice).lastRole + ".```"]
                if self.choice.lastRole in ["Loup-Garou", "Loup Alpha", "Loup Shamane"]:
                    await self.user.send("Vous vous transformez donc en Loup-Garou.")
                    self.lastRole = "Loup-Garou"
                if self.choice.lastRole in ["Tanneur"]:
                    await self.user.send("Vous vous transformez donc en Tanneur.")
                    self.lastRole = "Tanneur"
                else:
                    await self.user.send(
                        "Souhaitez vous regarder un deuxième rôle ? Répondez par ```#Oui``` ou par ```#Non```")
                    await self.wait()

        elif self.state == "FirstLook":
            if msg.content == "#Non":
                # Suceeed
                print("Succeed, don't want to look further role.")

            elif msg.content == "#Oui":
                # Succeed to find user
                print("Succeed, want to look further role.")
                self.state = "SecondLook"
                self.newChoice = self.getMembersName().copy()
                self.newChoice.remove(self.getMemberFromName(self.choice).user.name)
                await self.user.send("Écrivez le nom d'une personne dont vous souhaitez observer la carte parmis ```"
                                     + "``````".join(self.newChoice) +
                                     "```Vous rejoindrez le camp d'un loup, d'un vampire ou d'un tanneur si vous le trouvez.")
                await self.wait()

            else:
                print("Failed.")
                await self.user.send("Erreur, répondez par ```#Oui``` ou par ```#Non```")
                await self.wait()

        elif self.state == "SecondLook":
            if msg.content not in self.getMembersName():
                # Failed to find user
                print("Failed")
                await self.user.send("Erreur, impossible de trouver la personne visée. Veuillez réessayer parmis ```"
                                     + "``````".join(self.newChoice) + "```")
                await self.wait()
            else:
                # Succeed to find user
                print("Succeed")
                self.choice = msg.content
                await msg.author.send("Ce joueur est un(e) " + self.getMemberFromName(self.choice).lastRole + ".")
                self.courseOfTheGame += ["```Markdown\n#" + self.user.name + " a aussi vu " + self.choice +
                                         " qui était un(e) " + self.getMemberFromName(self.choice).lastRole + ".```"]

    async def play(self, members, centralDeck, courseOfTheGame):
        await super().play(members=members, centralDeck=centralDeck, courseOfTheGame=courseOfTheGame)

        if self.user not in ["gauche", "droite", "milieu"]:
            await self.user.send(
                "Vous êtes le chasseur de fantômes. Écrivez le nom d'une personne dont vous souhaitez observer la carte parmis ```"
                + "``````".join(self.getMembersName()) +
                "```Vous rejoindrez le camp d'un loup, d'un vampire ou d'un tanneur si vous le trouvez.")
            await self.wait()

        else:
            await asyncio.sleep(random.randint(a=8, b=14))
            self.courseOfTheGame += ["```css\nLe chasseur de fantôme était à/au " + self.user +
                                     ", le rôle n'a donc pas été joué.```"]
