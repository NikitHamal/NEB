# Session 30 authoring helpers (Electronics Circuit EX 154, Computer Aided Civil Drawing ENCE 204)
Reusable circuit / civil-section figure code and answer snippets. The scripts use absolute paths under `/app/shots`:
`mkdir -p /app/shots && cp -r tools/session30/* /app/shots/ && /app/shots/build.sh <paper-id>`.
- `figs_ec.py`, `figs_ec2.py`: CE amplifier, MOSFET bias, rectifiers, Zener, regulators, class A/B, op-amp, Wien bridge figures (use `ckt.py` helpers; a wrapper puts labels of vertical parts beside the part).
- `figs_cad.py`: canal fill/cut, hill road fill/cut-fill, retaining walls, 4 m cantilever wall, title block, location map + site plan, SW-DTM flow.
- `snips.py`: shared answers for the CAD paper family (CADD, blocks, layers, layouts, SW-DTM, BIM, CDE ...). `%%SNIP key%%`, `%%FIG name|caption|K=V;..%%`, `%%INC a b%%` (lines of the EX 151 md) are expanded by `asm.py` into `content/<id>.md`.
- `src/*.md`: the placeholder sources of the five papers.
