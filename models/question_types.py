from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import Column, String, Integer, and_

from models.users import Users


class Question_types(Base):
    __tablename__ = 'question_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=True)
    user_id = Column(Integer, nullable=False)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Question_types.user_id))

