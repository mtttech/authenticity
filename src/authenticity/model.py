"""
cli.py
Author:     Marcus T Taylor
Created:    23.11.23
Modified:   16.05.26
Purpose:    Main script.
"""

from typing import Optional

from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


DATABASE_URL = "sqlite:///authenticity.db"


class Base(DeclarativeBase):
    pass


class Exercises(Base):
    __tablename__ = "exercises"
    exercise_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workout_id: Mapped[int] = mapped_column(Integer)
    exercise_name: Mapped[str] = mapped_column(String(100))
    exercise_set: Mapped[int] = mapped_column(Integer)
    exercise_reps: Mapped[int] = mapped_column(Integer)
    exercise_weight: Mapped[int] = mapped_column(Integer)


class Workouts(Base):
    __tablename__ = "workouts"
    workout_id: Mapped[int] = mapped_column(primary_key=True)
    workout_title: Mapped[str] = mapped_column(String(100), nullable=False)
    workout_date: Mapped[str] = mapped_column(String(30))
    workout_category: Mapped[str] = mapped_column(String(20))
    workout_duration: Mapped[int] = mapped_column(Integer)
    workout_comments: Mapped[Optional[str]]


engine = create_engine(DATABASE_URL)
