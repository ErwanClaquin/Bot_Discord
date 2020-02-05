from Werewolf.classForWerewolf.werewolf import *


# =-=-=-= ALPHA WEREWOLF CLASS =-=-=-= #
class AlphaWerewolf(Werewolf):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    def getWolf(self):
        wolfs = []
        for member in self.members:
            if member.lastRole is not None:
                if member.lastRole in ["Loup-Garou", "Loup Alpha", "Loup Shamane"]:
                    wolfs.append(member.user.name)
            print("Wolfs are", str(wolfs))
            return wolfs

    def getMembersNameWithoutWolf(self):
        listMemberName = []
        for member in self.members:
            if member.user is not self.user and member.user.firstRole not in ["Loup-Garou", "Loup Alpha",
                                                                              "Loup Shamane", "Loup rêveur"]:
                listMemberName.append(member.user.name)
        random.shuffle(listMemberName)
        return listMemberName

    async def checkingMessage(self, msg):
        if msg.content not in self.getMembersNameWithoutWolf():
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

    async def play(self, members, centralDeck):
        await super().play(members, centralDeck)
        await self.user.send(
            "Vous êtes le loup Alpha. Sélectionnez un joueur parmis" + ", ".join(
                self.getMembersNameWithoutWolf()) + " pour le transformer en loup-garou.")
        await self.wait()
        member = self.getMemberFromName(self.choice)
        member.revealed = False
        member.lastRole = "Loup-Garou"
        print("Member", member.name, "is now a Werwolf.")
        return self.lastRole
