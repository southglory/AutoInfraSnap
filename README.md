# AutoInfraSnap

시스템 상태를 자동으로 수집하고 JSON 형식으로 저장하는 CLI 도구

## 설치 방법

1. 가상환경 생성 및 활성화:
```bash
python -m venv .venv
.venv/Scripts/activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

2. 패키지 설치:
```bash
pip install -r requirements.txt
pip install -e .
```

## 사용 방법

1. 시스템 상태 수집 및 리포트 생성:
```bash
autoinfrasnap --report
```

2. 특정 파일명으로 리포트 생성:
```bash
autoinfrasnap --report --output report.json
```

## 수집되는 정보

- CPU
  - 사용률 (%)
  - 코어 수
- 메모리
  - 전체 용량
  - 사용 가능한 용량
  - 사용률 (%)
- 디스크
  - 전체 용량
  - 사용 중인 용량
  - 여유 용량
  - 사용률 (%)
- Docker (설치된 경우)
  - 실행 중인 컨테이너 수
  - 컨테이너 상태 정보

## 요구사항

- Python 3.13 이상
- pip 패키지 관리자

[![오토인프라 스냅 소개 영상](https://img.youtube.com/vi/3VUKiSjrRP4/0.jpg)](https://youtu.be/3VUKiSjrRP4)
