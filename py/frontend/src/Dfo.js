import React, { useState, useEffect } from 'react';

function Dfo() {
    const [messages, setMessages] = useState([]);
    const [socket, setSocket] = useState(null);
    const [socketId, setSocketId] = useState(null);

    useEffect(() => {
        const newSocket = new WebSocket('ws://localhost:5000/api/v1/session/ws');
        setSocket(newSocket);

        return () => {
            newSocket.close(); // Close the socket connection on component unmount
        };
    }, []);

    useEffect(() => {
        if (!socket) return;

        socket.onopen = () => {
            socket.send(JSON.stringify({ type: 'getId', message: 'connected' }));
        };

        // Event listener for incoming messages
        socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            if (message.type === 'getId') {
                setSocketId(message.token);
                console.log(`Socket ID: ${message.token}`);
            } else {
                // Print the message key in the message dictionary
                console.log(message.message);
                setMessages((prevMessages) => [...prevMessages, message.message]);
            }
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