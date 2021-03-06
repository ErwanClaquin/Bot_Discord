from classForWerewolf.player import *


# =-=-=-= FREEMASSON CLASS =-=-=-= #
class Freemason(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    async def getFreemason(self):
        freemason = False
        print("\nSearch an other Freemason\n")

        for member in self.members:
            print("" + str(member.user.name) + " : " + str(member.lastRole))
            if (member.lastRole == "Franc-Maçon" or member.newRole == "Franc-Maçon") \
                    and self.user.name != member.user.name:
                print("found an other Freemason")
                await self.user.send(member.user.name + " est un autre franc-maçon.")
                freemason = True
        if not freemason:
            await self.user.send("Il n'y a pas d'autre franc-maçon parmis les joueurs.")

    async def playAudio(self, guild, start=True):
        pass

    async def play(self, members, centralDeck, courseOfTheGame):
        await super().play(members=members, centralDeck=centralDeck, courseOfTheGame=courseOfTheGame)
        if self.user not in ["gauche", "droite", "milieu"]:
            await super().play(members=members, centralDeck=centralDeck, courseOfTheGame=courseOfTheGame)
            await self.user.send("Vous êtes un Franc-Maçon.")
            self.courseOfTheGame += ["```css\n" + self.user.name + " était un des Franc-Maçon.```"]
            await self.getFreemason()

        else:
            self.courseOfTheGame += ["```css\nUn des Franc-Maçon était à/au " + self.user + ".```"]
