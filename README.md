# Grafana Monitoring Stack

Docker 컨테이너 및 시스템 리소스 모니터링을 위한 Grafana 스택

## 구성 요소

| 서비스 | 포트 | 설명 |
|--------|------|------|
| Grafana | 3001 | 대시보드 시각화 |
| Prometheus | 9091 | 메트릭 수집/저장 |
| cAdvisor | - | Docker 컨테이너 메트릭 |
| Node Exporter | - | 호스트 디스크 메트릭 |
| AMD GPU Exporter | 9101 | AMD GPU 메트릭 |

## 빠른 시작

```bash
# 1. 레포 클론
git clone https://github.com/fkid009/grafana-server.git
cd grafana-server

# 2. 환경 변수 설정
cp .env.example .env
# .env 파일 수정

# 3. 실행
docker compose up -d
```

## 환경 변수

| 변수 | 설명 | 기본값 |
|------|------|--------|
| GRAFANA_ADMIN_PASSWORD | Grafana 관리자 비밀번호 | admin |
| MONITOR_DOMAIN | Grafana 외부 도메인 | - |

## 대시보드

### Docker Containers
- CPU 사용량 (시계열 + 도넛 차트 + 게이지)
- Memory 사용량 (시계열 + 도넛 차트 + 게이지)
- Network I/O (RX/TX)
- Disk 사용량 (시계열 + 용량 stat + 게이지)
- GPU 사용량 (AMD Renoir)

## 명령어

```bash
# 시작
docker compose up -d

# 중지
docker compose down

# 로그 확인
docker compose logs -f grafana

# 재시작
docker compose restart
```

## 파일 구조

```
grafana-server/
├── docker-compose.yml
├── .env.example
├── grafana/
│   ├── grafana.ini           # Grafana 설정
│   ├── datasources.yml       # 데이터 소스 (Prometheus)
│   ├── dashboards.yml        # 대시보드 프로비저닝
│   └── dashboards/
│       └── docker.json       # Docker 모니터링 대시보드
├── prometheus/
│   └── prometheus.yml        # Prometheus 스크랩 설정
└── amd-gpu-exporter/
    ├── Dockerfile
    └── exporter.py           # AMD GPU 메트릭 수집
```
