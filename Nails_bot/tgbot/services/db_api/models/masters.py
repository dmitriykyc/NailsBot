from sqlalchemy import Column, Integer, String, Text, Boolean, sql

from Nails_bot.tgbot.services.db_api.db_gino import TimedBaseModel


class Master(TimedBaseModel):
    __tablename__ = 'Masters'

    master_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    photo_master_id = Column(Text)
    disc_master = Column(Text, nullable=False)
    working = Column(Boolean, default=True)

    query: sql.Select




