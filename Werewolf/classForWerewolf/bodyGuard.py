from Werewolf.classForWerewolf.player import *


# =-=-=-= BODYGUARD CLASS =-=-=-= #
class BodyGuard(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    async def play(self, members, centralDeck, courseOfTheGame):
        await super().play(members=members, centralDeck=centralDeck, courseOfTheGame=courseOfTheGame)
        if self.user not in ["gauche", "droite", "milieu"]:
            await self.user.send(
                "Vous êtes le garde du corps. La personne personne pour laquelle vous votez ne mourra pas lors du vote.")
            self.courseOfTheGame += ["```css\n" + self.user.name + " était le garde du corps.```"]

        else:
            self.courseOfTheGame += ["```css\nLe garde du corps était à/au " + self.user + ".```"]
