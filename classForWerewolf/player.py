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
        self.courseOfTheGame = list()

    async def playAudio(self, guild, start=True):
        path = "./classForWereWolf/AudioClasses/"
        for voiceClient in bot.voice_clients:
            if voiceClient.guild == guild:
                print("Check voiceClient.is_playing() for start==", start)
                while voiceClient.is_playing():
                    await asyncio.sleep(1)
                print("Not playing anymore.")
                if start:
                    audioSource = discord.FFmpegPCMAudio(
                        "./classForWereWolf/AudioClasses/" + self.__class__.__name__ + "Description.mp3")
                    voiceClient.play(source=audioSource, after=None)
                else:
                    audioSource = discord.FFmpegPCMAudio(
                        "./classForWereWolf/AudioClasses/" + self.__class__.__name__ + "End.mp3")
                    voiceClient.play(source=audioSource, after=None)

    async def play(self, members, centralDeck, courseOfTheGame):
        self.members = members
        self.centralDeck = centralDeck
        self.courseOfTheGame = courseOfTheGame

    def getMembersName(self):
        listMemberName = []
        for member in self.members:
            if member.user is not self.user:
                listMemberName.append(member.user.name)
        random.shuffle(listMemberName)
        return listMemberName

    def check(self, msg):
        if msg.author != bot.user:
            if msg.channel.id == self.user.dm_channel.id:
                return True
        return False

    async def checkingMessage(self, msg):
        pass

    async def wait(self):
        try:
            msg = await self.bot.wait_for(event='message', check=self.check, timeout=30)
            await self.checkingMessage(msg)
        except asyncio.TimeoutError:
            await self.user.send("Vous avez mis trop de temps à répondre. Le rôle n'est donc plus joué.")
            self.courseOfTheGame += [
                "```" + self.user.name + " n'a pas correctement joué son rôle de " + self.firstRole + ".```"]
            self.choice = "#None"

    def getMemberFromName(self, name):
        for member in self.members:
            if name in member.user.name:
                return member

    async def isDead(self, channel):
        if self.protected:
            await channel.send(self.user.name + " a été protégé. Il ne meurt donc pas.")
        return not self.protected

    async def death(self, channel, members):
        await channel.send(self.user.name + " est mort ! C'était un(e) " + self.lastRole)
        return [self]

    def getRoleFromDeck(self, position=""):
        for role in self.centralDeck:
            if role.user == position:
                return role
        return None

    def vote(self, player):
        pass
