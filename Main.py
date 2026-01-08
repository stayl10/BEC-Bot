import discord
from discord import app_commands
from pathlib import Path
from discord.ext import commands
from dotenv import load_dotenv
import logging
import sys
import os

import json



#=========================
#cfg

perms_int = 5066929685473296

game_chat_duration = 9 #in days
game_team_role = 123

CFG_FILE = "config.json"

def load_config():
    with open(CFG_FILE, "r") as f:
        return json.load(f)


def save_config(data):
    with open(CFG_FILE, "w") as f:
        json.dump(data, f, indent=4)



#=========================


ENV_PATH = Path(".env")
if not ENV_PATH.exists(): # create if no exist
    ENV_PATH.write_text("DISCORD_BOT_TOKEN=\n")
    print("Created .env file. Add your DISCORD_BOT_TOKEN and restart.")
    sys.exit(1)

# Load the token from the .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_BOT_TOKEN is not set")


# Define intents and bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

logging.basicConfig(filename='createdChannels.log', encoding='utf-8', level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"{bot.user} has synced {len(synced)} commands(s)")
    except Exception as e:
        print(e)


@bot.tree.command(
    name="set_game_week_channel",
    description="set channel for game week threads"
)
@app_commands.describe(
    channel_for_threads = "channel to put threads in"
)
@commands.has_permissions(administrator=True)
async def set_game_week_channel(
        interaction: discord.Interaction,
        channel_for_threads: discord.TextChannel
):
    await interaction.response.defer(ephemeral=True, thinking=True)
    print(f"setting game week channel to {channel_for_threads}")

    config = load_config()
    config["channel_id"] = channel_for_threads.id
    save_config(config)

    await interaction.followup.send(f"Setting game week channel to {channel_for_threads.mention}")



@bot.tree.command(
    name="create_game_week",
    description="make a thread for a game"
)
@app_commands.describe(
    week_number = "week number",
    home_team = "Home Team",
    away_team = "Away Team",
    #channel_for_thread = "#channel to put thread in"
)
async def create_game_thread(
    interaction: discord.Interaction,
    week_number: int,
    home_team: discord.Role,
    away_team: discord.Role,
    #channel_for_thread: discord.TextChannel,
):
    await interaction.response.defer(ephemeral=True, thinking=True)

    config = load_config()
    channel_id = config["channel_id"]

    channel_for_thread = bot.get_channel(channel_id)

    print(f"Creating thread week {week_number} | {home_team} vs {away_team}")
    #await interaction.response.send_message(f"I will make a thread in {channel_for_thread} with the home team {home_team} and away team {away_team} for week number {week_number}.")
    game_Thread = await channel_for_thread.create_thread(
        type=None, #private thread
        name = f"{home_team} vs {away_team} | Week {week_number}",
        #auto_archive_duration=(game_chat_duration * 24 * 60),
        reason=f"Game Created for week {week_number} | {home_team} vs {away_team} | {channel_for_thread.name}",
        invitable=True,

    )

    await game_Thread.send(
        f"Game thread created for week {week_number} | {home_team.mention} vs {away_team.mention}"
    )

    await interaction.followup.send(f"thread created for week {week_number} | {home_team} vs {away_team}", ephemeral=True)

    print("thread created")



bot.run(TOKEN)