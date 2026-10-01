"""survey-narrate: data-rich narrative captions for wind/current fields.

Pure-Python engine (no UI framework imports anywhere). Turns a wind or
current field — GFS-wind shape (``grids["u10"]/grids["v10"]``) or
CurrentField shape (``u`` / ``v``), as dicts or objects — into
JSON-serializable story facts (:func:`story_facts`) and renders them into
mapped.earth-style captions (:func:`render_caption`).

Public API:

    >>> from narrate import story_facts, render_caption
    >>> facts = story_facts(field, region_name="the North Sound")
    >>> caption = render_caption(facts, style="instagram")
"""

from .facts import MS_TO_KNOTS, NoValidDataError, compass_label, dominant_direction, story_facts
from .render import render_caption
from .shapes import (
    NormalizedField,
    UnrecognizedFieldError,
    normalize_field,
)

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "story_facts",
    "render_caption",
    "normalize_field",
    "NormalizedField",
    "dominant_direction",
    "compass_label",
    "MS_TO_KNOTS",
    "NoValidDataError",
    "UnrecognizedFieldError",
]
