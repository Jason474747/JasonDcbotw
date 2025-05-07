import os
import discord
from discord.ext import commands
from flask import Flask
import threading

# Bot-Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Eingeloggt als {bot.user.name}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Webserver (Flask)
app = Flask("")

@app.route("/")
def home():
    return "Bot läuft!"

def run():
    app.run(host="0.0.0.0", port=8080)

# Starte Webserver in eigenem Thread
threading.Thread(target=run).start()

# Bot starten
bot.run(os.getenv("DISCORD_TOKEN"))
