# MultMatrizes

Projeto de um super-serviodor com servidores parceiros que realiza multiplicações de matrizes

Projeto referente a disciplina de Sistemas Distribuidos.

### Passo 1:
Crie e execute os 3 containers de servidores auxiliares e, em seguida, o container do servidor principal executando este comando na raiz do projeto:

```sh
docker-compose -f "docker-compose.yml" up -d --build
```

### Passo 2:
Crie um container cliente qwue fará as requisições para o servidor principal executando este comando na raiz do projeto:

```sh
docker build --pull --rm -f "Dockerfile.client" -t client-app:latest "."
```

### Passo 3:
Execute o container do cliente passando alguns parametros para reduzir alguns recursos de processamento do container em relação aso servidores

```sh
docker run --rm -it --cpus="1.5" --memory="300m" --network multmatrizes_dist-net client-app > output.txt
```

O comando gerará uma arquivo ```output.txt``` contendo o tempo de execução dos 30 calculos de multiplicação de matrizes.



```sh
docker run --rm -it --network multmatrizes_dist-net client-app > t.txt
```

### Saida:
Para desligar os container do servidor em execução, execute este comando na raiz do projeto:

```sh
docker-compose -f 'docker-compose.yml'  -p 'multmatrizes' down
```
