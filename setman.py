import pickle
import requests

SET_API = 'https://api.scryfall.com/cards/search?q=e:{}'
SETLIST_FILE = 'data/{}_cards.pkl'

class SetManager():
    def __init__(self, code):
        # prob do some manual/auto lookup for set meta info
        self.code = code

    def get_cards_for_set(self):
        try:
            with open(SETLIST_FILE.format(self.code), 'rb') as f:
                print('Setlist found, loading')
                return pickle.load(f)
        except FileNotFoundError:
            cardlist = self.get_fresh_cardlist()
            self.save_fresh_cardlist(cardlist)
        return cardlist

    def get_fresh_cardlist(self):
        print('Getting fresh cardlist')
        full_url = SET_API.format(self.code)
        cardlist = self.recursive_bullshit(full_url)
        # maybe do some metadata checks
        return cardlist

    def recursive_bullshit(self, url):
        # if no more records, do something
        r = requests.get(url)
        result = r.json()
        # maybe do error checking
        if not result['has_more']:
            return result['data']
        return result['data'] + self.recursive_bullshit(result['next_page'])
         
    def save_fresh_cardlist(self, cardlist):
        print('Saving fresh cardlist')
        with open(SETLIST_FILE.format(self.code), 'wb') as f:
            pickle.dump(cardlist, f)
        return