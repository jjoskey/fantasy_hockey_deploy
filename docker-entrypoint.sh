#!/bin/bash

# Collect static files
echo "Collect static files"
python3.6 ./app/manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python3.6 ./app/manage.py migrate

# Start server
echo "Starting server"
supervisord -n
