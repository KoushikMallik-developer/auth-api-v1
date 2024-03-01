import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from core.db import Base, engine
from users.routes import user_router

app = FastAPI(debug=True, title="Auth API V1", version="0.1.0")
app.include_router(router=user_router)
Base.metadata.create_all(bind=engine)


@app.get("/")
def health_check():
    return JSONResponse(content={"status": "Running"})


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
