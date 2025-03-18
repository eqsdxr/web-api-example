This project was build for learning purposes. I learned - so can you.

Project Highlights:
- FastAPI
- Docker
- PostgreSQL
- Alembic
- Unit tests
- Rate limiter
- JWT Authentication

I expect you to troubleshoot everything yourself when starting this project. Here's a brief explanation of tasks you may need to do:

- Install dependencies inside the `backend` folder:
```bash
uv venv && uv sync
```
- Create a .env file in the same directory as .env-example.
- Run db migrations inside a Docker container with the backend:
```bash
alembic upgrade head
```
- Run tests inside a Docker container (you may need `sudo`):
```bash
bash scripts/test.sh
```
- Build and run the project with Docker (again, you may need to use `sudo`):
```bash
docker compose build && docker compose up
```
- Use private endpoints to create users.
- Set up pre-commit hooks:
```bash
pre-commit install
```
