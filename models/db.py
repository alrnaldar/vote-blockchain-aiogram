import psycopg2
from psycopg2 import sql
from config import *
class Database:
    async def create(self):
        self.conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        self.cursor = self.conn.cursor()
        # self.cursor.execute("""
        #     CREATE TABLE IF NOT EXISTS blockchain (
        #         index SERIAL PRIMARY KEY,
        #         prev_hash VARCHAR NOT NULL,
        #         timestamp TIMESTAMP NOT NULL,
        #         data VARCHAR NOT NULL,
        #         hash VARCHAR NOT NULL UNIQUE
        #     )
        # """)
    

        # self.cursor.execute("""

        #     CREATE TABLE IF NOT EXISTS users (
        #         id VARCHAR PRIMARY KEY
        #     )
        # """)

        # self.cursor.execute("""
        #     CREATE TABLE IF NOT EXISTS polls (
        #         id SERIAL PRIMARY KEY,
        #         block VARCHAR REFERENCES blockchain(hash),
        #         title VARCHAR NOT NULL,
        #         user_id VARCHAR REFERENCES users(id) NOT NULL
        #     )
        # """)

        # self.cursor.execute("""
        #     CREATE TABLE IF NOT EXISTS options (
        #         id SERIAL PRIMARY KEY,
        #         block VARCHAR REFERENCES blockchain(hash),
        #         text VARCHAR NOT NULL,
        #         poll_id INTEGER REFERENCES polls(id) NOT NULL
        #     )
        # """)

        # self.cursor.execute("""
        #     CREATE TABLE IF NOT EXISTS votes (
        #         id SERIAL PRIMARY KEY,
        #         block VARCHAR REFERENCES blockchain(hash),
        #         user_id VARCHAR REFERENCES users(id) NOT NULL,
        #         poll_id VARCHAR REFERENCES polls(id) NOT NULL,
        #         option_id INTEGER REFERENCES options(id) NOT NULL
        #     )
        # """)
        
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
        
            data.append({'user_id': i[0]})
        
        return users_count,polls_count,data
    
    async def create_user(self,user_id):
        self.cursor.execute(f"SELECT COUNT(*) FROM users WHERE id = '{user_id}'")
        self.count = self.cursor.fetchone()[0]
        if self.count > 0:
            print("Пользователь уже существует.")
        else:
            self.cursor.execute(f"""
                INSERT INTO users (id)
                VALUES ('{user_id}')
            """)
            self.conn.commit()
            print("Пользователь успешно зарегистрирован.")

    async def create_poll(self,name,user_id):
        from utils import addblock
        hash = await addblock.addblock(f"poll:{name}")

        self.cursor.execute(f"INSERT INTO polls(block,title,user_id) VALUES('{hash}','{name}','{user_id}')")
        self.cursor.execute(f"SELECT id FROM polls WHERE block = '{hash}'")
        poll_id = self.cursor.fetchone()[0]
        return poll_id
    async def create_option(self,poll_id,option):
        from utils import addblock
        hash = await addblock.addblock(f"option:{option}")
        self.cursor.execute(f"INSERT INTO options(block,text,poll_id) VALUES('{hash}','{option}','{poll_id}')")
        print(f"запись {option} создана 2")
    
    async def find_poll_by_hash(self,hash):
        self.cursor.execute(f"SELECT * FROM polls WHERE block = '{hash}'")
        result = self.cursor.fetchone()
        poll_id, block, title, user_id = result
        return result
    async def find_options_for_poll(self,id):
        self.cursor.execute(f"SELECT * FROM options WHERE poll_id = '{id}'")
        result = self.cursor.fetchall()
        return result

DB = Database()
