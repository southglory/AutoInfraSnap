from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
from . import collector

app = FastAPI(title="AutoInfraSnap API", description="시스템 상태 모니터링 API", version="0.1.0")


@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.get("/api/system")
def get_system_info():
    try:
        info = collector.collect_system_info()
        return JSONResponse(content=info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metrics/cpu")
def get_cpu_metrics():
    try:
        info = collector.collect_system_info()
        return JSONResponse(content=info["cpu"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metrics/memory")
def get_memory_metrics():
    try:
        info = collector.collect_system_info()
        return JSONResponse(content=info["memory"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metrics/disk")
def get_disk_metrics():
    try:
        info = collector.collect_system_info()
        return JSONResponse(content=info["disk"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/docker/containers")
def get_docker_info():
    try:
        info = collector.collect_system_info()
        return JSONResponse(content=info["docker"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
