import pandas as pd

STATS_FILE = 'data/{}_stats.csv'

class StatsManager():
    cols = ['wins', 'packs_won', 'n_rares', 'n_mythics']
    summary_kw = '<== Event.ClaimPrize'
    
    def __init__(self, code):
        self.code = code
        self.stats = self.load_stats()
     
    def load_stats(self):
        try:
            df = pd.read_csv(STATS_FILE.format(self.code))
            print('Stats file loaded')
        except Exception as e:
            print('No previous stats file, starting new one to fill out')
            df = pd.DataFrame(columns=self.cols)
            df.to_csv(STATS_FILE.format(self.code), index=False)
        return df

    def show_stats_table(self):
        print(self.stats)
        
    def show_summary(self, rares, mythics, n_packs):
        if self.stats.empty:
            print('No stats available to compute')
            return
        n_drafts = self.stats.shape[0]
        n_won = self.stats['wins'].sum()
        n_lost = n_drafts * 3
        print(f'Drafts played: {n_drafts}')
        print(f'Games won: {n_won}, Games lost: {n_lost}')
        print(f'Win rate: {float(n_won)/(n_won + n_lost) * 100:.2f}%')
        
        avg_packs = self.stats['packs_won'].mean()
        avg_rares = self.stats['n_rares'].mean()
        n_rares = len(rares) * 4
        n_rares_owned = sum(card['count'] for card in rares)
        rare_drafts_left = (n_rares - (n_packs * 7/8 * 11/12) - n_rares_owned) / (avg_rares + avg_packs * 7/8 * 11/12)
        print('\nRares\n---')
        print(f'Card totals - Set: {n_rares}, Owned: {n_rares_owned}')
        print(f'Averages per draft - Packs: {avg_packs}, Rares: {avg_rares}')
        print(f'Rare drafts left: {rare_drafts_left}')