
docker network create jupyterhub

docker build -t jupyterhub_simple:0.1 .

docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock --net jupyterhub --name jupyterhub_simple -p 8000:8000 jupyterhub_simple:0.1

