1. Set Template 

    - Set time
      ```
      timedatectl set-timezone Asia/Bangkok
      ```

    - Install Docker
      ```
      apt update; apt upgrade -y #update packet

      apt-get install ca-certificates curl wget gnupg lsb-release -y #install packet

      mkdir -m 0755 -p /etv/apt/keyrings

      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg #Download packet Docker

      echo \ "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \ $(lsb_release -cs) stable" |  tee /etc/apt/sources.list.d/docker.list > /dev/null

      apt-get update #update file packet give can install
      apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y #install Docker

      reboot
      ```

 2. Create node from Template
    - manage
    - work1
    - work2

 3. Set Hostname
    ```
    hostnamectl set-hostname "Hostname not must duplicate" #spcn19-swarm02
    ```

 4. Reset machine ID to request a public IP from DHCP
    ```
    cp /dev/null /etc/machine-id
    rm /var/lib/dbus/machine-id
    ln -s /etc/machine-id /var/lib/dbus/machine-id
    init 0
    ```

 5. [Stack swarm and Portainer CE](#stack-swarm)
 6. [Revert Proxy](#revert-proxy)

 ### Stack Swarm and Portainer CE
<a name="stack-swarm"></a>

 - Manager Swarm

   - Swarm init
     ```
     docker swarm init #Run on manage node
     ```

   - Copy token url, after that run on every worker node

   - Check node stack swarm
     ```
     docker node ls
     ```

   - Install portainer CE
     ```
     curl -L https://downloads.portainer.io/ce2-17/portainer-agent-stack.yml -o portainer-agent-stack.yml
     docker stack deploy -c portainer-agent-stack.yml portainer
     ```

   ### Ref
   - https://github.com/pitimon/dockerswarm-inhoure#swarm-init

### Revert Proxy
<a name="revert-proxy"></a>

 - Manager Traefik

   - Set IP for Client
     - Edit file hosts
       - windows C:\Windows\System32\drivers\etc\hosts
       - Linux /etc/hosts
     - Add domain is a IP of manager for every application 
       - Ex.
         ``` 
         "ip manage" traefik.demo.local
         ```

   - Create new network
     ```
     docker network create --driver=overlay traefik-public
     ```

   - Get ID node 
     ```
     export NODE_ID=$(docker info -f '{{.Swarm.NodeID}}') 
     echo $NODE_ID
     ```

   - Create label of node manage
     ```
     docker node update --label-add traefik-public.traefik-public-certificates=true $NODE_ID
     ```

   - Set Treafik
     ```
     export EMAIL=user@smtp.com
     export DOMAIN=<traefik domain that want access traefik>
     export USERNAME=admin
     export PASSWORD=<password traefik>
     export HASHED_PASSWORD=$(openssl passwd -apr1 $PASSWORD)
     echo $HASHED_PASSWORD
     ```

   - Deploy traefik stack
     ```
     docker stack deploy -c traefik-host.yml traefik
     ```
     
   - Test open dashboard Traefik

   ### Ref
   - https://github.com/pitimon/dockerswarm-inhoure/tree/main/ep03-traefik

### Remote Repo on LINUX
 1. Create file README.md in Repo swarm02 
 2. run
    ```
    git clone "URL GIT Repo"
    ```