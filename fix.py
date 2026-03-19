import sqlite3
conn = sqlite3.connect("letterboxd_master.db")
count = conn.execute('SELECT COUNT(*) FROM movies WHERE Poster_URL IS NOT NULL AND Poster_URL != ""').fetchone()
sample = conn.execute('SELECT Name, Poster_URL FROM movies WHERE Poster_URL != "" LIMIT 3').fetchall()
print("Poster olan film sayısı:", count)
for r in sample: print(r)
conn.close()