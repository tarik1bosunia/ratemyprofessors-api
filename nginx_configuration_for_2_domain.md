# rateteach.ru.ac.bd
```shell
server {
    listen 80;
    server_name rateteach.ru.ac.bd;

    # Redirect HTTP to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name rateteach.ru.ac.bd;

    ssl_certificate /etc/letsencrypt/live/rateteach.ru.ac.bd/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/rateteach.ru.ac.bd/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;  # Assuming Next.js app running on port 3000
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```
# apirateteach.ru.ac.bd
```shell
server {
    listen 80;
    server_name apirateteach.ru.ac.bd;
    
    location / {
        proxy_pass http://localhost:8000;  # Assuming Django API running on port 8000
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Optionally add SSL
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/apirateteach.ru.ac.bd/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/apirateteach.ru.ac.bd/privkey.pem;
}

```
```shell
sudo ln -s /etc/nginx/sites-available/rateteach.ru.ac.bd /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/apirateteach.ru.ac.bd /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/ratemyprofessor.ru.ac.bd /etc/nginx/sites-enabled/
```
```shell
sudo certbot --nginx -d rateteach.ru.ac.bd 
sudo certbot --nginx -d apirateteach.ru.ac.bd
sudo certbot --nginx -d ratemyprofessor.ru.ac.bd
```

```shell
sudo nginx -t
sudo systemctl restart nginx
```