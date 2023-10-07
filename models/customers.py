from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import Column, String, Integer, and_,Boolean

from models.users import Users


class Customers(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=True)
    user_id = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=True, default=True)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Customers.user_id))

