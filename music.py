import discord
from discord.ext import commands, tasks
import youtube_dl

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

YTDL_OPTIONS = {
    'format': 'bestaudio'
}

class music(commands.Cog):
    #https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html
    def __init__(self,client):
        self.client = client

    @commands.command(help = "Music bot joins the channel")
    async def join(self,ctx):
        #If user is not in a voice channel
        if (ctx.author.voice == None):
            print(ctx.author.voice)
            await ctx.send("Please join a voice channel before using this command")

        voiceChannelID = ctx.author.voice.channel
        #If bot is not in a voice channel
        if (ctx.voice_client == None):
            await voiceChannelID.connect()
        #if the bot is already in another channel
        else:
            await ctx.voice_client.move_to(voiceChannelID) 

    #Disconnect Command
    @commands.command(help = "Music bot leaves the channel")
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()


    @commands.command(help = "Play a url")
    async def play(self, ctx, url):
        
        voiceChannelID = ctx.author.voice.channel
        if (ctx.voice_client == None):
            await voiceChannelID.connect()
        #if the bot is already in another channel
        else:
            await ctx.voice_client.move_to(voiceChannelID) 
        #Reset to the next song
        ctx.voice_client.stop()
        voiceChannel = ctx.voice_client

        with youtube_dl.YoutubeDL(YTDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            extracted = info['formats'][0]['url']
            audioSource = await discord.FFmpegOpusAudio.from_probe(extracted, **FFMPEG_OPTIONS)
            voiceChannel.play(audioSource)

    @commands.command(help = "Pause the song")
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send("Audio Paused")


    @commands.command(help = "Resume the song after a pause")
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.send("Audio Resumed")

    


def setup(client):
    client.add_cog(music(client))
