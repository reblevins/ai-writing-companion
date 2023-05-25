# Modify stories.db to add a column for characters which accepts a JSON string

import sqlite3

conn = sqlite3.connect('stories.db')
c = conn.cursor()

# Add a table for scenes with a foreign key to stories
c.execute('''CREATE TABLE scenes (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT,
              summary TEXT,
              content TEXT,
              story_id INTEGER NOT NULL,
              FOREIGN KEY (story_id) REFERENCES stories(id)
              )''')


conn.commit()
conn.close()
