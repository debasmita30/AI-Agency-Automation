from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Lead(Base):

    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    project_description = Column(Text)
    project_type = Column(String)
    proposal = Column(Text)