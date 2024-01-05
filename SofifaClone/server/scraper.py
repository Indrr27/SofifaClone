import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import requests
from bs4 import BeautifulSoup as bs
import re

pd.set_option('display.max_columns',50)

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session
        
# Male players 1-160
all_male_players = []
for page in range(1,2):

    absolute = 'https://www.ea.com'
    url = 'https://www.ea.com/games/ea-sports-fc/ratings?gender=0&page={}'.format(page)
    html = requests.get(url)
    html.status_code == requests.codes.ok
    soup = bs(html.text)
    
    table = soup.find( 'tbody', class_ = 'Table_tbody__gYqSw')
    for link in table.findAll('a', class_ = 'Table_profileCellAnchor__VU0JH'):
        player_link = absolute+link['href']

        player_dict = {}
        player_html = requests.get(player_link)
        player_soup = bs(player_html.text)

        # Club and national team
        teams = []
        for item in player_soup.findAll(class_ ='Picture_responsiveImageWrap__XmvLe'):
            team = item.img['alt']
            if team == '':
                continue
            else:
                teams.append(team)
        try:
            national_team = teams[0]
        except:
            national_team = np.nan
        try:
            club = teams[1]
        except:
            club = np.nan

        # Age
        try:
            age = int(player_soup.find(string = 'AGE').parent.text[3:])
        except:
            age = np.nan


        # Get overall
        overall = player_soup.find(class_='Table_statCellValue____Twu').text

        # Get player position
        position = player_soup.find(class_='Table_tag__3Mxk9 generated_utility3sm__0pg6W generated_utility1lg__ECKe_').text

        # Name of player
        for stats in player_soup.findAll(class_ = 'Table_profileCellAnchor__VU0JH'):
            player_dict['Name'] =  stats.text
        
        player_dict.update({
            'Nation': national_team, 
            'Club': club,
            'Position':position, 
            'Age':age,
            'Overall':overall 
        })

        # Player general stats   
        for stats in player_soup.findAll('div', class_ ='Stat_stat__lh90p generated_utility2__1zAUs'):
            try:
                player_dict[re.search('[A-Za-z]+', stats.text)[0]] = int(re.search('[0-9]+', stats.text)[0])
            except:
                player_dict[re.search('[A-Za-z]+', stats.text)[0]] = np.nan

        # All player stats
        for stats in player_soup.findAll(class_='Stat_stat__lh90p Stat_bar__hVgdN generated_utility3__mFgLe'):
            player_dict[re.search('[A-Za-z]+', stats.text)[0]] = int(re.search('[0-9]+', stats.text)[0])

        # Attacking workrate
        att_work_rate = player_soup.find(string = 'ATT WORK RATE').parent.text[13:]

        # Defensive workrate
        def_work_rate = player_soup.find(string = 'DEF WORK RATE').parent.text[13:]

        # Preferred foot
        preferred_foot = player_soup.find(string = 'PREFERRED FOOT').parent.text[14:]

        # Weak foot
        weak_foot = player_soup.find(string = 'WEAK FOOT').parent.span['aria-label'][0]

        # Skill moves
        skill_moves = player_soup.find(string = 'SKILL MOVES').parent.span['aria-label'][0]

        player_dict.update({
            'Att work rate':att_work_rate,
            'Def work rate':def_work_rate,
            'Preferred foot':preferred_foot,
            'Weak foot': weak_foot,
            'Skill moves':skill_moves,
            'URL':player_link,
            'Gender':'M'
        })

        all_male_players.append(player_dict)

print('Total male players:',all_male_players)