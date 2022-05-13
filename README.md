# MultMatrizes
```sh
docker build -t server-aux-app -f Dockerfile.serveraux1 .
```

```sh
docker network create --driver bridge --subnet 192.168.1.0/24 dist-net
```

```sh
docker run --rm -it --network dist-net client-app
```
