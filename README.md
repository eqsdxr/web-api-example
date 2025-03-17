The project was made for learning purposes.

I expect you to troubleshoot everything yourself when starting this project. Here's a brief explanation of tasks you may need to do:

- Use `uv venv` and `uv sync` inside the backend folder to install dependencies.
- Run `alembic upgrade head` inside a running Docker container with the backend to create tables in the PostgreSQL database.
- Use private endpoints to create users.
- To run tests inside a Docker container, use `bash scripts/test.sh` (you may need to use it with `sudo`).
- Use `pre-commit install` to set up pre-commit hooks.
- Create a .env file in the same directory as .env-example.
- Use `docker compose build` and `docker compose up` to run the project in docker (again, you may need to use `sudo`).
