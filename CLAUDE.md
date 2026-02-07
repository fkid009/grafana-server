# Grafana Monitoring Stack

Docker 컨테이너 모니터링을 위한 Grafana + Prometheus + cAdvisor 스택

## 구조

```
grafana-server/
├── docker-compose.yml      # 전체 스택 정의
├── grafana/
│   ├── grafana.ini         # Grafana 서버 설정
│   ├── datasources.yml     # Prometheus 데이터 소스
│   ├── dashboards.yml      # 대시보드 프로비저닝
│   └── dashboards/
│       └── docker.json     # Docker 모니터링 대시보드
├── prometheus/
│   └── prometheus.yml      # 스크랩 타겟 설정
└── amd-gpu-exporter/
    ├── Dockerfile
    └── exporter.py         # sysfs에서 AMD GPU 메트릭 수집
```

## 서비스 포트

| 서비스 | 내부 포트 | 외부 포트 |
|--------|-----------|-----------|
| Grafana | 3000 | 3001 |
| Prometheus | 9090 | 9091 |
| cAdvisor | 8080 | - |
| Node Exporter | 9100 | - |
| AMD GPU Exporter | 9101 | 9101 |

## 주요 파일

### docker-compose.yml
- 모든 서비스 정의
- 환경 변수: GRAFANA_ADMIN_PASSWORD, MONITOR_DOMAIN

### grafana/grafana.ini
- 익명 접속 허용 (Viewer 권한)
- Explore, Alerting 비활성화
- 홈 대시보드: docker.json

### prometheus/prometheus.yml
- 스크랩 대상: cadvisor:8080, node-exporter:9100, amd-gpu-exporter:9101
- 글로벌 스크랩 간격: 30초
- node-exporter 스크랩 간격: 60초 (디스크 메트릭은 변화가 느림)

### amd-gpu-exporter/exporter.py
- /sys/class/drm/card0/device/에서 메트릭 수집
- 메트릭: gpu_busy_percent, vram, gtt, temperature

## 대시보드 섹션

1. **CPU**: 시계열, 도넛 차트, 총 사용률 게이지
2. **Memory**: 시계열, 도넛 차트, 총 사용률 게이지
3. **Network**: RX/TX 시계열
4. **Disk**: 사용률 시계열, 용량 stat (Used/Available/Total), 사용률 게이지
5. **GPU**: 사용률, VRAM, 온도

## 명령어

```bash
# 실행
docker compose up -d

# 중지
docker compose down

# 특정 서비스 재시작
docker compose restart grafana

# 로그
docker compose logs -f
```

## 환경 변수

.env 파일에서 관리 (gitignore됨):
- GRAFANA_ADMIN_PASSWORD: Grafana 관리자 비밀번호
- MONITOR_DOMAIN: 외부 접속 도메인 (Cloudflare Tunnel용)
