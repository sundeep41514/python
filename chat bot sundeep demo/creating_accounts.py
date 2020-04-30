import sqlite3

conn = sqlite3.connect("RandF_accounts.sqlite")
cur = conn.cursor()

# cur.execute('create table Accounts (Username STRING, Password STRING, key STRING)')
# conn.commit()

# cur.execute('insert into Accounts (Username, Password) values ("sundeep","uchiha")')
# conn.commit()

# to print the table contents
# cur.execute('select * from Accounts')
# print(cur.fetchall())