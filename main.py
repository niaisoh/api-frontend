import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.router:app", port=8443, log_level="info")