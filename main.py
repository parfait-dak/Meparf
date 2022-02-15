''''
import psycopg2

conn = psycopg2.connect('dbname=todoapp user=posgres port=5432')
cursor = conn.cursor()
# Open a cursor to perform database operations
cur = conn.cursor()
# drop any existing todos table
cur.execute("DROP TABLE IF EXISTS todos;")
# (re)create the todos table
# (note: triple quotes allow multiline text in python)
cur.execute("""
CREATE TABLE todos (
 id serial PRIMARY KEY,
 description VARCHAR NOT NULL );""")
conn.commit()
cur.close()
conn.close()
'''''