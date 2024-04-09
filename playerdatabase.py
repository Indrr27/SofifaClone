import sqlite3
import scraper

conn = sqlite3.connect('MalePlayerStats.db') #connect to d
cur = conn.cursor()


cur.execute('''CREATE TABLE IF NOT EXISTS player_table
            (Key PRIMARY KEY,Name TEXT,Nation TEXT,Club TEXT,Position TEXT, Age INT, Overall INT)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Pace_Table (
    PlayerKey INTEGER,
    PaceOVR INTEGER,
    Acceleration INTEGER,
    Sprint INTEGER,
    FOREIGN KEY(PlayerKey) REFERENCES Player_table(Key)
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Shooting_Table (
    PlayerKey INTEGER,
    ShootingOVR INTEGER,
    Positioning INTEGER,
    Finishing INTEGER,
    Shot INTEGER,
    Long INTEGER,
    Volleys INTEGER,
    Penalties INTEGER,
    FOREIGN KEY(PlayerKey) REFERENCES Player_table(Key)
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Passing_Table (
    PlayerKey INTEGER,
    PassingOVR INTEGER,
    Vision INTEGER,
    Crossing INTEGER,
    Free INTEGER,
    Curve INTEGER,
    FOREIGN KEY(PlayerKey) REFERENCES Player_table(Key)
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Dribbling_Table (
    PlayerKey INTEGER,
    DribblingOVR INTEGER,
    Agility INTEGER,
    Balance INTEGER,
    Reactions INTEGER,
    Ball INTEGER,
    Composure INTEGER,
    FOREIGN KEY(PlayerKey) REFERENCES Player_table(Key)
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Defending_Table (
    PlayerKey INTEGER,
    DefendingOVR INTEGER,
    Interceptions INTEGER,
    Heading INTEGER,
    Def INTEGER,
    Standing INTEGER,
    Sliding INTEGER,
    FOREIGN KEY(PlayerKey) REFERENCES Player_table(Key)
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Physicality_Table (
    PlayerKey INTEGER,
    PhysicalityOVR INTEGER,
    Jumping INTEGER,
    Stamina INTEGER,
    Strength INTEGER,
    Aggression INTEGER,
    FOREIGN KEY(PlayerKey) REFERENCES Player_table(Key)
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Attributes_Table (
    PlayerKey INTEGER,
    AttWorkRate TEXT,
    DefWorkRate TEXT,
    PreferredFoot TEXT,
    WeakFoot INTEGER,
    SkillMoves INTEGER,
    FOREIGN KEY(PlayerKey) REFERENCES Player_table(Key)
)
''')




conn.commit()
conn.close()