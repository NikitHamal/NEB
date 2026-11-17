

---

# Session 59: Interactive hub and course rebuilt (app and web), picks up session 58

Same file, same rule: nothing is built locally, the check is the GitHub Actions run. Session 58 items 335 to 339 were verified in the tree (search error and tab rail, create menu, question banks and model papers on the hub, labs retry and fullscreen, reader dock `24e8db3`); none redone.

## Done

| # | What | Where |
| --- | --- | --- |
| 340 | **App Interactive tab**: one flat list (white 24dp card, hairline, tonal tile, lessons and minutes chips) with a category chip row on top. The hero card, the per-category panels with a sideways scroller inside a vertical list, the blurb and the tagline are gone, so scrolling is one lazy list with stable keys. | `InteractiveLibraryContent.kt` |
| 341 | **App course screen**: rounded 22dp lesson cards clipped before clickable, squircle number tile, no tagline or skills strip, cancellation rethrown in the load. | `InteractiveCourseScreen.kt` |
| 342 | **Web Interactive hub**: category chip row filters the sections without a reload, category blurb removed. | `_hub_content.html`, `01-hub.css` |

## Next
- Reader (`ReadingMode`, `PdfReaderChrome`): Aa sheet and hiding dock from the concept, on device.
- Lesson list inside a course could show the chapter each lab belongs to once the API carries it.
