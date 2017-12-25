import pymysql

conn = pymysql.connect(host="127.0.0.1", user="root", password="dntjdwls12", db="scraping")
cur = conn.cursor()
cur.execute("select * from pages where id=2")
print(cur.fetchone())
cur.close()
conn.close()
