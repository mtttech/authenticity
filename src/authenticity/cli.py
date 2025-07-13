"""
cli.py
Author:     Marcus T Taylor
Created:    23.11.23
Modified:   12.07.25
"""

from datetime import datetime
from typing import Any

import rich_click as click
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from authenticity.exercises import get_exercises_by_group, get_muscle_groups
from authenticity.models import Exercises, Workouts, engine

console = Console(tab_size=4, width=80)


def io(choices: list[str] | int) -> str:
    """Captures user input from the console.

    Args:
        choices (list[str]|int): List of choices or max value in a range of numbers.

    Returns:
        str: Returns the user's response."""

    def first_and_last(choices: dict[int, Any]) -> tuple[int, int]:
        indexes = list(choices.keys())
        return (indexes[0], indexes[-1])

    def index_choices(choices: list[Any]) -> dict[int, Any]:
        indexed_choices = {}
        for index, option in enumerate(choices):  # pyright: ignore
            indexed_choices[index + 1] = option
        return indexed_choices

    # If using numbers as options, create a range, starting from 1.
    if isinstance(choices, int):
        choices = list(str(n + 1) for n in range(choices))

    indexed_choices = index_choices(choices)
    first_index, last_index = first_and_last(indexed_choices)
    message = f"\nMake a selection <{first_index}-{last_index}>.\n\n"
    for index, option in indexed_choices.items():
        message += f"\t{index}.) {option}\n"
    console.print(message)

    selections = []
    try:
        user_input = int(input(">> "))
        chosen_option = indexed_choices[user_input]
        selections.append(chosen_option)
        choices.remove(chosen_option)
    except (KeyError, TypeError, ValueError):
        return io(choices)

    return selections[0]


@click.group()
@click.version_option()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)


@cli.command("add", help="Add a workout.")
@click.pass_context
def add(ctx) -> None:
    def create_workout():
        from sqlalchemy import insert

        workout_title = Prompt.ask(
            "Name your workout session (i.e: My Meditation Session, etc)."
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

            num_of_exercises = int(Prompt.ask("How many exercises were performed?"))
            # Ask for workout info for each exercise
            for _ in range(1, num_of_exercises + 1):
                console.print("Enter the targeted body part.")
                muscle_group = io(get_muscle_groups())

                console.print("Enter the exercise performed.")
                exercise = io(get_exercises_by_group(muscle_group))

                num_of_sets = int(Prompt.ask("How many sets were performed?"))
                weight = int(Prompt.ask("How much weight was used?"))
                for set_number in range(1, num_of_sets + 1):
                    num_of_reps = int(
                        Prompt.ask(
                            f"How many reps were performed for set {set_number}?"
                        )
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
    if Confirm.ask(f"Do you want to delete WID {wid}?"):
        from sqlalchemy import delete

        with engine.connect() as conn:  # pyright: ignore[reportGeneralTypeIssues]
            conn.execute(delete(Workouts).where(Workouts.workout_id == wid))
            conn.execute(delete(Exercises).where(Exercises.workout_id == wid))
            conn.commit()
            console.print(f"Deleted WID {wid}.")


@cli.command("view", help="View a workout.")
@click.option("--wid", required=True, help="Workout ID number to view.")
@click.pass_context
def view(ctx, wid) -> None:
    from sqlalchemy import select

    with engine.connect() as conn:  # pyright: ignore[reportGeneralTypeIssues]
        workout_results = conn.execute(
            select(Workouts.workout_title, Workouts.workout_date).where(
                Workouts.workout_id == wid
            )
        )
        workout_results = workout_results.fetchone()

        # No workout found for the requested WID.
        if workout_results == None:
            console.print(f"No workout found for WID {wid}.")
            return

        workout_name, workout_date = workout_results
        table = Table(show_lines=True, title=f"{workout_name} on {workout_date}")

        table.add_column("Exercise")
        table.add_column("Weight", justify="center")
        table.add_column("Set", justify="center")
        table.add_column("Reps", justify="center")

        stmt = select(
            Exercises.exercise_name,
            Exercises.exercise_weight,
            Exercises.exercise_set,
            Exercises.exercise_reps,
        ).where(Exercises.workout_id == wid)
        for row in conn.execute(stmt):
            exercise_name, exercise_weight, exercise_set, exercise_reps = row
            table.add_row(
                exercise_name,
                str(exercise_weight),
                str(exercise_set),
                str(exercise_reps),
            )

        print()
        console.print(table)
        print()
