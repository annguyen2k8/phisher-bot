from modules.ext import BaseTable

class Config(BaseTable):
    def __init__(self, database) -> None:
        super().__init__(database)
    
    async def create_table(self):
        await self._db.execute(
            '''
            CREATE TABLE IF NOT EXISTS
            CONFIG(
                GUILD_ID INT PRIMARY KEY,
                WEBHOOK_URL STR
            )
            '''
        )
    
    async def set_webhook_url(
            self,
            guild_id:int,
            webhook_url:str
        ) -> None:
        await self._db.execute(
            '''
            INSERT INTO CONFIG
                VALUES({guild_id}, {webhook_url})
            UPDATE CONFIG
                SET WEBHOOK_URL = {webhook_url}
                WHERE GUILD_ID = {guild_id}
            '''.format(
                guild_id=guild_id,
                webhook_url=webhook_url
                )
            )
    
    async def fetch_webhook_url(self, guild_id: int) -> str:
        return await self._db.execute(
            '''
            SELECT WEBHOOK_URL
            FROM CONFIG 
            WHERE GUILD_ID = {guild_id}
            '''.format(guild_id=guild_id)
            )[1]
    
    async def remove_config(self, guild_id: int) -> None:
        await self._db.execute('DELETE FROM EMBED WHERE GUILD_ID = {guild_id}'.format(guild_id=guild_id))