#build in libry that helps to connect .db file and run sql query save/retrive
import sqlite3

#connect/create .db file
conn=sqlite3.connect('garbage.db')

#cursor to.send sql.commands
c=conn.cursor()

#create user table
c.execute("create table if not exists users(id integer primary key autoincrement,name text not null,birth_date text, phone text,address text,email text unique,password text)")

#create complaint table
c.execute("create table if not exists complaints(id integer primary key autoincrement,reported_by text,location text,waste_type text,description text,photo_fileName text,dateTime text,status text default'unresolved',latitude text,longitude text,assigned_to text)")

#authority table
c.execute("CREATE TABLE if not exists authorities(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,region TEXT NOT NULL,region_type TEXT,email TEXT UNIQUE,password TEXT)")


#admin table
c.execute("CREATE TABLE if not exists foundation_admins(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,email TEXT UNIQUE,password TEXT NOT NULL)")
#save changes into db file
conn.commit()

#close the db connection
conn.close()

print('database created')