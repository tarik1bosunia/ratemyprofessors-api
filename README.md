pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-cors-headers
pip install django-dotenv
python .\manage.py loaddata departments.json

# postgres SQL
pip install psycopg2
CREATE DATABASE ratemyprofessorsdb;
\l
\c ratemyprofessorsdb
CREATE USER tata WITH PASSWORD '11235813';
CREATE SCHEMA ratemyprofessorsdb AUTHORIZATION tata;
ALTER ROLE tata SET client_encoding TO 'utf8';
ALTER ROLE tata SET default_transaction_isolation TO 'read committed';
ALTER ROLE tata SET timezone TO 'UTC';
\dt
ALTER ROLE tata IN DATABASE ratemyprofessorsdb SET search_path = newschema;

# Trigram Similarity
https://dev.to/azayshrestha/enhance-your-searches-with-postgresql-trigram-similarity-in-django-4pad
sudo -u postgres psql -d database_name -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;

https://testdriven.io/blog/django-drf-elasticsearch/

# login with google
pip install google-api-python-client
pip install social-auth-app-django
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2

https://developers.google.com/identity/sign-in/web/server-side-flow

python manage.py loaddata content_initial_data.json