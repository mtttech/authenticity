"""
models.py
Author:     Marcus T Taylor
Created:    26.11.23
Modified:   03.07.25
"""

import os

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

db_path = os.path.join(os.path.expanduser("~"), "authenticity.db")
engine = create_engine(f"sqlite:///{db_path}")
Base = declarative_base()


class Exercises(Base):
    __tablename__ = "exercises"
    exercise_id = Column(Integer, primary_key=True)
    workout_id = Column(Integer)
    exercise_name = Column(String)
    exercise_set = Column(Integer)
    exercise_reps = Column(Integer)
    exercise_weight = Column(Integer)


class Workouts(Base):
    __tablename__ = "workouts"
    workout_id = Column(Integer, primary_key=True)
    workout_title = Column(String)
    workout_date = Column(String)


Base.metadata.create_all(engine)
