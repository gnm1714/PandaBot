import random
import re
import discord

welcome_message = " "
goodbye_message = " "
welcome_channel = None
goodbye_channel = None

rps_words = ["Rock", "Paper", "Scissors"]

# Creates all lowercase and uppercase variations of the words in the respective list
def create_variations(list1):
  new_list = []
  for word in list1:
    new_list.append(word.upper())
    new_list.append(word.lower())
    new_list.append(word)
  return new_list
    

def check_inside_words(words, message):
  message_words = message.split()
  for i in message_words:
    for j in words:
      if i == j:
        return True
  return False


def welcome(message, msg, msg_words):
  if len(msg_words) == 2:
    welcome_channel = msg_words[1]
    for channel in message.guild.channels:
      if welcome_channel == channel.name:
        welcome_channel = channel
        welcome_message = " "
  elif len(msg_words) > 2:
    welcome_channel = msg_words[1]
    user_welcome_message = msg_words[2:]
    welcome = " "
    welcome_message = welcome.join(user_welcome_message)
    for channel in message.guild.channels:
      if welcome_channel == channel.name:
        welcome_channel = channel
    #await message.channel.send(f"Welcome channel has been set to {welcome_channel} with a message: \"{botdata.welcome_message}\"")
  else:
    welcome_channel = " "
    welcome_message = " "
  return welcome_channel, welcome_message


def create_embed(titl, desc, img):
  embd = discord.Embed(title=titl, description=desc, colour=0xF7992E, type="rich").set_image(url=img)
  embd.set_footer(text="Pandabot v2.1")
  embd.set_author(name="Pandabot", url="https://github.com/gnm1714/PandaBot",icon_url="https://cdn.discordapp.com/avatars/788899598357889025/6597ed3783aa69710fe821d7a61b0876.png?size=256")
  return embd


def rps(throw):
  bot = rps_words[random.randint(0, 2)]

  if re.search(r"\b[rR][oO][cC][kK]\b", throw):
    if bot == "Paper":
      return create_embed("Rock, Paper, Scissors!", "You got covered by paper! Try again...", "https://www.myconfinedspace.com/wp-content/uploads/2017/07/angry-red-panda-720x450.jpg")
    elif bot == "Rock":
      return create_embed("Rock, Paper, Scissors!", "You tie! Try again...", "https://pbs.twimg.com/media/DGe-0rFXsAIJA70.jpg")
    else:
      return create_embed("Rock, Paper, Scissors!", "You banged scissors! Good job!", "https://memegenerator.net/img/images/15266018/excited-red-panda.jpg")
  elif re.search(r"\b[pP][aA][pP][eE][rR]\b", throw):
    if bot == "Scissors":
      return create_embed("Rock, Paper, Scissors!", "You got cut by scissors! Try again...", "https://www.myconfinedspace.com/wp-content/uploads/2017/07/angry-red-panda-720x450.jpg")
    elif bot == "Paper":
      return create_embed("Rock, Paper, Scissors!", "You tie! Try again...", "https://pbs.twimg.com/media/DGe-0rFXsAIJA70.jpg")
    else:
      return create_embed("Rock, Paper, Scissors!", "You covered rock! Good job!", "https://memegenerator.net/img/images/15266018/excited-red-panda.jpg")
  elif re.search(r"\b[sS][cC][iI][sS][sS][oO][rR][sS]\b", throw):
    if bot == "Rock":
      return create_embed("Rock, Paper, Scissors!", "You got banged by rock! Try again...", "https://www.myconfinedspace.com/wp-content/uploads/2017/07/angry-red-panda-720x450.jpg")
    elif bot == "Scissors":
      return create_embed("Rock, Paper, Scissors!", "You tie! Try again...", "https://pbs.twimg.com/media/DGe-0rFXsAIJA70.jpg")
    else:
      return create_embed("Rock, Paper, Scissors!", "You cut paper! Good job!", "https://memegenerator.net/img/images/15266018/excited-red-panda.jpg")
  else:
    return create_embed("Rock, Paper, Scissors!", "Please specify rock, paper, or scissors!", "https://i.pinimg.com/originals/63/89/82/638982bc7e19742c07b7e9868d3d2bf0.png")
