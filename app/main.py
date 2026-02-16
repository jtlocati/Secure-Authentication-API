#Entry point of API, creates the fast API app and includes routes
from fastapi import FastAPI
from app.api.routes.auth import router as auth_router

#Creates FastAPI application
app = FastAPI(title="Secure Auth API")

#includes the /auth/* route to it can be recalled by FastAPI
app.include_router(auth_router)

#checks docker heath.
@app.get("/health")
def health():
    return {"status": "ok"}