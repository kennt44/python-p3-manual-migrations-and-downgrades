import os
import sys
from datetime import datetime

# Add current working directory to sys path for module resolution
sys.path.append(os.getcwd())

# SQLAlchemy imports
from sqlalchemy import create_engine, desc
from sqlalchemy import CheckConstraint, UniqueConstraint, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Create SQLite engine
engine = create_engine('sqlite:///migrations_test.db')

# Create the base class for declarative models
Base = declarative_base()

# Define the Student model
class Student(Base):
    __tablename__ = 'students'

    # Define columns
    id = Column(Integer(), primary_key=True)
    name = Column(String(), index=True)
    email = Column(String(55), unique=True, nullable=False)  # Adding unique constraint on email
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    # Constraints
    __table_args__ = (
        CheckConstraint('grade >= 0', name='check_grade_non_negative'),  # Check constraint for grade
        UniqueConstraint('email', name='uq_email'),  # Unique constraint for email
    )

    def __repr__(self):
        return f"Student {self.id}: " \
               + f"{self.name}, " \
               + f"Grade {self.grade}, " \
               + f"Email: {self.email}, " \
               + f"Enrolled on: {self.enrolled_date}"
