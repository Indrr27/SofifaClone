import sqlite3

conn = sqlite3.connect('MalePlayerStats.db')
c = conn.cursor()


#c.execute('''CREATE TABLE player_table(Key PRIMARY KEY,Name TEXT,Nation TEXT,Club TEXT,Position TEXT, Age INT, Overall INT)''')

