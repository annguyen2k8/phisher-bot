import json
import asyncio
import warnings
from base import start_bot

if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    asyncio.set_event_loop_policy()
    
    config = json.loads(open('config.json').read())
    start_bot(config)