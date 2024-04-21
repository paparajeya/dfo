# -*- coding: utf-8 -*-
"""
@Author     : Dr Prashant Aparajeya
                Founder & Director @AISimply Ltd
                Computer Vision Scientist
                London, United Kingdom
                
@Copyright  : Copyright 2024 - present
@Project    : Dispersive Flies Optimization (DFO) Algorithm
"""

import asyncio
import json

from fastapi import WebSocket
from fastapi.param_functions import Header

from core.logger import logger
from core.router import APIRouter
from services.websocket import ws_manager

router = APIRouter()

@router.get("/", name="Session Index Page")
async def get(session_id: str = Header(None, convert_underscores=True)):
    if ws_manager.is_connected(session_id):
        return {"message": f"Welcome to the DFO algorithm session: {session_id}!"}
    return {"message": f"Session '{session_id}' doesn't exists. Please connect to the WebSocket endpoint to start the session."}

# WebSocket endpoint
@router.websocket("/ws")
async def websocket_chatpoint(websocket: WebSocket):
    
    # Accept the connection from the client
    session_id = await ws_manager.connect(websocket)
    
    try:        
        while True:
            # Receive the first connection message from the client
            data = await ws_manager.get_message(session_id)
            logger.info(f"Received message from session: {session_id} - {data}")
            
            if type(data) == bytes:
                data = data.decode("utf-8")
            if type(data) == str:
                json_data = json.loads(data)
            else:
                json_data = data
            
            if json_data.get("type") == "getId":
                # Send the message to the client
                message = {
                    "type": "getId",
                    "message": f"Message received: {json_data.get('data')}",
                    "token": session_id
                }
            else:
                message = {
                    "type": "error",
                    "message ": "Invalid message type",
                    "token": session_id
                }
            await ws_manager.send_message(session_id, message)
            
            # This one won't receive any message for client and we would like to keep the connection alive
            await asyncio.sleep(1)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        # Disconnect the client
        await ws_manager.disconnect(session_id)
        logger.info(f"Connection closed for session: {session_id}")