from Werewolf.classForWerewolf.player import *


# =-=-=-= BODYGUARD CLASS =-=-=-= #
class BodyGuard(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    async def play(self, members, centralDeck):
        await super().play(members, centralDeck)
        if self.user not in ["gauche", "droite", "milieu"]:
            await self.user.send(
                "Vous êtes le garde du corps. La personne personne pour laquelle vous votez ne mourra pas lors du vote.")

        else:
            await asyncio.sleep(random.randint(a=4, b=7))
