from sqlalchemy import Column,Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Document(Base):
    __tablename__="documents"
    document_id=Column(Integer,primary_key=True,index=True)
    document_name=Column(String,index=True,nullable=False)
    document_type=Column(String,index=True,nullable=False)
    owner_id=Column(Integer,ForeignKey("users.id"))

    owner=relationship("User",back_populates="documents")
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True, index=True)
    username=Column(String,index=True,nullable=False)
    email=Column(String,index=True,nullable=False)
    password=Column(String,nullable=True)

    documents=relationship("document",back_populates="owner")


