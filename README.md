# Django REST API Setup for RateMyProfessors

A professional Django REST API backend with PostgreSQL, JWT authentication, Google OAuth integration, and enhanced search using Trigram Similarity.

## Django REST Framework Setup

### Install Required Packages
```sh
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-cors-headers
pip install django-dotenv
```

## Load Initial Data
```sh
python manage.py loaddata departments.json
```

---

# PostgreSQL Setup

## Ubuntu Commands
```sh
sudo su - postgres
psql
```

### Install PostgreSQL Driver for Python
```sh
pip install psycopg2
```

### Create Database and User
```sql
CREATE DATABASE ratemyprofessorsdb;
\l
\c ratemyprofessorsdb

CREATE USER tata WITH PASSWORD '11235813';
CREATE SCHEMA ratemyprofessorsdbschema AUTHORIZATION tata;

ALTER ROLE tata SET client_encoding TO 'utf8';
ALTER ROLE tata SET default_transaction_isolation TO 'read committed';
ALTER ROLE tata SET timezone TO 'UTC';

\dt

ALTER ROLE tata IN DATABASE ratemyprofessorsdb SET search_path = newschema;
```

---

# Trigram Similarity for Enhanced Search

[Read More](https://dev.to/azayshrestha/enhance-your-searches-with-postgresql-trigram-similarity-in-django-4pad)

```sh
sudo -u postgres psql -d database_name -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"
```

Additional resource: [Django DRF Elasticsearch](https://testdriven.io/blog/django-drf-elasticsearch/)

---

# Google Authentication Setup
```sh
pip install google-api-python-client
pip install social-auth-app-django
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2
```

[Google OAuth Server-Side Flow Guide](https://developers.google.com/identity/sign-in/web/server-side-flow)

## Load Additional Content Data
```sh
python manage.py loaddata content_initial_data.json
