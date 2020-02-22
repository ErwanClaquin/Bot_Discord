from Werewolf.classForWerewolf.player import *


# =-=-=-= MINION CLASS =-=-=-= #
class Minion(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    def getWolf(self):
        wolfs = []
        for member in self.members:
            if member.firstRole in ["Loup-Garou", "Loup Alpha", "Loup Shamane", "Loup rêveur"] or member.newRole \
                    in ["Loup-Garou", "Loup Alpha", "Loup Shamane", "Loup rêveur"]:
                wolfs.append(member.user.name)
        print("Wolfs are", str(wolfs))
        return wolfs

    async def play(self, members, centralDeck):
        await super().play(members, centralDeck)
        if self.user not in ["gauche", "droite", "milieu"]:
            wolfs = self.getWolf()
            if len(wolfs) != 0:
                await self.user.send("Vous êtes le Sbire. Les loups sont :```" + "``````".join(wolfs) + "```")
            else:
                await self.user.send("Vous êtes le Sbire. Actuellement, il n'y a aucun loup.")

        else:
            await asyncio.sleep(random.randint(a=4, b=7))
