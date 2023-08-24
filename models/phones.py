from sqlalchemy.orm import relationship, backref

from database import Base
from sqlalchemy import Column, Integer, String, and_

from models.customers import Customers
from models.users import Users


class Phones(Base):
    __tablename__ = 'phones'
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    source = Column(String(255), nullable=False)
    source_id = Column(Integer, nullable=False)
    comment = Column(String(255), nullable=True)
    user_id = Column(Integer, nullable=False)

    user = relationship('Users', foreign_keys=[user_id],
                                primaryjoin=lambda: and_(Users.id == Phones.user_id))

    this_user = relationship('Users', foreign_keys=[source_id],
                             primaryjoin=lambda: and_(Users.id == Phones.source_id, Phones.source == "user"),
                             backref=backref("user_phones"))

    this_customer = relationship('Customers', foreign_keys=[source_id],
                                primaryjoin=lambda: and_(Customers.id == Phones.source_id,
                                                         Phones.source == "customer"), backref=backref("customer_phones"))

