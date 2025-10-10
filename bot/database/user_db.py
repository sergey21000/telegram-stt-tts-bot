import json
from pathlib import Path

import aiosqlite

from config.user import UserConfig


class DataBase:
    def __init__(self, db_path: str | Path):
        self.db_path = db_path
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.users_table_name = 'user_configs'

    async def init(self, delete_previous_db: bool = False):
        if delete_previous_db:
            Path(self.db_path).unlink(missing_ok=True)
        await self.init_users_table()

    async def init_users_table(self) -> None:
        query_str = f"""
        CREATE TABLE IF NOT EXISTS {self.users_table_name} (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_name TEXT,
            config_json TEXT NOT NULL
        );
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(query_str)
            await db.commit()

    async def get_user_dict(self, user_id: int) -> dict[str, str | int] | None:
        query_str = f'SELECT * FROM {self.users_table_name} WHERE user_id = ?'
        query_args = (user_id,)
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(query_str, query_args) as cursor:
                result: dict | None = await cursor.fetchone()
                return dict(result) if result else None

    async def get_user_lang(self, user_id: int) -> str | None:
        user_config = await self.get_user_config(user_id=user_id)
        return user_config.user_lang

    async def get_user_config(self, user_id: int) -> UserConfig:
        query = f'SELECT config_json FROM {self.users_table_name}  WHERE user_id = ?'
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(query, (user_id,)) as cursor:
                result = await cursor.fetchone()
            if result:
                return UserConfig.from_dict(json.loads(result[0]))
            else:
                default_config = UserConfig()
                await self.save_user_config(user_id, default_config)
                return default_config

    async def save_user_config(self, user_id: int, config: UserConfig) -> None:
        config_json = json.dumps(config.to_dict())
        query = f'INSERT OR REPLACE INTO {self.users_table_name}  (user_id, config_json) VALUES (?, ?)'
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(query, (user_id, config_json))
            await db.commit()

    async def update_user_config(self, user_id: int, **kwargs) -> UserConfig:
        config = await self.get_user_config(user_id)
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        await self.save_user_config(user_id, config)
        return config
