from sqlalchemy import Column, Integer, String, and_

from sqlalchemy.orm import relationship, backref

from database import Base
from models.categories import Categories
from models.customers import Customers
from models.question_states import Question_states
from models.users import Users


class Uploaded_files(Base):
    __tablename__ = "uploaded_files"
    id = Column(Integer, autoincrement=True, primary_key=True)
    file = Column(String(999))
    source = Column(String(255))
    source_id = Column(Integer)
    comment = Column(String(255))
    user_id = Column(Integer)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Uploaded_files.user_id))

    category_source = relationship('Categories', foreign_keys=[source_id],
                                   primaryjoin=lambda: and_(Categories.id == Uploaded_files.source_id,
                                                    Uploaded_files.source == "category"), backref=backref("category_files"))
    this_user = relationship('Users', foreign_keys=[source_id],
                             primaryjoin=lambda: and_(Users.id == Uploaded_files.source_id,
                                                      Uploaded_files.source == "user"), backref=backref("user_files"))
    this_customer = relationship('Customers', foreign_keys=[source_id],
                             primaryjoin=lambda: and_(Customers.id == Uploaded_files.source_id,
                                                      Uploaded_files.source == "customer"), backref=backref("customer_files"))

    state_source = relationship('Question_states', foreign_keys=[source_id],
                                 primaryjoin=lambda: and_(Question_states.id == Uploaded_files.source_id,
                                                            Uploaded_files.source == "question_state"),
                                   backref=backref("state_files"))
