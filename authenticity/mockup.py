"""
mockup.py
Author:     Marcus T Taylor
Created:    23.11.23
Modified:   11.10.24
"""

from datetime import datetime

import click
from sqlalchemy import delete, insert, select

from authenticity.models import Exercises, Workouts, engine


def create_workouts() -> None:
    exercises = ("Deadlift", "Dumbbell Curl")
    workout_title = click.prompt(
        "Give your workout session a name (i.e: My Meditation Session, etc)."
    )
    # TODO: Add something to track the workout's duration, perhaps? >:(
    with engine.connect() as conn:  # pyright: ignore[reportGeneralTypeIssues]
        result = conn.execute(
            insert(Workouts).values(
                workout_title=workout_title,
                workout_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
        )
        conn.commit()

        num_of_exercises = click.prompt(
            "How many exercises were performed during your workout?", type=int
        )
        # Ask info for each exercise
        for _ in range(1, num_of_exercises + 1):
            exercise = click.prompt(
                "Enter the exercise.",
                show_choices=True,
                type=click.Choice(exercises, case_sensitive=False),
            )
            num_of_sets = click.prompt(
                "How many sets were performed during this workout?", type=int
            )
            weight = click.prompt(
                "How much weight was used during this workout?", type=int
            )
            for set_number in range(1, num_of_sets + 1):
                num_of_reps = click.prompt(
                    f"How many reps were performed during set {set_number}?", type=int
                )
                conn.execute(
                    insert(Exercises).values(
                        exercise_name=exercise,
                        workout_id=result.lastrowid,
                        exercise_set=set_number,
                        exercise_reps=num_of_reps,
                        exercise_weight=weight,
                    )
                )
                conn.commit()


def delete_workouts() -> None:
    print("Deleting exercise/workout data...")
    with engine.connect() as conn:  # pyright: ignore[reportGeneralTypeIssues]
        conn.execute(delete(Workouts))
        conn.execute(delete(Exercises))
        conn.commit()


def read_workouts() -> None:
    print("Displaying exercise/workout data from database.")
    with engine.connect() as conn:  # pyright: ignore[reportGeneralTypeIssues]
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


def main():
    @click.command()
    @click.option("--count", default=1, help="Number of greetings.")
    @click.option("--name", prompt="Your name", help="The person to greet.")
    def hello(count, name):
        for x in range(count):
            click.echo(f"Hello {name}!")

    hello()
