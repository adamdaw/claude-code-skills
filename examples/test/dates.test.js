import test from 'node:test';
import assert from 'node:assert/strict';
import { clampDayOfMonth } from '../src/dates.js';

test('leaves a day inside the range untouched', () => {
  assert.equal(clampDayOfMonth(15), 15, 'mid-month day is unchanged');
});

test('clamps a day past the end of the month', () => {
  assert.equal(clampDayOfMonth(40), 31, 'day 40 clamps to 31');
});

test('clamps a day below the first', () => {
  assert.equal(clampDayOfMonth(0), 1, 'day 0 clamps to 1');
});

test('leaves the upper bound untouched', () => {
  assert.equal(clampDayOfMonth(31), 31, 'day 31 is already valid');
});

test('leaves the lower bound untouched', () => {
  assert.equal(clampDayOfMonth(1), 1, 'day 1 is already valid');
});
