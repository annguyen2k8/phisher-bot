from modules.ext import Database
from modules.embed_func import Embed

import asyncio

if __name__ == '__main__':
    database = Database('test.db')
    embed = Embed(database)
    asyncio.run(embed.create_table())