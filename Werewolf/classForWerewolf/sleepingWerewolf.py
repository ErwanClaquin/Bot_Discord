from Werewolf.classForWerewolf.player import *


# =-=-=-= SLEEPING WEREWOLF CLASS =-=-=-= #
class SleepingWerewolf(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    async def play(self, members, centralDeck):
        await super().play(members=members, centralDeck=centralDeck)
        self.user.send(
            "Vous êtes le loup-rêveur. Vous ne savez donc pas qui sont les autres loups, mais eux le savent.")
        return self.lastRole
