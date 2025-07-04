# AUTHENTICITY 

**Authenticity**, formerly called **Authenticity Fitness** is a workout tracking application written in Python.

> #### Authenticity
> - the quality of being authentic.

> #### Fitness
> - the condition of being physically fit and healthy.

**DISCLAIMER:** This codebase is currently a mock writeup.

## Dependencies

Authenticity Fitness "requires" the following dependencies.

* [rich-click](https://github.com/ewels/rich-click)
* [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)

## Installation & Usage


### Installation

Clone the repo and install the project.

```
# Clone authenticity.
git clone https://github.com/mtttech/authenticity.git

# Change into the directory.
cd authenticity

# Install using Poetry.
poetry install
```

### Usage

Run the following command in a virtual environment.

```
poetry run authenticity
```

OR if installed.

```
authenticity
```

You can view a full list of commands with the following command.

```
$authenticity --help
                                                                                                                      
 Usage: authenticity [OPTIONS] COMMAND [ARGS]...                                                                                                       
                                                                                                                                                       
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                                                                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ add                                        Add a workout.                                                                                           │
│ delete                                     Delete a workout.                                                                                        │
│ view                                       View workouts.                                                                                           │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
