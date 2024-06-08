import sqlite3

db = sqlite3.connect("db/db.db", detect_types=sqlite3.PARSE_DECLTYPES)

name = input("please enter the name/title of the infobox: ")
type = input("please enter the type of the infobox: ")
description = input("please enter the description/text of the infobox: ")
catid = input("please enter the id of the category this infobox belongs to: ")
ownerid = input("please enter the id of the user this infobox belongs to: ")
order = input("please enter the order of the infobox: ")

# this is the worst line of code, probably ever
db.execute(
    "INSERT INTO infoboxes (name, type, description, categoryid, owner, displayorder) VALUES (?, ?, ?, ?, ?, ?);",
    (name, type, description, catid, ownerid, order),
)
db.commit()
print("Done!")
