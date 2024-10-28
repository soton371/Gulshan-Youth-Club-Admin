

from .database import Base
from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))


class OTP(Base):
    __tablename__ = 'otp'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    otp = Column(String, index=True)
    expiry_time = Column(DateTime)
