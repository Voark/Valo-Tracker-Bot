def generate_url(ID):
    return f'https://tracker.gg/valorant/profile/riot/{urllib.parse.quote(ID)}/overview?playlist=competitive'

def open_url(URL) -> 'soup':
    page = requests.get(URL)
    return BeautifulSoup(page.content, 'html.parser')

def find_rank(soup) -> 'rank':
    search = soup.find('div', class_ = 'valorant-rank-bg')
    return search.text

def process_soup(soup):
    error = soup.find('p', class_ = 'error-message')
    if error != None:
        if error.text.strip() == 'If this is your account, you can view your stats by continuing with Riot Sign On below!':
            raise NotSignedInException
        elif error.text.strip() == 'Make sure you are not forgetting the # tag in the Riot ID, it\'s required.':
            raise NoAccountException
    else:
        return find_rank(soup)