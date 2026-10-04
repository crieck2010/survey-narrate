# API — survey-narrate v0.2.0

## `narrate.story_facts(field, region_name="", temperature_unit=None) -> dict`

See README for the full fact table. Error cases:

| Situation | Raised |
|---|---|
| Field matches neither supported shape | `UnrecognizedFieldError(ValueError)` |
| `len(times)` / `lats` / `lons` inconsistent with grid shape | `ValueError` |
| `temperature_unit` hint not °C/°F-like | `ValueError` |
| No valid (non-NaN, unmasked) u/v cells | `NoValidDataError(ValueError)` |

Both shapes accept dicts **or** objects — attribute access and mapping
access are tried in that order per key.

## `narrate.render_caption(facts, style="instagram") -> str`

- `"instagram"` → 2–4 sentences.
- `"email"` → one compact paragraph.
- Unknown style → `ValueError`. Missing fact keys → `KeyError`.

Knot formatting in captions: whole knots at ≥ 3 kt, one decimal below
(e.g. "19 knots", "2.4 knots").

## `narrate.headline_beats(facts, *, max_beats=4) -> list[tuple[float, str]]`

Draft headline text swaps for an animated reel, consuming only the
`story_facts` dict. Returns `(t_fraction, text)` pairs sorted
ascending, fractions in [0.0, 1.0], at most `max_beats` entries.

- Opening at 0.0 (region + subject), peak at the `peak.time` fraction
  inside `time_span` (0.5 fallback; knots, hemisphere-correct lat/lon),
  closing at 0.9 (mean speed / dominant direction), optional
  temperature-range mid beat at 0.65 when `max_beats >= 4` and the
  range is >= 1.0 in the reported unit.
- `max_beats=1` returns just the opening. `max_beats < 1` or a facts
  dict missing `field_kind`/`peak`/`time_span`/`mean_speed_knots`
  → `ValueError`.
- These are DRAFTS for human approval/editing; fractions are
  approximate placements and the lines only restate computed facts —
  no causal claims.

## `narrate.normalize_field(field, temperature_unit=None) -> NormalizedField`

Detects and normalizes to the internal record. `NormalizedField` fields:
`u`, `v` (m/s, (nt, ny, nx)); `temperature` (or None); `temperature_unit`
(`"°C"` / `"°F"` / None); `times`; `lats`; `lons`; `kind`
(`"wind"` / `"current"`).

## `narrate.dominant_direction(u, v)`

Vector mean of (u, v), NaN-aware; bearing clockwise from north of the
resultant (direction the flow heads). `(None, None)` when the mean is
zero or no cells are valid.

## `narrate.compass_label(bearing_deg) -> str`

Nearest 8-point compass label: northerly, northeasterly, easterly,
southeasterly, southerly, southwesterly, westerly, northwesterly.
