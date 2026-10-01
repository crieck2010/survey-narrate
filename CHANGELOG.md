# Changelog

All notable changes to survey-narrate. Follows [Semantic Versioning](https://semver.org/).

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
