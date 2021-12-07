import requests
from random_word import RandomWords
import random
r = RandomWords()

cookies = {
    'intercom-id-cnp1kltb': '5ada2e38-2d13-43a4-b3f6-c70be78fc685',
    '_ga': 'GA1.1.798528510.1630359165',
    'session': 'eyJjc3JmX3Rva2VuIjoiNTlmNDIyODZiNGQ3OGNmYzRkMDJjMTMxODhhMWIxMzc3ZWM2OTRhMCJ9.Ya2GhA.4rI26GcNH7LqtgKb9BS_kBjaKhg',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'http://localhost:5000',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'http://localhost:5000/team',
    'Accept-Language': 'en-US,en;q=0.9,ig;q=0.8',
}


for i in range(9):
    data = {
    'csrf_token': 'IjU5ZjQyMjg2YjRkNzhjZmM0ZDAyYzEzMTg4YTFiMTM3N2VjNjk0YTAi.Ya6oGg.rGL389drJaFyGNem0CrTA9y4u3U',
    'name': r.get_random_word(),
    'height': random.randint(30, 120),
    'weight': random.randint(50, 300),
    'sportName': 'basketball',
    'leagueName': 'Olympique Lyonnais',
    'teamName': 'Knicks',
    'isCaptain': 'No',
    'submit': 'Submit'
    }

    response = requests.post('http://localhost:5000/player', headers=headers, cookies=cookies, data=data)