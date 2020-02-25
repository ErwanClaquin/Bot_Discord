from Werewolf.classForWerewolf.player import *


# =-=-=-= FREEMASSON CLASS =-=-=-= #
class Freemason(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    async def getFreemason(self):
        freemason = False
        for member in self.members:
            print(member.lastRole)
            if member.lastRole is "Franc-Maçon":
                await self.user.send(member.user.name + " est un autre franc-maçon.")
                freemason = True
        if not freemason:
            await self.user.send("Il n'y a pas d'autre franc-maçon parmis les joueurs.")

    async def play(self, members, centralDeck, courseOfTheGame):
        if self.user not in ["gauche", "droite", "milieu"]:
            await super().play(members=members, centralDeck=centralDeck, courseOfTheGame=courseOfTheGame)
            await self.user.send("Vous êtes un Franc-Maçon.")
            self.courseOfTheGame += ["```css\n" + self.user.name + " était un des Franc-Maçon.```"]
            await self.getFreemason()

        else:
            self.courseOfTheGame += ["```css\nUn des Franc-Maçon était à/au " + self.user + ".```"]
