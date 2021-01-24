import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from util import *
import urllib.parse
import requests

f = open('api_key.txt')
api_key = f.read()
f.close()

class NotSignedInException(Exception):
    pass

class NoAccountException(Exception):
    pass

client = discord.Client()

bot = commands.Bot(command_prefix = '.', case_insensitive = True)

@bot.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@bot.command(name = 'track')
async def track(ctx, *, ID):
    URL = generate_url(ID)
    soup = open_url(URL) 
    try:
        await ctx.send(process_soup(soup))
    except NotSignedInException:
        await ctx.send('Sign in to your account here:')
    except NoAccountException:
        await ctx.send('Account doesn\'t exist')

bot.run(api_key)