import psycopg2
from psycopg2 import sql
from config import *
class Database:
    async def create(self):
        self.conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PORT, host=DB_HOST, port=DB_PORT)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR PRIMARY KEY,
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS polls (
                id SERIAL PRIMARY KEY,
                title VARCHAR NOT NULL,
                description VARCHAR,
                user_id INTEGER REFERENCES users(id) NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS options (
                id SERIAL PRIMARY KEY,
                text VARCHAR NOT NULL,
                poll_id INTEGER REFERENCES polls(id) NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) NOT NULL,
                poll_id INTEGER REFERENCES polls(id) NOT NULL,
                option_id INTEGER REFERENCES options(id) NOT NULL
            )
        """)

        self.conn.commit()
    async def admin_select_all(self):
        self.cursor.execute("SELECT COUNT(*) FROM users;")
        users_count = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT * FROM users;")
        users = self.cursor.fetchall()

        self.cursor.execute("SELECT COUNT(*) FROM polls;")
        polls_count = self.cursor.fetchone()[0]

        data = []
           
        for i in users:
        
            data.append({'user_id': i})
        
        return users_count,polls_count,data
    
    async def create_user(self,user_id):
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = %s ", (user_id))
        self.count = self.cursor.fetchone()[0]

        if self.count > 0:
            print("Пользователь уже существует.")
        else:
            self.cursor.execute("""
                INSERT INTO users (user_id)
                VALUES (%s)
            """, (user_id))
            self.conn.commit()
            print("Пользователь успешно зарегистрирован.")

DB = Database()