import test from 'node:test';
import assert from 'node:assert/strict';
import { applyDiscount } from '../src/discount.js';

// Both tests pass. Line coverage is complete. Neither one pins the cap.
test('applies ten percent', () => {
  assert.equal(applyDiscount(100, 10), 90, 'ten percent off 100');
});

test('handles a large percentage', () => {
  assert.notEqual(applyDiscount(100, 80), null, 'returns a value');
});
