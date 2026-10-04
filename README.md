# survey-narrate

Turns a wind or current data field into the kind of data-rich narrative
caption [mapped.earth](https://mapped.earth) writes:

> "The whole South Sound fills and drains through the Tacoma Narrows, a
> strait about a mile wide. At its strongest this week, the surface water
> there ran at nearly 5 knots."

Numbers come from the data; place names come from the caller. Pure-Python
engine — **zero UI-framework imports anywhere**.

## Install

```bash
pip install git+https://github.com/crieck2010/survey-narrate@v0.2.0
# or from a local clone
pip install -e .
```

## Usage

```python
from narrate import headline_beats, render_caption, story_facts

# field: a GFS-wind-shaped dict/object (grids["u10"]/grids["v10"])
#        or a CurrentField-shaped dict/object (u/v), times/lats/lons
facts = story_facts(field, region_name="the Tacoma Narrows")

print(render_caption(facts, style="instagram"))
# Across the Tacoma Narrows, 2 daily samples averaged 6 knots.
# At its strongest, the wind there ran at 19 knots, at 42.00°N, -7.00°E
# on 2026-09-29T00:00:00Z. The flow was mostly easterly.
# Air temperatures ranged from 50.0 to 50.0 °F.

print(render_caption(facts, style="email"))   # one compact paragraph

print(headline_beats(facts))
# [(0.0, 'the Tacoma Narrows — the wind in motion'),
#  (0.9, 'Average: 6 knots, mostly easterly'),
#  (1.0, 'Peak: 19 knots at 42.00°N, 7.00°W')]
```

## API reference

### `story_facts(field, region_name="", temperature_unit=None) -> dict`

Computes descriptive statistics from a wind or current field. Everything
is JSON-serializable (plain floats/ints/strings/None).

| Fact key | Contents |
|---|---|
| `field_kind` | `"wind"` or `"current"` |
| `region_name` | Caller-supplied label, verbatim ("" if not given) |
| `peak` | `value_m_s`, `value_knots`, `lat`, `lon`, `time` of the fastest valid cell |
| `mean_speed_m_s`, `mean_speed_knots` | Mean over valid cells |
| `p95_speed_m_s`, `p95_speed_knots` | 95th percentile over valid cells |
| `direction` | `bearing_deg` (0–360, clockwise from north), 8-point `label` (e.g. `"easterly"`), and a `note` documenting the convention |
| `temperature` | `{min, max, unit}` or `None` |
| `time_span` | `start`/`end` ISO, `n_timesteps`, `cadence` guess (`"hourly"`, `"daily"`, `"irregular"`, `"single"`), `median_step_s` |
| `n_valid_cells`, `n_total_cells`, `coverage_fraction` | NaN-gap accounting |

**Field shapes accepted (duck-typed, dicts or objects):**

- **GFS-wind shape**: `grids["u10"]` / `grids["v10"]` in m/s, `times`,
  `lats`, `lons`. Temperature from `air_temperature` (unit read from
  `temperature_unit`), falling back to `grids["t2m"]` (°C).
- **CurrentField shape**: `u` / `v` in m/s (east/north positive),
  `times`, `lats`, `lons`; optional `temperature` (assumed °C).

**Design choices:**

- **Direction convention**: the bearing is the direction the flow
  *heads* (vector mean of `(u, v)`), clockwise from true north —
  90°/"easterly" means the vector-mean flow moves toward the east. This
  is *not* the meteorological "wind from" convention (documented on
  every output in `direction.note`).
- **Knots**: 1 m/s = 1.9438444924 knots, applied exactly.
- **Temperature units**: auto-detected from the field's
  `temperature_unit`; the `temperature_unit` hint overrides it (accepts
  "°C"/"degC" or "°F"/"degF"-style strings). Unknown hint → `ValueError`.
- **NaN-aware throughout**: NaN/masked cells are excluded from every
  statistic and counted in `coverage_fraction`. Gaps stay gaps — never
  filled, never interpolated. A field with no valid cells raises
  `NoValidDataError`.
- **Unrecognized shapes**: raise `UnrecognizedFieldError` (a
  `ValueError`) with a message naming the expected layouts. The engine
  never guesses a field layout.

### `render_caption(facts, style="instagram") -> str`

Renders 2–4 sentences in the mapped.earth caption voice: concrete
numbers, no hype adjectives, specific but generic. Place names come only
from `facts["region_name"]` — never invented. Numbers are stated as
computed, never editorialized ("nearly", "a whopping").

- `style="instagram"`: the 2–4 sentence caption.
- `style="email"`: one compact paragraph for a daily-reel email body.
- Unknown style → `ValueError`.

### `headline_beats(facts, *, max_beats=4) -> list[tuple[float, str]]`

Drafts headline text swaps for an animated reel — the mapped.earth
"Where Italy lives" pattern, where the title changes at story moments.
Consumes **only** the dict returned by `story_facts` (never the raw
field) and returns `(t_fraction, text)` pairs sorted ascending,
fractions in [0.0, 1.0], at most `max_beats` entries
(`max_beats` must be >= 1; `max_beats=1` returns just the opening).

Beat design (deterministic — no RNG, no AI):

1. **Opening at 0.0** — region + subject framing, e.g.
   `"North America — the wind in motion"` (currents: `"the surface
   water"`). Uses `region_name` verbatim when present; falls back to
   the bare subject (`"The wind in motion"`) when empty.
2. **Peak** at the fraction where `peak.time` falls inside
   `time_span`, computed from the ISO timestamps (0.5 when that cannot
   be derived, e.g. a single timestep): `"Peak: 19 knots at 42.00°N,
   7.00°W"`. Speed is in knots for both wind and currents — the same
   unit `render_caption` uses — and lat/lon use the shared
   hemisphere-correct formatting.
3. **Closing at 0.9** — a synthesis line restating the mean speed and,
   when present, the dominant direction, e.g. `"Average: 6 knots,
   mostly easterly"`.
4. **Optional mid beat at 0.65**, only when `max_beats >= 4` and the
   facts carry a meaningful temperature range (>= 1.0 in the reported
   unit). Never padded with filler; fewer beats is fine.

**These are DRAFTS for human approval/editing** — review and edit the
text before putting it on a reel. Fractions are approximate placements
along the reel timeline, not frame-exact cues. The peak and closing
lines only restate computed facts (peak speed/location, mean speed,
dominant direction, temperature range); no causal claims are made.

Degenerate inputs still yield valid beats: no region name, no
temperature, or a single timestep returns at least the opening beat.
A facts dict missing required structure (`field_kind`, `peak`,
`time_span`, `mean_speed_knots`) raises a clear `ValueError`, as does
`max_beats < 1`.

### Helpers

- `normalize_field(field, temperature_unit=None) -> NormalizedField`
- `dominant_direction(u, v) -> (bearing_deg | None, label | None)`
- `compass_label(bearing_deg) -> str`
- `MS_TO_KNOTS`, `NoValidDataError`, `UnrecognizedFieldError`

## Honest limits — what it does NOT do

- **No place-name lookup.** Geography (`region_name`) is caller-supplied
  only. An empty label renders as "the area".
- **No causal claims.** "The flow was mostly easterly" is a description
  of the sampled vectors, not an explanation. Nothing here says why.
- **Stats describe the sampled window only.** Peak/mean/p95 summarize
  the grid cells and timesteps given — not the location in general, not
  other days, not the future.
- **Direction is vector-mean flow direction**, not the meteorological
  "wind from" convention — read `direction.note` before quoting a
  "westerly"/"easterly" to a mariner.
- **Cadence is a guess** from median inter-step spacing; irregular or
  gappy series report `"irregular"`.
- Temperature min/max reflect only the cells valid for u/v; if the
  temperature grid has its own gaps over those cells they are excluded.
- **Headline beats are drafts, not finished titles.** `headline_beats`
  fractions are approximate placements, and its lines only restate
  computed facts — a human still approves and edits the wording.

## Testing

```bash
pip install -e ".[test]"
pytest -q
```

64 tests, all synthetic fields, zero network access.
