from sqlalchemy import Column, String, Boolean, sql, Integer, ForeignKey
from sqlalchemy.orm import relationship

from Nails_bot.tgbot.services.db_api.db_gino import TimedBaseModel


class CategoryServices(TimedBaseModel):
    __tablename__ = 'category_services'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    active = Column(Boolean, default=True)
    services = relationship('services')

    query: sql.Select


class Services(TimedBaseModel):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    price = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey('category_services.id'))


    query: sql.Select
