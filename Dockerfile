# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG PYTHON_VERSION=3.11.4
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Install PostgreSQL client libraries and build dependencies.
RUN apt-get update && apt-get install -y \
libpq-dev \
gcc \
&& rm -rf /var/lib/apt/lists/*

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt


# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY . .


# Expose the port that the application listens on.
EXPOSE 8000

# development
CMD python manage.py migrate && python manage.py account_initial_data && python manage.py ratings_initial_data && python manage.py runserver 0.0.0.0:8000

# Run the application:
# 1. Apply migrations
# 2. Conditionally load the countries and states data (if they don't exist)
# 3. Start the Gunicorn server
#CMD python manage.py migrate && python manage.py account_initial_data && python manage.py ratings_initial_data && gunicorn 'ratemyprofessorsapi.wsgi' --bind=0.0.0.0:8000