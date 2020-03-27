from classForWerewolf.player import *


# =-=-=-= SLEEPING WEREWOLF CLASS =-=-=-= #
class SleepingWerewolf(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    async def playAudio(self, guild, start=True):
        pass

    async def play(self, members, centralDeck, courseOfTheGame):
        await super().play(members=members, centralDeck=centralDeck, courseOfTheGame=courseOfTheGame)
        if self.user not in ["gauche", "droite", "milieu"]:
            await self.user.send(
                "Vous êtes le loup-rêveur. Vous ne savez donc pas qui sont les autres loups, mais eux le savent.")
            self.courseOfTheGame += ["```diff\n-" + self.user.name + " était le loup rêveur.```"]

        else:
            self.courseOfTheGame += ["```diff\n-Le loup rêveur était à/au " + self.user + ".```"]
