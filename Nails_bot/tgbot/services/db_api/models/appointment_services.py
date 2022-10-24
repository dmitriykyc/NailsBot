import sqlalchemy
from sqlalchemy import Column, Integer, DATETIME, DateTime, ForeignKey, sql, Boolean, BigInteger
from sqlalchemy.orm import relationship

from Nails_bot.tgbot.services.db_api.db_gino import TimedBaseModel


class Appointment(TimedBaseModel):
    __tablename__ = 'appointment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'))
    id_master = Column(Integer, ForeignKey('Masters.master_id'))
    datetime = Column(DateTime)
    services = relationship('appointment_services')
    active = Column(Boolean, default=True)

    query: sql.Select


class AppointmentServices(TimedBaseModel):
    __tablename__ = 'appointment_services'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_appointment = Column(Integer, ForeignKey('appointment.id'))
    id_services = Column(Integer, ForeignKey('services.id'))

    query: sql.Select
