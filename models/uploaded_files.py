import json

from sqlalchemy import Column, Integer, String, and_
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy.orm import relationship

from database import Base
from models.categories import Categories
from models.users import Users


class Uploaded_files(Base):
    __tablename__ = "uploaded_files"
    id = Column(Integer, autoincrement=True, primary_key=True)
    file = Column(JSONB)   # Change the column type to String to store JSON
    source = Column(String(255))
    source_id = Column(Integer)
    comment = Column(String(255))
    user_id = Column(Integer)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Uploaded_files.user_id))

    category_source = relationship('Categories', foreign_keys=[source_id],
                                   primaryjoin=lambda: and_(Categories.id == Uploaded_files.source_id))
