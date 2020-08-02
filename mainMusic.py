from discord.ext import commands
import asyncio
import discord
import sys
from TOKEN import TOKEN_MUSIC

botMusic = commands.Bot(command_prefix='?', )
botMusic.remove_command(name="help")

try:
    voiceChannelID = sys.argv[1]
    guildID = sys.argv[2]
    audio = sys.argv[3]
except IndexError:
    print("Error", __name__)


@botMusic.event
async def on_ready():
    """
    After execute bot, will just print in log he's ready
    :return: None
    """
    await botMusic.change_presence(
        activity=discord.Game(name="Werewolf | ``" + botMusic.command_prefix + "help``"))
    for voiceClient in botMusic.voice_clients:
        await voiceClient.disconnect()
    print("Bot Music is ready")
    await connectMusic()


async def connectMusic():
    print('Connecting bot Music...')
    voiceChannel = await botMusic.fetch_channel(int(voiceChannelID))
    await voiceChannel.connect()
    await playMusic()


async def playMusic():
    print("Playing Music...")
    guild = await botMusic.fetch_guild(int(guildID))
    for voiceClient in botMusic.voice_clients:
        if voiceClient.guild == guild:
            print("Search audioSource for music...")
            audioSource = discord.FFmpegPCMAudio(audio)
            voiceClient.play(source=audioSource, after=None)
            while voiceClient.is_playing():
                await asyncio.sleep(1)
            await playMusic()


loopMusic = asyncio.get_event_loop()
loopMusic.create_task(botMusic.start(TOKEN_MUSIC))
loopMusic.run_forever()
