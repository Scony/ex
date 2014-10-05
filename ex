#!/usr/bin/python3
import sys
import urllib.request
import json

root = 'http://127.0.0.1:8888'

if len(sys.argv) > 1:
    try:
        data = urllib.request.urlopen(root+'/commands/'+sys.argv[1]+'/examples').read().decode('utf-8')
        data = json.loads(data)
        for d in data:
            if 'example' in d and 'description' in d and 'score' in d:
                print(d['example']+' \t# '+d['description']+' ('+str(d['score'])+')')
    except:
        print('No examples found')
else:
    print('Usage: ex command')
