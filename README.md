This project was build for learning purposes.

Project Highlights:
- FastAPI
- Docker
- PostgreSQL
- Alembic
- Unit tests
- Rate limiter
- JWT Authentication

I tested this on Debian 12. I expect you to troubleshoot everything yourself when starting this project. Here's a brief explanation of tasks you may need to do:

- Install dependencies inside the `backend` folder:
```bash
uv venv && uv sync
```
- To set up pre-commit hooks, use this:
```bash
pre-commit install
```
- Create a .env file in the same directory as .env-example.
- Build and run the project with Docker (again, you may need to use `sudo`):
```bash
docker compose build && docker compose up
```
- To run tests inside a Docker container, use this (you may need `sudo`):
```bash
bash scripts/test.sh
```
- Run db migrations within a running Docker container with the backend:
```bash
alembic upgrade head
```
- Use private endpoints to create users.
