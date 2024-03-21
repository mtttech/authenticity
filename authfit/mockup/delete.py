"""
delete.py
Author:     Marcus T Taylor
Created:    15.03.24
Modified:   16.03.24
"""
from sqlalchemy import delete

from authfit.models import Exercises, Workouts, engine


def main() -> None:
    print("Delete all the data in the databases.")

    with engine.connect() as conn: # pyright: ignore[reportGeneralTypeIssues]
        conn.execute(delete(Exercises))
        conn.execute(delete(Workouts))
