# -*- coding: utf-8 -*-
"""
@Author     : Dr Prashant Aparajeya
                Founder & Director @AISimply Ltd
                Computer Vision Scientist
                London, United Kingdom
                
@Copyright  : Copyright 2024 - present
@Project    : Dispersive Flies Optimization (DFO) Algorithm
"""

from fastapi import APIRouter
from api.routes.health_check import router as health_router
from api.routes.session import router as session_router

# from api.routes import items, login, users, utils

api_router = APIRouter()

api_router.include_router(health_router, tags=["health check"], prefix="/ping")
api_router.include_router(session_router, tags=["session"], prefix="/session")

