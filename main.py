import os
import random
import re
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pandabot.helpers.api import get_cat, get_panda, get_quote
from pandabot.helpers.text_adv import GameCog
from pandabot.helpers.utilities import (
    check_inside_words,
    create_embed,
    create_variations,
    rps,
    welcome,
)
from pandabot.helpers.web_server import web_server


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
intents = discord.Intents.all()
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
  responses_io = responses_io is False
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
  await botdata.welcome_channel.send(
      re.sub("@user", member.mention, botdata.welcome_message))


@client.event
async def on_member_remove(member):
  print(f"See ya {member}!")
  await botdata.welcome_channel.send(
      re.sub("@user", member.mention, botdata.goodbye_message))


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

  # Sending a random cat image
  if msg == f"{pfx}kitty":
    embd = create_embed("Here's your kitty picture!", "", get_cat())
    await message.channel.send(embed=embd)

  # Setting prefix
  if msg.startswith(f"{pfx}prefix") and len(msg_words) == 2:
    await message.channel.send(set_prefix(msg_words[1]))

  # Turn responses on and off
  if msg == f"{pfx}responses":
    await message.channel.send(set_responses())

  # Post pumpkin!!
  if msg == f"{pfx}pumpkin":
    await message.channel.send(embed=create_embed(
        "Grrrrr, evil pumpkins....", "",
        "https://cdn.discordapp.com/attachments/802421159878328350/909872775278231562/7BYDYUcEvrWaZiUX-1.gif"
    ))

  # Setting welcome channel
  if msg.startswith(
      f"{pfx}welcome") and message.author.guild_permissions.administrator:
    welcome_channel, welcome_message = welcome(message, msg, msg_words)

    botdata.welcome_channel = welcome_channel
    botdata.welcome_message = welcome_message

    if welcome_channel == " ":
      await message.channel.send("Please include a channel!")
    elif welcome_message != " ":
      await message.channel.send(
          f"Welcome channel has been set to {botdata.welcome_channel} with a message: \"{botdata.welcome_message}\""
      )
    else:
      await message.channel.send(
          f"Welcome channel has been set to {botdata.welcome_channel}")

  # Setting goodbye channel
  if msg.startswith(
      f"{pfx}goodbye") and message.author.guild_permissions.administrator:
    goodbye_channel, goodbye_message = welcome(message, msg, msg_words)

    botdata.goodbye_channel = goodbye_channel
    botdata.goodbye_message = goodbye_message

    if goodbye_channel == " ":
      await message.channel.send("Please include a channel!")
    elif goodbye_message != " ":
      await message.channel.send(
          f"Goodbye channel has been set to {botdata.goodbye_channel} with a message: \"{botdata.goodbye_message}\""
      )
    else:
      await message.channel.send(
          f"Goodbye channel has been set to {botdata.goodbye_channel}")

  # Responses to user typed words
  # Pandabot words
  if check_inside_words(create_variations(pandabot_words),
                        msg) and responses_io:
    r = random.random()
    if r <= 0.98:
      await message.channel.send(random.choice(pandabot_responses))
    else:
      await message.channel.send("**I am really freaking gay**")

  # BOP words
  if check_inside_words(create_variations(bop_words), msg) and responses_io:
    if message.author.id == 312414349480296449:
      await message.channel.send("Bop!")
      await message.channel.send(
          "BEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEN"
      )
    elif message.author.id == 773202852805345290:
      await message.channel.send("Sorry, I don't bop Canadians :)")
    elif message.author.id == 318036809454190593:
      await message.channel.send("Bop!")
      await message.channel.send("Ew I smell stinky catfox :(")
    elif message.author.id == 302949520994467841:
      await message.channel.send("Bop!")
      await message.channel.send(":baby::skin-tone-5: :baby::skin-tone-5: :baby::skin-tone-5:")
    elif message.author.id == 809675536791765033:
      await message.channel.send("Bop!")
      await message.channel.send("\"Why yes, of course I want to listen to you explain all the 40k lore\" -Nobody ever")
    elif message.author.id == 404550882160672770:
      await message.channel.send("Bop!")
      await message.channel.send("Rock n Stone? More like rock that ass of yours into the bath, stinky :)")
    elif message.author.id == 355483494362644480:
      await message.channel.send("Bop!")
      await message.channel.send("Okay but like, why Brazil tho?")
    elif message.author.id == 511912328934195200:
      await message.channel.send("Bop!")
      await message.channel.send("Nasral jsem se do kalhot jen kvůli tobě :D")
    elif message.author.id == 254372752952262656:
      await message.channel.send("Bop!")
      await message.channel.send("Answer truthfully, on a scale of 1 to 10, how gay is Ben?")
    elif message.author.id == 949776230079668284:
      await message.channel.send("Bop!")
      await message.channel.send("All hail Master Gabe")
    else:
      await message.channel.send("Bop!")

  # Small games
  # Rock, Paper, Scissors
  if msg.startswith(f"{pfx}rps"):
    if len(msg_words) == 2:
      embd = rps(msg_words[1])
      await message.channel.send(embed=embd)
    else:
      await message.channel.send(embed=create_embed(
          "Rock, Paper, Scissors!", "Please specify rock, paper, or scissors!",
          "https://i.pinimg.com/originals/63/89/82/638982bc7e19742c07b7e9868d3d2bf0.png"
      ))

  if msg == f"{pfx}game":
    await GameCog.start_game(message.author, message)


if __name__ == "__main__":
  for extension in initial_extensions:
    _ = client.load_extension(extension)

  load_dotenv(".env")
  web_server()
  client.run(os.getenv("TOKEN"))
