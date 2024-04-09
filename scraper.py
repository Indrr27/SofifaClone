from bs4 import BeautifulSoup as bs
import requests
import re
import numpy as np # linear algebra



def scrapePlayers(all_male_players):
    # Male players 1-160
    for page in range(1, 2):
        absolute = 'https://www.ea.com'
        url = 'https://www.ea.com/games/ea-sports-fc/ratings?gender=0&page={}'.format(page)
        html = requests.get(url)
        if html.status_code == requests.codes.ok:
            soup = bs(html.text, features="html.parser")

            table = soup.find('tbody', class_='Table_tbody__q3fMn')
            for link in table.findAll('a', class_='Table_profileCellAnchor__L23hq'):
                player_link = absolute + link['href']

                player_dict = {}
                player_html = requests.get(player_link)
                player_soup = bs(player_html.text, features="html.parser")

                # Club and national team
                teams = []
                for item in player_soup.findAll(class_='Picture_responsiveImageWrap__mI2vU'):
                    team = item.img['alt']
                    if team == '':
                        continue
                    else:
                        teams.append(team)
                try:
                    national_team = teams[0]
                except IndexError:
                    national_team = np.nan
                try:
                    club = teams[1]
                except IndexError:
                    club = np.nan

                # Age
                try:
                    age = int(player_soup.find(string='AGE').parent.text[3:])
                except Exception:
                    age = np.nan

                # Get overall
                overall = player_soup.find(class_='Table_statCellValue__0G9QI').text

                # Get player position
                position = player_soup.find(class_='Table_tag__FeM31 generated_utility17__YNcLk').text

                # Name of player
                for stats in player_soup.findAll(class_='Table_profileCellAnchor__L23hq'):
                    player_dict['Name'] = stats.text

                player_dict.update({
                    'Nation': national_team, 
                    'Club': club,
                    'Position': position, 
                    'Age': age,
                    'Overall': overall 
                })

                # Player general stats
                for stats in player_soup.findAll('div', class_='Stat_stat__AXspT generated_utility19__iBkEh'):
                    try:
                        player_dict[re.search('[A-Za-z]+', stats.text)[0]] = int(re.search('[0-9]+', stats.text)[0])
                    except Exception:
                        player_dict[re.search('[A-Za-z]+', stats.text)[0]] = np.nan

                # All player stats
                for stats in player_soup.findAll(class_='Stat_stat__AXspT Stat_bar__sE9wr generated_utility20__hbeDx'):
                    player_dict[re.search('[A-Za-z]+', stats.text)[0]] = int(re.search('[0-9]+', stats.text)[0])

                # Attacking workrate
                att_work_rate = player_soup.find(string='ATT WORK RATE').parent.text[13:]

                # Defensive workrate
                def_work_rate = player_soup.find(string='DEF WORK RATE').parent.text[13:]

                # Preferred foot
                preferred_foot = player_soup.find(string='PREFERRED FOOT').parent.text[14:]

                # Weak foot
                weak_foot = player_soup.find(string='WEAK FOOT').parent.span['aria-label'][0]

                # Skill moves
                skill_moves = player_soup.find(string='SKILL MOVES').parent.span['aria-label'][0]

                player_dict.update({
                    'Att work rate': att_work_rate,
                    'Def work rate': def_work_rate,
                    'Preferred foot': preferred_foot,
                    'Weak foot': weak_foot,
                    'Skill moves': skill_moves,
                    'URL': player_link,
                    'Gender': 'M'
                })

                all_male_players.append(player_dict)
