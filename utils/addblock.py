from models.blockchain import blockchain

async def addblock(data,user_id):
    block = blockchain.add_block(data=data,user_id=user_id)
    return block.hash 
    