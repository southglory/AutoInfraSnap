# AutoInfraSnap

시스템 상태를 자동으로 수집하고 공유하는 CLI 도구

## 설치 방법

```bash
pip install autoinfrasnap
```

## 사용 방법

1. 시스템 상태 수집 및 리포트 생성:

```bash
autoinfrasnap --report
```

2. S3에 리포트 업로드:

```bash
autoinfrasnap --report --upload
```

## 기능

- CPU, 메모리, 디스크 사용률 모니터링
- Docker 컨테이너 상태 확인
- JSON 형식의 리포트 생성
- AWS S3 자동 업로드

## 요구사항

- Python 3.13 이상
- pip 패키지 관리자
- AWS 자격 증명 (S3 업로드 시)

[![오토인프라 스냅 소개 영상](https://img.youtube.com/vi/3VUKiSjrRP4/0.jpg)](https://youtu.be/3VUKiSjrRP4)
