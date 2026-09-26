# Fonts

The books use Poppins (display), Inter (UI/labels), Source Serif 4 (body),
Noto Sans Devanagari (Nepali) and JetBrains Mono (code). All five are
SIL Open Font License 1.1.

They are not vendored here — the binaries are large and Google Fonts is the
canonical source. Install them once before building:

    ./install.sh

WeasyPrint and matplotlib both resolve them through fontconfig by family name,
so nothing in `theme.css` or the Python needs a path.
