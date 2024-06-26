import discord
from discord.ext import tasks
from mcstatus import JavaServer
import os

# Set your token and channel ID here
DISCORD_TOKEN = 'putyourdiscordbottokenhere'
CHANNEL_ID = butchannelidhereforstatusmessages

# Minecraft server details
MINECRAFT_SERVER_IP = 'minecraftserveriphere'
MINECRAFT_SERVER_PORT = 25565  # Default Minecraft port

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

server = JavaServer.lookup(f"{MINECRAFT_SERVER_IP}:{MINECRAFT_SERVER_PORT}")
last_status = None

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    check_server_status.start()

@tasks.loop(minutes=1.0)
async def check_server_status():
    global last_status
    channel = client.get_channel(CHANNEL_ID)
    
    if channel is None:
        print(f"Error: Channel with ID {CHANNEL_ID} not found.")
        return
    
    try:
        status = server.status()
        print(f"Server status: {status}")
        current_status = 'online'
    except Exception as e:
        print(f"Error checking server status: {e}")
        current_status = 'offline'
    
    if last_status != current_status:
        last_status = current_status
        if current_status == 'online':
            await channel.send('Minecraft server is online.')
            await client.change_presence(activity=discord.Game(name="Online"))
        else:
            await channel.send('Minecraft server is offline.')
            await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Offline"))
    else:
        print(f'Server status is still {current_status}.')

client.run(DISCORD_TOKEN)
