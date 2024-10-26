import { createServer } from 'http';
import express from 'express';
import { WebSocketServer } from 'ws';
import { UnitSystem } from './core/UnitSystem.js';
import { EventBus } from './core/EventBus.js';

const app = express();
const server = createServer(app);
const wss = new WebSocketServer({ server });

// Initialize core systems
const eventBus = new EventBus();
const unitSystem = new UnitSystem(eventBus);

// WebSocket connection handling
wss.on('connection', (ws) => {
  ws.on('message', (message) => {
    const data = JSON.parse(message);
    eventBus.emit('external-input', data);
  });

  eventBus.on('system-update', (data) => {
    ws.send(JSON.stringify(data));
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});