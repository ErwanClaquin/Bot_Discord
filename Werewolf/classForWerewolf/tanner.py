from Werewolf.classForWerewolf.player import *


# =-=-=-= TANNER CLASS =-=-=-= #
class Tanner(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    async def play(self, members, centralDeck, courseOfTheGame):
        await super().play(members=members, centralDeck=centralDeck, courseOfTheGame=courseOfTheGame)
        if self.user not in ["gauche", "droite", "milieu"]:
            await self.user.send("Vous êtes le tanneur. Vous souhaitez mourir lors de la décision du village.")
            self.courseOfTheGame += ["```Fix\n#" + self.user.name + " était le Tanneur.```"]

        else:
            await asyncio.sleep(random.randint(a=4, b=7))
            self.courseOfTheGame += ["```Fix\n#Le Tanneur était à/au " + self.user.name + ".```"]
