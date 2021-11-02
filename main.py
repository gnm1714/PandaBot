import discord
import os
import random
from pandabot.helpers.web_server import web_server
from dotenv import load_dotenv
from pandabot.helpers.utilities import create_variations, check_inside_words, welcome, rps
from pandabot.helpers.api import get_panda, get_quote

class BotData:
    def __init__(self):
        self.welcome_channel = None
        self.goodbye_channel = None
        self.welcome_message = " "
        self.goodbye_message = " "

# Bot intents, so events function properly
intents = discord.Intents.default()
intents.members = True

# Setting up the client itself
botdata = BotData()
client = discord.Client(intents=intents)

#Global variables which alter behavior of the bot
responses_io = True
prefix = "="

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
    if msg.startswith(f"{pfx}inspire"):
        await message.channel.send(get_quote())

    # Sending a random red panda image
    if msg.startswith(f"{pfx}panda"):
        await message.channel.send(get_panda())

    # Setting prefix
    if msg.startswith(f"{pfx}prefix"):
        if len(msg_words) == 2:
            await message.channel.send(set_prefix(msg_words[1]))

    # Turn responses on and off
    if msg.startswith(f"{pfx}responses"):
        await message.channel.send(set_responses())

    # Setting welcome channel
    if msg.startswith(f"{pfx}welcome"):
        welcome_channel, welcome_message = welcome(message, msg, msg_words)

        botdata.welcome_channel = welcome_channel
        botdata.welcome_message = welcome_message

        if welcome_message != " ":
          await message.channel.send(f"Welcome channel has been set to {botdata.welcome_channel} with a message: \"{botdata.welcome_message}\"")
        else:
          await message.channel.send(f"Welcome channel has been set to {botdata.welcome_channel}")

    # Setting goodbye channel
    if msg.startswith(f"{pfx}goodbye"):
        goodbye_channel, goodbye_message = welcome(message, msg, msg_words)

        botdata.goodbye_channel = goodbye_channel
        botdata.goodbye_message = goodbye_message

        if goodbye_message != " ":
          await message.channel.send(f"Goodbye channel has been set to {botdata.goodbye_channel} with a message: \"{botdata.goodbye_message}\"")
        else:
          await message.channel.send(f"Goodbye channel has been set to {botdata.goodbye_channel}")

    # Responses to user typed words
    # Pandabot words
    if any(word in msg for word in create_variations(pandabot_words)):
      if responses_io is True:
        await message.channel.send(random.choice(pandabot_responses))

    # BOP words
    if any(word in msg for word in create_variations(bop_words)):
      if responses_io is True:
        await message.channel.send("Bop!")

    # Small games
    # Rock, Paper, Scissors
    if msg.startswith(f"{pfx}rps"):
      if len(msg_words) == 2:
        await message.channel.send(rps(msg_words[1]))
      else:
        await message.channel.send("Please specify rock, paper, or scissors!")


load_dotenv(".env")
web_server()
client.run(os.getenv("TOKEN"))
