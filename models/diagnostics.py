from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import Column, Integer, and_, Boolean, Date, func

from models.categories import Categories
from models.customers import Customers
from models.users import Users


class Diagnostics(Base):
    __tablename__ = 'diagnostics'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False, default=False)
    date = Column(Date, nullable=False, default=func.now())

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Diagnostics.user_id))

    customer = relationship("Customers", foreign_keys=[customer_id],
                            primaryjoin=lambda: and_(Customers.id == Diagnostics.customer_id))

    category = relationship("Categories", foreign_keys=[category_id],
                            primaryjoin=lambda: and_(Categories.id == Diagnostics.category_id))
