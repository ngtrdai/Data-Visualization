#!/usr/bin/env bash

cd /src/data-viz-analyzer

cp .env.example .env

uvicorn app.main:app --host 0.0.0.0 --port 8080