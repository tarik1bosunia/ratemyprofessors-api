
```shell

server {
    listen 80;
    listen [::]:80;
    server_name ratemyprofessor.ru.ac.bd www.ratemyprofessor.ru.ac.bd;

    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name ratemyprofessor.ru.ac.bd www.ratemyprofessor.ru.ac.bd;

    ssl_certificate /etc/letsencrypt/live/ratemyprofessor.ru.ac.bd/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ratemyprofessor.ru.ac.bd/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Proxy for Next.js (running on port 3000)
    location / {
        proxy_pass http://localhost:3000;  # Ensure the URL is valid here
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Proxy for Django (running on port 8000)
    location /api/ {
        proxy_pass http://localhost:8000/;  # Ensure the URL is valid here
        rewrite ^/api(.*) $1 break;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    # Proxy for Django Admin Panel
    location /admin/ {
        proxy_pass http://localhost:8000/admin/;  # Proxying admin requests correctly
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
      # Serve static files for Django
    location /static/ {
        alias /home/tata/ratemyprofessors-api/staticfiles/;  # Path inside the container
        autoindex on;
    }

    # Serve media files for Django
    location /media/ {
        alias /home/tata/ratemyprofessors-api/media/;  # Path inside the container
        autoindex on;
    }
}

```