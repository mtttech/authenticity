# AUTHENTICITY 

**Authenticity**, formerly called *Authenticity Fitness* is a workout tracking application written in Python.

> #### Authenticity
> - the quality of being authentic.

> #### Fitness
> - the condition of being physically fit and healthy.

**DISCLAIMER:** This codebase is currently a mock writeup. Thus, its far from a finished product.

## Dependencies

Authenticity Fitness "requires" the following dependencies - really only SQLAlchemy thus far.

* [click](https://github.com/pallets/click)
* [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)

## Installation & Usage

```
# Clone authenticity.
git clone https://github.com/mtttech/authenticity.git

# Change into the directory.
cd authenticity

# Install using Poetry.
poetry install
```

### Add Exercises

You can add an exercise with the following command.

```
poetry run af-create
```

The following prompts will occur.

* Name your workout.
* State how many exercises were done.
* State the name of the targeted body part, the exercise, how many sets, reps in each set and how much weight was used.

### Delete Exercises

You can delete all records within the databases with the following command.

```
poetry run af-delete
```

You can delete a specific workout record ID from the database with the following command.

```
poetry run af-delete --wid=<WID>
```

### View Workout

You can view the workout information stored in the database with the following command.

```
poetry run af-read
```
