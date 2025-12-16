from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/health")
async def health_check(request: Request):
    details = {
        "status": "healthy",
        "version": "1.0.0",
        "service": "rozana-cart-service"
    }
    return JSONResponse(content=details)
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/health")
async def health_check(request: Request):

    details = {
        "status": "healthy",
        "version": "1.0.0",
        "service": "rozana-cart-service"
    }
    return JSONResponse(content=details)