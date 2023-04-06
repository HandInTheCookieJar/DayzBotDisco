import os
import discord
import requests
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents)

# Replace with your BattleMetrics server ID
SERVER_ID = "20192791"
BATTLEMETRICS_URL = f"https://api.battlemetrics.com/servers/{SERVER_ID}"
# Replace with your bot token
BOT_TOKEN = "MTA5MzQxMTc1NDM1NDE0NzM5OQ.GEMunJ.g0AxxYBPxXiQ-j8VGhgXScN3sfXKG8PIsNPavw"

@bot.event
async def on_ready():
    print(f"{bot.user} is online.")
    server_status.start()

@tasks.loop(minutes=5)
async def server_status():
    channel = discord.utils.get(bot.get_all_channels(), name='📜server-status')
    if not channel:
        return

    response = requests.get(BATTLEMETRICS_URL)
    if response.status_code != 200:
        await channel.send("Error fetching server status.")
        return

    data = response.json()
    players_online = data["data"]["attributes"]["players"]
    max_players = data["data"]["attributes"]["maxPlayers"]
    server_status = data["data"]["attributes"]["status"]
    server_version = data["data"]["attributes"]["details"]["version"]

    status_message = f"**Status:** {server_status.capitalize()}\n"
    status_message += f"**Server Version:** {server_version}\n"
    status_message += f"**Online Players:** {players_online}/{max_players}"
    await channel.send(status_message)

bot.run(BOT_TOKEN)
