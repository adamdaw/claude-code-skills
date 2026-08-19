// The "a score below 100 is not a defect list" example: thoroughly tested, and
// what survives is an equivalent mutant rather than a gap.
export function clampDayOfMonth(day) {
  if (day > 31) {
    day = 31;
  }
  if (day < 1) {
    day = 1;
  }
  return day;
}
