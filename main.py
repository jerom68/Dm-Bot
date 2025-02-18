import discord
from discord.ext import commands
import requests
from flask import Flask
import threading

# Intents for the bot to listen to messages and member events
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# Flask app for managing the web server
app = Flask(__name__)

# Route for the status page (runs on port 5000)
@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=5000)

# Event to notify when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Meme Generation Command
@bot.command()
async def meme(ctx):
    try:
        # Fetch a random meme from an API
        response = requests.get('https://meme-api.com/gimme')
        meme_data = response.json()
        meme_url = meme_data['url']
        
        # Create an embed message to display the meme
        embed = discord.Embed(title="Here’s your meme!", color=discord.Color.blue())
        embed.set_image(url=meme_url)
        embed.set_footer(text="Enjoy the meme! :D")
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send("Sorry, something went wrong. Try again later.")
        print(f"Error: {e}")

# DM on Join with avatar and username - Cool Message
@bot.event
async def on_member_join(member):
    # Create a DM channel
    dm = await member.create_dm()
    
    # Custom Message with cool formatting and a stylish embed
    embed = discord.Embed(
        title=f"✨ Welcome to the server, {member.name}! ✨",
        description=f"Hey {member.name}, we’re super excited to have you join us. 💥\n\n"
                    "Here’s your profile info:",
        color=discord.Color.green()
    )
    
    # Add avatar as a thumbnail
    embed.set_thumbnail(url=member.avatar.url)
    
    # Add fields for username and more details
    embed.add_field(name="Username", value=member.name, inline=False)
    embed.add_field(name="User ID", value=member.id, inline=False)
    
    # Add a footer with extra details
    embed.set_footer(text="We're glad you're here! 🎉")
    
    # Send the stylish DM to the member
    await dm.send(embed=embed)

# Run Flask in a separate thread
def start_flask():
    thread = threading.Thread(target=run_flask)
    thread.start()

# Start Flask and the Bot
if __name__ == "__main__":
    start_flask()
    bot.run("YOUR_BOT_TOKEN")
