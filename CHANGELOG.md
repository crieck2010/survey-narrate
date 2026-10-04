# Changelog

All notable changes to survey-narrate. Follows [Semantic Versioning](https://semver.org/) and [Keep a Changelog](https://keepachangelog.com/).

## [0.2.0] - 2026-10-04

### Added

- `headline_beats(facts, *, max_beats=4) -> list[tuple[float, str]]`:
  deterministic draft headline text swaps for an animated reel (the
  mapped.earth "Where Italy lives" pattern), consuming only the
  `story_facts` dict. Opening beat at 0.0 (region + subject framing),
  peak beat at the fraction where `peak.time` falls inside `time_span`
  (0.5 fallback; knots and hemisphere-correct lat/lon shared with
  `render_caption`), closing beat at 0.9 (mean speed / dominant
  direction), and an optional temperature-range mid beat at 0.65 only
  when `max_beats >= 4` and the range is meaningful. Drafts for human
  approval/editing; fractions are approximate and lines only restate
  computed facts — no causal claims.
- Exported `headline_beats` from `narrate` alongside `story_facts`
  and `render_caption`; 19 new tests in `tests/test_beats.py`.

## [0.1.0] - 2026-10-01

Initial release.

- `story_facts(field, region_name="", temperature_unit=None)`: NaN-aware
  descriptive statistics from GFS-wind-shaped fields
  (`grids["u10"]/grids["v10"]`) or CurrentField-shaped fields (`u`/`v`),
  as dicts or objects. Peak speed (m/s + knots) with lat/lon/timestamp,
  mean and p95 speeds, dominant flow direction (bearing + 8-point compass
  label), temperature range with unit, time span with cadence guess,
  valid-cell coverage. All JSON-serializable.
- `render_caption(facts, style="instagram")`: 2–4 sentences in the
  mapped.earth caption voice; `style="email"` for a compact one-paragraph
  daily-email body.
- Duck-typed shape detection; `UnrecognizedFieldError` (a `ValueError`)
  for unrecognized shapes — never guesses.
- 38 pytest tests, all synthetic fields, no network.
