from classForWerewolf.player import *


# =-=-=-= DOPPELGANGER CLASS =-=-=-= #
class Diviner(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    async def reveal(self, user):
        if user.lastRole not in ["Loup-Garou", "Loup Alpha", "Loup Shamane", "Sbire", "Tanneur", "Loup rêveur"]:
            user.revealed = True
            await self.user.send(user.name + " est un " + user.lastRole + ", il sera donc révélé aux autres joueurs.")
        else:
            await self.user.send(
                user.name + " est un " + user.lastRole + ", il ne sera donc pas révélé aux autres joueurs.")
        self.courseOfTheGame += ["```css\n" + self.user.name + " était le divinateur, et à vu " + user.name + \
                                 " qui était un(e) " + user.lastRole + ".```"]

    async def checkingMessage(self, msg):
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
            member = self.getMemberFromName(self.choice)
            await self.reveal(user=member)

    async def play(self, members, centralDeck, courseOfTheGame):
        await super().play(members=members, centralDeck=centralDeck, courseOfTheGame=courseOfTheGame)
        if self.user not in ["gauche", "droite", "milieu"]:

            await self.user.send(
                "Vous êtes le Divinateur. Écrivez le nom d'une personne dont vous souhaitez révéler le rôle parmis ```"
                + "``````".join(self.getMembersName()) + "```")
            await self.wait()

        else:
            self.courseOfTheGame += [
                "```css\nLe divinateur était à/au " + self.user + ", le rôle n'a donc pas été joué.```"]
            await asyncio.sleep(random.randint(a=4, b=7))
