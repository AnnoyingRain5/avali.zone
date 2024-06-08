import sqlite3

db = sqlite3.connect(
    "db/db.db", detect_types=sqlite3.PARSE_DECLTYPES
)

name = input("please enter the name of the link: ")
destination = input("please enter the destination of the link: ")
infoboxid = input("please enter ID of the infobox this link belongs to: ")

db.execute("INSERT INTO links (name, destination, infoboxid) VALUES (?, ?, ?);", (name, destination, infoboxid))
db.commit()
print("Done!")