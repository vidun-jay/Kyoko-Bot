import discord
from discord import SyncWebhook
from discord.utils import get
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup

load_dotenv()
TOKEN = os.getenv("TOKEN")
client = discord.Client(intents=discord.Intents.all())
webhook = os.getenv("WEBHOOK")
results = []

@client.event
async def on_ready():
    ''' Sends up message to console '''
    print('Bot started with username: {0.user}'.format(client))

@client.event
async def on_message(message):
    ''' Listens for message event and reads command '''

    username = str(message.author).split('#')[0] # gets username of message author
    user_message = str(message.content) # gets content of message
    channel = str(message.channel.name) # gets name of current channel

    if message.author == client.user:
        return

    # only respond in current channel
    if channel == 'general':
        if user_message.lower().startswith('!anime'):
            await animeSearch(user_message, message)

        return

async def animeSearch(user_message, message):
    ''' Takes in user message as input and searches MyAnimeList for those keywords '''
    global results
    keyword = user_message[7:].replace(" ", "%20") # parse the command out of the message, replace spaces with '%20'

    # parse MyAnimeList and return top 10 results
    r = requests.get(f'https://myanimelist.net/anime.php?q={keyword}&cat=anime')
    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all('a', attrs={'class':'hoverinfo_trigger fw-b fl-l'})
    return_message = ""

    # take the top 5 results from MyAnimeList
    for i in range(0, 5, 1):
        results[i] = str(results[i].find('strong'))[8:-9]
        # results.append(str(results[i].find('strong'))[8:-9])
        return_message += f'{i + 1}. {str(results[i])}\n'

    # send message as embed and set reaction buttons 1-5
    embed = discord.Embed(title=f'Results for: {user_message[7:].replace("%20", " ")}', description=f"{return_message}", color=0x36509D)
    msg = await message.channel.send(embed=embed)
    reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]

    for reaction in reactions:
        await msg.add_reaction(reaction)

@client.event
async def on_reaction_add(reaction, user):
    ''' Returns further information based on selection from list '''

    # if the bot is the one reacting, do nothing
    if reaction.message.author == user:
        return
    else:
        # expand the reaction, return further details
        if reaction.emoji == '1️⃣':
            # await reaction.message.channel.send('selected: 1')
            embed = discord.Embed(title=f'{results[0]}', description=f"description", color=0x36509D)
            await reaction.message.channel.send(embed=embed)
        elif reaction.emoji == '2️⃣':
            embed = discord.Embed(title=f'{results[1]}', description=f"description", color=0x36509D)
        elif reaction.emoji == '3️⃣':
            embed = discord.Embed(title=f'{results[2]}', description=f"description", color=0x36509D)
        elif reaction.emoji == '4️⃣':
            embed = discord.Embed(title=f'{results[3]}', description=f"description", color=0x36509D)
        elif reaction.emoji == '5️⃣':
            embed = discord.Embed(title=f'{results[4]}', description=f"description", color=0x36509D)
    return

if __name__ == "__main__":
    client.run(TOKEN)
