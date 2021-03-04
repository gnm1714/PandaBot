import discord
import os
import requests
import json
import random
from web_server import web_server
from dotenv import load_dotenv

class BotData:
    def __init__(self):
        self.welcome_channel = None
        self.goodbye_channel = None
        self.welcome_message = " "
        self.goodbye_message = " "

intents = discord.Intents.default()
intents.members = True

botdata = BotData()
client = discord.Client(intents=intents)

responses_io = False
prefix = "="

# A mess of lists the bot refers back to
pandabot_words = ["Pandabot", "PandaBot", "pandaBot"]
bop_words = ["Bop", "Bops"]
pandabot_responses = ["nya!", "*squeak*", "^ w^", "*nuzzles*"]

# Creates all lowercase and uppercase variations of the words in the respective list
def create_variations(list1):
    new_list = []
    for word in list1:
        new_list.append(word.upper())
        new_list.append(word.lower())
        new_list.append(word)
    return new_list


# Gets a random inspiration quote and sends back to the async
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + " -" + json_data[0]["a"]
    return (quote)


# Gets a random red panda picture and sends back to the async
def get_panda():
    response = requests.get("https://some-random-api.ml/img/red_panda")
    json_data = json.loads(response.text)
    quote = "Here's your panda uwu: " + json_data["link"]
    return (quote)


# Gets a random undertale goat picture and sends back to the async
def get_goat():
    response = requests.get("http://0.0.0.0:8081/")
    json_data = json.loads(response.text)
    quote = "Here's your goat uwu: " + json_data[0]["link"]
    return (quote)


def set_responses():
    global responses_io
    if responses_io is False:
        responses_io = True
    else:
        responses_io = False


def set_prefix(new):
    global prefix
    prefix = new

    return f"The prefix has been set to {new}, nyaa~"


def check_inside_words(responses, message):
    message_list = []
    response_list = []
    marker = 0
    counter = 0
    for item in message:
        message_list.append(item)
    if len(message_list[0]) > 1:
        new_list = []
        for letter in message_list:
            new_list.append(letter)
        message_list = new_list
    print(message_list)

    for i in range(0, len(responses)):
        response_list = []
        for item in responses[i]:
            response_list.append(item)
        for j in range(0, len(response_list) - 1):
            if message_list[j] == response_list[j]:
                print(message_list)
                print(response_list)
                print(message_list[j] + " - " + response_list[j])
                marker = j
                print(marker)
            else:
                marker = 0

    return True


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_member_join(member):
    print(f"Welcome {member}")
    await botdata.welcome_channel.send(botdata.welcome_message)


@client.event
async def on_member_remove(member):
    print(f"See ya {member}")
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
        quote = get_quote()
        await message.channel.send(quote)

    # Sending a random red panda image
    if msg.startswith(f"{pfx}panda"):
        panda = get_panda()
        await message.channel.send(panda)

    # Sending a random undertale goat image
    if msg.startswith(f"{pfx}goat"):
        goat = get_goat()
        await message.channel.send(goat)

    # Setting prefix
    if msg.startswith(f"{pfx}prefix"):
        if len(msg_words) == 2:
            pfx = set_prefix(msg_words[1])
            await message.channel.send(pfx)

    # Setting welcome channel
    if msg.startswith(f"{pfx}welcome"):
        if len(msg_words) == 2:
          welcome_channel = msg_words[1]
          for channel in message.guild.channels:
            if welcome_channel == channel.name:
              botdata.welcome_channel = channel
          await message.channel.send(f"Welcome channel has been set to {welcome_channel}")
        elif len(msg_words) > 2:
          welcome_channel = msg_words[1]
          welcome_message = msg_words[2:]
          welcome = " "
          botdata.welcome_message = welcome.join(welcome_message)
          for channel in message.guild.channels:
            if welcome_channel == channel.name:
              botdata.welcome_channel = channel
          await message.channel.send(f"Welcome channel has been set to {welcome_channel} with a message: \"{botdata.welcome_message}\"")
        else:
          await message.channel.send("Please include a welcome channel")
    
    # Setting goodbye channel
    if msg.startswith(f"{pfx}goodbye"):
        goodbye_message = ""
        if len(msg_words) == 2:
          goodbye_channel = msg_words[1]
          for channel in message.guild.channels:
            if goodbye_channel == channel.name:
              botdata.goodbye_channel = channel
          await message.channel.send(f"Goodbye channel has been set to {goodbye_channel}")
        elif len(msg_words) > 2:
          goodbye_channel = msg_words[1]
          goodbye_message = msg_words[2:]
          goodbye = " "
          botdata.goodbye_message = goodbye.join(goodbye_message)
          for channel in message.guild.channels:
            if goodbye_channel == channel.name:
              botdata.goodbye_channel = channel
          await message.channel.send(f"Goodbye channel has been set to {goodbye_channel} with a message: \"{botdata.goodbye_message}\"")
        else:
          await message.channel.send("Please include a goodbye channel")

    # Responses to user typed words
    # Pandabot words
    if any(word in msg for word in create_variations(pandabot_words)):
        await message.channel.send(random.choice(pandabot_responses))

    # BOP words
    if any(word in msg for word in create_variations(bop_words)):
        await message.channel.send("Bop!")


load_dotenv(".env")
web_server()
client.run(os.getenv("TOKEN"))

