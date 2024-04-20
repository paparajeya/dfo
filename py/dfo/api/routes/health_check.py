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
from starlette import status
from starlette.responses import HTMLResponse

from core.logger import logger

router = APIRouter()


@router.get("", name="Api health check", status_code=status.HTTP_200_OK)
def get_info():
    logger.info("PING")

    return HTMLResponse("PONG", status_code=status.HTTP_200_OK)
