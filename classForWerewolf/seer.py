from classForWerewolf.player import *


# =-=-=-= SEER CLASS =-=-=-= #
class Seer(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)
        self.state = None
        self.firstChoice = None
        self.newList = ["gauche", "droite", "milieu"]

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
                if msg.content == "joueurs":
                    await self.user.send("Écrivez le nom d'une personne dont vous souhaitez voir la carte parmis :```"
                                         + "``````".join(self.getMembersName()) + "```")
                else:
                    await self.user.send(
                        " Écrivez une position parmis ```gauche``````droite``````milieu```pour voir une des carte.")
                await self.wait()

        elif self.state == "joueurs":
            if msg.content not in self.getMembersName():
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
                player = self.getMemberFromName(self.choice)
                await self.user.send(player.user.name + " est un(e) " + player.lastRole)
                self.courseOfTheGame += ["```css\n" + self.user.name + " était la sorcière et a observé " +
                                         player.user.name + " qui était un(e) " + player.lastRole + ".```"]
                print("Member", player.user.name, "is a ", player.lastRole)

        elif self.state == "deck":
            if self.firstChoice == msg.content:
                print("Already seen this role.")
                await self.user.send(
                    "Vous avez déjà choisi de regarder ce rôle. Veuillez réessayer parmis :```" + "``````".join(
                        self.newList) + "```")
                await self.wait()
            else:
                if self.getRoleFromDeck(position=msg.content) is not None:
                    print("Succeed")
                    await self.user.send(
                        "Il y a " + self.getRoleFromDeck(position=msg.content).lastRole + " à la position choisie.")
                    if self.firstChoice is None:
                        self.firstChoice = msg.content
                        self.newList.remove(self.firstChoice)
                        await self.user.send(
                            "Choisissez une autre position parmis :```" + "``````".join(self.newList) + "```")
                        await self.wait()
                    else:
                        self.courseOfTheGame += ["```css\n" + self.user.name + " était la sorcière et a observé à/au " +
                                                 self.firstChoice + " où il y avait un(e) " +
                                                 self.getRoleFromDeck(position=self.firstChoice) + " ainsi qu'à/au" +
                                                 msg.content + " où il y avait un(e)" +
                                                 self.getRoleFromDeck(position=self.firstChoice) + ".```"]
                        print("End of look.")
                else:
                    print("Failed")
                    await self.user.send(
                        "Erreur, impossible de trouver le rôle visé. Veuillez réessayer parmis ```gauche``````droite``````milieu```")
                    await self.wait()

    async def play(self, members, centralDeck, courseOfTheGame):
        await super().play(members=members, centralDeck=centralDeck, courseOfTheGame=courseOfTheGame)
        if self.user not in ["gauche", "droite", "milieu"]:
            await self.user.send(
                "Vous êtes la voyante. Écrivez :```joueurs```si vous souhaitez voir une carte d'un joueur ou :```deck```si vous souhaitez voir deux cartes au centre.")
            await self.wait()

        else:
            await asyncio.sleep(random.randint(a=4, b=7))
            self.courseOfTheGame += ["```css\nLa Sorcière était à/au " + self.user +
                                     ", le rôle n'a donc pas été joué.```"]
