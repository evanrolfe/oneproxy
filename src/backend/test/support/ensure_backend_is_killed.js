const ensureBackendIsKilled = (backendPId) => {
  const events = [
    `SIGINT`,
    `SIGUSR1`,
    `SIGUSR2`,
    `uncaughtException`,
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

  process.on('exit', () => {
    console.log(`[Test] Closing backend PID: ${backendPId}`);

    process.kill(-backendPId);
  });
};

module.exports = { ensureBackendIsKilled };
