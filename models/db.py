# import psycopg2
# from psycopg2 import sql
# from config import *
# class Database:
#     async def create(self):
#         self.conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
#         self.cursor = self.conn.cursor()
#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                 id SERIAL PRIMARY KEY,
#                 blocks VARCHAR
#             );
#         """)

#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS blockchain (
#                 index SERIAL PRIMARY KEY,
#                 prev_hash VARCHAR NOT NULL,
#                 timestamp TIMESTAMP NOT NULL,
#                 data VARCHAR NOT NULL,
#                 hash VARCHAR NOT NULL UNIQUE,
#                 owner INTEGER REFERENCES users(id)
#             );
#         """)

#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS polls (
#                 block VARCHAR REFERENCES blockchain(hash) PRIMARY KEY,
#                 title VARCHAR NOT NULL
#             );
#         """)

#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS options (
#                 block VARCHAR REFERENCES blockchain(hash) PRIMARY KEY,
#                 text VARCHAR NOT NULL,
#                 poll_block VARCHAR REFERENCES polls(block) NOT NULL
#             );
#         """)

#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS votes (
#                 block VARCHAR REFERENCES blockchain(hash) PRIMARY KEY,
#                 poll_block VARCHAR REFERENCES polls(block) NOT NULL,
#                 option_block VARCHAR REFERENCES options(block) NOT NULL
#             );
#         """)
        
#         self.conn.commit()
#     async def admin_select_all(self):
#         self.cursor.execute("SELECT COUNT(*) FROM users;")
#         users_count = self.cursor.fetchone()[0]

#         self.cursor.execute("SELECT * FROM users;")
#         users = self.cursor.fetchall()

#         self.cursor.execute("SELECT COUNT(*) FROM polls;")
#         polls_count = self.cursor.fetchone()[0]

#         data = []
           
#         for i in users:
        
#             data.append({'user_id': i[0]})
        
#         return users_count,polls_count,data
    
#     async def create_user(self,user_id):
#         self.cursor.execute(f"SELECT COUNT(*) FROM users WHERE id = '{user_id}'")
#         self.count = self.cursor.fetchone()[0]
#         if self.count > 0:
#             print("Пользователь уже существует.")
#         else:
#             self.cursor.execute(f"""
#                 INSERT INTO users (id)
#                 VALUES ('{user_id}')
#             """)
#             self.conn.commit()
#             print("Пользователь успешно зарегистрирован.")

#     async def create_poll(self,name,user_id):
#         from utils import addblock

#         hash = await addblock.addblock(f"poll:{name}",user_id)

#         self.cursor.execute(f"INSERT INTO polls(block,title) VALUES('{hash}','{name}')")
#         poll_block = hash
#         self.conn.commit()
#         return poll_block
        
        
#     async def create_option(self,poll_block,option,user_id):
#         from utils import addblock
#         hash = await addblock.addblock(f"option:{option}",user_id)
#         self.cursor.execute(f"INSERT INTO options(block,text,poll_block) VALUES('{hash}','{option}','{poll_block}')")
#         self.conn.commit()

#     async def create_vote(self, option_block,poll_block,user_id):
#         from utils import addblock
#         hash = await addblock.addblock(f"vote:option[{option_block}],poll:[{poll_block}]",user_id)
#         self.cursor.execute(f"INSERT INTO votes(block,poll_block,option_block) VALUES('{hash}','{poll_block}','{option_block}')")
#         self.conn.commit()

#     async def find_poll_by_hash(self,hash):
#         try:
#             self.cursor.execute(f"SELECT * FROM polls WHERE block = '{hash}'")
#             result = self.cursor.fetchone()
#             block, title = result
#             return result
#         except Exception:
#             return False
#     async def find_options_for_poll(self,poll_block):
#         self.cursor.execute(f"SELECT * FROM options WHERE poll_block = '{poll_block}'")
#         result = self.cursor.fetchall()
#         return result
#     async def search_by_hash(self, hash):
#         try:
#             self.cursor.execute(f"SELECT * FROM blockchain WHERE hash = '{hash}'")
#             result = self.cursor.fetchone()
#             return result
#         except Exception:
#             return False
#     async def my_blocks(self, user_id):
#         try:
#             self.cursor.execute(f"SELECT * FROM blockchain WHERE owner = '{user_id}'")
#             result = self.cursor.fetchall()
#             return result
#         except Exception:
#             return False
#     async def show_stat_on_poll(self, poll_block,option_block):
#         try:
#             self.cursor.execute(f"SELECT COUNT(*) FROM votes WHERE poll_block = '{poll_block}' AND option_block = '{option_block}'")
#             result = self.cursor.fetchone()[0]
#             return result
#         except Exception:
#             return False
        
# DB = Database()

import asyncpg
from config import *

class Database:
    async def create(self):
        self.pool = await asyncpg.create_pool(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id BIGINT PRIMARY KEY
                    );
                ''')

                await connection.execute('''
                    CREATE TABLE IF NOT EXISTS blockchain (
                        index SERIAL PRIMARY KEY,
                        prev_hash VARCHAR NOT NULL,
                        timestamp TIMESTAMP NOT NULL,
                        data VARCHAR NOT NULL,
                        hash VARCHAR NOT NULL UNIQUE,
                        owner BIGINT  REFERENCES users(id)
                    );
                ''')

                await connection.execute('''
                    CREATE TABLE IF NOT EXISTS polls (
                        block VARCHAR REFERENCES blockchain(hash) PRIMARY KEY,
                        title VARCHAR NOT NULL
                    );
                ''')

                await connection.execute('''
                    CREATE TABLE IF NOT EXISTS options (
                        block VARCHAR REFERENCES blockchain(hash) PRIMARY KEY,
                        text VARCHAR NOT NULL,
                        poll_block VARCHAR REFERENCES polls(block) NOT NULL
                    );
                ''')

                await connection.execute('''
                    CREATE TABLE IF NOT EXISTS votes (
                        block VARCHAR REFERENCES blockchain(hash) PRIMARY KEY,
                        poll_block VARCHAR REFERENCES polls(block) NOT NULL,
                        option_block VARCHAR REFERENCES options(block) NOT NULL
                    );
                ''')

    async def admin_select_all(self):
        async with self.pool.acquire() as connection:
            users_count = await connection.fetchval('SELECT COUNT(*) FROM users;')
            users = await connection.fetch('SELECT * FROM users;')
            polls_count = await connection.fetchval('SELECT COUNT(*) FROM polls;')

            data = [{'user_id': user['id']} for user in users]

            return users_count, polls_count, data

    async def create_user(self, user_id):
        async with self.pool.acquire() as connection:
            count = await connection.fetchval(f"SELECT COUNT(*) FROM users WHERE id = '{user_id}'")
            if count > 0:
                print("Пользователь уже существует.")
            else:
                await connection.execute(f"INSERT INTO users (id) VALUES ('{user_id}')")
                print("Пользователь успешно зарегистрирован.")

    async def create_poll(self, name, user_id):
        from utils import addblock

        hash_value = await addblock.addblock(f"poll:{name}", user_id)

        async with self.pool.acquire() as connection:
            await connection.execute(f"INSERT INTO polls(block, title) VALUES('{hash_value}', '{name}')")
            return hash_value

    async def create_option(self, poll_block, option, user_id):
        from utils import addblock

        hash_value = await addblock.addblock(f"option:{option}", user_id)

        async with self.pool.acquire() as connection:
            await connection.execute(f"INSERT INTO options(block, text, poll_block) VALUES('{hash_value}', '{option}', '{poll_block}')")

    async def create_vote(self, option_block, poll_block, user_id):
        from utils import addblock

        hash_value = await addblock.addblock(f"vote:option[{option_block}],poll:[{poll_block}]", user_id)

        async with self.pool.acquire() as connection:
            await connection.execute(f"INSERT INTO votes(block, poll_block, option_block) VALUES('{hash_value}', '{poll_block}', '{option_block}')")

    async def find_poll_by_hash(self, hash):
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetchrow(f"SELECT * FROM polls WHERE block = '{hash}'")
                return result
        except Exception:
            return None

    async def find_options_for_poll(self, poll_block):
        async with self.pool.acquire() as connection:
            result = await connection.fetch(f"SELECT * FROM options WHERE poll_block = '{poll_block}'")
            return result

    async def search_by_hash(self, hash):
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetchrow(f"SELECT * FROM blockchain WHERE hash = '{hash}'")
                return result
        except Exception:
            return None

    async def my_blocks(self, user_id):
        try:
            async with self.pool.acquire() as connection:
                count = await connection.fetchval(f"SELECT COUNT(*) FROM blockchain WHERE owner = '{user_id}'")
                result = await connection.fetch(f"SELECT * FROM blockchain WHERE owner = '{user_id}'")
                return result,count
        except Exception:
            return None

    async def show_stat_on_poll(self, poll_block, option_block):
        try:
            async with self.pool.acquire() as connection:
                result = await connection.fetchval(f"SELECT COUNT(*) FROM votes WHERE poll_block = '{poll_block}' AND option_block = '{option_block}'")
                return result
        except Exception:
            return None
    async def get_last_block(self):
        async with self.pool.acquire() as connection:
            result = await connection.fetchrow("SELECT * FROM blockchain ORDER BY index DESC LIMIT 1")
            return result
    async def create_block(self,index,prev_hash,timestamp,data,hash,owner):
        async with self.pool.acquire() as connection:
            await connection.execute(f"INSERT INTO blockchain (index, prev_hash, timestamp, data, hash,owner) VALUES ('{index}', '{prev_hash}', to_timestamp({timestamp}), '{data}', '{hash}','{owner}')")


DB = Database()