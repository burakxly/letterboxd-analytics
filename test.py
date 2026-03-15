import sqlite3
import pandas as pd

pd.set_option('display.max_columns', None)
conn = sqlite3.connect("letterboxd_master.db")

# Sorunlu filmlerin ve sağlam filmlerin iki farklı tarih sütununda nasıl durduğuna bakıyoruz
query = """
SELECT Name, Rating, Watched_Date_Log, "Watched Date" 
FROM movies 
WHERE Name LIKE '%Sherlock%' OR Name LIKE '%Shazam%' OR Name LIKE '%Citizen Kane%'
"""
df = pd.read_sql(query, conn)
conn.close()

print(df)