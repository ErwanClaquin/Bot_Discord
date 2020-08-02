from classForWerewolf.player import *


# =-=-=-= SLEEPING WEREWOLF CLASS =-=-=-= #
class Hunter(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    async def death(self, channel, members):
        deadPlayer = []
        selfdead = await super().death(members=members, channel=channel)
        deadPlayer += selfdead
        await self.user.send(
            "La majoritée vous a visé ! Vengez-vous parmis :```" + "``````".join(self.getMembersName()) + "```")
        await self.wait()
        if self.choice == "#None":
            return None
        else:
            member = self.getMemberFromName(name=self.choice)
            if await member.isDead(channel=channel):
                deadPlayer += await member.death(channel=channel, members=members)
            return deadPlayer

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

    async def play(self, members, centralDeck, courseOfTheGame):
        await super().play(members=members, centralDeck=centralDeck, courseOfTheGame=courseOfTheGame)
        if self.user not in ["gauche", "droite", "milieu"]:
            await self.user.send("Vous êtes le chasseur. Vous pourrez tuer quelqu'un à votre mort.")
            self.courseOfTheGame += ["```css\n" + self.user.name + " était le Chasseur.```"]

        else:
            self.courseOfTheGame += ["```css\nLe Chasseur était à/au " + self.user + ".```"]
