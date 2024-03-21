"""
read.py
Author:     Marcus T Taylor
Created:    14.03.24
Modified:   16.03.24
"""
from sqlalchemy import select

from authfit.models import Exercises, Workouts, engine


def main() -> None:
    print("Displaying database data.")

    with engine.connect() as conn: # pyright: ignore[reportGeneralTypeIssues]
        results = conn.execute(select(Workouts.workout_title))
        for row in results:
            print(row)

        stmt = (
            select(
                Workouts.workout_id,
                Workouts.workout_date,
                Workouts.workout_title,
                Exercises.exercise_name,
                Exercises.exercise_weight,
                Exercises.exercise_set,
                Exercises.exercise_reps,
            )
            .select_from(Workouts)
            .join(Exercises, Workouts.workout_id == Exercises.workout_id)
        )
        for row in conn.execute(stmt):
            print(row)

        # Workout datasheet example
        try:
            stmt = select(Workouts).where(Workouts.workout_id == 1)
            workout_id, workout_title, workout_date = [r for r in conn.execute(stmt)][0]
            print(workout_title)
            print(workout_date)
            stmt = select(Exercises).where(Exercises.workout_id == workout_id)
            for row in conn.execute(stmt):
                exercise, set_count, reps, weight = row[2:]
                print(set_count, exercise, reps, weight)
        except IndexError:
            pass
