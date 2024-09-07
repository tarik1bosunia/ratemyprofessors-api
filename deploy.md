
- Install Django Extensions Package It will help to clear pyc and cache (Optional)
   ```sh
      pip install django-extensions
    ```
      ```sh
      INSTALLED_APPS = (
        ...
        'django_extensions',
        ...
      )
    ```
- Create requirements.txt File
    ```sh
      pip freeze > requirements.txt
    ```
    ```sh
      INSTALLED_APPS = (
        ...
        'django_extensions',
        ...
      )
    ```
    - Create requirements.txt File
    ```sh
      pip freeze > requirements.txt
    ```
  
    ```sh
      ssh-keygen -t ed25519 -C "tarik.ru.cse@gmail.com"
    ```
  
    - Install Dependencies
    ```sh
      pip install -r requirements.txt
    ```
  
  ```sh
   pip install gunicorn
   ```
  
- Create System Socket File for Gunicorn
```sh
Syntax:- sudo nano /etc/systemd/system/your_domain.gunicorn.socket
Example:- sudo nano /etc/systemd/system/sonamkumari.com.gunicorn.socket
```
- Write below code inside sonamkumari.com.gunicorn.socket File
```sh
Syntax:- 
[Unit]
Description=your_domain.gunicorn socket

[Socket]
ListenStream=/run/your_domain.gunicorn.sock

[Install]
WantedBy=sockets.target

Example:- 
[Unit]
Description=sonamkumari.com.gunicorn socket

[Socket]
ListenStream=/run/sonamkumari.com.gunicorn.sock

[Install]
WantedBy=sockets.target
```
- Create System Service File for Gunicorn
```sh
Syntax:- sudo nano /etc/systemd/system/your_domain.gunicorn.service
Example:- sudo nano /etc/systemd/system/sonamkumari.com.gunicorn.service
```
- Write below code inside sonamkumari.com.gunicorn.service File
```sh
Syntax:-
[Unit]
Description=your_domain.gunicorn daemon
Requires=your_domain.gunicorn.socket
After=network.target

[Service]
User=username
Group=groupname
WorkingDirectory=/home/username/project_folder_name
ExecStart=/home/username/project_folder_name/virtual_env_name/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/your_domain.gunicorn.sock \
          inner_project_folder_name.wsgi:application

[Install]
WantedBy=multi-user.target

Example:-
[Unit]
Description=sonamkumari.com.gunicorn daemon
Requires=sonamkumari.com.gunicorn.socket
After=network.target

[Service]
User=raj
Group=raj
WorkingDirectory=/home/raj/miniblog
ExecStart=/home/raj/miniblog/mb/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/sonamkumari.com.gunicorn.sock \
          miniblog.wsgi:application

[Install]
WantedBy=multi-user.target
```

- Start Gunicorn Socket and Service
```sh
Syntax:- sudo systemctl start your_domain.gunicorn.socket
Example:- sudo systemctl start sonamkumari.com.gunicorn.socket

Syntax:- sudo systemctl start your_domain.gunicorn.service
Example:- sudo systemctl start sonamkumari.com.gunicorn.service
```
- Enable Gunicorn Socket and Service
```sh
Syntax:- sudo systemctl enable your_domain.gunicorn.socket
Example:- sudo systemctl enable sonamkumari.com.gunicorn.socket

Syntax:- sudo systemctl enable your_domain.gunicorn.service
Example:- sudo systemctl enable sonamkumari.com.gunicorn.service


- Check Gunicorn Status
```sh
sudo systemctl status sonamkumari.com.gunicorn.socket
sudo systemctl status sonamkumari.com.gunicorn.service
```
- Restart Gunicorn (You may need to restart everytime you make change in your project code)
```sh
sudo systemctl daemon-reload
sudo systemctl restart sonamkumari.com.gunicorn #this is service file name without extension
```

- Create Virtual Host File
```sh
Syntax:- sudo nano /etc/nginx/sites-available/your_domain
Example:- sudo nano /etc/nginx/sites-available/sonamkumari.com
```
- Write following Code in Virtual Host File
```sh
Syntax:-
server{
    listen 80;
    listen [::]:80;
    
    server_name your_domain www.your_domain;
    
    location = /favicon.ico { access_log off; log_not_found off; }
    
    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://unix:/run/your_domain.gunicorn.sock;
    }
    
    location  /static/ {
        root /var/www/project_folder_name;
    }

    location  /media/ {
        root /var/www/project_folder_name;
    }
}

Example:-
server{
    listen 80;
    listen [::]:80;

    server_name sonamkumari.com www.sonamkumari.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://unix:/run/sonamkumari.com.gunicorn.sock;
    }

    location  /static/ {
        root /var/www/miniblog;
    }

    location  /media/ {
        root /var/www/miniblog;
    }
}

- Enable Virtual Host or Create Symbolic Link of Virtual Host File
```sh
Syntax:- sudo ln -s /etc/nginx/sites-available/virtual_host_file /etc/nginx/sites-enabled/virtual_host_file
Example:- sudo ln -s /etc/nginx/sites-available/sonamkumari.com /etc/nginx/sites-enabled/sonamkumari.com
```
- Check Configuration is Correct or Not
```sh
sudo nginx -t
```
- Restart Nginx
```sh
sudo service nginx restart
```