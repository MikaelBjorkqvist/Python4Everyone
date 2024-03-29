import sqlite3


conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('''
DROP TABLE IF EXISTS Counts''')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

fname = "mbox.txt"
fh = open(fname)


for line in fh:

    if not line.startswith('From: ') : continue
    pieces = line.split()
    email = pieces[1]
    (emailname, organization) = email.split("@")
    print(email)

    cur.execute('SELECT count FROM Counts WHERE org = ? ', (organization, ))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count) 
                VALUES ( ?, 1 )''', ( organization, ) )
    else :
        cur.execute('UPDATE Counts SET count=count+1 WHERE org = ?',
            (organization, ))


conn.commit()


sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'
print
print("Counts:")
for row in cur.execute(sqlstr) :
    print(str(row[0]), row[1])

#Closing the DB
cur.close()
