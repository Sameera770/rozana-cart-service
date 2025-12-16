from typing import List, Dict
from fastapi import APIRouter
from pydantic import BaseModel

# Core functions
from app.core.cart_functions import (
    get_available_promotions_core,
    calculate_cart_discount_core,
    get_available_payment_methods_core,
)
from app.dto.cart import (
    PromotionListRequest,
    PromotionListResponse,
    CartDiscountRequest,
    CartDiscountResponse,
    PaymentMethodsRequest,
)

app_router = APIRouter(prefix="/cart", tags=["app-cart"])


@app_router.post("/promotions/available", response_model=List[PromotionListResponse])
async def get_available_promotions(request: PromotionListRequest):  
    """ Get list of available promotions for mobile app channel """
    return await get_available_promotions_core(request, "app")



@app_router.post("/discount/calculate", response_model=CartDiscountResponse)
async def calculate_cart_discount(request: CartDiscountRequest):
    """ Calculate proportional discount for cart items for mobile app channel """
    return await calculate_cart_discount_core(request, "app")


@app_router.post("/payment_methods/available", response_model=Dict[str, List[str]])
async def get_available_payment_methods(request: PaymentMethodsRequest):
    """Return available payment methods for the given user."""
    return {"available_payment_methods": await get_available_payment_methods_core(request.user_id)}

