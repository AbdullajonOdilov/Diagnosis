from sqlalchemy.orm import relationship, backref

from database import Base
from sqlalchemy import Column, String, Integer, and_, Text

from models.question_options import Question_options
from models.question_states import Question_states
from models.users import Users


class Question_options_answers(Base):
    __tablename__ = 'question_options_answer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_state_id = Column(Integer, nullable=False)
    question_option_id = Column(Integer, nullable=False)
    answer = Column(Text, nullable=False)
    comment = Column(String(255), nullable=True)
    user_id = Column(Integer, nullable=False)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Question_options_answers.user_id))

    question_state = relationship("Question_states", foreign_keys=[question_state_id],
                            primaryjoin=lambda: and_(Question_states.id == Question_options_answers.question_state_id))
    question_option = relationship("Question_options", foreign_keys=[question_option_id],
                            primaryjoin=lambda: and_(Question_options.id == Question_options_answers.question_option_id),
                                   backref=backref("question_options_answer"))



