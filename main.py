import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/health-check")
def health_check():
    return JSONResponse(content={"status": "Running"})


@app.get("/")
def home():
    return JSONResponse(content={"status": "Running"})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
