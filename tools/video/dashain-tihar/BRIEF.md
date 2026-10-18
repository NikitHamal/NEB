# BRIEF: Dashain and Tihar with NEBians

Spec: 1920x1080@60, 34.6 s (14 bars + 1 s tail), 100 BPM, pace: calm, audio: earshot kit (calm, tuned to D major) + light synth score; re-layouts Film9x16 and Film1x1.
For: students and families in Nepal, on social feeds and the landing page during the festival season.
Message: the festival season from Dashain to Tihar, with NEBians' wish. Every on-screen word is Nepali (Poppins Devanagari).
Look: 2D pixel art drawn per frame (320x180 art pixels in 16:9, 180x320 in 9:16, scaled exactly 6x), with the NEBians mark and wordmark on the end card.

Brand- and culture-supplied exceptions (the festivals themselves, so the hard bans' colour rules yield):
- marigold (sayapatri) orange and yellow, diyo flame amber, tika red, jamara green, kite colours, warm skin and wall tones, the dawn sky's peach.
  Each line that sets one is marked `// cinetic:brand-supplied festival palette` (brand/tokens.ts, P).
- the NEBians N mark gradients and Poppins, as in the launch film.

Hard bans otherwise as cinetic: no eyebrows, no stacked taglines, fragments of 1-4 words, no glow/bloom/neon on UI, no confetti/particles standing in for ideas (the stars, flames and petals here are the scene's real objects), no serif or italic.

Sound note: the brief pointed at react-bits for sound; react-bits is an animation component library with no audio, so it informed motion only. Sound is made in code (earshot kit), every cue computed from the picture.
