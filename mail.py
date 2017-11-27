import smtplib
import sqlite3
from sqlite3 import Error

class gm:
    def __init__(self, gmail_address, gmail_password, msg):
        self.gmail_address = gmail_address
        self.gmail_password = gmail_password
        self.msg = msg
        self.mailserver = self.connect(gmail_address, gmail_password)

    def connect(self, gmailaddress, gmailpassword):
        mailserver = smtplib.SMTP('smtp.gmail.com', 587)
        mailserver.starttls()
        mailserver.login(gmailaddress, gmailpassword)
        return mailserver

    def send_mail(self, mailto):
        self.mailserver.sendmail(self.gmail_address, mailto, self.msg)
        print("Sent!")

class db:
    def __init__(self, dbfile):
        self.connect(dbfile)
        self.clients()

    def connect(self, dbfile):
        try:
            self.conn = sqlite3.connect(dbfile)
        except Error as e:
            print(e)

    def clients(self):
        clients = []
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM clients')
        rows = cur.fetchall()
        for i in rows:
            clients.append(i[1])
        return clients

    def add(self, client):
        cur = self.conn.cursor()
        cur.execute('INSERT INTO clients (email) VALUES (?)', (client, ))
        print("Added {0}".format(client))
        self.conn.commit()

    def remove_last(self):
        cur = self.conn.cursor()
        client = cur.execute('SELECT * FROM clients WHERE id = (SELECT MAX(id) FROM clients)').fetchall()
        cur.execute('DELETE FROM clients WHERE id = (SELECT MAX(id) FROM clients);')
        print("Removed {0}".format(client))
        self.conn.commit()


gmail_address = ""
gmail_password = ""
msg = "test"

clients = db("clients.db").clients()
db("clients.db").remove_last()



