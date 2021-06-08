import re
import json

LOG_LOCATION = 'C:/Users/zbebb/AppData/LocalLow/Wizards Of The Coast/MTGA/Player.log'
#LOG_LOCATION = 'data/draft_game_log.log'

def load_log_kw(kw):
    with open(LOG_LOCATION, encoding='utf-8') as f:
        blah = f.read()
    matches = list(re.finditer(kw, blah))
    # find index of /n and check for request or payload 
    for match in matches[::-1]:
        matchend = match.end()
        esc = re.search('\\n', blah[matchend:])
        escstart = esc.start()
        raw = blah[matchend + 1:matchend + escstart]
        return json.loads(raw)['payload']
    else:
        print(f'Warning: log kw {kw} not found')
        return None

        
if __name__ == '__main__':
    pass
