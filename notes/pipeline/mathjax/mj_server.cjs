/* MathJax SVG typesetter for the NEBians PDF pipeline.
 *
 * Protocol (one JSON object per line on stdin, one per line on stdout):
 *   in : {"tex": "\\frac{a}{b}", "display": false}
 *   out: {"ok": true, "svg": "<svg ...>"}   or   {"ok": false, "err": "message"}
 *
 * Glyphs are embedded as outlines (fontCache "none"), so the PDF needs no math
 * font. mathsvg.py wraps this process, caches the result by hash and fixes the
 * baseline from the viewBox.
 */
const readline = require("readline");
const { mathjax } = require("mathjax-full/js/mathjax.js");
const { TeX } = require("mathjax-full/js/input/tex.js");
const { SVG } = require("mathjax-full/js/output/svg.js");
const { liteAdaptor } = require("mathjax-full/js/adaptors/liteAdaptor.js");
const { RegisterHTMLHandler } = require("mathjax-full/js/handlers/html.js");
const { AllPackages } = require("mathjax-full/js/input/tex/AllPackages.js");

// every package except the ones that load code at run time
const PACKAGES = AllPackages.filter((p) => !["autoload", "require", "noundefined", "noerrors"].includes(p));

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);

const macros = {
  degree: "{^\\circ}",
  micro: "\\mu",
  lvert: "\\vert",
  rvert: "\\vert",
  iff: "\\Longleftrightarrow",
  implies: "\\Longrightarrow",
};

const tex = new TeX({
  packages: PACKAGES,
  macros,
  inlineMath: [["$", "$"]],
  formatError(jax, err) { throw err; },
});
const svg = new SVG({ fontCache: "none" });
const doc = mathjax.document("", { InputJax: tex, OutputJax: svg });

function typeset(src, display) {
  const node = doc.convert(src, { display: !!display, em: 16, ex: 8, containerWidth: 1280 });
  const el = adaptor.firstChild(node);
  return adaptor.outerHTML(el);
}

const rl = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });
rl.on("line", (line) => {
  let req;
  try { req = JSON.parse(line); } catch (e) { return; }
  let out;
  try {
    out = { ok: true, svg: typeset(req.tex, req.display) };
    if (/data-mml-node="merror"|data-mjx-error/.test(out.svg)) {
      const m = out.svg.match(/data-mjx-error="([^"]*)"/);
      out = { ok: false, err: m ? m[1] : "merror" };
    }
  } catch (e) {
    out = { ok: false, err: String((e && e.message) || e).slice(0, 200) };
  }
  process.stdout.write(JSON.stringify(out) + "\n");
});
