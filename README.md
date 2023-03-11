# swarm02 fastapi

### Ref awaresome-compose
- https://github.com/docker/awesome-compose/tree/master/fastapi

### Wakatime project
- https://wakatime.com/@spcn19/projects/iickecxaxq

### Url fastapi app
- https://spcn19fastapi.xops.ipv9.xyz

### Step on Work
 
 1. [Create Image of Dockerfile](#create-image-on-dockerfile)
 2. Create docker-compose.yml `spcn19fastapi`
    <details>
    <summary>Show code</summary>

    ```ruby
    version: '3.3' #version compose must than 3 
    services: 
      api: #name application
        image: thanawat1303/fastapi-main:v1 #image service on dockerhub
        networks: #network in service
        - webproxy #network traefik
        environment: #environment application
          PORT: 8000 
        logging:
          driver: json-file #type file 
        volumes: #mount data volume of container
          - /var/run/docker.sock:/var/run/docker.sock
          - app:/app #"path data on host" : "path data on container"
        restart: 'no'
        deploy: #set deploy for swarm
          replicas: 1 #set amount worker want deploy container
          labels: #set labels application connect Traefik
            - traefik.docker.network=webproxy #name network of Traefik
            - traefik.enable=true #status of connect
            - traefik.constraint-label=webproxy #select traefik want container working
            - traefik.http.routers.spcn19fastapi-https.entrypoints=websecure #set position when have request to traefik
            - traefik.http.routers.spcn19fastapi-https.rule=Host("spcn19fastapi.xops.ipv9.xyz") #set domain access to application
            - traefik.http.routers.spcn19fastapi-https.tls.certresolver=default #set certresolver
            - traefik.http.services.spcn19fastapi.loadbalancer.server.port=8000 #set balance when request to port on container
            - traefik.http.routers.spcn19fastapi-https.tls=true #set status Protocal TLS
          resources: #set space that want of Container
            reservations: #set low space
              cpus: '0.1' 
              memory: 10M
            limits: #set high space
              cpus: '0.4'
              memory: 250M
              
    networks: #set networks outside container
      webproxy: #service network revert proxy on cluster
        external: true
    volumes: #volumes on host of Docker
      app:
    ```

    </details>
 3. Push docker-compose.yml to github swarm02
 4. Open https://portainer.ipv9.me/

<div align="center"><img src="app/image/openportainer.png" width="500px"></div>

 5. Click Cluster Xopx.ipv9.xyz on Portainer
 6. Click menu Stack on Cluster Xopx.ipv9.xyz

<div align="center"><img src="app/image/cluster.png" width="500px"></div>

 7. Click button Add Stack

<div align="center"><img src="app/image/menuservice.png" width="500px"></div>

 8. Click Build medthod is Repository

<div align="center"><img src="app/image/addStack.png" width="500px"></div>

  - Name = name Stack
  - Repository URL = https://github.com/thanawat1303/swarm02
  - Repository reference = refs/heads/main
  - Compose path = name Compose file
  - Automatic updates = enable
    - Fetch interval = time check change on compose file from github 
    
 9. Click button Deploy the stack

### Create Image on Dockerfile
 1. Create main.py
    <details>
    <summary>Show code</summary>

    ```ruby
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    def hello_world():
        return {"message": "ผมรักวิชานี้ SPCN19"}
    ```

    </details>
 2. Create Dockerfile
    <details>
    <summary>Show code</summary>

    ```ruby
    FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim AS builder #image container

    WORKDIR . #Set path working command on container

    COPY requirements.txt ./ #Copy file on host to container
    RUN --mount=type=cache,target=/root/.cache/pip \
        pip install -r requirements.txt #run command on container

    COPY . ./app/ #Copy file on host to container

    FROM builder as dev-envs

    RUN <<EOF
    apt-get update
    apt-get install -y --no-install-recommends git
    EOF

    RUN <<EOF
    useradd -s /bin/bash -m vscode
    groupadd docker
    usermod -aG docker vscode
    EOF
    # install Docker tools (cli, buildx, compose)
    COPY --from=gloursdocker/docker / /
    ```

    </details>
 3. Build image from Dockerfile
 
    ```
    docker build . -t <usernameDockerHub>/<repo>:<tag> #thanawat1303/fastapi-main:v1
    ```
 4. Push image to DockerHub

     ```
     docker push <image ID> <usernameDockerHub>/<repo>:<tag> #thanawat1303/fastapi-main:v1
     ```