import pickle
import json
import requests

SET_API = 'https://api.scryfall.com/cards/search?q=e:{}'
SETLIST_FILE = 'data/all_cards.json'
PULLED_FILE = 'data/pulled.json'

class SetManager():
    codes = {'eld', 'iko', 'khm', 'sta', 'stx', 'thb', 'znr'}
    def __init__(self):
        # prob do some manual/auto lookup for set meta info
        self.cards = self.format_cardlist()
    
    def format_cardlist(self):
        output = {code: {} for code in self.codes}
        cardlist = self.load_cards()
        for aid, card in cardlist.items():
            output[card['set']][aid] = card
        return output

    def get_cardlist(self, code):
        return self.cards[code]

    def get_card_data(self, aid):
        try:
            return self.cards[str(aid)]
        except:
            print(f'ERROR LOOKING UP CARD ID - {aid}')

    def load_cards(self):
        try:
            with open(SETLIST_FILE, 'r') as f:
                print('Setlist found, loading')
                cardlist = json.load(f)
                sets = {card['set'] for card in cardlist.values()}
                if self.codes <= sets:
                    return cardlist
                print('Missing codes')
                raise KeyError
        except (FileNotFoundError, KeyError):
            cardlist = self.get_fresh_cardlist()
            self.save_fresh_cardlist(cardlist)
        return cardlist

    def get_fresh_cardlist(self):
        # i don't necessarily understand all the fields in scryfall but 
        # booster doesn't work for sta for some reason
        overrides = {'sta'}
        output = {}
        print('Getting fresh cardlist')
        for code in self.codes:
            full_url = SET_API.format(code)
            cardlist = self.recursive_bullshit(full_url)
            # maybe do some metadata checks
            for card in cardlist:
                if not card['booster'] and card['set'] not in overrides:
                    continue
                output[int(card['arena_id'])] = card
        return output

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
        with open(SETLIST_FILE, 'w') as f:
            json.dump(cardlist, f)
