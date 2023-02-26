# swarm02 Fast API:Python
### ขั้นตอนการติดตั้ง และใช้งาน ใน VM
 1. Set Template 

   set time

    timedatectl set-timezone Asia/Bangkok

   install Docker

    apt update; apt upgrade -y #อัปเดตแพ็คเกจภายในเครื่อง

    apt-get install ca-certificates curl wget gnupg lsb-release -y #ติดตั้งแพ็คเกจ

    mkdir -m 0755 -p /etv/apt/keyrings

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg #ดาวโหลดไฟล์แพ็คเกจ Docker

    echo \ "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \ $(lsb_release -cs) stable" |  tee /etc/apt/sources.list.d/docker.list > /dev/null

    apt-get update #อัปเดทไฟล์แพ็คเกจเพื่อไว้สำหรับให้ติดตั้ง
    apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y #ติดตั้ง Docker

    reboot

 2. Set Hostname 

   ```
   hostnamectl set-hostname "ชื่อ Hostname โดยต้องห้ามซ้ำ" #spcn19-swarm02
   ```

 3. Reset Machine ID เพื่อขอ Public IP จาก DHCP
   
   ```
   cp /dev/null /etc/machine-id
   rm /var/lib/dbus/machine-id
   ln -s /etc/machine-id /var/lib/dbus/machine-id
   init 0
   ```
   
 4. ทำการนำ Url Token จากคำสั่ง 
 
    docker swarm init 
        
    ในเครื่อง Manage มาทำการรันเพื่อเชื่อมต่อ swarm

 5. <a href="revert-proxy">ทำการเตรียม Revert Proxy</a>
 6. ทำการเตรียมไฟล์ docker-compose.yml
    - version => เวอร์ชั่นของไฟล์ compose ต้อง 3 ขึ้นไป
    - services :
      - api : => ชื่อของ application
        - image => ใช้ image จาก DockerFile หรือ image ที่ต้องการใน DockerHub
        - network => เน็ตเวิร์คของ Traefik
        - command => สั่งใช้งาน command หลังจากรีบูท containner เสร็จสิ้น
        - environment => สภาพแวดล้อมที่ application ต้องการ
          - PORT => พอร์ตที่ application ต้องการ
        - logging => ประวัติการทำงานของ container
          - driver => json-file คือ เลือกประเภทการ log เป็น json
        - volumes => ส่วนของการเก็บข้องมูลของ containner
          - path ที่เก็บข้อมูลภายใน host : path ที่เก็บข้อมูลภายใน container
        - deploy => เซ็ตการ deploy สำหรับ swarm
          - replicas => กำหนดเครื่อง worker ที่ต้องการให้ deploy containner ลงไป
          - labels => กำหนด labels ให้ application โดยจะเป็นการตั้งค่าเชื่อมต่อกับ Traefik
            - traefik.docker.network => ชื่อ network ของ Traefik
            - traefik.enable => กำหนดสถานะการใช้งาน
            - traefik.constraint-label => เลือก traefik ที่ต้องการให้ container ไปทำงาน
            - traefik.http.routers.spcn19fastapi-https.entrypoints => กำหนด port ในการเชื่อมต่อเมื่อมีคำขอเข้าไปที่ traefik
            - traefik.http.routers.spcn19fastapi-https.rule=Host("spcn19fastapi.xops.ipv9.xyz") 
            traefik.http.routers.spcn19fastapi-https.tls.certresolver => กำหนดการสร้างใบรับรองที่ตัว treafik จะทำการร้องขอไป
            - traefik.http.services.spcn19fastapi.loadbalancer.server.port กำหนดให้มีการ balance ในการร้องขอ port ที่ container ทำงาน
            - traefik.http.routers.spcn19fastapi-https.tls => เปิดใช้งาน Protocal TLS
          - resources => กำหนดสเปคที่ต้องการของ Containner
            - reservations => กำหนดค่าขั้นต่ำของสเปค
            - limits => กำหนดค่าสูงสุดของสเปค
    - networks => กำหนด networks ที่อยู่ภายในระบบ
      - webproxy => บริการ network revert proxy ที่อยู่ภายในระบบ
        - external => กำหนดสถานะของ network ที่อยู่ภายใน host
    - volumes => พื้นที่เก็บข้อมูลที่จะสร้างไว้ให้อยู่บน Host
      - app => ชื่อพื้นที่เก็บข้อมูล ภายใน host ต้องตรงตามที่กำหนดที่ volumes ที่ mount กับ contianner
        - external => กำหนดสถานะของที่เก็บข้อมูลที่อยู่ภายใน host
 7. จัดการไฟล์ main.py ใน path app/main.py เพื่อจัดการ UI ใน application
 8. ทำการ Remote และ upload ไฟล์งานเข้าสู่ Repo swarm02 บน github
 9. ทำการนำข้อมูลในไฟล์ docker-compose หรือ LINK repo github เข้ากับ potainer ของระบบ
 10. Deploy

### Revert Proxy
<a name="revert-proxy"></a>

 - Manage Traefik

   - Set IP สำหรับเครื่อง Client
     - แก้ไขไฟล์ hosts
     - windows C:\Windows\System32\drivers\etc\hosts
     - Linux /etc/hosts
     - เพิ่ม Domain ให้แต่ละโปรแกรมโดยเชื่อมเข้าสู่ IP ของ manager เช้น 172.31.1.178 traefik.demo.local

   - สร้าง Network ใหม่
 
   docker network create --driver=overlay traefik-public

   - Get ID Node 

   export NODE_ID=$(docker info -f '{{.Swarm.NodeID}}')
   echo $NODE_ID

   - สร้าง Label ของ Node Manage

   docker node update --label-add traefik-public.traefik-public-certificates=true $NODE_ID

   - set Treafik

   export EMAIL=user@smtp.com
   export DOMAIN=<ชื่อ traefik domain ที่ต้องการให้เข้าถึง traefik>
   export USERNAME=admin
   export PASSWORD=<รหัสผ่าน traefik>
   export HASHED_PASSWORD=$(openssl passwd -apr1 $PASSWORD)
   echo $HASHED_PASSWORD

   - deploy traefik stack

   docker stack deploy -c traefik-host.yml traefik

   - ทดลองเปิดหน้า Dashboard Traefik

   ![image.png]

   ### Ref

   - https://github.com/pitimon/dockerswarm-inhoure/tree/main/ep03-traefik

### Remote Repo on LINUX
 1. ทำการสร้างไฟล์ README.md ใน Repo 
 2. git clone <URL GIT Repo>

## Ref
- https://github.com/docker/awesome-compose/tree/master/fastapi