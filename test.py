import json

with open('config.json') as f:
    apikey = json.loads(f.read())['apikey'].get('hypixel')

import hypixel
from hypixel import HypixelException
import asyncio
import selectors

class MyPolicy(asyncio.DefaultEventLoopPolicy):
   def new_event_loop(self):
      selector = selectors.SelectSelector()
      return asyncio.SelectorEventLoop(selector)

asyncio.set_event_loop_policy(MyPolicy())

async def main():
    client = hypixel.Client(apikey)
    async with client:
        try:
            player = await client.player('Technoblade')
            print(f'[{player.level}✫] [{player.rank}] {player.name}')
        except HypixelException as error:
            print(error)

if __name__ == '__main__':
    asyncio.run(main())