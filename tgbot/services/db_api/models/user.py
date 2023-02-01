

from sqlalchemy import Column, BigInteger, String, sql

from Nails_bot.tgbot.services.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    name = Column(String(255))

    query: sql.Select

