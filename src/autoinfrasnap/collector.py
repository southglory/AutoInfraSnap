import psutil
import docker
import json
from datetime import datetime


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
        info["docker"] = {"error": str(e)}

    return info


def save_report(info, filename=None):
    """수집된 정보를 JSON 파일로 저장"""
    if filename is None:
        filename = f"infra_snap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    return filename
