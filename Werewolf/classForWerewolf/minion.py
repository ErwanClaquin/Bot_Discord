from Werewolf.classForWerewolf.player import *


# =-=-=-= MINION CLASS =-=-=-= #
class Minion(Player):
    def __init__(self, user, firstRole, botRef):
        super().__init__(user=user, firstRole=firstRole, botRef=botRef)

    def getWolf(self):
        wolfs = []
        for member in self.members:
            if member.lastRole is not None:
                if member.lastRole in ["Loup-Garou", "Loup Alpha", "Loup Shamane", "Loup rêveur"]:
                    wolfs.append(member.user.name)
            print("Wolfs are", str(wolfs))
            return wolfs

    async def play(self, members, centralDeck):
        await super().play(members, centralDeck)
        self.user.send("Vous êtes le Sbire. Les loups sont : " + ", ".join(self.getWolf()))
        return self.lastRole()
