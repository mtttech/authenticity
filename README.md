# AUTHENTICITY 

**Authenticity**, formerly called "Authenticity Fitness" is a fitness application written in Python.

> ### Authenticity
> - the quality of being authentic.

> ### Fitness
> - the condition of being physically fit and healthy.

**DISCLAIMER:** This codebase is currently a mock writeup. Thus, its far from a finished product.

## Dependencies

Authenticity Fitness requires the following dependencies.

* [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
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

You can add an exercise with the following command.

```
poetry run af-create
```

You can empty all the databases with the following command.

```
poetry run af-delete
```

You can view the gui mockup with the following command.

```
poetry run af-gui
```

You can view the workout information stored in the database with the following command.

```
poetry run af-read
```
