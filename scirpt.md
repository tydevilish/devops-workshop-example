0. เข้าไปที่โปรเจคแรกที่เคยสร้างไว้ (my-project)

1. 
จากนั้นกดคลิก code

2. กดก๊อปปี้ลิงค์ url repo โปรเจคที่สร้างไว้

3. เปิด terminal ตรงที่ๆต้องการให้โปรเจคไปอยู่จากนั้นใช้คำสั่ง "git clone (url)"

4. เมื่อ clone เรียบร้อยให้ทำการ "cd my-project" เพื่อเข้าไปยังโปรเจคที่เรา clone

5. จากนั้นใช้คำสั่ง "code ." เพื่อเปิด vscode ขึ้นมา

6. หลังจาก vscode เปิดขึ้นมาจะมีไฟล์ของโปรเจคที่เราเคยทำไว้อยู่ จากนั้นสร้างไฟล์ใหม่ชื่ิอ "index.html"

ึึ7. นำโค้ด portflolio ที่เราเคยทำไว้มาใส่ในไฟล์ "index.html"

8. และสร้างไฟล์ใหม่ชื่อ "nginx.conf"

9. พิมพ์ config ในไฟล์นี้ โดยจะเป็นไฟล์สำหรับตั้งค่า web server กำหนดหน้าแรก บีบอัดไฟล์ให้ และซ่อนเวอร์ชันเพื่อความปลอดภัย
Code Copy
server {
    listen 80;
    server_name localhost;

    # ปิดการโชว์เวอร์ชัน Nginx ป้องกันแฮกเกอร์เจาะระบบจากเวอร์ชัน
    server_tokens off; 

    location / {
        root   /usr/share/nginx/html;
        index  index.html;
    }

    # เปิดบีบอัดไฟล์ (Gzip) ทำให้ไฟล์เล็กลง เว็บโหลดเร็วขึ้นมาก
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/javascript;
}

10. จากนั้นสร้างไฟล์ใหม่ชื่อ "Dockerfile"

11. พิมพ์โค้ดเพื่อสร้างไฟล์ image สำหรับ docker
copycode
# ใช้ Nginx เวอร์ชัน Alpine เพราะมีขนาดเล็กมาก ประหยัดทรัพยากร
FROM nginx:alpine

# เอาระบบตั้งค่า Nginx (ที่มี Gzip) ไปทับการตั้งค่าเดิมของระบบ
COPY nginx.conf /etc/nginx/conf.d/default.conf

# เอาไฟล์เว็บทั้งหมดในโปรเจกต์ ไปไว้ในโฟลเดอร์แสดงผล
COPY . /usr/share/nginx/html

# เปิดประตูพอร์ต 80 ของกล่องนี้เอาไว้
EXPOSE 80

# สั่งให้ Nginx ทำงานแบบไม่หยุด
CMD ["nginx", "-g", "daemon off;"]

12. สร้างไฟล์ชื่อ "docker-compose.yml" เพื่อกำหนด services ต่างๆ

13. พิมพ์โค้ด โดยไฟล์ตัวนี้จะถูกโยนไปรันบนเซิร์ฟเวอร์ เพื่อเปิดพอร์ตของตัวเอง
copy  services:
  web:
    # ดึงกล่องเวอร์ชันล่าสุดมาจากโกดังของ GitLab (เปลื่ยน username เป็นชื่อ gitlab ของคุณ)
    image: registry.gitlab.com/**username**/my-project:latest
    container_name: my_website
    
    ports:
      # เลขซ้ายคือพอร์ตเครื่องเซิร์ฟเวอร์ (99xx) : เลขขวาคือพอร์ตของกล่อง (80) (ให้เปลื่ยนเฉพาะด้านซ้ายเป็นเลขที่ของคุณ)
      - "**99xx**:80" 
      
    # ถ้าระบบค้าง พัง หรือไฟดับ ให้รันตัวเองขึ้นมาใหม่เสมอ
    restart: unless-stopped 
    
    # จำกัดขนาดไฟล์ Log (ประวัติการใช้งาน) ไม่ให้กินพื้นที่ฮาร์ดดิสก์เครื่องเซิร์ฟเวอร์
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

14 กำหนดชืื่อใน gitlab และหมายเลข port ให้ตรงกับของตัวเอง

15. เข้าไปที่ไฟล์ ".gitlab-ci.yml" ซึ่งเราเคยสร้างไว้จาก workshop ก่อนหน้าโดยเป็นไฟล์สำหรับสั่งงานระบบ ci/cd 

16. พิมพ์โค้ดลงไปจะมี 3 ขั้นตอน **สร้าง (Build) -> ตรวจสอบโค้ด (Test) -> รีโมทรันบนเซิร์ฟเวอร์ (Deploy)** โดยขั้นตอนที่ 1 จะเป็นการ...... 2..... 3........ เขียนให้หน่อย ai

copy code
stages:
  - build
  - test
  - deploy

variables:
  # ตั้งชื่อกล่องให้เป็นมาตรฐานอัตโนมัติ
  IMAGE_TAG: $CI_REGISTRY_IMAGE:latest

# ==========================================
# 1. BUILD: สร้างกล่องแล้วดันขึ้นเก็บในโกดัง GitLab
# ==========================================
build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG
  only:
    - main

# ==========================================
# 2. TEST: ตรวจสอบความถูกต้องของไฟล์ HTML
# ==========================================
test:
  stage: test
  image: alpine:latest
  needs: ["build"]
  script:
    - apk add --no-cache tidyhtml
    - tidy -q -e index.html; [ $? -le 1 ]
  only:
    - main

# ==========================================
# 3. DEPLOY: รีโมทไปสั่งเซิร์ฟเวอร์ดึงกล่องมารัน
# ==========================================
deploy:
  stage: deploy
  image: alpine:latest
  needs: ["test"]
  before_script:
    - apk add --no-cache openssh-client sshpass
  script:
    # สร้างโฟลเดอร์รอไว้บนเซิร์ฟเวอร์ (แยกชื่อโฟลเดอร์ตามโปรเจกต์อัตโนมัติ)
    - sshpass -p "$SERVER_PASSWORD" ssh -o StrictHostKeyChecking=no "$SERVER_USER@$SERVER_IP" "mkdir -p ~/deploys/$CI_PROJECT_PATH_SLUG"
    
    # ส่งไฟล์ docker-compose.yml ข้ามอินเทอร์เน็ตไปวางที่เซิร์ฟเวอร์
    - sshpass -p "$SERVER_PASSWORD" scp -o StrictHostKeyChecking=no docker-compose.yml $SERVER_USER@$SERVER_IP:~/deploys/$CI_PROJECT_PATH_SLUG/
    
    # รีโมทไปสั่งเซิร์ฟเวอร์: เข้าโฟลเดอร์ -> ล็อกอิน GitLab -> โหลดกล่องใหม่ -> รันเว็บ
    - >
      sshpass -p "$SERVER_PASSWORD" ssh -o StrictHostKeyChecking=no "$SERVER_USER@$SERVER_IP" "
      cd ~/deploys/$CI_PROJECT_PATH_SLUG &&
      docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY &&
      docker compose pull &&
      docker compose up -d
      "
  only:
    - main


17. คลิกที่ terminal

18 กด new terminal เพื่อเปิด terminal ขึ้นมา

19. ใช้คำสั่ง "git add ." เพื่อนำไฟล์ที่เราแก้ไขทั้งหมดไปเก็บไว้ใน Staging Area เพื่อเตรียมพร้อมก่อน git commit ต่อไป 

20. ใช้คำสั่ง "git commit -m "fest: Add index, Dockerfile, docker-compose, gitlab, nginx"" บันทึกประวัติพร้อมระบุข้อความอธิบาย

21. จากนั้นใช้คำสั่ง "git branch -m main" เพิื่อไปที่ branch main หรือ เพื่อให้แน่ใจว่าจะ push โค้ดไป branch main แน่ๆเพราะในไฟล์ ".gitlab-ci.yml" เรากำหนดว่าให้ทำงานเฉพาะ branch main เท่านั้นถ้า push โค้ดขึ้นไปที่ branch อื่นจะไม่ทำงาน

22. ขั้นตอนสุดท้ายใช้ "git push -u origin main" เพื่อ push โค้ดไปยัง gitlab 23. ใส่รูปไว้ข้างล่างรูป 22 เลยเพราะมันแค่แสดงหลังรันคำสั่งทั้งหมดเฉยๆ

24. กลับเข้ามาที่ gitlab และ my-project จะสังเกตเห็นว่าโค้ดที่เราแก้หรือสร้างทั้งหมดมาอยู่ใน gitlab แล้วและ จะมี CI/CD Pipeline กำลังทำงานอยู่ สังเกตจากไอคอนกลม ๆ ข้างเวอร์ชั่นของ commit แต่ในตอนนี้อาจจะกำลังทำงานหรือ error  เนื่องจากเรายังไม่ได้กำหนดตัวแปร (variable) ที่จะใช้เชื่อมต่อกับ server

25 แถบด้านข้างเลือก setting (เอาภาพขึ้นตอนเดียวกันเลยแค่เอาไปไว้ด้านล้าง ) 26.เลือก ci/cd 

27. หลังจากนั้นเลือก "Variables"

28. เลื่อนลงมาเลือก Add variable เพื่อเพิ่มตัวแปรใหม่ใช้เข้า server

29. เลือกตัวแปรแบบ visible

30. ตัวแปรแรก SERVER_IP	49.229.108.152 จากนั้นกด "Add variable"

31. หลังจากกดตัวแปรที่เพิ่มก็จะแสดง 32-35 (เหมือนกันแต่เปลื่ยนเป็น เอารูปมาไว้ด้วยกันก็ได้แค่ให้ดู) SERVER_USER	user 36-38 (ก็เหมือนกัน) SERVER_PASSWORD	9875321

39. มาที่แถบด้านซ้ายเลื่อนขึ้นไปเลือกชื่อ my-project เพื่อกลับไปยังโปรเจคของเรา

40. หลังมาที่โปรเจค สังเกตด้านข้างหมายเลข commit จะมีไอคอนกลม ๆ อยู่อาจจะทำงานอยู่หรือทำสำเร็จแล้วกดเข้าไป

41. จะเห็นว่าการทำงานทั้ง 3 ขั้นตอนเสร็จสิ้นแล้ว **แต่ถ้า error ก็กด retry ด้านบนล้วก็รอซักแปปนะ 55555**

42. คลิกเลือกขั้นตอน deploy

43. จะมี log การทำงานแสดงถ้าทำงานสำเร็จก็จะขึ้น "Job Succeeded" และถ้างานไม่สำเร็จก็จะขึ้น "Job Failed" ก็สามารถกด retry ลองอีกรอบได้ (สำหรับ ai อธิบายให้ด้วยว่ามีข้อความอะไรแสดง)

อันนี้สหรับ ai อธิบายเป็นหมายเหตุว่าทำอะไรในขั้นตอนนี้

Running with gitlab-runner 19.2.0~pre.1355.g471b878c (471b878c)
  on green-5.saas-linux-small-amd64.runners-manager.gitlab.com/default xS6Vzpvoq, system ID: s_6b1e4f06fcfd
  feature flags: FF_USE_GIT_PROACTIVE_AUTH:true, FF_HASH_CACHE_KEYS:true

Preparing the "docker+machine" executor
00:06
Using Docker executor with image alpine:latest ...
Using effective pull policy of [always] for container alpine:latest
Pulling docker image alpine:latest ...
Using docker image sha256:d529dd0c6e5597ac7e4a3e2dea65c3fcc6173f4cae713c409265c1dd9914a11b for alpine:latest with digest alpine@sha256:28bd5fe8b56d1bd048e5babf5b10710ebe0bae67db86916198a6eec434943f8b ...

Preparing environment
00:01
Using effective pull policy of [always] for container sha256:84bb709aa2bbc1c5e5b14dbd5948b334d2f8a07caccb202f860b3c3f4ee6e254
Running on runner-xs6vzpvoq-project-85096556-concurrent-0 via runner-xs6vzpvoq-s-l-s-amd64-1786468958-18d4308d...

Getting source from Git repository
00:01
Gitaly correlation ID: 886a27ca67004d3f8ca1c6af6f053273
Fetching changes with git depth set to 20...
Initialized empty Git repository in /builds/tydevilish/my-project/.git/
Created fresh repository.
Checking out 225f53b8 as detached HEAD (ref is main)...
Skipping Git submodules setup
$ git remote set-url origin "${CI_REPOSITORY_URL}" || echo 'Not a git repository; skipping'

Executing "step_script" stage of the job script
00:22
Using effective pull policy of [always] for container alpine:latest
Using docker image sha256:d529dd0c6e5597ac7e4a3e2dea65c3fcc6173f4cae713c409265c1dd9914a11b for alpine:latest with digest alpine@sha256:28bd5fe8b56d1bd048e5babf5b10710ebe0bae67db86916198a6eec434943f8b ...
$ apk add --no-cache openssh-client sshpass
(1/7) Installing openssh-keygen (10.3_p1-r0)
(2/7) Installing ncurses-terminfo-base (6.6_p20260516-r0)
(3/7) Installing libncursesw (6.6_p20260516-r0)
(4/7) Installing libedit (20260508.3.1-r1)
(5/7) Installing openssh-client-common (10.3_p1-r0)
(6/7) Installing openssh-client-default (10.3_p1-r0)
(7/7) Installing sshpass (1.10-r0)
Executing busybox-1.37.0-r31.trigger
OK: 11.8 MiB in 23 packages
$ sshpass -p "$SERVER_PASSWORD" ssh -o StrictHostKeyChecking=no "$SERVER_USER@$SERVER_IP" "mkdir -p ~/deploys/$CI_PROJECT_PATH_SLUG"
Warning: Permanently added '[MASKED]' (ED25519) to the list of known hosts.
$ sshpass -p "$SERVER_PASSWORD" scp -o StrictHostKeyChecking=no docker-compose.yml $SERVER_USER@$SERVER_IP:~/deploys/$CI_PROJECT_PATH_SLUG/
$ sshpass -p "$SERVER_PASSWORD" ssh -o StrictHostKeyChecking=no "$SERVER_USER@$SERVER_IP" " cd ~/deploys/$CI_PROJECT_PATH_SLUG && docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY && docker compose pull && docker compose up -d "
WARNING! Using --password via the CLI is insecure. Use --password-stdin.
WARNING! Your credentials are stored unencrypted in '/home/user/.docker/config.json'.
Configure a credential helper to remove this warning. See
https://docs.docker.com/go/credential-store/
Login Succeeded
 Image registry.gitlab.com/tydevilish/my-project:latest Pulling 
 6ca27e509c31 Pulling fs layer 0B
 d9cb6464796a Pulling fs layer 0B
 6ca27e509c31 Download complete 0B
 d9cb6464796a Download complete 0B
 6ca27e509c31 Extracting 1B
 d9cb6464796a Pull complete 0B
 6ca27e509c31 Pull complete 0B
 Image registry.gitlab.com/tydevilish/my-project:latest Pulled 
 Container my_website Recreate 
 Container my_website Recreated 
 Container my_website Starting 
 Container my_website Started 

Cleaning up project directory and file based variables
00:00
Job succeeded

44. มาที่ browser ของเราจากนั้นพิมพ์ "49.229.108.152:99xx" แก้ 2 ตัวท้ายเป็นเลขที่เรานะ จากนั้นกด enter ที่คีย์บอร์ด

45. หน้าเว็บ index.html ที่เราทำก็จะมาแสดงแล้ว เป็นอันเสร็จสิ้น โคตรโหด