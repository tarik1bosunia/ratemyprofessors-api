docker init
pip install whitenoise
python .\manage.py collectstatic
docker-compose exec django python manage.py collectstatic --noinput
docker-compose exec server python manage.py migrate
docker-compose exec server python manage.py createsuperuser

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
docker build . -t ghcr.io/tarik1bosunia/rtserver:tata

docker build . -t ghcr.io/tarik1bosunia/rtserver:latest

docker compose up -d --restart unless-stopped
