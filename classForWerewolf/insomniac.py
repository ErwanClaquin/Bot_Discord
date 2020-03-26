from classForWerewolf.player import *


# =-=-=-= SEER CLASS =-=-=-= #
class Insomniac(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    async def play(self, members, centralDeck, courseOfTheGame):
        await super().play(members=members, centralDeck=centralDeck, courseOfTheGame=courseOfTheGame)
        if self.user not in ["gauche", "droite", "milieu"]:
            await self.user.send("Vous êtes l'Insomniaque. Votre rôle final est un(e) " + self.lastRole)
            self.courseOfTheGame += [
                "```css\n" + self.user.name + " était l'Insomniaque est s'est réveillé en " + self.lastRole + ".```"]

        else:
            self.courseOfTheGame += [
                "```css\nL'Insomniaque était à/au " + self.user + ", le rôle n'a donc pas été joué.```"]
