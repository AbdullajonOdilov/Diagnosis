from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import Column, String, Integer, and_, Text

from models.question_state_options import Question_state_options
from models.users import Users


class Question_state_answers(Base):
    __tablename__ = 'question_state_answers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_state_option_id = Column(Integer, nullable=False)
    answer = Column(Text, nullable=False)
    comment = Column(String(255), nullable=True)
    user_id = Column(Integer, nullable=False)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Question_state_answers.user_id))

    question_state_option = relationship("Question_state_options", foreign_keys=[question_state_option_id],
                            primaryjoin=lambda: and_(Question_state_options.id == Question_state_answers.question_state_option_id))

