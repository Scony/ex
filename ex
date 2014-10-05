#!/usr/bin/python3
import sys
import urllib.request
import json
from colorama import Fore, Style

root = 'http://127.0.0.1:8888'

if len(sys.argv) > 1:
    try:
        data = urllib.request.urlopen(root+'/commands/'+sys.argv[1]+'/examples').read().decode('utf-8')
        data = json.loads(data)
        for d in data:
            if 'example' in d and 'description' in d and 'score' in d:
                print(Fore.GREEN+Style.BRIGHT+d['example']+Fore.RED+Style.NORMAL+' \t# '+d['description']+' ('+str(d['score'])+')'+Style.RESET_ALL)
    except:
        print(Fore.RED+'No examples found'+Style.RESET_ALL)
else:
    print('Usage: ex command')
