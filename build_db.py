import sqlite3

db = sqlite3.connect('groomsmen.sqlite')
c = db.cursor()
c.execute('DROP TABLE groomsmen;')
c.execute('''CREATE TABLE groomsmen (name text, last_name text, pronunciation text, phone text, email text, paid int, party_paid int, tux int, march int, bridesmaid text);''')
c.execute("INSERT INTO groomsmen VALUES ('Brian', 'Hoch', 'Hoke', '509.279.4277', 'brianhoch@me.com', 0,0,0,0, 'Nicole');")
c.execute("INSERT INTO groomsmen VALUES ('Craig', 'Maertens', 'Martinz','331.645.1330', 'camaertens@gmail.com', 0,0,0,1, 'Isabel');")
c.execute("INSERT INTO groomsmen VALUES ('Eric', 'Maertens', 'Martinz', '630.903.0957', 'emaertens@gmail.com', 0,0,0,2, 'Lily');")
c.execute("INSERT INTO groomsmen VALUES ('Levi', 'Wood', '', '509.638.9965', 'afserewood@yahoo.com', 0,0,0,3, 'Catherine');")
c.execute("INSERT INTO groomsmen VALUES ('Elijah', 'Hoch', 'Hoke', '509.270.5708', 'ehoch1023@gmail.com', 0,0,0,4, 'Jessie');")

#name = "'test'"

#del_query = "DELETE FROM groomsmen WHERE name={};".format(name)

#c.execute(del_query)

db.commit()
db.close()
