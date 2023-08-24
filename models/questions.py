from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import Column, String, Integer, and_

from models.categories import Categories
from models.question_types import Question_types
from models.users import Users


class Questions(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=True)
    category_id = Column(Integer)
    step = Column(Integer, nullable=False)
    question_type_id = Column(Integer)
    user_id = Column(Integer, nullable=False)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Questions.user_id))
    category = relationship('Categories', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Categories.id == Questions.category_id))
    question_type = relationship('Question_types', foreign_keys=[question_type_id],
                                 primaryjoin=lambda: and_(Question_types.id == Questions.question_type_id))
