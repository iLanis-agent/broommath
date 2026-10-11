const E = require('./engine.js');
const cases = require('./expected.json');
const fns = { sweepPlan: E.sweepPlan, weekPlan: E.weekPlan, headPlan: E.headPlan };
const renders = {
  sweepPlan: (r, a) => E.renderSweep(r),
  weekPlan: (r, a) => E.renderWeek(r, a[0], a[2]),
  headPlan: (r, a) => E.renderHead(r, a[0])
};
let checks = 0, failed = 0;
for (const c of cases) {
  const got = fns[c.fn](...c.args);
  for (const k of Object.keys(c.result)) {
    checks++;
    if (got[k] !== c.result[k]) { failed++; console.log('FAIL', c.fn, c.args, k, 'expected', c.result[k], 'got', got[k]); }
  }
  if (c.render !== undefined) {
    checks++;
    const g = renders[c.fn](got, c.args);
    if (g !== c.render) { failed++; console.log('FAIL render', c.fn, c.args, '\n exp:', c.render, '\n got:', g); }
  }
}
console.log(cases.length + ' cases, ' + checks + ' checks ' + (failed ? failed + ' FAILED' : 'green'));
process.exit(failed ? 1 : 0);
