from Werewolf.classForWerewolf.player import *


# =-=-=-= WEREWOLF CLASS =-=-=-= #
class Werewolf(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    def getWolf(self):
        wolfs = []
        print("Get wolf")
        for member in self.members:
            if member.lastRole in ["Loup-Garou", "Loup Alpha", "Loup Shamane"] and member.user != self.user:
                wolfs.append(member.user.name)
        print("Wolfs are", str(wolfs))
        return wolfs

    async def getSleepingWolf(self):
        sleepingWolf = False
        for member in self.members:
            if member.lastRole is not None:
                if member.lastRole is "Loup rêveur":
                    await self.user.send(member.user.name + " est un loup rêveur.")
                    sleepingWolf = True
        if not sleepingWolf:
            await self.user.send("Il n'y a pas de loup rêveur parmis les joueurs.")

    async def checkingMessage(self, msg):
        if msg.content not in ["gauche", "droite", "milieu"]:
            # Failed to find user
            print("Failed")
            await self.user.send(
                "Erreur, impossible de trouver la postion visée. Veuillez réessayer parmis :```gauche``````droite``````milieu```")
            await self.wait()
        else:
            # Succeed to find user
            print("Succeed")
            self.choice = msg.content
            await msg.author.send(
                "Le rôle à/au " + self.choice + " est un(e) " + self.getRoleFromDeck(
                    position=self.choice).lastRole + ".")
            self.courseOfTheGame += ["```diff\n-" + self.user.name + "était le seul des loups et a observé à/au " +
                                     self.choice + "ou il y avait un(e) " + self.getRoleFromDeck(position=self.choice).lastRole
                                     + "```"]

    async def play(self, members, centralDeck, courseOfTheGame):
        await super().play(members=members, centralDeck=centralDeck, courseOfTheGame=courseOfTheGame)
        if self.user not in ["gauche", "droite", "milieu"]:

            wolfs = self.getWolf()
            if len(wolfs) == 0:
                await self.user.send("Vous êtes un " + self.firstRole +
                                     ", et le seul des loups-Garous. Vous pouvez choisir une carte du deck parmis :```gauche``````droite``````milieu```")
                await self.wait()

            else:
                await self.user.send("Vous êtes un " + self.firstRole + ". Les autres loups sont :```" +
                                     "``````".join(wolfs) + "```")
                self.courseOfTheGame += ["```diff\n-" + self.user.name + " était un " + self.firstRole + ".```"]

            await self.getSleepingWolf()

        else:
            await asyncio.sleep(random.randint(a=4, b=7))
            self.courseOfTheGame += ["```diff\n-Le " + self.firstRole + " était à/au " + self.user + ".```"]
