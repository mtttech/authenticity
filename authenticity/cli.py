"""
mockup.py
Author:     Marcus T Taylor
Created:    29.10.24
Modified:   29.10.24
"""
from prompt_toolkit import prompt


def main():
    workout = prompt("Name your workout session.")
    print(workout)


if __name__ == "__main__":
    main()