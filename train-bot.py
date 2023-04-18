
import datetime
from discord.ext import commands, tasks
import discord
from dataclasses import dataclass
import datetime

import requests
import pandas as pd
import random

from sys import exit

print("Ham Rankings Process commenced")

# Members
member_json = requests.get(r"https://raider.io/api/v1/guilds/profile?region=us&realm=barthilas&name=steamed%20hams&fields=members").json()

member_list = [i['character']['name'] for i in member_json['members']]

print("Members list obtained")

# Generate Ranks

def rank_set(member_list):

    rank_list = {}

    for i in member_list:

        req = requests.get(f"https://raider.io/api/v1/characters/profile?region=us&realm=barthilas&name={i}&fields=mythic_plus_scores_by_season:current").json()

        if 'mythic_plus_scores_by_season' in req:

            tank_rank = req['mythic_plus_scores_by_season'][0]['segments']['tank']['score']
            healer_rank = req['mythic_plus_scores_by_season'][0]['segments']['healer']['score']
            dps_rank = req['mythic_plus_scores_by_season'][0]['segments']['dps']['score']

        rank_list[i] = {
            'Tank':tank_rank,
            'Healer':healer_rank,
            'DPS':dps_rank}
    return rank_list

ranks = rank_set(member_list)

rank_df = pd.DataFrame.from_dict(ranks, orient='index')
rank_df.index.name = 'character'
rank_df.reset_index(inplace=True)

print("Ham Rankings Generated")

#rank_df.to_csv('D:\My Drive\Steamed Hams\Train-Bot\Ham_Ranks.csv')

#rank_df = pd.read_csv('D:\My Drive\Steamed Hams\Train-Bot\Ham_Ranks.csv')

# Top 10s (or 5s?)
tank_top_5 = rank_df.sort_values('Tank', ascending=False).head(5)
healer_top_5 = rank_df.sort_values('Healer', ascending=False).head(5)
dps_top_5 = rank_df.sort_values('DPS', ascending=False).head(5)

discord_text = f'''

** Oceanic's Top Hams ** \t *{datetime.datetime.now().day}/{datetime.datetime.now().month}/{datetime.datetime.now().year}*

:shield: **Tank**
```
{tank_top_5.iloc[0]['Tank']} \t {tank_top_5.iloc[0]['character']}
{tank_top_5.iloc[1]['Tank']} \t {tank_top_5.iloc[1]['character']}
{tank_top_5.iloc[2]['Tank']} \t {tank_top_5.iloc[2]['character']}
{tank_top_5.iloc[3]['Tank']} \t {tank_top_5.iloc[3]['character']}
{tank_top_5.iloc[4]['Tank']} \t {tank_top_5.iloc[4]['character']}
```
:green_heart: **Healer**
```
{healer_top_5.iloc[0]['Healer']} \t {healer_top_5.iloc[0]['character']}
{healer_top_5.iloc[1]['Healer']} \t {healer_top_5.iloc[1]['character']}
{healer_top_5.iloc[2]['Healer']} \t {healer_top_5.iloc[2]['character']}
{healer_top_5.iloc[3]['Healer']} \t {healer_top_5.iloc[3]['character']}
{healer_top_5.iloc[4]['Healer']} \t {healer_top_5.iloc[4]['character']}
```
:crossed_swords: **DPS**
```
{dps_top_5.iloc[0]['DPS']} \t {dps_top_5.iloc[0]['character']}
{dps_top_5.iloc[1]['DPS']} \t {dps_top_5.iloc[1]['character']}
{dps_top_5.iloc[2]['DPS']} \t {dps_top_5.iloc[2]['character']}
{dps_top_5.iloc[3]['DPS']} \t {dps_top_5.iloc[3]['character']}
{dps_top_5.iloc[4]['DPS']} \t {dps_top_5.iloc[4]['character']}
```
Message *!score character* for your personalised report from Train-Bot

'''

# BOT

BOT_TOKEN = 'BOT_TOKEN' #Your Bot Token
CHANNEL_ID = 0 #Discord Channel ID

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
session = Session()

@bot.command(aliases=["quit"])
async def close(ctx):
    await client.close()
    print("Bot Closed")

@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)  
    await channel.send(discord_text)
    print("Discord text sent")
    await bot.close()


# Add More
random_phrases = [
    "You're really out there putting the P in Pumper",
    "What are you still doing here, don't you have some pumping to do?",
    "You must be single-handedly carrying our guild with your pumping."]


@bot.command()
async def score(ctx, character):

    tank_score = rank_df[rank_df['character'] == character]['Tank'].iloc[0]
    healer_score = rank_df[rank_df['character'] == character]['Healer'].iloc[0]
    dps_score = rank_df[rank_df['character'] == character]['DPS'].iloc[0]

    await ctx.send(f'''
    {character} has a Tank Score of {str(tank_score)}, a Healer Score of {str(healer_score)}, and a DPS Score of {str(dps_score)}\n
    {random.choice(random_phrases)}
    
    '''
    )
    
bot.run(BOT_TOKEN)

#sys.exit()