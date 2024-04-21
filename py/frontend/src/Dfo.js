import React, { useState, useEffect } from 'react';

function Dfo() {
    const [socket, setSocket] = useState(null);
    const [socketId, setSocketId] = useState(null);

    useEffect(() => {
        const ws = new WebSocket('ws://localhost:5000/api/v1/session/ws');
        ws.onopen = () => {
            ws.send(JSON.stringify({ type: 'getId', message: 'connected' }));
        };
        ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            if (message.type === "connection") {
                console.log('connected to server with id: ', message.token);
            }
            else {
                console.log(message);
            }
        };
        ws.onclose = () => {
            console.log('disconnected');
        };

        setSocket(ws);

        return () => {
            ws.close(); // Close the socket connection on component unmount
        };
    }, []);

    useEffect(() => {
        if (!socket) return;

        // Event listener for incoming messages
        socket.onmessage = (event) => {
            const message = event.data;
            // Print the message key in the message dictionary
            console.log(JSON.parse(message).message);
            setMessages((prevMessages) => [...prevMessages, JSON.parse(message).message]);
        };

        return () => {
            socket.onclose = null; // Clear event listener on unmount
        };
    }, [socket]);

    return (
        <div>
            <h1>DFO</h1>
        </div>
    );
}

export default Dfo;