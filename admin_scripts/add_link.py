import sqlite3

db = sqlite3.connect("db/db.db", detect_types=sqlite3.PARSE_DECLTYPES)

name = input("please enter the name of the link: ")
destination = input("please enter the destination of the link: ")
infobox_id = input("please enter ID of the infobox this link belongs to: ")

db.execute(
    "INSERT INTO links (name, destination, infoboxid) VALUES (?, ?, ?);",
    (name, destination, infobox_id),
)
db.commit()
print("Done!")
