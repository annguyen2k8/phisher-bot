import discord
import aiosqlite

from typing import Any, Optional
from modules.ext import Database, BaseTable

discord.Embed()

class FisherEmbed(BaseTable):
    def __init__(self, database) -> None:
        super().__init__(database)
    
    async def create_table(self):
        await self._db.execute('PRAGMA FOREIGN_KEYS = ON;')
        
        await self._db.execute(
            '''
            CREATE TABLE IF NOT EXISTS
            FISHER_EMBED(
                ID INT PRIMARY KEY AUTOINCREMENT,
                GUILD_ID INT NOT NULL,
                TITLE STR NOT NULL,
                DESCRIPTION STR NOT NULL,
                BUTTON_LABLE STR NOT NULL,
                FOREIGN KEY (GUILD_ID)
                REFERENCES GUILD (ID)
                ON DELETE CASCADE
            )'''
        )

    async def update_embed(
            self,
            guildId: int,
            title: Optional[str],
            description: Optional[str],
            button_label: Optional[str]
        ) -> None:
        await self._db.execute(
            '''
            UPDATE FISHER_EMBED
            SET TITLE = ?,
                DESCRIPTION = ?,
                BUTTON_LABLE = ?
            WHERE GUILD_ID = ?
            ''',
            (title, description, button_label, guildId)
            )
    
    async def fetch_embed(self, guildId: int) -> None:
        return await self._db.execute(
            '''
            SELECT TITLE, DESCRIPTION, BUTTON_LABLE
            FROM FISHER_ENBED 
            WHERE GUILD_ID = ?
            ''', 
            (guildId,)
            )

class Guild(BaseTable):    
    def __init__(self, database) -> None:
        super().__init__(database)
    
    async def create_table(self) -> None:   
        await self._db.execute('PRAGMA FOREIGN_KEYS = ON;')
        
        await self._db.execute(
            '''
            CREATE TABLE IF NOT EXISTS
            OAUTH_EMBED(
                ID INT PRIMARY KEY AUTOINCREMENT,
                GUILD_ID INT NOT NULL,
                TITLE STR,
                DESCRIPTION STR NOT NULL,
                BUTTON_LABLE STR NOT NULL,
                BUTTON_LINK STR NOT NULL,
                FOREIGN KEY (GUILD_ID)
                REFERENCES GUILD (ID)
                ON DELETE CASCADE
            )
            '''
        )
        
        await self._db.execute(
            '''
            
            '''
        )
        
        await self._db.execute(
            '''
            CREATE TABLE IF NOT EXISTS
            GUILD(
                ID INT PRIMARY KEY,
            )
            '''
        )
    
    # async def insert_guild(self, guildId:int) -> None:
    #     ...

    # async def remove_guild(self) -> None:
    #     ... 
    
    # async def update_oauth_embed(self) -> None:
    #     ...
    
    # async def fetch_oauth_embed(self) -> None:
    #     ...
    
