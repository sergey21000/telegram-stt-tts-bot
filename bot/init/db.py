from bot.database.user_db import DataBase
from config.config import Config


db = DataBase(db_path=Config.BOT_DB_PATH)
