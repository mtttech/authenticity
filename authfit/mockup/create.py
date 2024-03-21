"""
create.py
Author:     Marcus T Taylor
Created:    23.11.23
Modified:   21.03.24
"""
from datetime import datetime

from sqlalchemy import insert

from authfit.models import Exercises, Workouts, engine


def enter_number(message: str) -> int:
    number = 0
    while number == 0:
        try:
            number = int(input(message))
        except ValueError:
            pass
        if number >= 1:
            break
    return number


def prompt() -> None:
    while True:
        workout_title = input("Give your workout a title: ")
        # TODO: Add something to track the workout's duration, perhaps? >:(
        with engine.connect() as conn: # pyright: ignore[reportGeneralTypeIssues]
            result = conn.execute(
                insert(Workouts).values(
                    workout_title=workout_title,
                    workout_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
            )
            conn.commit()

            num_of_exercises = enter_number(
                "How many exercises were performed during your workout?: "
            )
            for _ in range(1, num_of_exercises + 1):
                exercise_name = input(
                    "Enter the exercise (i.e Deadlift, Dumbbell Curl, Military Press, etc): "
                )
                exercise_weight = enter_number("Enter the amount of weight used: ")
                number_of_sets = enter_number("How many sets: ")
                for set_number in range(1, number_of_sets + 1):
                    exercise_reps = enter_number(
                        f"Enter the number of reps done in set {set_number}: "
                    )
                    conn.execute(
                        insert(Exercises).values(
                            exercise_name=exercise_name,
                            workout_id=result.lastrowid,
                            exercise_set=set_number,
                            exercise_reps=exercise_reps,
                            exercise_weight=exercise_weight,
                        )
                    )
                    conn.commit()
        break


def main() -> None:
    try:
        prompt()
    except KeyboardInterrupt:
        print("")
        print("Exit")
        exit(1)
