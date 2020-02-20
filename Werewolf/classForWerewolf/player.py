from botBasics import *
import random


# =-=-=-= MOTHER CLASS =-=-=-= #
class Player:
    def __init__(self, user, firstRole, botRef):
        self.bot = botRef
        self.user = user
        self.firstRole = firstRole
        self.newRole = None  # Only for Doppel
        self.lastRole = firstRole
        self.members = None
        self.centralDeck = None
        self.choice = None
        self.protected = False
        self.revealed = False

    async def play(self, members, centralDeck):
        print(self.user, " : ", self.firstRole)
        self.members = members
        self.centralDeck = centralDeck

    def getMembersName(self):
        listMemberName = []
        for member in self.members:
            if member.user is not self.user:
                name = "```" + member.user.name + "```"
                listMemberName.append(name)
        random.shuffle(listMemberName)
        return listMemberName

    def check(self, msg):
        if not is_me(msg):
            if msg.channel.id == self.user.dm_channel.id:
                print("Message from", msg.author.name + "'s DM")
                return True
        return False

    async def checkingMessage(self, msg):
        pass

    async def wait(self):
        msg = await self.bot.wait_for('message', check=self.check)
        print("Attempt to find user or role :", msg.content)
        await self.checkingMessage(msg)
        return msg

    def getMemberFromName(self, name):
        for member in self.members:
            if name in member.user.name:
                return member

    async def isDead(self, channel):
        if self.protected:
            await channel.send(self.user.name + " a été protégé. Il ne meurt donc pas.")
        return not self.protected

    async def death(self, channel):
        await channel.send(self.user.name + " est mort ! C'était un(e) " + self.lastRole)
        return [self]

    def getRoleFromDeck(self, position=""):
        for role in self.centralDeck:
            if role.user == position:
                return role
        return None
