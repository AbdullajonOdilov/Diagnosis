from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import Column, Integer, and_

from models.diagnostics import Diagnostics


class Diagnostic_options(Base):
    __tablename__ = 'diagnostic_options'
    id = Column(Integer, primary_key=True, autoincrement=True)
    diagnostic_id = Column(Integer, nullable=False)
    question_state_option_id = Column(Integer, nullable=False)

    diagnostic = relationship("Diagnostics", foreign_keys=[diagnostic_id],
                              primaryjoin=lambda: and_(Diagnostics.id == Diagnostic_options.diagnostic_id))

    question_state_option = relationship("Question_state_options", foreign_keys=[question_state_option_id],
                                         primaryjoin=lambda: and_(Diagnostics.id == Diagnostic_options.question_state_option_id))
