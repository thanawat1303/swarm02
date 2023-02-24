# swarm02
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

    hostnamectl set-hostname "ชื่อ Hostname โดยต้องห้ามซ้ำ" => spcn19-swarm02

 3. Reset Machine ID เพื่อขอ Public IP จาก DHCP
 4. ทำการนำ Url Token จากคำสั่ง 
 
    docker swarm init 
        
    ในเครื่อง Manage มาทำการรันเพื่อเชื่อมต่อ swarm

 5. ทำการเตรียมไฟล์ docker-compose.yml
    - image => ใช้ image จาก DockerFile
    - logging => json-file คือ เลือกประเภทการ log เป็น json
    - command => สั่งใช้งาน command หลังจากรีบูท containner เสร็จสิ้น
    - containner_name => ตั้งชื่อ containner
    - environment => PORT คือ PORT ที่ตัว containner ทำงานอยู่
    - ports => พอร์ตในการเข้าถึงโปรแกรม - พอร์ตที่เข้าถึงผ่าน Host : พอร์ตที่ทำการเชื่อมเข้าหา Containner
    - volumes => mount ส่วนเก็บข้อมูล - Path ข้อมูลบน Host : Path ข้อมูลบน Containner
    - deploy เซ็ตการ deploy สำหรับ swarm
      - replicas => กำหนดเครื่อง worker ที่ต้องหการให้ deploy containner ลงไป
      - resources => กำหนดสเปคที่ต้องการของ Containner
        - reservations => กำหนดค่าขั้นต่ำของสเปค
        - limits => กำหนดค่าสูงสุดของสเปค
    - volumes => พื้นที่เก็บข้อมูลที่จะสร้างไว้ให้อยู่บน Host
      - app => ชื่อพื้นที่เก็บข้อมูล ต้องตรงตามที่กำหนดที่ volumes ที่ mount กับ cpntianner

 6. ทำการ Remote ไฟล์งานเข้าสู่ Repo swarm02 บน github
 7. ทำการนำข้อมูลในไฟล์ docker-compose หรือ LINK repo github

### Remote Repo on LINUX
 1. ทำการสร้างไฟล์ README.md ใน Repo 
 2. git clone <URL GIT Repo>

## Ref
- https://github.com/docker/awesome-compose/tree/master/fastapi