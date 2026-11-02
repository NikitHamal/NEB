// Run a jQuery snippet against an HTML fixture in jsdom; prints console.log output. stdin: JSON {html, js}
const { JSDOM } = require("jsdom");
const input = JSON.parse(require("fs").readFileSync(0, "utf8"));
const dom = new JSDOM(input.html);
const $ = require("jquery")(dom.window);
const log = (...a) => console.log(a.map(x => typeof x === "string" ? x : JSON.stringify(x)).join(" "));
try { new Function("$", "window", "document", "console", input.js)($, dom.window, dom.window.document, { log }); }
catch (e) { console.log("ERROR: " + e.message); }
