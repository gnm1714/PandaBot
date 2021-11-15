import discord
from discord.ext import commands
import os
import random
from pandabot.helpers.text_adv import GameCog
from pandabot.helpers.web_server import web_server
from dotenv import load_dotenv
from pandabot.helpers.utilities import check_inside_words, create_variations, welcome, rps, create_embed
from pandabot.helpers.api import get_panda, get_quote, get_cat

class BotData:
    def __init__(self):
        self.welcome_channel = None
        self.goodbye_channel = None
        self.welcome_message = " "
        self.goodbye_message = " "


#Global variables which alter behavior of the bot
responses_io = True
prefix = "="

# Bot intents, so events function properly
intents = discord.Intents.default()
intents.members = True

# Setting up the client itself
botdata = BotData()
client = commands.Bot(command_prefix=prefix, intents=intents)

initial_extensions = ['pandabot.helpers.text_adv']

# A mess of lists the bot refers back to
pandabot_words = ["Pandabot", "PandaBot", "pandaBot"]
bop_words = ["Bop", "Bops"]
pandabot_responses = ["nya!", "*squeak*", "^ w^", "Hello!"]

def set_responses():
    global responses_io
    if responses_io == False:
      responses_io = True
    else:
      responses_io = False
    return f"Responses have been set to {str(responses_io).lower()}"
    

def set_prefix(new):
    global prefix
    prefix = new

    return f"The prefix has been set to {new}!"


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_member_join(member):
    print(f"Welcome {member}!")
    await botdata.welcome_channel.send(botdata.welcome_message)


@client.event
async def on_member_remove(member):
    print(f"See ya {member}!")
    await botdata.welcome_channel.send(botdata.goodbye_message)


@client.event
async def on_message(message):
    pfx = prefix
    if message.author == client.user:
        return

    msg = message.content

    if msg is not None:
        msg_words = msg.split()

    # Sending a random inspirational quote
    if msg == f"{pfx}inspire":
      embd = create_embed("Here's your inspirational quote!", get_quote(), "")
      await message.channel.send(embed=embd)

    # Sending a random red panda image
    if msg == f"{pfx}panda":
      embd = create_embed("Here's your panda picture!", "", get_panda())
      await message.channel.send(embed=embd)

      # Sending a random red panda image
    if msg == f"{pfx}kitty":
      embd = create_embed("Here's your kitty picture!", "", get_cat())
      await message.channel.send(embed=embd)

    # Setting prefix
    if msg.startswith(f"{pfx}prefix"):
        if len(msg_words) == 2:
            await message.channel.send(set_prefix(msg_words[1]))

    # Turn responses on and off
    if msg == f"{pfx}responses":
        await message.channel.send(set_responses())


    # Post pumpkin!!
    if msg == f"{pfx}pumpkin":
        await message.channel.send(embed=create_embed("Grrrrr, evil pumpkins....", "", "https://cdn.discordapp.com/attachments/802421159878328350/909872775278231562/7BYDYUcEvrWaZiUX-1.gif"))
    

    # Setting welcome channel
    if msg.startswith(f"{pfx}welcome") and message.author.guild_permissions.administrator:
        welcome_channel, welcome_message = welcome(message, msg, msg_words)

        botdata.welcome_channel = welcome_channel
        botdata.welcome_message = welcome_message

        if welcome_channel == " ":
          await message.channel.send("Please include a channel!")
        elif welcome_message != " ":
          await message.channel.send(f"Welcome channel has been set to {botdata.welcome_channel} with a message: \"{botdata.welcome_message}\"")
        else:
          await message.channel.send(f"Welcome channel has been set to {botdata.welcome_channel}")

    # Setting goodbye channel
    if msg.startswith(f"{pfx}goodbye") and message.author.guild_permissions.administrator:
        goodbye_channel, goodbye_message = welcome(message, msg, msg_words)

        botdata.goodbye_channel = goodbye_channel
        botdata.goodbye_message = goodbye_message

        if goodbye_channel == " ":
          await message.channel.send("Please include a channel!")
        elif goodbye_message != " ":
          await message.channel.send(f"Goodbye channel has been set to {botdata.goodbye_channel} with a message: \"{botdata.goodbye_message}\"")
        else:
          await message.channel.send(f"Goodbye channel has been set to {botdata.goodbye_channel}")

    # Responses to user typed words
    # Pandabot words
    if check_inside_words(create_variations(pandabot_words), msg):
      if responses_io is True:
        r = random.random()
        if r <= 0.98:
          await message.channel.send(random.choice(pandabot_responses))
        else:
          await message.channel.send("**I am really fucking gay**")

    # BOP words
    if check_inside_words(create_variations(bop_words), msg):
      if responses_io is True:
        await message.channel.send("Bop!")

    # Small games
    # Rock, Paper, Scissors
    if msg.startswith(f"{pfx}rps"):
      if len(msg_words) == 2:
        embd = rps(msg_words[1])
        await message.channel.send(embed=embd)
      else:
        await message.channel.send(embed=create_embed("Rock, Paper, Scissors!", "Please specify rock, paper, or scissors!", "https://i.pinimg.com/originals/63/89/82/638982bc7e19742c07b7e9868d3d2bf0.png"))

    if msg == f"{pfx}game":
      await GameCog.start_game(message.author, message)

if __name__ == "__main__":
  for extension in initial_extensions:
          client.load_extension(extension)
          
load_dotenv(".env")
web_server()
client.run(os.getenv("TOKEN"))
