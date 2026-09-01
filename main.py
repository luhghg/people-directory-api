from fastapi import FastAPI
from app.routers import (auth_router, person_router, auditlog_router)
import uvicorn

app = FastAPI()


app.include_router(auth_router.router)
app.include_router(person_router.router)
app.include_router(auditlog_router.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
