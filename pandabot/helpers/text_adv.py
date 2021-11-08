import discord
from discord.ext import commands
import random
import re
from pandabot.helpers.utilities import create_embed

class GameCog(commands.Cog):

  def __init__(self, client):
        self.client = client

  def save_player(player, items):
    with open("savefile.txt", "a") as f:
      f.write("\n"+str(player)+" "+items)

  def load_player(player):
    with open("savefile.txt", "r") as f:
      lines = f.readlines()
      for line in lines:
        if line[0] == player:
          items = line[1]
          return items
        else:
          return False

  async def start_game(player, message):
    if not GameCog.load_player(player):
      embd = create_embed("Text Adventure Game!!", "You don't seem to have any save data. Would you like to begin a new game?","https://ichef.bbci.co.uk/news/976/cpsprodpb/2051/production/_111037280_gettyimages-85209802.jpg")
      msg = await message.channel.send(embed=embd)
      await msg.add_reaction("\N{THUMBS UP SIGN}")
      await msg.add_reaction("\N{THUMBS DOWN SIGN}")

  @commands.Cog.listener()
  @commands.guild_only()
  async def on_reaction_add(self, reaction, user):
    emoji = reaction.emoji

    if user.bot:
      return
    else:
      if emoji == "\N{THUMBS UP SIGN}":
        GameCog.save_player(user.id, "Sword,Armor,Poop")
      elif emoji == "\N{THUMBS DOWN SIGN}":
        embd = create_embed("Text Adventure Game!!", "Aww that's too bad... :(", "https://i.redd.it/4clmam942yy31.jpg")
        await reaction.message.channel.send(embed=embd)

def setup(client):
    client.add_cog(GameCog(client))
