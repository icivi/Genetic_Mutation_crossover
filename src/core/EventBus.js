import EventEmitter from 'eventemitter3';

export class EventBus extends EventEmitter {
  constructor() {
    super();
    this.messageLog = [];
  }

  emit(event, data) {
    this.messageLog.push({ event, data, timestamp: Date.now() });
    super.emit(event, data);
  }

  getRecentEvents(count = 10) {
    return this.messageLog.slice(-count);
  }
}