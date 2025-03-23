
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, validates
from sqlalchemy import String, DateTime, func, ForeignKey 
import uuid
from datetime import date
from typing import List
import re

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'
    user_id:Mapped[uuid.UUID] = mapped_column(default=lambda:uuid.uuid4(),unique=True, primary_key=True) 
    username: Mapped[str] = mapped_column(String(60),nullable=False,unique=True)
    password:Mapped[str] = mapped_column(String, nullable=False)
    date_of_birth: Mapped[date] = mapped_column(DateTime,nullable=True)
    user_img: Mapped[str] = mapped_column(String(225),nullable=True)
    user_cv:Mapped[str] = mapped_column(String(225),nullable=True)
    todos:Mapped[List['Todo']] = relationship(back_populates='user')

    @validates
    def validate_date_of_birth(self,key,value):
        accepted_date = date(1950,1,1)
        if value < accepted_date:
            raise ValueError('date of birth can not be less than 01-01-1950')
        return value

    @validates
    def validate_password(self,key,value):
        if len(value) < 6:
            raise ValueError('Password must be at least 6 characters long')

        if not re.search(r'[A-Za-z]', value):  # Check for at least one letter
            raise ValueError('Password must include at least one letter')

        if not re.search(r'\d', value):  # Check for at least one number
            raise ValueError('Password must include at least one number')
        
        return value





class Todo(Base):
    __tablename__ = 'todo'
    todo_id:Mapped[uuid.UUID] = mapped_column(default=lambda: uuid.uuid4(), primary_key=True)
    title:Mapped[str]= mapped_column(String)
    content:Mapped[str]= mapped_column(String)
    completed:Mapped[bool] = mapped_column(default=False,nullable=False)
    created_at :Mapped[DateTime] = mapped_column(DateTime,default=func.now())
    updated_at:Mapped[DateTime]= mapped_column(DateTime,default=func.now(),nullable=False)
    user_id:Mapped[uuid.UUID] = mapped_column(ForeignKey('user.user_id'))
    user: Mapped['User'] = relationship('User', back_populates='todos', uselist=False)

