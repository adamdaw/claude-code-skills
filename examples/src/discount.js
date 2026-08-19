// The worked example from mutation-testing.md: a cap that the suite executes
// and verifies nothing about. Deliberately paired with thin tests.
export function applyDiscount(amount, pct) {
  if (pct > 50) {
    pct = 50;
  }
  return amount - (amount * pct) / 100;
}
