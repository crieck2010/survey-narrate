# API — survey-narrate v0.1.0

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
