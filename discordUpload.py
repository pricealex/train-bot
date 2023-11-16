import discord
from discord.ext import commands, tasks
from dataclasses import dataclass
import os

BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
CHANNEL_ID = 1095138030517489694 #Train Server Test

import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    channel = client.get_channel(CHANNEL_ID)  
    #await channel.send(discord_text)
    #await channel.send(all_quotes) #Test Only
    #print("Discord text sent")

    #await channel.send(file=discord.File('double_threat.png'))
    await channel.send("We're off an away - who has been pumping?", file=discord.File("double_threat.png"))

    await client.close()

client.run(BOT_TOKEN)