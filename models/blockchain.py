# import hashlib
# import time
# from models.db import DB
# class Block:
#     def __init__(self, index, previous_hash, timestamp, data, hash):
#         self.index = index
#         self.previous_hash = previous_hash
#         self.timestamp = timestamp
#         self.data = data
#         self.hash = hash

# class SimpleBlockchain:
#     def __init__(self):
#         DB.cursor.execute("SELECT * FROM blockchain WHERE index = '1'")
#         result = DB.cursor.fetchone()
#         if result is None:
#             self.chain = [self.create_genesis_block()]
#         else:
#             self.chain = [Block(result[0], result[1], result[2], result[3], result[4])]
#         self.block_by_hash = {self.chain[0].hash: self.chain[0]}

#     def create_genesis_block(self):
#         DB.cursor.execute(f"INSERT INTO blockchain (index, prev_hash, timestamp, data, hash) VALUES ('0', '0', to_timestamp({time.time()}), 'Genesis Block', '{self.calculate_hash(0, "0", int(time.time()), "Genesis Block")}')")
#         return Block(0, "0", int(time.time()), "Genesis Block", self.calculate_hash(0, "0", int(time.time()), "Genesis Block"))

#     def calculate_hash(self, index, previous_hash, timestamp, data):
#         value = f"{index}{previous_hash}{timestamp}{data}".encode()
#         return hashlib.sha256(value).hexdigest()

#     def add_block(self, data):
#         DB.cursor.execute("SELECT COUNT(*) FROM blockchain")
#         result = DB.cursor.fetchone()[0]
#         index = result+1
#         previous_block = self.chain[-1]
#         timestamp = int(time.time())
#         hash_value = self.calculate_hash(index, previous_block.hash, timestamp, data)
#         new_block = Block(index, previous_block.hash, timestamp, data, hash_value)
#         self.chain.append(new_block)
#         self.block_by_hash[hash_value] = new_block

#         DB.cursor.execute(f"INSERT INTO blockchain (index, prev_hash, timestamp, data, hash) VALUES ('{index}', '{previous_block.hash}', to_timestamp({timestamp}), '{data}', '{hash_value}')")
#         DB.conn.commit()


#     def find_block_by_hash(self, target_hash):
#         return self.block_by_hash.get(target_hash, None)

# blockchain = SimpleBlockchain()

import hashlib
import time
from models.db import DB
class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash,owner):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
        self.owner = owner

class SimpleBlockchain:
    def __init__(self):
        DB.cursor.execute("SELECT * FROM blockchain ORDER BY index DESC LIMIT 1")
        result = DB.cursor.fetchall()
        result_row = result[0]
        index, previous_hash, timestamp, data, hash_value,owner = result_row

        self.prev_block = Block(index, previous_hash, timestamp, data, hash_value, owner)


    def calculate_hash(self, index, previous_hash, timestamp, data,owner):
        value = f"{index}{previous_hash}{timestamp}{data}{owner}".encode()
        return hashlib.sha256(value).hexdigest()

    def add_block(self, data,user_id):
        DB.cursor.execute("SELECT * FROM blockchain ORDER BY index DESC LIMIT 1")
        result = DB.cursor.fetchone()
        prev_block = result
        p_index, p_previous_hash, p_timestamp, p_data, p_hash_value,owner = prev_block
        
        index = p_index+1
        previous_block_hash = p_hash_value
        timestamp = int(time.time())
        owner = user_id
        hash_value = self.calculate_hash(index, previous_block_hash, timestamp, data,owner)
        new_block = Block(index, previous_block_hash, timestamp, data, hash_value,owner)
        
        DB.cursor.execute(f"INSERT INTO blockchain (index, prev_hash, timestamp, data, hash,owner) VALUES ('{new_block.index}', '{new_block.previous_hash}', to_timestamp({new_block.timestamp}), '{new_block.data}', '{new_block.hash}','{owner}')")
        DB.conn.commit()
        return new_block
        


blockchain = SimpleBlockchain()


