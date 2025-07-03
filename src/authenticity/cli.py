"""
cli.py
Author:     Marcus T Taylor
Created:    23.11.23
Modified:   02.07.25
"""

from datetime import datetime

import click

from authenticity.exercises import exercise_list
from authenticity.models import Exercises, Workouts, engine


def _create() -> None:
    def create_workout():
        from sqlalchemy import insert

        workout_title = click.prompt(
            "Give your workout session a name (i.e: My Meditation Session, etc).",
            prompt_suffix=" ",
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
                "How many exercises were performed?",
                prompt_suffix=" ",
                type=int,
            )
            # Ask info for each exercise
            for _ in range(1, num_of_exercises + 1):
                target = click.prompt(
                    "Enter the targeted body part.",
                    prompt_suffix=" ",
                    show_choices=True,
                    type=click.Choice(list(exercise_list.keys()), case_sensitive=False),
                )
                exercise = click.prompt(
                    "Enter the exercise performed.",
                    prompt_suffix=" ",
                    show_choices=True,
                    type=click.Choice(exercise_list[target], case_sensitive=False),
                )
                num_of_sets = click.prompt(
                    "How many sets were performed?",
                    prompt_suffix=" ",
                    type=int,
                )
                weight = click.prompt(
                    "How much weight was used?",
                    prompt_suffix=" ",
                    type=int,
                )
                for set_number in range(1, num_of_sets + 1):
                    num_of_reps = click.prompt(
                        f"How many reps were performed for set {set_number}?",
                        prompt_suffix=" ",
                        type=int,
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

    try:
        create_workout()
    except click.exceptions.Abort:
        print("\nExit")
        exit()


def _delete() -> None:
    @click.command()
    @click.option("--wid", help="Workout ID to delete.", type=int)
    def delete_workout(wid):
        from sqlalchemy import delete

        with engine.connect() as conn:  # pyright: ignore[reportGeneralTypeIssues]
            conn.execute(delete(Workouts))
            if wid is not None:
                conn.execute(delete(Exercises).where(Exercises.workout_id == wid))
                print(f"Deleted WID {wid}.")
            else:
                conn.execute(delete(Exercises))
                print("Deleted all records.")
            conn.commit()

    delete_workout()


@click.command()
@click.option("--read")
def main() -> None:
    from sqlalchemy import select

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
