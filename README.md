#### Docker build

#to start:
sudo docker-compose up

#to restart, picking up changes:
sudo docker-compose up -d --build --force-recreate

#to take down:
docker-compose down

#site will appear at localhost:8000 in your browser


``````
docker-compose build
docker-compose up -d --build --force-recreate

``````
#### Docker deploy and running

```.dockerfile
docker-compose up -d --build --force-recreate
docker ps 

docker exec -it <web container id> python manage.py migrate admin
docker exec -it <web container id> python manage.py collectstatic --no-input
docker exec -it <web container id> python manage.py import_file incipit -f input_files/incipits.xls
docker exec -it <web container id> python manage.py import_file explicit -f input_files/reverse_explicits.xls
docker exec -it <web container id> python manage.py import_file title -f input_files/titles_rubrics_and_colophons.xls
docker exec -it <web container id> python manage.py import_file subject -f input_files/general_index.xls

```

###### Useful docker helper commands

```dockerfile
docker volume ls | prune | rm
docker volume 
docker ps --no-trunc
docker inspect <container>
docker images
docker rmi <image ID>
docker exec -it <containerID> /bin/bash
```