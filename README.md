![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fgjbae1212%2Fhit-counter&count_bg=%233D7CC8&title_bg=%236E3131&icon=&icon_color=%23371C41&title=Hits&edge_flat=true)

# KimJW Git Page

### 1. Migration

- DB 데이터를 Migration 하기위한 코드
- (예시) python IrisMigration_JW.py ./migration.conf 실행시 마이그레이션 실행
    -  config 에 정의된 Table 명으로 Directory 생성
- (예시) python IrisMigration_JW.py ./migration.conf {Table명}
    - Table 명은 Table 명으로 된 Directory 명과 일치

### 2. selenium_sms

- 상태체크 모듈 ( 에러, 오류, 상태이상 체크 )
-  (예시) python SMS.py IrisOpenLab Filter SMSSend SMS.conf TEST_SMS
-   Collect 하위의 IrisOpenLab.py 로 점검할 항목 정의
-   Filter 하위의 Fileter.py 로 필터링 작업
-   Noti 하위의 SMSSend 로 Noti 발생
-   SMS.conf 의 config 정보를 읽어옴
-   ./logs/TEST_SMS.log 로 로그 적용

### 3. ETL
- 이벤트 플로우 ( EMS 작업을 받아와서 Parsing, DB Loading 및 Rabbit MQ 적재 )
- (예시) sh ef_start_run.sh
    - SIOEF2 0.0.0.0 30000 /home/tacs/TACS-EF/ETL/conf/SIOEF2/conf/30000_ETL.conf &
