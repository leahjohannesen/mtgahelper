import pickle
import json
import requests

SET_API = 'https://api.scryfall.com/cards/search?q=e:{}'
SETLIST_FILE = 'data/{}_cards.json'

class SetManager():
    def __init__(self, code):
        # prob do some manual/auto lookup for set meta info
        self.code = code
        self.cards = self.load_cards_for_set()

    def get_cardlist(self):
        return self.cards

    def get_card_data(self, aid):
        try:
            return self.cards[str(aid)]
        except:
            print(f'ERROR LOOKING UP CARD ID - {aid}')

    def load_cards_for_set(self):
        try:
            with open(SETLIST_FILE.format(self.code), 'r') as f:
                print('Setlist found, loading')
                return json.load(f)
        except FileNotFoundError:
            cardlist = self.get_fresh_cardlist()
            self.save_fresh_cardlist(cardlist)
        return cardlist

    def get_fresh_cardlist(self):
        print('Getting fresh cardlist')
        full_url = SET_API.format(self.code)
        cardlist = self.recursive_bullshit(full_url)
        # maybe do some metadata checks
        return {int(card['arena_id']): card for card in cardlist if card['booster']}

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
        with open(SETLIST_FILE.format(self.code), 'w') as f:
            json.dump(cardlist, f)
