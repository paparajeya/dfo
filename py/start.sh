#! /usr/bin/env bash

export PYTHONPATH="."

# Reference: https://fastapi.tiangolo.com/deployment/server-workers/
gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000 --log-level info --timeout 0 --keep-alive 30
