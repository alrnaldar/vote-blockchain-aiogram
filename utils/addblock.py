from models.blockchain import blockchain

async def addblock(data):
    block = blockchain.add_block(data=data)
    return block.hash
    