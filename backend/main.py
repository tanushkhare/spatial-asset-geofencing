from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import terraform_router

app = FastAPI(title="Project 19: Terraform IaC API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(terraform_router.router)

@app.get("/")
def read_root():
    return {"message": "Project 19 Terraform State Manager Backend is online!"}