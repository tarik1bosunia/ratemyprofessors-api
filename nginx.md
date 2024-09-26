/etc/nginx/sites-available/ratemyprofessors.ru.ac.bd

server {
    listen 80;
    server_name ratemyprofessor.ru.ac.bd www.ratemyprofessor.ru.ac.bd;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/tata/ratemyprofessorsapi:;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn_ratemyprofessors.sock;
    }
}