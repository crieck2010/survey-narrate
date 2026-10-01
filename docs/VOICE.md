# Voice guide — the mapped.earth caption register

Captions in this engine follow the mapped.earth register observed in its
reels and captions. The rules are enforced by construction in
`src/narrate/render.py`:

1. **Concrete numbers, always.** "ran at 19 knots" — never "very fast",
   never "extremely strong". Every numeric claim in a caption traces to
   one key in the facts dict.
2. **No hype adjectives.** "whopping", "massive", "incredible", "wild",
   "extreme" are banned. The test suite asserts their absence.
3. **Specific but generic.** The caption names the place (caller-supplied
   only), the number, the when, and the where-in-the-grid. It does not
   explain mechanisms.
4. **Numbers stated, not editorialized.** No "nearly", "just over",
   "a whopping". If the data says 19 knots, the caption says 19 knots.
5. **Honest about absence.** No dominant direction → "No dominant
   direction — the flow averaged out." No temperature → no temperature
   sentence. No region name → "the area".

## Why this matters for the reel pipeline

A caption that states only what the data supports can be audited:
re-render `story_facts` from the same field and every number in the
caption must match. The `email` style exists so the same audited facts
can ride inside the daily-reel email body without rewording by hand.
