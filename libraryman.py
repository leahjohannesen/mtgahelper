import re
import json
import pickle
from utils import load_log_kw

OLD_LIB_FILE = 'data/old_lib.pkl'

class LibraryManager():
    log_kw = '<== PlayerInventory.GetPlayerCardsV3'
    
    def __init__(self):
        self.library = None

    def refresh_library(self):
        lib = self.get_raw_library()
        # just in case
        self.write_new_lib(lib)
        self.library = lib

    def get_count(self, arena_id):
        return self.library.get(str(arena_id), 0)

    def get_raw_library(self):
        '''yoinkin internet code'''
        library = load_log_kw(self.log_kw)
        if library is None:
            print('Warning: decklist not found, loading old decklist')
            library = self.load_old_list()
        return library


    def load_old_list(self):
        try:
            with open(OLD_LIB_FILE, 'rb') as f:
                return pickle.load(f)
        except:
            raise Exception('No new list + no old list, please unfuck')
        return

    def write_new_lib(self, lib):
        with open(OLD_LIB_FILE, 'wb') as f:
            pickle.dump(lib, f)
        return
        