// Broom math - pure arithmetic engine, runs in browser and node.
(function(root){
"use strict";
function r1(x){ return Math.round(x*10)/10; }
function r2(x){ return Math.round(x*100)/100; }
var OVERLAP = 0.8;   // labeled: 20% stroke overlap
var HEAD_HOURS = 300; // labeled: broom-head life in sweeping hours
function pos(nums, msg){
  for (var i=0;i<nums.length;i++){ if (!isFinite(nums[i]) || nums[i] <= 0) return { error: msg }; }
  return null;
}
function strokeArea(widthCm, strokeM){ return (widthCm / 100) * OVERLAP * strokeM; }
function sweepPlan(widthCm, strokeM, roomM2){
  var bad = pos([widthCm, strokeM, roomM2], "broom width, stroke and room size must be positive");
  if (bad) return bad;
  var area = strokeArea(widthCm, strokeM);
  var strokes = Math.ceil(roomM2 / area);
  return { m2PerStroke: r2(area), strokes: strokes, minutes: r1(strokes / 60) };
}
function weekPlan(rooms, roomM2, sweepsWeek, widthCm, strokeM){
  var bad = pos([rooms, roomM2, sweepsWeek, widthCm, strokeM], "rooms, size, pace, width and stroke must be positive");
  if (bad) return bad;
  var strokes = Math.ceil(rooms * sweepsWeek * Math.ceil(roomM2 / strokeArea(widthCm, strokeM)));
  var minutes = r1(strokes / 60);
  return { strokesWeek: strokes, minutesWeek: minutes, hoursYear: r1(minutes * 52 / 60) };
}
function headPlan(hoursWeek, headCost){
  var bad = pos([hoursWeek, headCost], "hours and head price must be positive");
  if (bad) return bad;
  var headsYear = r2(hoursWeek * 52 / HEAD_HOURS);
  var months = r1(HEAD_HOURS / (hoursWeek * 52 / 12));
  return { months: months, headsYear: headsYear, costYear: r2(headsYear * headCost) };
}
function plural(n, w){ return n + " " + w + (n === 1 ? "" : "s"); }
function renderSweep(r){
  return "Each stroke covers " + r.m2PerStroke + " m² after a labeled 20% overlap - " + plural(r.strokes, "stroke") + ", " + (r.minutes === 0 ? "under a minute" : "about " + r.minutes + " minutes") + " for the room at a labeled stroke a second.";
}
function renderWeek(r, rooms, sweepsWeek){
  return "Sweeping " + plural(rooms, "room") + " " + sweepsWeek + " " + (sweepsWeek === 1 ? "time" : "times") + " a week is " + plural(r.strokesWeek, "stroke") + " - about " + r.minutesWeek + " minutes a week, " + r.hoursYear + " hours a year.";
}
function renderHead(r, hoursWeek){
  return "At " + hoursWeek + " " + (hoursWeek === 1 ? "hour" : "hours") + " a week, a labeled " + HEAD_HOURS + "-hour head lasts about " + plural(r.months, "month") + " - " + r.headsYear + " " + (r.headsYear === 1 ? "head" : "heads") + " a year, about " + r.costYear + " at your price.";
}
var api = { HEAD_HOURS: HEAD_HOURS, sweepPlan: sweepPlan, weekPlan: weekPlan, headPlan: headPlan,
  renderSweep: renderSweep, renderWeek: renderWeek, renderHead: renderHead };
if (typeof module !== "undefined" && module.exports) module.exports = api;
root.BroomMath = api;
})(typeof window !== "undefined" ? window : globalThis);
