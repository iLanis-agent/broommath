#!/usr/bin/env python3
"""Python mirror of engine.js - regenerates expected.json. Exact float-for-float mirror."""
import json, math, os

OVERLAP = 0.8
HEAD_HOURS = 300

def r1(x): return math.floor(x * 10 + 0.5) / 10
def r2(x): return math.floor(x * 100 + 0.5) / 100
def jsnum(x):
    if isinstance(x, float) and x == int(x): return int(x)
    return x
def fmt(x): return repr(jsnum(x))
def pos(nums, msg):
    for n in nums:
        if not (n > 0) or n != n or n == float('inf'): return {"error": msg}
    return None

def stroke_area(widthCm, strokeM): return (widthCm / 100) * OVERLAP * strokeM

def sweepPlan(widthCm, strokeM, roomM2):
    bad = pos([widthCm, strokeM, roomM2], "broom width, stroke and room size must be positive")
    if bad: return bad
    area = stroke_area(widthCm, strokeM)
    strokes = math.ceil(roomM2 / area)
    return {"m2PerStroke": jsnum(r2(area)), "strokes": strokes, "minutes": jsnum(r1(strokes / 60))}

def weekPlan(rooms, roomM2, sweepsWeek, widthCm, strokeM):
    bad = pos([rooms, roomM2, sweepsWeek, widthCm, strokeM], "rooms, size, pace, width and stroke must be positive")
    if bad: return bad
    strokes = math.ceil(rooms * sweepsWeek * math.ceil(roomM2 / stroke_area(widthCm, strokeM)))
    minutes = r1(strokes / 60)
    return {"strokesWeek": strokes, "minutesWeek": jsnum(minutes), "hoursYear": jsnum(r1(minutes * 52 / 60))}

def headPlan(hoursWeek, headCost):
    bad = pos([hoursWeek, headCost], "hours and head price must be positive")
    if bad: return bad
    headsYear = r2(hoursWeek * 52 / HEAD_HOURS)
    months = r1(HEAD_HOURS / (hoursWeek * 52 / 12))
    return {"months": jsnum(months), "headsYear": jsnum(headsYear), "costYear": jsnum(r2(headsYear * headCost))}

def plural(n, w): return str(n) + " " + w + ("" if n == 1 else "s")

def renderSweep(r):
    return "Each stroke covers " + fmt(r["m2PerStroke"]) + " m² after a labeled 20% overlap - " + plural(r["strokes"], "stroke") + ", " + ("under a minute" if r["minutes"] == 0 else "about " + fmt(r["minutes"]) + " minutes") + " for the room at a labeled stroke a second."

def renderWeek(r, rooms, sweepsWeek):
    return "Sweeping " + plural(rooms, "room") + " " + str(sweepsWeek) + " " + ("time" if sweepsWeek == 1 else "times") + " a week is " + plural(r["strokesWeek"], "stroke") + " - about " + fmt(r["minutesWeek"]) + " minutes a week, " + fmt(r["hoursYear"]) + " hours a year."

def renderHead(r, hoursWeek):
    return "At " + str(hoursWeek) + " " + ("hour" if hoursWeek == 1 else "hours") + " a week, a labeled " + str(HEAD_HOURS) + "-hour head lasts about " + plural(r["months"], "month") + " - " + fmt(r["headsYear"]) + " " + ("head" if r["headsYear"] == 1 else "heads") + " a year, about " + fmt(r["costYear"]) + " at your price."

cases = []
sweep_args = [(30,1,20),(35,1.2,25),(25,0.8,12),(40,1,30),(30,1,10),(45,1.5,40),
              (28,0.9,15),(32,1.1,22),(30,1,5),(35,1,18),(26,0.85,14),(38,1.3,28),
              (0,1,20),(30,0,20),(30,1,-5)]
for a in sweep_args:
    r = sweepPlan(*a)
    case = {"fn": "sweepPlan", "args": list(a), "result": r}
    if "error" not in r: case["render"] = renderSweep(r)
    cases.append(case)
week_args = [(3,20,2,30,1),(4,15,3,35,1.2),(2,12,1,25,0.8),(5,18,2,40,1),
             (1,20,1,30,1),(6,22,3,45,1.5),(3,16,4,28,0.9),(2,25,2,32,1.1),
             (4,14,7,30,1),(3,19,5,35,1),(2,10,3,26,0.85),(5,24,2,38,1.3),
             (0,20,2,30,1),(3,20,0,30,1)]
for a in week_args:
    r = weekPlan(*a)
    case = {"fn": "weekPlan", "args": list(a), "result": r}
    if "error" not in r: case["render"] = renderWeek(r, a[0], a[2])
    cases.append(case)
head_args = [(2,8),(1,6),(3,10),(0.5,5),(4,12),(1.5,7),(2.5,9),(5,15),
             (1,8),(6,11),(0.75,6.5),(3.5,9.5),(0,8),(2,0)]
for a in head_args:
    r = headPlan(*a)
    case = {"fn": "headPlan", "args": list(a), "result": r}
    if "error" not in r: case["render"] = renderHead(r, a[0])
    cases.append(case)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expected.json")
with open(out, "w") as f:
    json.dump(cases, f, separators=(",", ":"))
    f.write("\n")
print("wrote", len(cases), "cases")
