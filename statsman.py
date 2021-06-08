import pandas as pd
from setman import SetManager

PARSED_HIST_FILE = 'data/parsed_draft_hist.json'
PACK_BONUS = {
    0: 0.20,
    1: 0.22,
    2: 0.24,
    3: 0.26,
    4: 0.30,
    5: 0.35,
    6: 0.40,
    7: 1.00,
    }

class StatsManager(): 
    def __init__(self):
        self.load_history()

    def load_history(self):
        try:
            df = pd.read_json(PARSED_HIST_FILE, orient='index')
        except:
            return None
        self.stats = df.reset_index(drop=True).drop('id', axis=1)
        return
    
    def show_history(self, code):
        self.load_history()
        print(self.stats[self.stats['set'] == code])
    
    def show_summary(self, code, n_packs, rares, myths):
        self.load_history()
        if self.stats is None:
            print('No stats available to compute')
            return
        df = self.stats[self.stats['set'] == code]
        n_drafts = df.shape[0]
        n_won = df['wins'].sum()
        n_lost = df['losses'].sum()
        print(f'Drafts played: {n_drafts}')
        print(f'Games won: {n_won}, Games lost: {n_lost}')
        print(f'Win rate: {float(n_won)/(n_won + n_lost) * 100:.2f}%')
        
        avg_packs = df['wins'].apply(lambda x: PACK_BONUS[x]).mean() + 1
        avg_rares = df['rares'].mean()
        n_rares = len(rares) * 4
        n_rares_owned = sum(card['count'] for card in rares)
        rare_drafts_left = (n_rares - (n_packs * 7/8 * 11/12) - n_rares_owned) / (avg_rares + avg_packs * 7/8 * 11/12)
        print('\nRares\n---')
        print(f'Card totals - Set: {n_rares}, Owned: {n_rares_owned}')
        print(f'Averages per draft - Packs: {avg_packs}, Rares: {avg_rares}')
        print(f'Rare drafts left: {rare_drafts_left}')
        
        
