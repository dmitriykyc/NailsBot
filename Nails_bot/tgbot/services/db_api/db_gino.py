import datetime
from typing import List

from aiogram import Dispatcher
from gino import Gino
import sqlalchemy as sa

from Nails_bot.tgbot.config import load_config

config = load_config(r'D:\Programming\TG_BOTS\Nails_bot\Nails_bot\.env')
db = Gino()

class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = db.Column(db.DateTime(True), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=db.func.now())


async def on_startup(dispatcher: Dispatcher):
    await db.set_bind(config.db.postgres_uri)

async def close_startup(dispatcher: Dispatcher):
    await db.pop_bind().close()
