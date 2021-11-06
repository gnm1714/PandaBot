import random
import re

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
    welcome_channel = "Please include a channel"
    welcome_message = " "

  return welcome_channel, welcome_message
def rps(throw):

  bot = rps_words[random.randint(0, 2)]
  bot_words = create_variations(bot)

  if re.search(bot_words[0], throw) or re.search(bot_words[1], throw) or re.search(bot_words[2], throw):
    return "You tie!!"
  elif re.search(r"\b[rR][oO][cC][kK]\b", throw):
    if bot == "Paper":
      return "You got covered by paper! Try again..."
    else:
      return "You banged scissors! Good job!"
  elif re.search(r"\b[pP][aA][pP][eE][rR]\b", throw):
    if bot == "Scissors":
      return "You got cut by scissors! Try again..."
    else:
      return "You covered rock! Good job!"
  elif re.search(r"\b[sS][cC][iI][sS][sS][oO][rR][sS]\b", throw):
    if bot == "Rock":
      return "You got banged by rock! Try again..."
    else:
      return "You cut paper! Good job!"
  else:
    return "Please specify rock, paper, or scissors!"