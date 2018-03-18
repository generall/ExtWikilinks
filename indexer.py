"""
This script should create SQLite database with indexed mentions.
"""

import sqlite3
import sys

query = """
CREATE VIRTUAL TABLE IF NOT EXISTS sentences 
USING fts4(
    left_context TEXT,
    mention TEXT,
    concept TEXT,
    right_context TEXT,
    notindexed=left_context, 
    notindexed=right_context, 
    notindexed=concept
)
"""

conn = sqlite3.connect("db_sent.sqlite")
cursor = conn.cursor()
cursor.execute(query)
cursor.close()
conn.commit()


cursor = conn.cursor()

filename = sys.argv[1]

insert_query = """
INSERT INTO sentences VALUES (?, ?, ?, ?)
"""

with open(filename) as fd:
    for line in fd:
        left_context, mention, concept, right_context = line.split('\t')
        cursor.execute(insert_query, (left_context, mention, concept, right_context))

conn.commit()
