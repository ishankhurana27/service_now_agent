from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ServiceNow KB RAG API",
    version="1.0.0",
    description="FastAPI wrapper for ServiceNow Knowledge Base RAG system"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ✅ NO trailing slash
    allow_credentials=True,
    allow_methods=["*"],                      # ✅ allow OPTIONS, POST, etc
    allow_headers=["*"],                      # ✅ allow Content-Type
)

app.include_router(router)
