// import { ipcRenderer } from 'electron';
const { IPC } = require('node-ipc');
const uuid = require('uuid');

const ipc = new IPC();

class IPCClient {
  constructor(socketId) {
    this.replyHandlers = new Map();
    this.listeners = new Map();
    this.messageQueue = [];
    this.socketClient = null;
    this.socketId = socketId;
  }

  async connect() {
    this.ipcConnect = (id, func) => {
      ipc.config.silent = true;
      ipc.connectTo(id, () => {
        func(ipc.of[id]);
      });
    };

    this.uuid = uuid;

    return new Promise((resolve) => {
      this.connectSocket(this.socketId, () => {
        console.log('[IPC Client] Connected!');
        resolve();
      });
    });
  }

  connectSocket(name, onOpen) {
    this.ipcConnect(name, client => {
      client.on('message', data => {
        const response = JSON.parse(data);
        if (response.type === 'reply' || response.type === 'error') {
          const diffTime = Date.now() - parseInt(response.sentAt);
          //console.log(`[IPC Client] received response from backend in ${diffTime}ms, ${data}`);
          const { id } = response;
          const handler = this.replyHandlers.get(id);
          if (handler) {
            this.replyHandlers.delete(id);

            delete response.id;
            handler.resolve(response.body);
          }
        } else if (response.type === 'push') {
          const args = response.args;
          const listenerName = response.name;

          const listeners = this.listeners.get(listenerName);
          if (listeners) {
            listeners.forEach(listener => {
              listener(args);
            });
          }
        } else {
          throw new Error(`Unknown message type: ${JSON.stringify(response)}`);
        }
      });

      client.on('connect', () => {
        this.socketClient = client;

        // Send any messages that were queued while closed
        if (this.messageQueue.length > 0) {
          this.messageQueue.forEach(msg => client.emit('message', msg));
          this.messageQueue = [];
        }

        console.log(`[IPC Client] connected on socket: ${name}`);
        onOpen();
      });

      client.on('disconnect', () => {
        this.socketClient = null;
      });
    });
  }

  disconnect() {
    ipc.disconnect(this.socketId);
  }

  send(message) {
    return new Promise((resolve, reject) => {
      const id = this.uuid.v4();
      const sentAt = Date.now();
      this.replyHandlers.set(id, { resolve, reject });
      if (this.socketClient) {
        this.socketClient.emit(
          'message',
          JSON.stringify({ id, sentAt, message })
        );
      } else {
        this.messageQueue.push(
          JSON.stringify({ id, sentAt, message })
        );
      }
    });
  }

  listen(name, cb) {
    if (!this.listeners.get(name)) {
      this.listeners.set(name, []);
    }
    this.listeners.get(name).push(cb);

    return () => {
      const arr = this.listeners.get(name);
      this.listeners.set(
        name,
        arr.filter(cb_ => cb_ !== cb)
      );
    };
  }

  unlisten(name) {
    this.listeners.set(name, []);
  }
}

module.exports = { IPCClient };
