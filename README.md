Panabara


# 로컬에서 참조 프로젝트 설치 dd
```
1) C:\Panabara\>python -m venv pnbr_env

2) C:\Panabara\pnbr_env\Scripts>activate

3) (pnbr_env) C:\Panabara>git clone 주소

4) (pnbr_env) C:\Panabara\django-bootstrap-modal-forms>pip install -r requirements.txt

5) (pnbr_env) C:\Users\dc\Downloads\django-bootstrap-modal-forms-2.0.1>pip install .

6) (pnbr_env) C:\Panabara\panabara> python manage.py makemigrations 이후, python manage.py migrate

7) (pnbr_env) C:\Panabara\panabara>python manage.py runserver
```
# Django Super User 생성
```
>python manage.py createsuperuser
Username (leave blank to use 'pinco'): xxxx
Email address: test@example.com
Password:xxxx
Password (again):xxxx
Superuser created successfully.
```

# 프로젝트 실행


```
cd C:\Panabara\pnbr_env\Scripts  
activate

cd C:\Panabara\pnbr_env\Scripts\activate.bat

cd C:\Panabara\PANABARA

(pnbr_env) C:\Panabara\PANABARA>python manage.py runserver --noreload

(pnbr_env) C:\Panabara\PANABARA>python manage.py runserver --noreload  0.0.0.0:8000
```


# 외부 접속 설정 (무선 공유기 활용시..)

  - Settings.py 내 ALLOWED_HOSTS 등록 필요


# github repository location
        - https://github.com/dcjamespark/panabara.git


# sqlite3 실행하기

```
> python manage.py dbshell

sqlite> .tables  

-- users 테이블 보기

sqlite> .schema examples_mystocks

sqlite> select * from auth_user;

sqlite> select * from examples_mystocks where author_id ='3';

sqlite> select * from examples_stockbaseinfo;

sqlite> select * from examples_MyStocks;

select * from examples_balances;

-- 유저별로 남긴 코멘트 조회 (join문)
sqlite> select users.naeme, comments.content
        from users join comments
        on comments.author_id = users.id;

-- 유저ID 1번이 남긴 코멘트 조회
sqlite> select users.naeme, comments.content
        from users join comments
        on comments.author_id = users.id
        where users.id=1;
```


# 모듈 설치
  - Upbit : pip install pyupbit


# 배치프로세싱 설치하기

- 상세 링크 : https://m.blog.naver.com/c_ist82/220777045214
  - Celery 설치 : pip install celery
  - kombu 설치 - 메세징 라이브러리(Messaging library) : pip install kombu


# 시작 시 실행 필요 설정
- 파일 위치 : __init.py__
  - default_app_config = 'examples.stockbaseinfo.MyAppConfig' 주석 해제 필요
  - runserver 뒤에 --noreload 붙이기



# FinanceDataReader
  - https://github.com/FinanceData/FinanceDataReader


# requirement.txt 만들기
  - pip freeze > requirements.txt

# 주의 사항
  - Null  값 존재시, Sorting 기능 안됨.

```
<link rel="stylesheet" href="https://cdn.datatables.net/1.10.23/css/dataTables.bootstrap4.min.css">
<script src="https://code.jquery.com/jquery-3.5.1.js"></script>

<!-- https://code.jquery.com/jquery-3.5.1.js -->
<!-- https://cdn.datatables.net/1.10.23/js/jquery.dataTables.min.js -->
```
# 알림 메시지 관련

```

from django.contrib import messages

messages.debug(request, '%s SQL statements were executed.' % count)
messages.info(request, 'Three credits remain in your account.')
messages.success(request, 'Profile details updated.')
messages.warning(request, 'Your account expires in three days.')
messages.error(request, 'Document deleted.')

```


# Div 태그 숨기기/펼치기

```

      <a href="#Foo" class="btn btn-default" data-toggle="collapse">Toggle Foo</a>
      <button href="#Bar" class="btn btn-default" data-toggle="collapse">Toggle Bar</button>
      <div id="Foo" class="collapse in">
          This div (Foo) is hidden by default
      </div>
      <div id="Bar" class="collapse in">
          This div (Bar) is shown by default and can toggle
      </div>
```

# TO_DO List

- 완료 사항
  - 신규 입력 시, 코드값으로 관련 종목명, 정보 데이터에 저장

- 조회시 종목별로 아래 불러와서 화면에 보여주기 -> 언제??? 인덱스 띄울때? 버튼 클릭 시??

  - 주식 현재가 불러오는 펑션 : 완료
  - 비트코인 현재가 불러오는 펑션 : 완료
  -

  - refresh 버튼으로 현재가 갱신하기
  - 비트코인 소수점 처리

  - 2/11 AWS 서버구축 관련 마크다운에 추가, 속도개선(bulk_update, bulk_insert 반영)

  # 서버 패치 시 주의 사항
   - 아래 Setting.py 적용 필요
   ```
   STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
```




******************************************************************


***
# 전 종목 리스트 받아오기 to Stocklistinfo 테이블

## 구분별 가져오기 다름
  - 코스피, 코스닥 : krx 사이트
  - 우선주 : 크롤링 대상 사이트 없어 아래 파일에 저장하여 가져옴
    - \\examples\\uploadfiles\\UseonjuList.txt
  - ETF, ETN : 네이버 증권 사이트로 부터 가져옴
    - finance.naver.com
  - NYSE, NASDAQ : FinanceDataReader 에서 가져옴.

## 업데이트 방법
  - 컨셉 : 로컬에서 종목 정보들을 가져와 DB 저장 후 sqlite3 데이터를 그대로 서버에 올림
  - 방법
    - init.py 파일의 default_app_config = 'examples.stockbaseinfo.MyAppConfig' 주석 해제
    - 로컬에서 python manage.py runserver --noreload 실행
    - 이후 shell 에서 갯수 확인
    ```
    (pnbr_env) C:\Panabara\PANABARA>python manage.py dbshell
    SQLite version 3.33.0 2020-08-14 13:23:32
    Enter ".help" for usage hints.
    sqlite> select count(*) from examples_stockbaseinfo;
    9785
    ```
    - init.py 파일의 default_app_config = 'examples.stockbaseinfo.MyAppConfig' 주석 원복


***

# AWS 에 Django 프로젝트 구축하기
본 링크 참조하여 작성함 : <https://nerogarret.tistory.com/> to 작성자: 감사드립니다. 많은 도움이 되었습니다.^^

## AWS 임대하기

#### AWS 로그인 후 서비스 -> EC2
  - 리전 선택 (서울)
  - 인스턴스 시작 -> Ubuntu Server 18.04 LTS를 선택
  - 인스턴스 유형 : 12 micro 프리티어 선택 -> 검토 및 시작
  - 키페어 설정 및 다운로드 진행 (pem 파일) 이후 인스턴스 시작하기
  - 키 페어를 홈 폴더(~)의 .ssh 폴더로 옮긴다
  ```
  (~/.ssh 폴더가 없을 경우) $ mkdir ~/.ssh/
  $ mv ~/Downloads/deploy_test.pem ~/.ssh/
  ```
  - 키페어 확인
  ```
  $ ls ~/.ssh/
  deploy_test.pem
  ```
  - 권한을 소유주만 읽을 수 있도록 변경
  ```
  $ chmod 400 ~/.ssh/deploy_test.pem
  ```
  - AWS 로 돌아와서 보면 EC2가 켜져 있는 것을 볼 수 있습니다. Name에서 원하는 이름을 써둔다.

## AWS 원격접속하기

  #### 원격 연결

  - $ ssh -i [키 페어 경로] [유저 이름]@[퍼블릭 DNS 주소]
  ```
  $ ssh -i ~/.ssh/deploy_test.pem ubuntu@ec2-15-164-212-231.ap-northeast-2.compute.amazonaws.com
  ```
  - yes 로 연결을 진행합니다. 만약 "WARNING: UNPROTECTED PRIVATE KEY FILE!" 오류가 나면 위의 chmod 400 을 적용하셨는지 다시 확인


### AWS EC2 서버 기본 세팅

- 패키지 정보 업데이트
```
$ sudo apt-get update
```
- 패키지 의존성 검사 및 업그레이드:
```
$ sudo apt-get dist-upgrade
```
- python3 패키지 매니저(pip3) 설치
```
$ sudo apt-get install python3-pip
```


## Git 을 통해 로컬에서 Git 으로 옮기기

### Git Bash 통해 진행
  - 프로젝트 폴더 안에 manage.py가 있는 곳으로 터미널에 접속
  - git을 초기화
  ```
  $ git init
  ```
  - git에 현재 폴더 전체를 담는다.
  ```
  $ git add .
  ```
  - 업로드할 레포지토리 주소를 origin이라는 이름으로 추가
  ```
  $ git remote add origin [레포지토리 주소]
  ```
  - 변경 사항을 모으고, 어떤 것이 바뀌었는지 알려주는 메세지를 붙입니다. 이를 commit이라고 합니다
  ```
  $ git commit -m "first commit"
  ```
  - 담은 파일들을 origin이라는 이름의 레포지토리 주소로 업로드합니다.
  ```
  $ git push origin master
  ```

  -  이 다음 부터 로컬 컴퓨터에서 파일들이 수정되면 아래로 진행
  ```
  $ git add .
  $ git commit -m "무엇을 했나"
  $ git push origin master
```

## AWS EC2 서버에서 git clone 하기

### github을 통해 업로드한 파일들을 서버에 원격 접속하여 clone



  - 먼저 서버에 접속
  ```
  $ ssh -i ~/.ssh/deploy_test.pem ubuntu@ec2-15-164-212-231.ap-northeast-2.compute.amazonaws.com
  ```

  - 프로젝트 파일들은 모두 /srv/ 폴더에 다운로드 받을 것입니다.
    - 따라서 이 폴더를 현재 유저인 ubuntu의 폴더로 소유권을 바꾸어 줍니다.
    - sudo는 관리자 권한으로 명령함을 의미
    - chown은 change owner의 줄임말로 폴더의 소유권을 변경할 때 사용

  ```
  $ sudo chown -R ubuntu:ubuntu /srv/
  ```
  - 소유권이 잘 바뀌었는지 확인하려면 루트 폴더(/) 로 이동한 뒤, 파일 리스트를 자세히 표시 (ls -al)하면 srv 폴더의 소유자가 ubuntu로 바뀌었음을 알 수 있습니다.

  ```
  $ cd /
  $ ls -al
  total 96
  drwxr-xr-x  23 root   root    4096 Mar 14 19:32 .
  drwxr-xr-x  23 root   root    4096 Mar 14 19:32 ..
  drwxr-xr-x   2 root   root    4096 Mar 14 19:31 bin
  drwxr-xr-x   3 root   root    4096 Mar 14 19:32 boot
  drwxr-xr-x  15 root   root    2980 Mar 14 18:59 dev
  drwxr-xr-x  89 root   root    4096 Mar 14 19:36 etc
  drwxr-xr-x   3 root   root    4096 Mar 14 18:59 home
  lrwxrwxrwx   1 root   root      31 Mar 14 19:32 initrd.img -> boot/initrd.img-4.15.0-1060-aws
  lrwxrwxrwx   1 root   root      31 Jan 12 17:42 initrd.img.old -> boot/initrd.img-4.15.0-1057-aws
  drwxr-xr-x  20 root   root    4096 Mar 14 19:36 lib
  drwxr-xr-x   2 root   root    4096 Jan 12 17:33 lib64
  drwx------   2 root   root   16384 Jan 12 17:38 lost+found
  drwxr-xr-x   2 root   root    4096 Jan 12 17:33 media
  drwxr-xr-x   2 root   root    4096 Jan 12 17:33 mnt
  drwxr-xr-x   2 root   root    4096 Jan 12 17:33 opt
  dr-xr-xr-x 103 root   root       0 Mar 14 18:59 proc
  drwx------   4 root   root    4096 Mar 14 18:59 root
  drwxr-xr-x  25 root   root     920 Mar 14 20:27 run
  drwxr-xr-x   2 root   root   12288 Mar 14 19:31 sbin
  drwxr-xr-x   5 root   root    4096 Mar 14 18:59 snap
  drwxr-xr-x   2 ubuntu ubuntu  4096 Jan 12 17:33 srv
  dr-xr-xr-x  13 root   root       0 Mar 14 18:59 sys
  drwxrwxrwt   9 root   root    4096 Mar 14 20:27 tmp
  drwxr-xr-x  10 root   root    4096 Jan 12 17:33 usr
  drwxr-xr-x  13 root   root    4096 Jan 12 17:37 var
  lrwxrwxrwx   1 root   root      28 Mar 14 19:32 vmlinuz -> boot/vmlinuz-4.15.0-1060-aws
  lrwxrwxrwx   1 root   root      28 Jan 12 17:42 vmlinuz.old -> boot/vmlinuz-4.15.0-1057-aws
```

  - 이제 /srv/ 폴더로 이동하여 github 의 파일들을 다운 받습니다
  ```
  $ cd /srv
$ git clone [레포지토리 주소]
```
  - 업로드 성공
  ```
  $ git clone https://github.com/nero96in/django-deploy-test.git
  Cloning into 'django-deploy-test'...
  remote: Enumerating objects: 32, done.
  remote: Counting objects: 100% (32/32), done.
  remote: Compressing objects: 100% (25/25), done.
  remote: Total 32 (delta 4), reused 32 (delta 4), pack-reused 0
  Unpacking objects: 100% (32/32), done.

  $ ls
  django-deploy-test

  ```


## uWSGI python 패키지를 이용해 WSGI 서버를 Django와 연결

### 가상환경을 만들어 주고, 패키지 버전들을 저장한 requirements.txt를 통해 패키지 설치

  - 가상환경을 만들기 전에 python3-venv를 설치
  ```
  $ sudo apt-get install python3-venv
  ```
  - 가상환경의 위치는 현재 사용하고 있는 유저인 ubuntu의 홈 폴더에 만들도록 하겠습니다.
  ```
  $ source myvenv/bin/activate
  ```
  - 프로젝트 폴더에 있는 requirememts.txt 파일을 통해 패키지를 설치
  ```
  $ cd /srv/django-deploy-test/
$ pip3 install -r requirements.txt
  ```
  - runserver 실행
  ```
  - $ python3 manage.py runserver 0:8080
  ```
  - 자신의 퍼블릭 DNS 주소 뒤에 포트 번호를 의미하는 :8080을 붙여 브라우저에 접속
  ```
  http://ec2-15-164-212-231.ap-northeast-2.compute.amazonaws.com:8080/
  ```
  - inbound rules 설정안했으므로 접속이 안된다.
    - WS 로 접속하여 EC2 화면으로 가봅시다.
    - 생성한 인스턴스를 클릭하고 하단에 보면 보안 그룹이라고 있습니다.
    - 그 보안 그룹을 클릭해 주세요.
    - Edit inbound rules를 클릭해주세요.
    - 새로운 8080 포트를 추가해주시고 저장해줍니다.

  - settings.py에 추가되어 있지 않아서 오류 발생한다.
    - 로컬 컴퓨터에 있는 프로젝트의 settings.py에 ALLOWED_HOSTS에 주소를 추가
    ```
    ALLOWED_HOSTS = [
    ".ap-northeast-2.compute.amazonaws.com"
    ]
```
  - 저장하고 github에 업로드합니다. manage.py가 있는 폴더로 이동한 뒤,
  ```
  $ git add .
$ git commit -m "allowed host update"
$ git push origin master
```
  - 서버 컴퓨터로 접속해서 manage.py가 있는 폴더로 가서,
  ```
  $ git pull origin master
  ```

  - 일단 접속은 된다. 그러나 usgi 사용을 해야한다.
  ```
  $ python3 manage.py runserver 0:8080
  ```

  ### uWSGI 서버 연결하기
    - webServer(nginx) --- uWSGI --- Django 구성 필요
    - 가상환경을 활성화 하고 uwsgi 패키지를 설치
    ```
    $ source ~/myvenv/bin/activate
    $ pip3 install uwsgi
    ```
    - uwsgi 서버를 이용해 Django 프로젝트를 연결
    ```
    uwsgi --http :[포트번호] --home [가상환경 경로] --chdir [장고프로젝트폴더 경로] -w [wsgi 모듈이 있는 폴더].wsgi
    ```
      - 포트번호: 8080
      - 가상환경 경로: uwsgi를 설치한 myvenv의 경로입니다. ~/myvenv/ 이지만 홈 폴더를 절대 경로로 지정해 주는 것이 좋습니다. ~는 /home/ubuntu/이니까 /home/ubuntu/myvenv/ 가 가상환경 경로입니다.
      - 장고 프로젝트 폴더 경로: /srv/django-deploy-test/, srv 폴더 내의 각자의 프로젝트 폴더 명을 입력하면 됩니다.
      - wsgi 모듈이 있는 폴더: 프로젝트 폴더에 mysite 안에 wsgi.py가 있을겁니다. 그 경로이기 때문에 mysite를 입력해줍니다.

      ```
      $ uwsgi --http :8080 --home /home/ubuntu/myvenv/ --chdir /srv/django-deploy-test/ -w /여기서 경로 확인 필요/mysite.wsgi
    ```
    - 다음과 같은 내용과 함께 서버가 켜집니다.
    ```
     Operational MODE: single process
    WSGI app 0 (mountpoint='') ready in 1 seconds on interpreter 0x557cd6278b80 pid: 1939 (default app)
     uWSGI is running in multiple interpreter mode ***
    spawned uWSGI worker 1 (and the only) (pid: 1939, cores: 1)
      ```

  - 서버 주소:8080으로 접속을 하면, 성공
  ```
  http://ec2-15-164-212-231.ap-northeast-2.compute.amazonaws.com:8080/
  ```

### 배포를 위한 계정 만들기

  - 서버 컴퓨터 내에 ubuntu 말고 다른 계정을 만들 수 있는데, 배포를 위한 계정을 따로 만드는 것이 좋습니다.
  - - 로컬 컴퓨터로 돌아와서 manage.py가 있는 폴더에서 .config 폴더를 만들고 그 안에 uwsgi 폴더를 만듭니다.버 컴퓨터에서 deploy라는 이름의 계정을 만들고, 비밀번호는 알맞게 쳐주세요
  ```
  $ sudo adduser deploy
  ```

  - 로컬 컴퓨터로 돌아와서 manage.py가 있는 폴더에서 .config 폴더를 만들고 그 안에 uwsgi 폴더를 만듭니다.
  ```
  $ ls
  db.sqlite3       manage.py        requirements.txt
  main             mysite
  $ mkdir .config
  $ cd .config
  $ mkdir uwsgi
  ```
  -  uwsgi 폴더에서 mysite.ini 를 만들고 다음을 추가합니다. 저는 아까 길게 친 uwsgi 명령을 바탕으로 다음과 같이 작성했습니다.

    - .config/uwsgi/mysite.ini

```
    [uwsgi]
    chdir = /srv/django-deploy-test/
    module = mysite.wsgi:application
    home = /home/ubuntu/myvenv/

    uid = deploy
    gid = deploy

    http = :8080

    enable-threads = true
    master = true
    vacuum = true
    pidfile = /tmp/mysite.pid
    logto = /var/log/uwsgi/mysite/@(exec://date +%%Y-%%m-%%d).log
    log-reopen = true
```
    - chdir: 장고 프로젝트 폴더의 경로. 아까 uwsgi 명령어를 칠 때 chdir 다음에 왔던 경로와 동일합니다.
    - modeule: 아까 입력했던 -w 옵션 뒤의 값과 같으나 뒤에 :application을 붙여주세요.
    - home: 아까 입력했던 가상환경의 경로와 동일합니다.
    - uid: uwsgi를 사용할 계정입니다. 아까 만들어 둔 배포용 계정 deploy를 입력해주세요.
    - gid: uwsgi를 사용할 그룹입니다. 아까 만들어 둔 배포용 계정 deploy를 입력해주세요.
    - http: 사용할 포트 번호이고
    - logto: uwsgi 서버의 로그를 저장할 폴더입니다.

  - github에 올리신 뒤에 서버 컴퓨터에 돌아가서 다시 git pull 하여 변경 사항(mysite.ini 추가)을 업데이트

  - 먼저 logto 경로에 폴더 (/var/log/uwsgi/mysite/)가 없기 때문에 만들어주어야 합니다.

  ```
  $ sudo mkdir -p /var/log/uwsgi/mysite
  ```
  - 이 로그는 uwsgi 실행자인 deploy의 소유여야 로그를 작성할 수 있습니다. 만든 로그 폴더 전체를 deploy의 소유로 변경
  ```
  $ sudo chown -R deploy:deploy /var/log/uwsgi/mysite/
  ```
  - mysite.ini에 있는 옵션을 이용해 uwsgi 서버를 다시 켜봅니다
  - 관리자 권한으로 실행해야 하기 때문에 ubuntu의 홈 폴더에 있는 가상환경 내의 uwsgi를 직접 실행
  - 설치한 uwsgi는 가상환경 폴더 안의 bin 폴더에 있습니다.

  ```
  $ sudo /home/ubuntu/myvenv/bin/uwsgi -i /srv/django-deploy-test/.config/uwsgi/mysite.ini

  [uWSGI] getting INI configuration from /srv/django-deploy-test/.config/uwsgi/mysite.ini
  ```

  - 서버 컴퓨터의 8080 포트로 접속하시면 정상적으로 작동함을 확인할 수 있습니다.
  - 오류 내용을 확인하고 싶을 때는 다음과 같이 로그 폴더를 관리자 권한으로 확인
  ```
  sudo cat /var/log/uwsgi/mysite/2020-03-15.log
  ```

## nginx 와 uwsgi를 연결하기

### 먼저 서버 컴퓨터에서 nginx를 설치

  ```
  $ sudo apt-get install nginx
  ```
  - 배포를 위한 계정인 deploy를 만들었습니다. 따라서, nginx의 설정 파일에서 nginx를 사용하는 유저가 deploy임을 알려줍니다.

  ```
  $ sudo vi /etc/nginx/nginx.conf
  ```
  -  수정 모드로 바꾼 뒤 첫 줄에 www-data로 되어 있는 user를 deploy로 아래와 같이 수정, !WQ 저- 구조

  ```  
   user deploy;
   worker_processes auto;
   pid /run/nginx.pid;
   include /etc/nginx/modules-enabled/*.conf;
   events {
           worker_connections 768;
           # multi_accept on;
   }
   http {

           ##
           # Basic Settings
           ##
   .... 중략
  ```
  - 구조
  .config
    ├── nginx

    │   └── mysite.conf
    └── uwsgi
    │   └── mysite.ini

  - config/mysite.conf
  ```
  server {
    listen 80;
    server_name *.compute.amazonaws.com;
    charset utf-8;
    client_max_body_size 128M;
    location / {
        uwsgi_pass  unix:///tmp/mysite.sock;
        include     uwsgi_params;
    }
}
  ```
    - listen: 요청을 받을 포트 번호를 의미합니다. 80 포트가 http 기본 포트로 여겨집니다.
    - server_name: 요청을 받을 서버 주소를 의미합니다. 어디서 많이 봤죠? settings.py의 ALLOWED_HOSTS 변수에 추가한 적이 있습니다.
    - location / { }: "server_name/" 식의 요청이 들어올 경우, 처리할 내용에 대해서 정의합니다. location /static/ {} 의 경우엔 "server_name/static/" 주소 요청이 올 경우를 뜻하겠죠?

  -
엇 포트가 80포트로 변경되었네요. 우선 .config/uwsgi/mysite.ini 파일에는 8080포트로 되어 있는데 이 부분을 먼저 수정해주어야 할 것 같습니다. (http = :8080이 삭제되고 그 자리에 소켓 정보와 소유자, 권한을 서술한 세 줄이 추가 됩니다.)
  - .config/uwsgi/mysite.ini
  ```
  [uwsgi]
  chdir = /srv/django-deploy-test/
  module = mysite.wsgi:application
  home = /home/ubuntu/myvenv/
  uid = deploy
  gid = deploy
  socket = /tmp/mysite.sock
  chmod-socket = 666
  chown-socket = deploy:deploy
  enable-threads = true
  master = true
  vacuum = true
  pidfile = /tmp/mysite.pid
  logto = /var/log/uwsgi/mysite/@(exec://date +%%Y-%%m-%%d).log
  log-reopen = true
  ```

  - 로컬 컴퓨터의 프로젝트 폴더의 .config 폴더의 uwsgi 폴더안에 uwsgi.service 파일을 만들어 다음과 같이 입력해주고 저장
  ```
  [Unit]
  Description=uWSGI service
  After=syslog.target
  [Service]
  ExecStart=/home/ubuntu/myvenv/bin/uwsgi -i /srv/django-deploy-test/.config/uwsgi/mysite.ini
  Restart=always
  KillSignal=SIGQUIT
  Type=notify
  StandardError=syslog
  NotifyAccess=all
  [Install]
  WantedBy=multi-user.target
  ```
  - ExecStart에 있는 값을 어디서 많이 보지 않았나요? 이전 포스트에서 uwsgi를 관리자 권한으로 실행할 때의 명령어입니다. 이걸 service 로 등록하여 백그라운드에 계속 실행하게 할 거에요.
  - 프로젝트 내의 파일들이 변경되었으니 다시 github으로 git push 한 뒤,
  - 서버 컴퓨터에서 git pull 합니다. git pull과 push는 모두 manage.py가 있는 폴더에서 진행함을 잊지 말아주세요.
  - 먼저 uwsgi.service 파일을 데몬(백그라운드에 실행)에 등록해줍니다. 이 파일을 /etc/systemd/system/ 에 링크를 걸어줍니다
  ```
  $ sudo ln -f /srv/django-deploy-test/.config/uwsgi/uwsgi.service /etc/systemd/system/uwsgi.service
  ```
  - 데몬을 새로고침 해주고,
  ```
  $ sudo systemctl daemon-reload
  ```
  - uwsgi 서비스를 사용 가능하게 변경해주고 restart 한 번 해줍니다.
  ```
  $ sudo systemctl enable uwsgi
  $ sudo systemctl restart uwsgi
  ```
  - 또한, Django 프로젝트 내의 nginx 설정 파일을 nginx 어플리케이션에 등록해 주어야 합니다. cp 명령어를 이용해 등록하는 경로(sites-available)로 파일을 복사해줍니다.
  ```
  $ sudo cp -f /srv/django-deploy-test/.config/nginx/mysite.conf /etc/nginx/sites-available/mysite.conf
  ```
  - sites-available에 복사된 설정 파일을 sites-enables폴더 안에서도 링크해줍니다.
  ```
  $ sudo ln -sf /etc/nginx/sites-available/mysite.conf /etc/nginx/sites-enabled/mysite.conf
  ```
  - sites-enables폴더 안의 default 파일을 삭제해줍니다.
  ```
  $ sudo rm /etc/nginx/sites-enabled/default
  ```
  - 이제, 다시 데몬을 새로 고침 해주고 nginx와 uwsgi를 다시 실행해 줍니다.

  ```
  $ sudo systemctl daemon-reload
  $ sudo systemctl restart uwsgi nginx
  ```
  - 마지막으로 AWS에 들어가서 지금까지 등록하지 않았던 80번 포트를 열어줍니다. 그리고 저장해줍니다.
    - Eidt inbound rules
  - 이제 다 됐습니다! EC2 인스턴스의 퍼블릭 DNS 주소로 포트 번호 없이 접속해 봅니다.
  ```
  http://ec2-15-164-212-231.ap-northeast-2.compute.amazonaws.com/
  ```

### static 파일 연결해주기

  - 이건 우리가 보던 admin 페이지의 모습이 아닙니다. 보아하니, html을 꾸며주는 css, js 파일들(정적 파일이라 하여 static 파일이라고 불립니다.)을 로드하지 못하는 것 같군요. 문제는 static 파일의 경로가 nginx에서 설정되어 있지 않기 때문에 발생합니다. static 파일들은 Django 프로젝트 내에 앱 별로 구분되어 놓여있는 경우가 대부분이기 때문에, 이 static 파일들을 하나의 경로로 먼저 모아둘 필요가 있습니다. 이를 쉽게 해주는 명령어는 python3 manage.py collectstatic이에요. 먼저, 이 명령어를 사용하려면 settings.py에 static 파일이 모이는 경로를 설정해 주어야 합니다.

  - 로컬 컴퓨터에서 settings.py 파일의 제일 하단 STATIC_URL 밑에 아래 값을 추가합니다.
  ```
  STATIC_ROOT = os.path.join(BASE_DIR, 'static')
  ```
  - STATIC_ROOT 값을 추가한 뒤에 collectstatic 명령어를 사용하면 STATIC_ROOT의 경로에 각 앱의 static 파일들이 모아집니다. 위의 값은 프로젝트 폴더 안에 static 폴더를 만들어 그곳에 모이게 해두게 됩니다. (BASE_DIR이 프로젝트 폴더의 절대 경로를 의미합니다.)
  - 그럼 변경 사항을 git push 하고 서버 컴퓨터에서 pull 합니다. (이제 git push pull 명령어는 생략할게요!) 그 후, 서버 컴퓨터의 manage.py가 있는 폴더에 가서 아래 명령어를 칩니다. 그러면 현재 폴더에 static 폴더가 생기고,
  ```
  $ python3 manage.py collectstatic
  130 static files copied to '/srv/django-deploy-test/static'.
  $ ls
  db.sqlite3  main  manage.py  mysite  requirements.txt  static
  ```
  - 다음과 같이 admin폴더를 포함한 static 파일들이 모인 것을 볼 수 있습니다.

        static
      └── admin
        ├── css
        ├── fonts
        ├── img
        └── js


  - mysite.conf 로 설정한 우리의 nginx는 현재 static 파일들이 어디에 있는지 알 수 없습니다. 다시 로컬 컴퓨터로 돌아와서 mysite.conf 파일에서 /static/ 요청시 파일의 경로를 알려줍니다.
  - .config/nginx/mysite.conf
  ```
  server {
    listen 80;
    server_name *.compute.amazonaws.com;
    charset utf-8;
    client_max_body_size 128M;
    location / {
        uwsgi_pass  unix:///tmp/mysite.sock;
        include     uwsgi_params;
    }
    location /static/ {
        alias /srv/django-deploy-test/static/;
      }
  }
  ```
  - 그러면 이제 css, js 등 static 파일의 요청이 있을 경우 프로젝트 폴더의 static 폴더를 찾아 적절히 response 해줄 수 있을겁니다.
  - 수정 사항을 git으로 서버 컴퓨터에 옮겨주세요.
  - 이제 mysite.conf 파일을 다시 nginx에 등록해 주어야 합니다. mysite.conf 파일이 수정되었으니까요. 위에서 처럼 다시 nginx에 등록하기 위한 명령어를 입력해줍시다.
  ```
  $ sudo cp -f /srv/django-deploy-test/.config/nginx/mysite.conf /etc/nginx/sites-available/mysite.conf
  $ sudo ln -sf /etc/nginx/sites-available/mysite.conf /etc/nginx/sites-enabled/mysite.conf
  ````
  - nginx, uwsgi를 다시 껐다 켜줍니다.
  ```
  http://ec2-15-164-212-231.ap-northeast-2.compute.amazonaws.com/admin/
  ```


## 도메인 연결하기

### 가비아 도메인 등록
### AWS Route 53으로 도메인 등록하기
  - 구매한 도메인을 Route 53을 통해 만든 EC2 인스턴스와 연결해 주어야 합니다.
  - 먼저 EC2 콘솔에 들어가셔서 등록하고자 하는 인스턴스의 IP 주소를 따로 메모장에 기록해두세요.
  - 좌측 상단에 서비스 탭을 클릭하여 Route 53을 검색하여 들어가줍니다.
  - 좌측 메뉴에서 호스팅 영역으로 들어가 준 뒤, 호스팅 영역 생성을 선택하면 우측에 창이 뜨는데요,
  - 아래의 사진처럼 도메인 이름에 구매한 도메인 이름을 입력해줍니다.
  - 설명은 자유롭게 적어주시고, 유형은 그대로 둬주세요!
  - 입력 후에 생성 눌러주세요.

#### 레코드 세트 생성
  - 그 후 레코드 세트 생성을 클릭해주세요. 이름에는 연결하고 싶은 주소를 입력해주시면 되는데, 비워두시면 nerogarret.shop 주소로 연결이 되고 www를 붙여 연결하고 싶으시면 이름에 www를 입력하시면 됩니다.
  - 혹은 두 개 모두 연결하고 싶으시면 레코드 세트를 두 개 만드셔서 하나는 이름을 비우고 하나는 www를 넣고 만드시면 돼요! 저는 비워두고 생성하겠습니다.
  - 그리고 아래 값 부분에 아까 기록해둔 EC2 인스턴스의 IP를 입력해주세요. 그러면 이름의 주소에 그 인스턴스를 연결하겠다는 뜻이 됩니다.

  - 그러면 다음과 같이 레코드 세트가 총 3개가 됩니다.
  - 이제 네임 서버를 변경해주어야 합니다.
  - 유형이 NS인 레코드를 선택하시면 총 4개의 값이 들어가 있는 것을 확인할 수가 있는데요,
  - 이 네임서버들을 가비아에 있는 여러분이 구매한 도메인의 네임서버로 바꿔주시면 됩니다. 우선 이 창을 띄워둡시다

### 가비아 설정

    - 가비아 페이지로 돌아가서 My가비아를 클릭하면 도메인 목록을 볼 수 있었죠?
    - 구매한 도메인의 관리툴에 들어가주시면 하단에 네임서버 설정하는 곳이 있을 거에요.
    -  여기서 설정을 눌러주세요. (안전 잠금 신청하셨으면 해지해 주세요.)

    - 그러면 1~4차 네임 서버 정보가 있습니다. 여기에 위 AWS 화면에 있는 4개의 네임 서버 주소를 위에서부터 차례로 1~4차 네임 서버에 넣어주세요. 이렇게 설정이 되면 됩니다.
    - 하지만, 아직 구매한 주소로 들어가면 접속이 안됩니다. nginx 설정을 바꿔주어야 해요!

## nginx한테 바꾼 도메인 알려주기

  - 이제 nginx와 django한테 도메인이 추가되었음을 알려주어야 해요. 로컬 컴퓨터에서 작업을 하고 올려주도록 해봅시다.
  - 먼저, `settings.py`에서 `ALLOWED_HOSTS`에 도메인(nerogarret.shop)을 추가해 줄게요.
  ```
  ALLOWED_HOSTS = [
    ".ap-northeast-2.compute.amazonaws.com",
    ".nerogarret.shop",
]
```


  - 그리고 `.config/nginx/mysite.conf` 에서 `server_name`에 도메인을 추가해줄게요.
  ```
  server {
      listen 80;
      server_name *.compute.amazonaws.com *.nerogarret.shop;
      charset utf-8;
      client_max_body_size 128M;
      location / {
          uwsgi_pass  unix:///tmp/mysite.sock;
          include     uwsgi_params;
      }
    location /static/ {
          alias /srv/django-deploy-test/static/;
      }
  }
  ```
  - 그 다음 `git push`, `pull`을 통해 서버 컴퓨터에 업로드 해주세요. 그리고 `mysite.conf` 파일이 수정되었으니, nginx에 다시 등록 해줍니다.

  ```
  $ sudo cp -f /srv/django-deploy-test/.config/nginx/mysite.conf /etc/nginx/sites-available/mysite.conf
$ sudo ln -sf /etc/nginx/sites-available/mysite.conf /etc/nginx/sites-enabled/mysite.conf
  ```

  - 그리고 nginx, uwsgi를 껐다 켜줄게요.
  ```
  $ sudo systemctl daemon-reload && sudo systemctl restart nginx uwsgi
  ```






1) 서버접속 (도메인 주소 변경됨, 확인 필요)
ssh -i ~/.ssh/deploy_test.pem ubuntu@ec2-13-125-246-100.ap-northeast-2.compute.amazonaws.com

2) 가상환경 실행
source myvenv/bin/activate


3) 
cd /srv/panabara/

4)
git pull origin master


* conf 설정 변경되었을 때만...
$ sudo cp -f /srv/panabara/.config/nginx/mysite.conf /etc/nginx/sites-available/mysite.conf
$ sudo ln -sf /etc/nginx/sites-available/mysite.conf /etc/nginx/sites-enabled/mysite.conf
 
 아래 케이스일때,
error: Your local changes to the following files would be overwritten by merge:
        db.sqlite3
=> git stash && git pull origin master && git stash pop

=> git status

=> git add .



 DB readonly 일 떄 권한 주기
(myvenv) ubuntu@ip-172-31-33-127:/srv/panabara$ sudo chown -R deploy /srv/panabara
(myvenv) ubuntu@ip-172-31-33-127:/srv/panabara$ sudo chown -R deploy /srv/panabara/db.sqlite3

그리고 nginx, uwsgi를 껐다 켜줄게요.

$ sudo systemctl daemon-reload && sudo systemctl restart nginx uwsgi

# log
  - nginx : grep -i "504" /var/log/nginx/access.log

  - tail -f /var/log/nginx/access.log