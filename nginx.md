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
gunicorn_ratemyprofessorsapi.socket
[Unit]
Description=gunicorn socket for ratemyprofessorsapi                                                                                                                                                                                             [Socket]
ListenStream=/run/gunicorn_ratemyprofessorsapi.sock                                                                     
[Install]
WantedBy=sockets.target

gunicorn_ratemyprofessorsapi.service
[Service]
User=tata                                                                                                               Group=www-data                                                                                                          WorkingDirectory=/home/tata/rateteachapi
ExecStart=/home/tata/ratemyprofessorsapi/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \                                                                                                           --bind unix:/run/gunicorn_ratemyprofessorsapi.sock \
          ratemyprofessorsapi.wsgi:application                                                                                                                                                                                                  [Install]
WantedBy=multi-user.target