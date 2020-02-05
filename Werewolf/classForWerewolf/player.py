from botBasics import *
import random


# =-=-=-= MOTHER CLASS =-=-=-= #
class Player:
    def __init__(self, user, firstRole, botRef):
        self.bot = botRef
        self.user = user
        self.firstRole = firstRole
        self.lastRole = firstRole
        self.members = None
        self.centralDeck = None
        self.choice = None
        self.protected = False
        self.revealed = False

    async def play(self, members, centralDeck):
        self.members = members
        self.centralDeck = centralDeck

    def getMembersName(self):
        listMemberName = []
        for member in self.members:
            if member.user is not self.user:
                listMemberName.append(member.user.name)
        random.shuffle(listMemberName)
        return listMemberName

    def check(self, msg):
        print("Checked ! : ", msg.content, self.user.name)
        if not is_me(msg):
            print("Message from user : ", msg.author)
            if msg.channel.id == self.user.dm_channel.id:
                print("Message from DM of : ", msg.author, ". Should be similar for user : ", self.user)
                return True

    async def checkingMessage(self, msg):
        pass

    async def wait(self):
        msg = await self.bot.wait_for('message', check=self.check)
        print("Attempt to find user")
        await self.checkingMessage(msg)
        return msg

    def getMemberFromName(self, name):
        for member in self.members:
            if name in member.user.name:
                return member

    async def on_death(self, members, channel):
        if self.protected:
            await channel.send(self.user.name + " a été protégé. Il ne meurt donc pas.")
        return not self.protected

    def getRoleFromDeck(self, position=""):
        for role in self.centralDeck:
            if role.user == position:
                return role
        return None