#!/bin/bash

# Check if the database is ready
until pg_isready -h $DB_HOST -U $DB_USER; do
  echo "Waiting for database..."
  sleep 2
done

# Load data if the table is empty
if [ $(python manage.py dbshell -c "SELECT COUNT(*) FROM countries;") -eq 0 ]; then
  echo "Loading countries data..."
  python manage.py loaddata countries
else
  echo "Countries data already exists. Skipping..."
fi

if [ $(python manage.py dbshell -c "SELECT COUNT(*) FROM states;") -eq 0 ]; then
  echo "Loading states data..."
  python manage.py loaddata states
else
  echo "States data already exists. Skipping..."
fi
