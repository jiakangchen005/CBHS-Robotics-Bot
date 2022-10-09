import discord
from discord.ext import commands

import os

client = commands.Bot(command_prefix = '>', intents = discord.Intents.all())

# Start of Bot

@client.event
async def on_ready():
    status = discord.Status.online
    
    # activity = discord.Activity(type = discord.ActivityType.watching, name = "you")

    platform = "YouTube"
    url = "https://www.youtube.com/watch?v=RQmEERvqq70"
    activity = discord.Streaming(platform = platform, url = url, name = "to you")

    await client.change_presence(status = status, activity = activity)
    print("yey")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("it's pretty *sus* that i've never heard of that command before.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("missing something?")

@client.command()
async def load(ctx, extension):
    await client.load_extension("cogs." + extension)

@load.error
async def load_error(ctx, error):
    await ctx.send("i don't know what you are trying to load.")

@client.command()
async def unload(ctx, extension):
    await client.unload_extension("cogs." + extension)


async def load_extensions():
    for file in os.listdir("./cogs"):
        await client.load_extension("cogs." + file[:-3])

# End of Bot

token = "haha, nice try"

with open("../cbhs_robotics_bot_token", 'r') as file:
    token = file.read()

client.run(token)

