from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from firebase_admin import credentials
import firebase_admin

load_dotenv()

cred_app = credentials.Certificate("app/auth/firebase_app.json")
firebase_admin.initialize_app(cred_app, name="app")

cred_pos = credentials.Certificate("app/auth/firebase_pos.json")
firebase_admin.initialize_app(cred_pos, name="pos")

from app.routes.app.cart import app_router
from app.routes.pos import pos_router
from app.routes.health import router as health_router
from app.middlewares.firebase_auth_app import FirebaseAuthMiddlewareAPP
from app.middlewares.firebase_auth_pos import FirebaseAuthMiddlewarePOS

app = FastAPI(title="Rozana Cart Service", version="1.0.0")

allowed_origins = os.getenv("ALLOWED_ORIGINS")
if allowed_origins:
   origins = [origin.strip() for origin in allowed_origins.split(",")]
else:
   origins = ["*"]

app.add_middleware(FirebaseAuthMiddlewareAPP)
app.add_middleware(FirebaseAuthMiddlewarePOS)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(app_router, prefix="/app/v1")
app.include_router(pos_router, prefix="/pos/v1")
app.include_router(health_router)


