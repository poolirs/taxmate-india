from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    file_path = Column(String, nullable=False)
    document_type = Column(String)
    parsed_data = Column(JSON)

class TaxCalculation(Base):
    __tablename__ = 'tax_calculations'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tax_year = Column(String, nullable=False)
    income_data = Column(JSON)
    calculated_tax = Column(JSON)

class ChatSession(Base):
    __tablename__ = 'chat_sessions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    messages = Column(JSON)  # Or use Text if storing as one big string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
