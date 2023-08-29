from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import Column, Integer, String, and_,Boolean

from models.users import Users


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=False)
    source_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=True, default=True)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Categories.user_id))


