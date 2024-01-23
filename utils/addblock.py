from models.blockchain import blockchain
from models.db import DB
async def addblock(data,user_id):
    block = await blockchain.add_block(data=data,user_id=user_id)
    return block.hash 


