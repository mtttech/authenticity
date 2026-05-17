"""
cli.py
Author:     Marcus T Taylor <mtaylor3121@gmail.com>
Created:    23.11.23
Modified:   16.05.26
Purpose:    Main script.
"""

from datetime import datetime
from typing import Any

import rich_click as click
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from authenticity.model import Base, Exercises, Workouts, engine


console = Console(soft_wrap=True, tab_size=4, width=80)


def menu(choices: list[str]) -> str:
    """Captures user input from the prompt.

    Args:
        choices (list[str]): List of choices.

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
        return menu(choices)

    return selections[0]


@click.group()
@click.version_option()
@click.pass_context
def main_cli(ctx):
    Base.metadata.create_all(engine)

    ctx.ensure_object(dict)


@main_cli.command("add", help="Add a workout.")
@click.pass_context
def add(ctx) -> None:
    def create_workout():
        from sqlalchemy import insert

        # Title
        workout_title = Prompt.ask("Workout title.")
        # Category
        console.print("Workout category.")
        workout_category = menu(["Cardio", "Flexibility", "HIIT", "Other", "Sports", "Strength"])
        # Duration
        workout_duration = int(Prompt.ask("Workout duration."))
        # Comments
        workout_comments = Prompt.ask("Workout comments.")

        with engine.connect() as conn:  # pyright: ignore[reportGeneralTypeIssues]
            result = conn.execute(
                insert(Workouts).values(
                    workout_title=workout_title,
                    workout_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    workout_category=workout_category,
                    workout_duration=workout_duration,
                    workout_comments=workout_comments,
                )
            )
            conn.commit()

            while True:
                # Exercise name
                exercise_name = Prompt.ask("Exercise performed.")
                # Exercise sets
                exercise_sets = int(Prompt.ask("How many sets were performed?"))
                # Exercise weight
                exercise_weight = int(Prompt.ask("Exercise weight."))
                for set_number in range(1, exercise_sets + 1):
                    exercise_reps = int(
                        Prompt.ask(
                            f"How many reps were performed for set {set_number}?"
                        )
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

                yes_no = menu(["Y", "N"])
                if yes_no == "N":
                    break

    try:
        create_workout()
    except click.ClickException:
        console.print("\n")
        console.print("Exit")
        exit()


@main_cli.command("delete", help="Delete a workout by ID.")
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


@main_cli.command("view", help="View a workout by ID.")
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

        console.print()
        console.print(table)
        console.print()


if __name__ == "__main__":
    main_cli()
