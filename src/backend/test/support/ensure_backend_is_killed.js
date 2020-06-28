const ensureBackendIsKilled = (backendPId) => {
  const events = [
    `SIGINT`,
    `SIGUSR1`,
    `SIGUSR2`,
    `SIGTERM`,
    `SIGHUP`
  ];

  for (let i = 0; i < events.length; i++) {
    const eventType = events[i];
    process.on(eventType, () => {
      console.log(`[Test] received event: ${eventType}`);
      process.exit(1);
    });
  }

  process.on('uncaughtException', (err, origin) => {
    console.log(`[Test] received event: uncaughtException`);
    console.log(err);
    console.log(origin);
    process.exit(1);
  });

  process.on('exit', () => {
    console.log(`[Test] Closing backend PID: ${backendPId}`);

    try {
      process.kill(-backendPId);
    } catch(err) {
      console.log(`[Test] Backend already closed.`)
    }
  });
};

module.exports = { ensureBackendIsKilled };
