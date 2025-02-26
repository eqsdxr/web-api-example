The project was made for learning purposes.

### Usage

- Make sure you have `uv` and `docker` (optional) are installed on your machine.
- Clone the repository.
- Create and activate a virtual environment.
```
uv venv
uv sync
```
- Make sure you\'re in the project's root.

To run tests:
```python
bash scripts/test.sh
```

To build and run docker app in docker container:
```python
bash scripts/build.sh
```
You may need to use `sudo bash scripts/build.sh`.

To run locally:
```python
bash scripts/run.sh
```
