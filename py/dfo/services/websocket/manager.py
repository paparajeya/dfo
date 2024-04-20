# -*- coding: utf-8 -*-
"""
@Author     : Dr Prashant Aparajeya
                Founder & Director @AISimply Ltd
                Computer Vision Scientist
                London, United Kingdom
                
@Copyright  : Copyright 2024 - present
@Project    : Dispersive Flies Optimization (DFO) Algorithm
"""

import logging
from typing import Dict
from fastapi import WebSocket

logger = logging.getLogger(__name__)

class WebsocketManager:
    def __init__(self):
        self.clients: Dict[str, WebSocket] = {}
        
    async def __get_connection(self, session_id: str):
        try:
            # Get the websocket connection
            websocket = self.clients[session_id]
            return websocket
        except KeyError:
            logger.error(f"User {session_id} not found")
            return None
        
    async def add_client(self, websocket: WebSocket) -> str:
        # Generate a unique identifier for the user
        session_id = str(id(websocket))
        # Add the client to the clients dictionary
        self.clients[session_id] = websocket
        # Return the session_id
        return session_id
        
    async def connect(self, websocket: WebSocket):
        # Accept the WebSocket connection and add the client
        await websocket.accept()
        return await self.add_client(websocket)
    
    async def disconnect(self, session_id: str):
        # Remove the client from the clients dictionary, the Redis cache and close the WebSocket connection
        await self.remove_client(session_id)
        
    async def get_active_sessions(self):
        # Return the list of active sessions
        return list(self.clients.keys())
        
    async def get_message(self, session_id: str) -> str:
        # Get the WebSocket connection
        if websocket := await self.__get_connection(session_id):
            # Receive the message from the WebSocket connection
            return await websocket.receive_text()
        return None
    
    def is_connected(self, session_id: str) -> bool:
        # Check if the session_id is in the clients dictionary
        return session_id in self.clients
        
    async def remove_client(self, session_id: str):
        # Get the WebSocket connection
        if websocket := await self.__get_connection(session_id):
            # Close the WebSocket connection
            try:
                await websocket.close()
            except Exception as e:
                logger.error(f"Error closing WebSocket connection: {e}")
            # Check if the session_id is in the clients dictionary
            try:            
                # Remove the client from the clients dictionary
                del self.clients[session_id]
                logger.info(f"User {session_id} disconnected")
            except KeyError:
                logger.error(f"User {session_id} not found")
        
    async def send_message(self, session_id: str, message: str | Dict | bytes):
        # Get the WebSocket connection
        if websocket := await self.__get_connection(session_id):
            # Send the message to the WebSocket connection
            if type(message) == dict:
                await websocket.send_json(message)
            elif type(message) == bytes:
                await websocket.send_bytes(message)
            else:
                await websocket.send_text(str(message))
        
ws_manager = WebsocketManager()
