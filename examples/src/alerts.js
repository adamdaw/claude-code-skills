// The "a suite can assert, pass, and still detect nothing" example. Delivery is
// deferred past the end of the synchronous test, which is what makes the
// assertion in test/alerts.test.js incapable of failing.
export function raiseCritical(event, mailer) {
  if (event.severity !== 'critical') {
    return false;
  }
  queueMicrotask(() => mailer.send(`ALERT: ${event.name}`));
  return true;
}
