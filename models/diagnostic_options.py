from sqlalchemy.orm import relationship, backref

from database import Base
from sqlalchemy import Column, Integer, and_

from models.diagnostics import Diagnostics
from models.question_options import Question_options
from models.questions import Questions


class Diagnostic_options(Base):
    __tablename__ = 'diagnostic_options'
    id = Column(Integer, primary_key=True, autoincrement=True)
    diagnostic_id = Column(Integer, nullable=False)
    question_option_id = Column(Integer, nullable=False)
    question_id = Column(Integer)

    diagnostic = relationship("Diagnostics", foreign_keys=[diagnostic_id],
                              primaryjoin=lambda: and_(Diagnostics.id == Diagnostic_options.diagnostic_id))

    question_option = relationship("Question_options", foreign_keys=[question_option_id],
                                         primaryjoin=lambda: and_(Question_options.id ==
                                                                  Diagnostic_options.question_option_id),
                                   backref=backref("question_option_get"))
    question = relationship("Questions", foreign_keys=[question_id],
                            primaryjoin=lambda: and_(Questions.id == Diagnostic_options.question_id),
                            backref=backref("diagnosis_option_question"))

