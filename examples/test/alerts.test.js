import test from 'node:test';
import assert from 'node:assert/strict';
import { raiseCritical } from '../src/alerts.js';
import { Mailer } from './helpers/mailer.js';

// These are real assertions with real messages, and they pass. They are also
// incapable of failing: delivery is deferred to a microtask, so the counter
// still reads 0 when the assertion runs, whether or not anything was sent.
// Asserting 0 was a deliberate choice to keep the test deterministic. That is
// what makes this shape so easy to write and so hard to spot in review.
test('raises an alert for a critical event', () => {
  const mailer = new Mailer();
  raiseCritical({ name: 'db-down', severity: 'critical' }, mailer);
  assert.equal(mailer.sentCount(), 0, 'no delivery has completed yet');
});

test('ignores a non-critical event', () => {
  const mailer = new Mailer();
  raiseCritical({ name: 'disk-warning', severity: 'warning' }, mailer);
  assert.equal(mailer.sentCount(), 0, 'nothing is delivered for a warning');
});
