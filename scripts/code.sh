#!/bin/bash

isort .

ruff check --fix .

ruff format .
