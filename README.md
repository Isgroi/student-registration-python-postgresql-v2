# Student Registration with Python and PostgreSQL

This is a study project that I am building while learning Python, PostgreSQL,
SQL, Git, and software development.

I decided to start this version from scratch so I can understand each part of
the project instead of only copying a finished application.

## Sobre este projeto

Estou desenvolvendo este projeto em português e inglês:

- o código e os nomes técnicos ficam em inglês;
- os commits são escritos em inglês;
- algumas mensagens da aplicação estão em português;
- as anotações pessoais podem aparecer em português.

A ideia é aprender praticando e registrar minha evolução ao longo do caminho.

## What the project can do

At the moment, the application can:

- register a student;
- store the first name and surname;
- generate an example email;
- accept a custom email;
- perform basic email validation;
- connect Python to PostgreSQL;
- load database settings from `.env`;
- use a Python virtual environment;
- keep project dependencies in `requirements.txt`.

## Technologies

- Python
- PostgreSQL
- Psycopg
- python-dotenv
- Git and GitHub
- Visual Studio Code

## Project structure

```text
.
├── .env
├── .env.example
├── .gitignore
├── app.py
├── database.py
├── requirements.txt
├── schema.sql
└── .venv/
```

The main files are:

- `app.py`: starts the application and handles user input.
- `database.py`: contains the database connection and database functions.
- `schema.sql`: contains the SQL structure used by the project.
- `.env`: stores local database settings.
- `.env.example`: shows which settings are needed without exposing a password.
- `requirements.txt`: lists the Python packages used by the project.

## Running the project

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Create a local `.env` file based on `.env.example` and add the PostgreSQL
connection settings.

Then run:

```bash
python app.py
```

## Email behavior

When only the name and surname are provided, the application creates an
example email:

```text
João Pereira
joao.pereira@example.com
```

It is also possible to enter a different email. If the email field is left
empty, the generated example email is used.

The `example.com` domain is being used only for testing.

## Security notes

The `.env` file is local and must not be uploaded to GitHub.

The project should never include:

- database passwords;
- private SSH keys;
- access tokens;
- secret webhook URLs;
- real private configuration files.

## What I am learning

While building this project, I am practicing:

- Python functions and modules;
- user input and validation;
- SQL commands;
- PostgreSQL connections;
- environment variables;
- virtual environments;
- Git commits and GitHub repositories;
- organizing a project into smaller parts.

## Next ideas

Some features I plan to add are:

- a better interactive menu;
- a list of all students;
- search by ID or name;
- update and delete operations;
- better email validation;
- automated tests;
- a simple graphical interface with Tkinter.

## Status

This project is still in progress.

I am building it one step at a time and using each new feature as an opportunity
to understand the code better.

## Running the tests

With the virtual environment active, run:

```bash
python -m pytest -q
```

## Database connection errors

If PostgreSQL is unavailable, the application displays a simple error message instead of a long traceback.

Se o PostgreSQL estiver desligado ou o arquivo `.env` estiver incorreto, o programa informa o problema de forma clara.

Make sure that:

- PostgreSQL is running;
- the database exists;
- the values in `.env` are correct.