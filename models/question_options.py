from sqlalchemy.orm import relationship, backref

from database import Base
from sqlalchemy import *

from models.questions import Questions
from models.users import Users


class Question_options(Base):
    __tablename__ = 'question_options'
    id = Column(Integer, primary_key=True, autoincrement=True)
    answer = Column(Text, nullable=False)
    comment = Column(String(255), nullable=True)
    user_id = Column(Integer, nullable=False)
    question_id = Column(Integer, nullable=False)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Question_options.user_id))
    question = relationship("Questions", foreign_keys=[question_id],
                            primaryjoin=lambda: and_(Questions.id == Question_options.question_id),
                            backref=backref("question"))

