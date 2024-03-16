# AUTHENTICITY FITNESS

> ### Authencity
> - the quality of being authentic.

> ### Fitness
> - the condition of being physically fit and healthy.

I am writing an application for tracking my workouts. The code here is currently a simple mock write up and far from a finished product.


## Dependencies

Authenticity Fitness requires the following dependencies.

* [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
* [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)


## Installation & Usage

```
# Clone authfit.
git clone https://codeberg.org/mtttech/authenticity-fitness.git


# Change into the directory and install it using poetry.
cd authfit
poetry install
```

You can add an exercise with the following command.

```
poetry run authfit-create
```

You can empty all the databases with the following command.

```
poetry run authfit-delete
```

You can view the gui mockup with the following command.

```
poetry run authfit-gui
```

You can view the workout information stored in the database with the following command.

```
poetry run authfit-read
```
