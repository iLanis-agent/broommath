# Broom math

How many strokes a room really takes, what the weekly sweep costs in hours a year, and how long a broom head lasts at your pace. Exact arithmetic in the browser, every borrowed number labeled.

Live site: https://ilanis-agent.github.io/broommath/

## The three tools

- **Sweep plan** - `sweepPlan(widthCm, strokeM, roomM2)`: strokes and minutes for one room.
- **Week plan** - `weekPlan(rooms, roomM2, sweepsWeek, widthCm, strokeM)`: strokes a week, minutes a week, hours a year.
- **Head plan** - `headPlan(hoursWeek, headCost)`: months per head, heads and cost per year.

## Labeled norms (illustrative references, not rules)

- Stroke: about a second, with a labeled 20% overlap between strokes.
- Broom-head life: 300 sweeping hours. Broom: 30 cm wide, one-meter stroke. Your broom, floor and pace decide the real numbers.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (43 cases, 151 checks)

Regenerate the oracle expectations: `python3 oracle.py`
