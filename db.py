import sqlite3
con = sqlite3.connect("sqlite.db")

cur = con.cursor()

res = cur.execute("SELECT * FROM appartments")
print(res.fetchall())

# Plan:
# - make a web page (simple HTML) that has a form for adding a record
# - update this file to allow HTTP data to be received
# - make a web page that shows results from the database



