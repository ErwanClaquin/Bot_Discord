from Werewolf.classForWerewolf.player import *


# =-=-=-= SLEEPING WEREWOLF CLASS =-=-=-= #
class SleepingWerewolf(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    async def play(self, members, centralDeck):
        await super().play(members=members, centralDeck=centralDeck)
        if self.user not in ["gauche", "droite", "milieu"]:
            self.user.send(
                "Vous êtes le loup-rêveur. Vous ne savez donc pas qui sont les autres loups, mais eux le savent.")

        else:
            await asyncio.sleep(random.randint(a=4, b=7))
