import youtube_dl
import os
from youtube_dl.utils import YoutubeDLError
from botBasics import *

# =-=-=-= VARIABLES =-=-=-= #
songQueued = {}


# =-=-=-= DISPLAY FUNCTION =-=-=-= #
def getSongName(file):
    fileSplit = file.split("-")[:-1]
    fileToReturn = "-".join(fileSplit)
    return fileToReturn.split("/")[1]  # get after the Musics/


def getURL(url):
    try:
        urlSplit = url.split("=")[1]
        return urlSplit
    except IndexError:
        pass


# =-=-=-= CHECKING FUNCTION =-=-=-= #
def alreadyDl(url):
    print("Checking Musics directory ...")
    for file in os.listdir("./Musics"):
        fileURL = file.split("-")[-1]  # Get the last element
        fileURL = fileURL.split(".")[0]  # Get all except last element
        try:
            if getURL(url) == fileURL:
                print("Found.")
                return file
        except YoutubeDLError:
            print("FoundError while checking already download.")

            return ""

    print("Not found.")
    return ""


# =-=-=-= OTHER FUNCTION =-=-=-= #
async def playAudio(guild):
    print("Start playing audio ...")
    for voiceClient in bot.voice_clients:
        if voiceClient.guild == guild:
            print("Founded channel : ", voiceClient.channel)
            if songQueued.get(voiceClient.guild.name) is not None:
                if not voiceClient.is_playing() and len(songQueued[voiceClient.guild.name]) != 0:
                    print("Optimal condition to play.")
                    audioSource = discord.FFmpegPCMAudio(songQueued[voiceClient.guild.name][0])
                    voiceClient.play(source=audioSource, after=None)


async def download(ctx, url):
    fileAlreadyDl = alreadyDl(url)
    if fileAlreadyDl == "":
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Starting download ...")
            ydl.download([url])
            print("Download complete.")

    else:
        print("Download already done.")
        if songQueued.get(ctx.guild.name) is None:
            songQueued[ctx.guild.name] = []
        songQueued[ctx.guild.name].append("Musics/" + fileAlreadyDl)

    await ctx.message.add_reaction("✅")
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "./Musics/" + file)
            print("./Musics" + file)
            if songQueued.get(ctx.guild.name) is None:
                songQueued[ctx.guild.name] = []
            songQueued[ctx.guild.name].append(file)


# =-=-=-= BOT LOOPING FUNCTION =-=-=-= #
async def endedSong():
    while not bot.is_closed():
        for voiceClient in bot.voice_clients:
            if songQueued.get(voiceClient.guild.name) is not None:
                if not voiceClient.is_playing() and not voiceClient.is_paused() and len(
                        songQueued[voiceClient.guild.name]) > 1:
                    print("Next song played")
                    songQueued[voiceClient.guild.name].pop(0)
                    await playAudio(voiceClient.guild)
        await asyncio.sleep(2)


# =-=-=-= BOT COMMANDS =-=-=-= #
@bot.command()
async def play(ctx, url=" "):
    """
    Will try to connect to a user channel and then try to play the music passed in URL.
    If false : send a message error.
    If true : send a embed with title, song name, position in queue etc...
              Will also display on Activity the name of the music.
    """

    if ctx.message.guild.voice_client is None:
        await join(ctx)

    if ctx.author.voice is not None:
        try:
            await download(ctx, url)
            await playAudio(ctx.guild)
            await bot.change_presence(activity=discord.Activity(name="Music 🎶", type=discord.ActivityType.listening))

        except YoutubeDLError:
            await ctx.message.add_reaction("❌")
            await ctx.message.channel.send("Erreur : URL non valide ou problème(s) de téléchargement.")


@bot.command()
async def queue(ctx):
    listToShow = ""
    for musics in songQueued[ctx.guild.name]:
        listToShow += getSongName(musics) + "; "
    await ctx.message.channel.send("song in queue : " + listToShow)
