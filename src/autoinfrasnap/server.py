import uvicorn
from fastapi import FastAPI, HTTPException
from datetime import datetime
from . import collector

app = FastAPI(title="AutoInfraSnap API", version="1.0.0")


@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.get("/api/system")
async def get_system_info():
    return collector.collect_system_info()


@app.get("/api/metrics/cpu")
async def get_cpu_metrics():
    info = collector.collect_system_info()
    return info["cpu"]


@app.get("/api/metrics/memory")
async def get_memory_metrics():
    info = collector.collect_system_info()
    return info["memory"]


@app.get("/api/metrics/disk")
async def get_disk_metrics():
    info = collector.collect_system_info()
    return info["disk"]


@app.get("/api/docker/containers")
async def get_docker_containers():
    info = collector.collect_system_info()
    return info.get("docker", {"error": "Docker information not available"})


@app.get("/api/reports")
async def list_reports():
    """모든 리포트 목록 조회"""
    return collector.list_reports()


@app.get("/api/report/{filename}")
async def get_report(filename: str):
    """특정 리포트 조회"""
    report = collector.get_report(filename)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@app.post("/api/report/generate")
async def generate_report():
    """새 리포트 생성"""
    return collector.generate_report()


def run_server(host="0.0.0.0", port=8080, reload=True):
    """API 서버 실행"""
    if reload:
        uvicorn.run("autoinfrasnap.server:app", host=host, port=port, reload=reload)
    else:
        uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_server()
