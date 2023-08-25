from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import *

from models.question_states import Question_states
from models.questions import Questions
from models.users import Users


class Question_state_options(Base):
    __tablename__ = 'question_state_options'
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_state_id = Column(Integer, nullable=False)
    answer = Column(Text, nullable=False)
    comment = Column(String(255), nullable=True)
    user_id = Column(Integer, nullable=False)
    question_id = Column(Integer, nullable=False)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Question_state_options.user_id))
    question = relationship("Questions", foreign_keys=[question_id],
                            primaryjoin=lambda: and_(Questions.id == Question_state_options.question_id))

    question_state = relationship("Question_states", foreign_keys=[question_state_id],
                                  primaryjoin=lambda: and_(Question_states.id == Question_state_options.question_state_id))
