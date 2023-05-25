# Script to create an sqlite database with the following schema:
#
# CREATE TABLE stories (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     title TEXT NOT NULL,
#     genre TEXT NOT NULL,
#     summary TEXT NOT NULL,
#     content TEXT NOT NULL
# );

import sqlite3

conn = sqlite3.connect('stories.db')
c = conn.cursor()

c.execute('''CREATE TABLE stories (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              genre TEXT,
              summary TEXT,
              content TEXT
              )''')

# Insert some dummy data
c.execute('''INSERT INTO stories (title) VALUES ('Untitled')''')

# Create a table for characters with a foreign key to stories
c.execute('''CREATE TABLE characters (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              attributes TEXT,
              story_id INTEGER NOT NULL,
              FOREIGN KEY (story_id) REFERENCES stories(id)
              )''')


conn.commit()
conn.close()
