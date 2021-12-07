import requests
from random_word import RandomWords
import random
import sqlite3
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


teamName = ['Celtics', 'Bulls', 'Lakers', 'Pistons', 'Trail Blazers', 'Knicks']
homeTeam = teamName[random.randint(0,5)]
awayTeam = homeTeam
while (awayTeam == homeTeam):
    awayTeam = teamName[random.randint(0,5)]

conn = sqlite3.connect('test_copy.db')
cursor = conn.cursor()

result = conn.execute('''select m_teamOne, m_teamTwo, m_date from match where m_date > '2021-12-12' ''')

for row in result:
    homeTeam = row[0]
    awayTeam = row[1]
    date = row[2]

    data = {
        'csrf_token': 'IjU5ZjQyMjg2YjRkNzhjZmM0ZDAyYzEzMTg4YTFiMTM3N2VjNjk0YTAi.Ya68xA.h8q79NyKMp_3ck3wRqCAZRvtuzg',
        'date': date,
        'homeTeamName': homeTeam,
        'homeTeamScore': random.randint(0, 150),
        'awayTeamName': awayTeam,
        'awayTeamScore': random.randint(0, 150),
        'submit': 'Submit'
    }

    response = requests.post('http://localhost:5000/add-score', headers=headers, cookies=cookies, data=data)

'''
for i in range(20):
    #print("working")
    for j in range(6):
        homeTeam = teamName[random.randint(0,5)]
        awayTeam = homeTeam
        while (awayTeam == homeTeam):
            awayTeam = teamName[random.randint(0,5)]
        #print(homeTeam, awayTeam)
        
        data = {
            'csrf_token': 'IjU5ZjQyMjg2YjRkNzhjZmM0ZDAyYzEzMTg4YTFiMTM3N2VjNjk0YTAi.Ya68xA.h8q79NyKMp_3ck3wRqCAZRvtuzg',
            'sportName': 'basketball',
            'leagueName': 'Olympique Lyonnais',
            'homeTeamName': homeTeam,
            'awayTeamName': awayTeam,
            'date': '2021-12-' + str(10+i),
            'submit': 'Submit'
        }

        #print(data)

        #response = requests.post('http://localhost:5000/make-match', headers=headers, cookies=cookies, data=data)
'''