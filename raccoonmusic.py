import discord
from discord.ext import commands, tasks
import youtube_dl
from itertools import cycle
import os
import music


cogsList = [music]
cogsLength = len(cogsList)


raccoon_status = cycle(["Drums with a Stick", "Raccoon Metal", "Raccoon Pirate Shanty", "Raccoon Meditation Music", "Raccoon Lullaby"])

help_command = commands.DefaultHelpCommand(no_category = 'Commands')
client = commands.Bot(command_prefix = '-', intents = discord.Intents.all())

for i in range(cogsLength):
    cogsList[i].setup(client)

@client.event
async def on_ready():
    change_status.start()
    print('Logged in as {0.user} successfully'.format(client))


@client.command(help = "Return the ping time")
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)} ms')


'''
Loops/Background Events
'''
@tasks.loop(seconds = 3600)
async def change_status():
    await client.change_presence(activity=discord.Game(next(raccoon_status)))



'''
Error Handling
'''
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("This command does not exist. Please try again")



client.run(os.getenv('TOKEN'))