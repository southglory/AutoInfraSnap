import psutil
import docker
import json
import os
from datetime import datetime
from pathlib import Path

# 패키지 루트 디렉토리 기준으로 reports 디렉토리 경로 설정
PACKAGE_ROOT = Path(__file__).parent.parent.parent
REPORTS_DIR = PACKAGE_ROOT / "reports"


def ensure_reports_dir():
    """리포트 저장 디렉토리 생성"""
    try:
        REPORTS_DIR.mkdir(exist_ok=True)
        return True
    except Exception as e:
        print(f"리포트 디렉토리 생성 실패: {e}")
        return False


def collect_system_info():
    """시스템 기본 정보 수집"""
    info = {
        "timestamp": datetime.now().isoformat(),
        "cpu": {"percent": psutil.cpu_percent(interval=1), "count": psutil.cpu_count()},
        "memory": {"total": psutil.virtual_memory().total, "available": psutil.virtual_memory().available, "percent": psutil.virtual_memory().percent},
        "disk": {"total": psutil.disk_usage("/").total, "used": psutil.disk_usage("/").used, "free": psutil.disk_usage("/").free, "percent": psutil.disk_usage("/").percent},
    }

    try:
        client = docker.from_env()
        containers = client.containers.list()
        info["docker"] = {"running_containers": len(containers), "containers": [{"name": c.name, "status": c.status, "image": c.image.tags[0] if c.image.tags else "unknown"} for c in containers]}
    except Exception as e:
        if "CreateFile" in str(e):
            info["docker"] = {"status": "not_running", "message": "Docker가 실행되지 않았습니다. Docker 데몬을 실행해주세요."}
        else:
            info["docker"] = {"status": "error", "message": "Docker 정보를 가져올 수 없습니다."}

    return info


def save_report(info, filename=None):
    """수집된 정보를 JSON 파일로 저장"""
    ensure_reports_dir()

    if filename is None:
        filename = f"infra_snap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    filepath = REPORTS_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    return str(filepath)


def list_reports():
    """저장된 리포트 목록 조회"""
    if not ensure_reports_dir():
        return {"error": "리포트 디렉토리에 접근할 수 없습니다."}

    reports = []
    try:
        for file in REPORTS_DIR.glob("*.json"):
            reports.append({"filename": file.name, "created_at": datetime.fromtimestamp(file.stat().st_mtime).isoformat(), "size": file.stat().st_size})
        return sorted(reports, key=lambda x: x["created_at"], reverse=True)
    except Exception as e:
        return {"error": f"리포트 목록 조회 실패: {e}"}


def get_report(filename):
    """특정 리포트 내용 조회"""
    if not ensure_reports_dir():
        return None

    filepath = REPORTS_DIR / filename
    try:
        if not filepath.exists():
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"리포트 읽기 실패: {e}")
        return None


def generate_report(upload=False, bucket=None, prefix=None):
    """새 리포트 생성"""
    if not ensure_reports_dir():
        return {"error": "리포트 디렉토리에 접근할 수 없습니다."}

    try:
        info = collect_system_info()
        filepath = save_report(info)

        if upload and bucket:
            # TODO: S3 업로드 구현
            pass

        return {"filename": os.path.basename(filepath), "content": info, "path": str(filepath)}
    except Exception as e:
        return {"error": f"리포트 생성 실패: {e}"}
