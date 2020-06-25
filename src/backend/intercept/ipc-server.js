const { IPC } = require('node-ipc');

/*
 * Response (OK): { type: 'reply', id: '1232', result: { status: 'OK', id: '...' } }
 * Response (INVALID): { type: 'reply', id: '1232', result: { status: 'INVALID', messages: [] } }
 * Response (ERROR): { type: 'error', id: '1232', result: 'ERROR: bla bla bla' }
 */

class IPCServer {
  constructor(socketId) {
    this.socketId = socketId;

    this.ipc = new IPC();
    this.ipc.config.id = this.socketId;
    this.ipc.config.silent = true;
  }

  onMessage(callback) {
    this.onMessage = callback;
  }

  start() {
    console.log(`[IPC Server] starting...`)
    this.ipc.serve(() => {
      this.ipc.server.on('message', (data, socket) => {
        const message = JSON.parse(data);

        try {
          const replyCallback = (body) => this.ipc.server.emit(
            socket,
            'message',
            JSON.stringify({
              type: 'reply',
              id: message.id,
              sentAt: message.sentAt,
              body: body
            })
          );

          this.onMessage(message.message, replyCallback);

        } catch (error) {
          this.ipc.server.emit(
            socket,
            'message',
            JSON.stringify({
              type: 'error',
              id: message.id,
              sentAt: message.sentAt,
              body: error.message
            })
          );
        }
      });
    });

    this.ipc.server.start();
    console.log(`[IPC Server] listening.`)
  }

  broadcast(message) {
    // HACK: Broadcast is not available in test mode
    if (typeof this.ipc.server.broadcast === 'function') {
      this.ipc.server.broadcast(
        'message',
        JSON.stringify({ type: 'push', name: message.name, args: message.args })
      );
    }
  }
}

module.exports = { IPCServer };
