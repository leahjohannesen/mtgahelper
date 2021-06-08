import re
import json
import requests
import os
from math import ceil
from itertools import zip_longest

from draftman import DraftManager
from libraryman import LibraryManager
from setman import SetManager
from statsman import StatsManager

import sys

COL_WIDTH = 30

COLORS = {
    'G': 'Green',
    'W': 'White',
    'U': 'Blue', 
    'B': 'Black',
    'R': 'Red',
    'M': 'Misc',
}
    
class MTGAHelper():
    def __init__(self):
        self.sm = SetManager()
        self.dm = DraftManager()
        self.lm = LibraryManager()
        self.stm = StatsManager()

    def finish_draft(self):
        self.dm.record_draft()
        
    def show_draft_history(self, code):
        self.stm.show_history(code)

    def show_cards(self, code):
        self.lm.refresh_library()
        rares, mythics = self.get_card_stuff(code)
        self.display_cards(rares, 'RARES')
        self.display_cards(mythics, 'MYTHS')
        return
        
    def show_stats(self, code, n_packs):
        self.lm.refresh_library()
        rares, mythics = self.get_card_stuff()
        self.stm.show_summary(code, n_packs, rares, mythics)

    def get_card_stuff(self, code):
        all_cards = self.sm.get_cardlist(code)
        rares = []
        mythics = []
        for i, (aid, card) in enumerate(all_cards.items()):
            card_data = self.get_card_data(card)
            if card_data['rarity'] == 'rare':
                rares.append(card_data)
            elif card_data['rarity'] == 'mythic':
                mythics.append(card_data)
        return rares, mythics

    def get_card_data(self, card):
        # lookup count + format output
        try:
            return {
                'name': card['name'],
                'colors': card['color_identity'],
                'count': self.lm.get_count(card['arena_id']),
                'rarity': card['rarity'],
            }
        except KeyError as e:
            raise Exception(f'Error with {card}\n{e}')
   
    def display_cards(self, cards, label): 
        n_coll = sum(x['count'] for x in cards)
        print(f'{label} | Number: {len(cards)}, Collected: {n_coll} / {len(cards) * 4}')
        sorted_cards = {label: [] for label in COLORS.values()}
        for card in cards:
            color = self.assign_color(card)
            sorted_cards[color].append(card)
        self.print_labels(sorted_cards)
        max_n = max(len(val) for val in sorted_cards.values())
        for row_idx in range(max_n):
            row_vals = []
            for color_list in sorted_cards.values():
                val = color_list[row_idx] if row_idx < len(color_list) else None
                row_vals.append(self.format_card(val))
            print(' | '.join(row_vals))
        return
        
    def assign_color(self, card):
        card_colors = card['colors']
        if len(card_colors) == 1:
            val = card_colors[0]
        else:
            val = 'M'
        return COLORS[val]
        
    def print_labels(self, cards):
        vals = []
        for label, cardlist in cards.items():
            n_coll = sum(card['count'] for card in cardlist)
            vals.append(label.ljust(COL_WIDTH - 5) + f'{n_coll:2}/{len(cardlist) * 4:2}')
        print(' | '.join(vals))
  
    def format_card(self, card):
        if card is None:
            return ' ' * COL_WIDTH
        n_cards = card['count']
        if n_cards == 4:
            cardname = '-'*2 + card['name'][:COL_WIDTH - 5].ljust(COL_WIDTH - 1 - 2, '-')
        else:
            cardname = card['name'][:COL_WIDTH - 4].ljust(COL_WIDTH - 1)
        return cardname + str(n_cards)


if __name__ == '__main__':
    mh = MTGAHelper()
    
