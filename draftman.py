import re
import json
import pickle
from utils import load_log_kw
from setman import SetManager

DRAFT_HIST_FILE = 'data/raw_draft_hist.json'
PARSED_HIST_FILE = 'data/parsed_draft_hist.json'

class DraftManager():
    summary_kw = '<== Event.ClaimPrize'
    
    def record_draft(self):
        draft = load_log_kw(self.summary_kw)
        # save the raw draft for later just in case
        self.append_to_hist(draft['Id'], draft, DRAFT_HIST_FILE)
        # parse and save for current use case
        parsed = self.parse_raw_draft(draft)
        self.append_to_hist(parsed['id'], parsed, PARSED_HIST_FILE)
        self.summarize_draft(parsed)
        return

    def append_to_hist(self, key, draft, fp):
        try:
            with open(fp, 'r') as f:
                hist = json.load(f)
        except:
            print('No log found, creating new one')
            hist = {}
        if key in hist:
            print('Duplicate ID found, skipping insert')
            return
        hist[key] = draft
        with open(fp, 'w') as f:
            json.dump(hist, f)

    def parse_raw_draft(self, draft):
        code = draft['InternalEventName'].split('_')[1].lower()
        print(f'Parsing {code} draft')
        gamestuff = draft['ModuleInstanceData']['WinLossGate']
        cardstuff = draft['CardPool']
        sm = SetManager(code)
        fullcards = [sm.get_card_data(card) for card in cardstuff]
        rares, myths = 0, 0
        for card in fullcards:
            if card is None:
                continue
            if card.get('rarity') == 'rare':
                rares += 1
            if card.get('rarity') == 'mythic':
                myths += 1
        return {
            'id': draft['Id'],
            'set': code,
            'wins': gamestuff['CurrentWins'],
            'losses': gamestuff['CurrentLosses'],
            'rares': rares, 
            'mythics': myths,
        }

    def summarize_draft(self, draft):
        print('\n***Draft quick summary***')
        print(f"Wins: {draft['wins']}, Losses: {draft['losses']}")
        print(f"Rares: {draft['rares']}, Mythics: {draft['mythics']}")
        
    def manually_add_draft(self, code, idval, wins, losses, rares, myths):
        parsed = {
            'id': str(idval),
            'set': code,
            'wins': wins,
            'losses': losses,
            'rares': rares,
            'mythics': myths,
        }
        self.append_to_hist(parsed['id'], parsed, PARSED_HIST_FILE)
        self.summarize_draft(parsed)

if __name__ == '__main__':
    dm = DraftManager()
    draft = load_log_kw(dm.summary_kw)
    sm = SetManager('thb')
    dm.record_draft() 
