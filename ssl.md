https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04
Step 1 — Installing Certbot
```sh
sudo apt install certbot python3-certbot-nginx
```

Step 2 — Confirming Nginx’s Configuration
```sh
sudo apt install certbot python3-certbot-nginx

```
Obtaining an SSL Certificate
```shell
sudo certbot --nginx -d ratemyprofessor.ru.ac.bd -d www.ratemyprofessor.ru.ac.bd
```
Certificate is saved at: /etc/letsencrypt/live/ratemyprofessor.ru.ac.bd/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/ratemyprofessor.ru.ac.bd/privkey.pem

# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name ratemyprofessor.ru.ac.bd www.ratemyprofessor.ru.ac.bd;

    return 301 https://$host$request_uri;
}

# HTTPS server block
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name ratemyprofessor.ru.ac.bd www.ratemyprofessor.ru.ac.bd;

    ssl_certificate /etc/letsencrypt/live/ratemyprofessor.ru.ac.bd/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ratemyprofessor.ru.ac.bd/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://localhost:3000;  # Assuming your app runs on port 3000
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
     # Proxy for Django
    location /api/ {
        proxy_pass http://localhost:8000/;
        rewrite ^/django(.*) $1 break;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

gunicorn
cd /etc/systemd/system
sudo vim gunicorn_rateteachapi.socket

[Unit]
Description=gunicorn socket for rateteachapi

[Socket]
ListenStream=/run/gunicorn_rateteachapi.sock

[Install]
WantedBy=sockets.target

cd /etc/systemd/system/
sudo vim gunicorn_rateteachapi.service
[Service]
User=tata
Group=www-data
WorkingDirectory=/home/tata/rateteachapi
ExecStart=/home/tata/rateteachapi/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn_rateteachapi.sock \
          rateteachapi.wsgi:application

[Install]
WantedBy=multi-user.target

sudo systemctl start gunicorn_rateteachapi.socket
sudo systemctl enable gunicorn_rateteachapi.socket
sudo ln -s /etc/nginx/sites-available/ratemyprofessor.ru.ac.bd /etc/nginx/sites-enabled/
sudo systemctl restart nginx

