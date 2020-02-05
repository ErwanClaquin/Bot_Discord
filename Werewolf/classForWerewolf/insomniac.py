from Werewolf.classForWerewolf.player import *


# =-=-=-= SEER CLASS =-=-=-= #
class Insomniac(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    async def play(self, members, centralDeck):
        await super().play(members, centralDeck)
        await self.user.send("Vous êtes l'Insomniaque. Votre rôle final est un(e) " + self.lastRole)
        return self.lastRole
