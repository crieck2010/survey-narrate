# Interop — how survey-narrate consumes peer fields

No peer package is imported. `survey-narrate` duck-types two layouts
that the stack already produces; pass them straight through.

## GFS wind (survey-currents `GfsWindField`)

```python
from narrate import story_facts, render_caption

field = fetch_gfs_wind(...)          # survey-currents
facts = story_facts(field, region_name="the North Sound",
                    temperature_unit="°F")   # optional; field declares °F already
print(render_caption(facts))
```

Detected via `grids["u10"]/grids["v10"]`; temperature from
`air_temperature` (unit read from `temperature_unit`), else
`grids["t2m"]` (°C). `times`/`lats`/`lons` are read as-is.

## Ocean currents (survey-currents `CurrentField`)

```python
facts = story_facts(current_field, region_name="the Strait")
print(render_caption(facts))
```

Detected via `u`/`v` attributes; `temperature` is optional (°C per the
CurrentField convention).

## survey-viz dict forms

The generic dict form `survey-viz`'s `render_viz` documents
(`grids`/`times`/`lats`/`lons`) flows through the same gfs-wind path —
no adapter needed.
