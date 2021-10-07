import discord
from discord.ext import commands, tasks


client = commands.Bot(command_prefix = '!', intents = discord.Intents.all())

raccoon_status = cycle(["Drums with a Stick", "Raccoon Metal", "Raccoon Pirate Shanty", "Raccoon Meditation Music", "Raccoon Lullaby"])























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