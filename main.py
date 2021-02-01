import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from util import *
from json import *

f = open('api_key.txt')
api_key = f.read()
f.close()

client = discord.Client()

bot = commands.Bot(command_prefix = '.', case_insensitive = True)

@bot.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@bot.command(name = 'track')
async def track_id(ctx, *, ID):
    ID = ID.replace(' ', '')
    try:
        await ctx.send(rank_from_id(ID))
    except NotSignedInException:
        await ctx.send('Sign in to your account here:')
    except NoAccountException:
        await ctx.send('Account doesn\'t exist')
    
@bot.command(name = 'add')
async def add_id(ctx, *, ID):
    ID = ID.replace(' ', '')
    guild_id = ctx.guild.id
    try:
        rank, url = rank_from_id(ID, return_url = True)
        data = open_json(guild_id)
        if data == None:
            data = dict()
        data[ID] = {'rank': rank, 'link': url}
        write_json(data, guild_id)
        await ctx.send(f'Successfully added {ID}')
    except NotSignedInException:
        await ctx.send(f'Unprivate your profile. {generate_url(ID)}')
    except NoAccountException:
        await ctx.send('Account doesn\'t exist')

@bot.command(name = 'remove')
async def remove_id(ctx, *, ID):
    guild_id = ctx.guild.id
    try:
        data = open_json(guild_id)
        del data[ID]
        write_json(data, guild_id)
        await ctx.send(f'Successfully removed {ID}')
    except:
        await ctx.send('Account not on list.')

@bot.command(name = 'list')
async def list_ids(ctx):
    guild_id = ctx.guild.id
    await reload_json(guild_id)
    data = open_json(guild_id)
    if not data:
        await ctx.send('No accounts to track. Add accounts using \'.add\'')
        return
    await ctx.message.delete()
    async for x in ctx.message.channel.history(limit = 2):
        if x.author == bot.user:
            await x.delete()
    #formatted_usernames = '\n'.join([f'[{key}]({value["link"]})' for key, value in sorted(data.items(), key = lambda x: rank_to_int(x[1]['rank']), reverse = True)])
    #formatted_ranks = '\n'.join([rank['rank'] for rank in sorted(data.values(), key = lambda x: rank_to_int(x['rank']), reverse = True)])
    formatted_usernames = [f'{key}' for key, value in sorted(data.items(), key = lambda x: rank_to_int(x[1]['rank']), reverse = True)]
    formatted_ranks = [rank['rank'] for rank in sorted(data.values(), key = lambda x: rank_to_int(x['rank']), reverse = True)]
    response = []
    for username, rank in zip(formatted_usernames, formatted_ranks):
        response.append(f'{username}: {rank}')
    #embed = discord.Embed(title="Accounts")
    #embed.add_field(name = "Username", value = formatted_usernames, inline = True)
    #embed.add_field(name = "Rank", value = formatted_ranks, inline = True)
    #await ctx.send(embed = embed)
    await ctx.send('\n'.join(response))

bot.run(api_key)