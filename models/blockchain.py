import hashlib
import time
from models.db import DB

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash, owner):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
        self.owner = owner

class SimpleBlockchain:
    def __init__(self):
        # result = await DB.get_last_block()

        # index, previous_hash, timestamp, data, hash_value, owner = result

        # self.prev_block = Block(index, previous_hash, timestamp, data, hash_value, owner)
        pass


    async def calculate_hash(self, index, previous_hash, timestamp, data, owner):
        value = f"{index}{previous_hash}{timestamp}{data}{owner}".encode()
        return hashlib.sha256(value).hexdigest()

    async def add_block(self, data, user_id):
        result = await DB.get_last_block()
        prev_block = result
        p_index, p_previous_hash, p_timestamp, p_data, p_hash_value, owner = prev_block
        
        index = p_index + 1
        previous_block_hash = p_hash_value
        timestamp = int(time.time())
        owner = user_id
        hash_value = await self.calculate_hash(index, previous_block_hash, timestamp, data, owner)
        new_block = Block(index, previous_block_hash, timestamp, data, hash_value, owner)
        await DB.create_block(new_block.index, new_block.previous_hash, new_block.timestamp, new_block.data, new_block.hash, owner)
        
        return new_block

blockchain = SimpleBlockchain()


