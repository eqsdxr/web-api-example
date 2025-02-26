The project was made for learning purposes.

### Usage

- Make sure you have `uv` and `docker` (optional) installed on your machine.

Clone the repository.

Create and activate a virtual environment.
```
uv venv
source .venv/bin/activate
```

Install the project's dependencies.
```
uv sync
```

- Make sure you\'re in the project's root before using the following scripts.

To run tests:
```bash
bash scripts/test.sh
```

To build and run docker app in docker container:
```bash
bash scripts/docker.sh
```
You may need to use `sudo bash scripts/docker.sh`.

To run locally:
```bash
bash scripts/local.sh
```

To install pre-commit hooks:
```bash
pre-commit install
```

To format and lint code use:
```bash
bash scripts/code.sh
```
