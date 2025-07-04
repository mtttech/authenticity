"""
cli.py
Author:     Marcus T Taylor
Created:    23.11.23
Modified:   05.07.25
"""

from datetime import datetime

import rich_click as click
from rich.console import Console
from rich.table import Table

from authenticity.exercises import get_exercises_by_group, get_muscle_groups
from authenticity.models import Exercises, Workouts, engine


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)


@cli.command("add", help="Add a workout.")
@click.pass_context
def add(ctx) -> None:
    def create_workout():
        from sqlalchemy import insert

        workout_title = click.prompt(
            "Name your workout session (i.e: My Meditation Session, etc).",
            prompt_suffix=" ",
        )
        # TODO: Add something to track the workout's duration, perhaps? >:(
        # TODO: Functional but lets clean this system up a lil bit.
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
            # Ask for workout info for each exercise
            for _ in range(1, num_of_exercises + 1):
                muscle_group = click.prompt(
                    "Enter the targeted body part.",
                    prompt_suffix=" ",
                    show_choices=True,
                    type=click.Choice(get_muscle_groups(), case_sensitive=False),
                )
                exercise = click.prompt(
                    "Enter the exercise performed.",
                    prompt_suffix=" ",
                    show_choices=True,
                    type=click.Choice(
                        get_exercises_by_group(muscle_group), case_sensitive=False
                    ),
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


@cli.command("delete", help="Delete a workout.")
@click.option("--wid", required=True, help="Workout ID number to delete.")
@click.pass_context
def delete(ctx, wid):
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


@cli.command("view", help="View a workout.")
@click.option("--wid", required=True, help="Workout ID number to view.")
@click.pass_context
def view(ctx, wid) -> None:
    from sqlalchemy import select

    with engine.connect() as conn:  # pyright: ignore[reportGeneralTypeIssues]
        results = conn.execute(
            select(Workouts.workout_title, Workouts.workout_date).where(
                Workouts.workout_id == wid
            )
        )
        console = Console()
        table = Table()
        for row in results:
            table = Table(title=f"{row[0]} on {row[1]}")

        table.add_column("Exercise")
        table.add_column("Weight", justify="center")
        table.add_column("Set", justify="center")
        table.add_column("Reps", justify="center")

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
            .join(Exercises, wid == Exercises.workout_id)
        )
        for row in conn.execute(stmt):
            table.add_row(row[3], str(row[4]), str(row[5]), str(row[6]))

        print()
        console.print(table)
        print()
