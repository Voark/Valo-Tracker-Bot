import urllib.parse
import requests
import json
from bs4 import BeautifulSoup
import asyncio

RANKS = {'Iron 1'    : 0 , 'Iron 2'    : 1 , 'Iron 3'    : 2 , 
         'Bronze 1'  : 3 , 'Bronze 2'  : 4 , 'Bronze 3'  : 5 ,
         'Silver 1'  : 6 , 'Silver 2'  : 7 , 'Silver 3'  : 8 ,
         'Gold 1'    : 9 , 'Gold 2'    : 10, 'Gold 3'    : 11,
         'Platinum 1': 12, 'Platinum 2': 13, 'Platinum 3': 14,
         'Diamond 1' : 15, 'Diamond 2' : 16, 'Diamond 3' : 17,
         'Immortal 1': 18, 'Immortal 2': 19, 'Immortal 3': 20,
         'Radiant '  : 69, 'Error': -2, 'Unrated': -1}

# Exceptions
class NotSignedInException(Exception):
    pass

class NoAccountException(Exception):
    pass

def rank_to_int(rank):
    return RANKS[rank]

def generate_url(ID):
    return f'https://tracker.gg/valorant/profile/riot/{urllib.parse.quote(ID)}/overview?playlist=competitive'

def open_url(URL) -> 'soup':
    # TODO: Handle rate limit/no response
    page = requests.get(URL)
    return BeautifulSoup(page.content, 'html.parser')

def find_rank(soup) -> 'rank':
    search = soup.find('div', class_ = 'valorant-rank-bg')
    return search.text.strip()

def process_soup(soup):
    error = soup.find('p', class_ = 'error-message')
    if error != None:
        if error.text.strip() == 'If this is your account, you can view your stats by continuing with Riot Sign On below!':
            raise NotSignedInException
        elif error.text.strip() == 'Make sure you are not forgetting the # tag in the Riot ID, it\'s required.':
            raise NoAccountException
    else:
        return find_rank(soup)

def rank_from_id(ID, return_url = False):
    URL = generate_url(ID)
    soup = open_url(URL) 
    if return_url:
        return process_soup(soup), URL
    return process_soup(soup)

# {ID: {'link': str, 'rank': int}}

def open_json(server_id):
    try:
        with open('data/' + str(server_id) + '.json', 'r') as file:
            data = json.load(file)
    except:
        return None
    return data

def write_json(data, server_id):
    with open('data/' + str(server_id) + '.json', 'wt') as file:
        json.dump(data, file)

async def reload_json(server_id):
    data = open_json(server_id)
    if data == None:
        return 
    for ID in data:
        try:
            rank, url = rank_from_id(ID, return_url = True)
        except:
            rank = 'Error'
            url = generate_url(ID)
        await asyncio.sleep(1)
        data[ID] = {'rank': rank, 'link': url}
    write_json(data, server_id)

if __name__ == '__main__':
    write_json({'a': 'b', 'c': 'd'}, 1)
    print(open_json(1))
    print(open_json(1))