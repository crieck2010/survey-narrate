"""Render mapped.earth-style narrative captions from fact dicts.

The voice: concrete numbers, no hype adjectives, specific but generic.
Place names come only from ``facts["region_name"]`` — nothing is ever
invented. Numbers are never rounded beyond one decimal and never
editorialized ("nearly", "a whopping") — the honesty rules that make a
caption auditable against the data.
"""

from __future__ import annotations

from typing import Dict


def _kt(knots: float) -> str:
    """Knot value for captions: whole knots >= 3, else one decimal."""
    if knots >= 3:
        return f"{knots:.0f}"
    return f"{knots:.1f}"


def _subject(kind: str) -> str:
    return "the wind" if kind == "wind" else "the surface water"


def _time_window(facts: Dict) -> str:
    span = facts["time_span"]
    return f"{span['start']} to {span['end']}"


def _peak_clause(facts: Dict) -> str:
    peak = facts["peak"]
    subj = _subject(facts["field_kind"])
    return (f"At its strongest, {subj} there ran at "
            f"{_kt(peak['value_knots'])} knots, "
            f"at {peak['lat']:.2f}°N, {peak['lon']:.2f}°E "
            f"on {peak['time']}.")


def _mean_clause(facts: Dict) -> str:
    subj = _subject(facts["field_kind"])
    span = facts["time_span"]
    region = facts.get("region_name") or "the area"
    return (f"Across {region}, {span['n_timesteps']} {span['cadence']} samples "
            f"averaged {_kt(facts['mean_speed_knots'])} knots.")


def _direction_clause(facts: Dict) -> str:
    d = facts["direction"]
    if d["label"] is None:
        return "No dominant direction — the flow averaged out."
    return f"The flow was mostly {d['label']}."


def _temperature_clause(facts: Dict) -> str:
    t = facts.get("temperature")
    if t is None:
        return ""
    noun = "Air temperatures" if facts["field_kind"] == "wind" else "Water temperatures"
    return f"{noun} ranged from {t['min']:.1f} to {t['max']:.1f} {t['unit']}."


def render_caption(facts: Dict, style: str = "instagram") -> str:
    """Render a 2–4 sentence caption from a :func:`story_facts` dict.

    Parameters
    ----------
    facts:
        The fact dict returned by :func:`narrate.facts.story_facts`.
    style:
        ``"instagram"`` — 2–4 sentences in the mapped.earth caption
        voice (concrete numbers, no hype adjectives, place label from
        ``region_name`` only, never invented).
        ``"email"`` — one compact paragraph for a daily-reel email body:
        same facts, tighter phrasing, still full sentences.

    Raises
    ------
    ValueError
        Unknown style.
    KeyError
        Missing expected fact keys (not a :func:`story_facts` dict).
    """
    if style == "instagram":
        return _render_instagram(facts)
    if style == "email":
        return _render_email(facts)
    raise ValueError(
        f"unknown caption style {style!r}; expected 'instagram' or 'email'.")


def _render_instagram(facts: Dict) -> str:
    sentences = [_mean_clause(facts), _peak_clause(facts), _direction_clause(facts)]
    temp = _temperature_clause(facts)
    if temp:
        sentences.append(temp)
    return " ".join(sentences)


def _render_email(facts: Dict) -> str:
    peak = facts["peak"]
    span = facts["time_span"]
    subj = _subject(facts["field_kind"])
    region = facts.get("region_name") or "the area"
    d = facts["direction"]
    direction_bit = f"Mostly {d['label']} flow" if d["label"] else "No dominant direction"
    parts = [
        f"{region} — {subj} from {span['start']} to {span['end']} "
        f"({span['n_timesteps']} {span['cadence']} samples): "
        f"averaged {_kt(facts['mean_speed_knots'])} knots, "
        f"peaked at {_kt(peak['value_knots'])} knots "
        f"({peak['lat']:.2f}°N, {peak['lon']:.2f}°E, {peak['time']}).",
        direction_bit + ".",
    ]
    temp = _temperature_clause(facts)
    if temp:
        parts.append(temp)
    return " ".join(parts)
