"""Listings and covers for the NEBians Class 8 BLE (Basic Level Examination) solved papers.

    python tools/publish/build_class8_listings.py     # merges into papers_listing.json, writes paper_covers/

Add one dict to PAPERS per new paper (id = notes/papers/content id). The page count comes from the built PDF.
exam_type is "Final" (BLE is the end-of-year exam of Class 8, set by each municipality), type stays "Past Paper".
"""
import io, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_papers as bp
from PIL import Image, ImageDraw
import pymupdf

REPO = bp.REPO
PAPERS = [
    {"id": "8-math-ble-2082-kathmandu", "file": "NEBians-BLE-Past-Paper-Grade-8-Mathematics-2082-Kathmandu.pdf",
     "subject": "Mathematics", "year_bs": "2082", "year_ad": "2026", "muni": "Kathmandu Metropolitan City",
     "district": "Kathmandu", "pradesh": "Bagmati", "marks": "50", "time": "2 hours",
     "topics": "sets, number systems, ratio, simple interest, direct and indirect variation, area of a trapezium, indices, "
               "quadratic expressions, algebraic tiles, coordinates and reflection, tessellation and the square pyramid, "
               "construction of a rectangle, and mean"},
    {"id": "8-eng-ble-2082-kathmandu", "file": "NEBians-BLE-Past-Paper-Grade-8-English-2082-Kathmandu.pdf",
     "subject": "English", "year_bs": "2082", "year_ad": "2026", "muni": "Kathmandu Metropolitan City",
     "district": "Kathmandu", "pradesh": "Bagmati", "marks": "50", "time": "2 hours",
     "topics": "reading comprehension (formal request letter, natural habitat passage, vacancy advertisement, and unseen passage on friendship), "
               "punctuation and error correction, pie-chart interpretation (crop production of Dang), essay writing (advantages and disadvantages "
               "of using mobile phones), sentence transformation (question tag, negative, passive voice, tense, indirect speech), and grammar cloze"},
]
SOC = {"id": "8-soc-ble-2082-kathmandu", "file": "NEBians-BLE-Past-Paper-Grade-8-Social-Studies-2082-Kathmandu.pdf",
       "subject": "Social Studies and Human Values", "year_bs": "2082", "year_ad": "2026", "muni": "Kathmandu Metropolitan City",
       "district": "Kathmandu", "pradesh": "Bagmati", "marks": "50", "time": "2 hours", "lang": "ne",
       "topics": "federalism, the federal council of ministers, culture and tradition, social media and online behaviour, dowry and conflict management, "
                 "foreign employment and consular services, unity in diversity, drug abuse, Greek and Roman civilisation, climate change, "
                 "rural to urban migration, the Kirat period, foreign trade, and a labelled outline map of Nepal (Sagarmatha and Boudhanath)"}
NEP = {"id": "8-nep-ble-2082-pokhara", "file": "NEBians-BLE-Past-Paper-Grade-8-Nepali-2082-Pokhara.pdf",
       "subject": "Nepali", "year_bs": "2082", "year_ad": "2026", "muni": "Pokhara Metropolitan City",
       "district": "Kaski", "pradesh": "Gandaki", "marks": "50", "time": "2 hours", "lang": "ne",
       "topics": "synonyms and antonyms, proverbs, spelling, sentence correction, parts of speech, verb forms and tenses, voice and sentence change, "
                 "prefixes, suffixes, compound words, case, two unseen passages (Badimalika and organic manure), summary writing, story and dialogue writing, "
                 "letter writing, expansion of ideas, comprehension of a story extract, poem and story appreciation, and an essay"}
SCI = {"id": "8-sci-ble-2082-kathmandu", "file": "NEBians-BLE-Past-Paper-Grade-8-Science-2082-Kathmandu.pdf",
       "subject": "Science and Technology", "year_bs": "2082", "year_ad": "2026", "muni": "Kathmandu Metropolitan City",
       "district": "Kathmandu", "pradesh": "Bagmati", "marks": "50", "time": "2 hours",
       "topics": "sustainable development (Brundtland Commission), seed storage and vegetative propagation (stem cutting and tissue culture), "
                 "displacement and relative velocity, simple machines (lever and velocity ratio), force and pressure of a rectangular block, "
                 "domestic electric circuits and monthly electricity bill calculation, wave frequency, atomic structure, periodic table and "
                 "valency of oxygen, acids, bases, pH and antacids, metallic minerals, hard and soft water, plant and animal cell Venn diagram, "
                 "five-kingdom classification, biodiversity, geological eras (Palaeozoic and Mesozoic), virtual reality vs artificial intelligence, "
                 "internet security, and ray diagram of a concave mirror"}
HPCA = {"id": "8-hpca-ble-2082-dmun", "file": "NEBians-BLE-Past-Paper-Grade-8-Health-Physical-Creative-Arts-2082-DMUN.pdf",
        "subject": "Health, Physical and Creative Arts", "year_bs": "2082", "year_ad": "2026", "muni": "DMUN",
        "district": "Siraha", "pradesh": "Madhesh", "marks": "50", "time": "2 hours",
        "topics": "nerve cell and reproductive system (ovary vs testes), characteristics of a healthy person, anemia and cancer prevention, "
                  "junk food and preserving nutrients while cooking, unsafe abortion, community health problems, heart disease and healthy "
                  "lifestyle, school health screening and first aid box materials, kabaddi, football field dimensions, long jump landing safety, "
                  "volleyball service and rules, Bhastrika pranayama, construction work and papier collé, Kaharwa taal vs Rupak taal, "
                  "Sorathi dance, and international fame of Nepali art (Araniko, pagoda architecture, Paubha and Mithila art)"}
HPCA81 = {"id": "8-hpca-ble-2081-pokhara", "file": "NEBians-BLE-Past-Paper-Grade-8-Health-Physical-Creative-Arts-2081-Pokhara.pdf",
          "subject": "Health, Physical and Creative Arts", "year_bs": "2081", "year_ad": "2025", "muni": "Pokhara Metropolitan City",
          "district": "Kaski", "pradesh": "Gandaki", "marks": "50", "time": "2 hours",
          "topics": "spinal nerves and melatonin hormone, addiction and mental health in Nepal, anaemia and goitre prevention, food safety, "
                    "first aid, ovaries and stages of the menstrual cycle, HIV/AIDS transmission, school health screening and playground safety, "
                    "drill (kawaj), relay race and baton, Halasana yoga, volleyball, football skills and kho-kho chasing rules, clay work and "
                    "construction work, musical terms, Grade 8 class song (antara), Jhyaure dance, and human figure drawing showing a happy mood"}
PAPERS.extend([SOC, NEP, SCI, HPCA, HPCA81])
COMMON = "BLE, basic level examination, class 8, grade 8, past paper, solved paper, with solutions, Nepal"


def cover(big, sub, foot, out, yr="2082"):
    img = Image.new("RGB", (1280, 720), bp.PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 1279, 719], outline=bp.LINE, width=2)
    d.rectangle([56, 96, 62, 130], fill=bp.BLUE)
    d.text((80, 96), "NEBIANS", font=bp.font(30, "bold"), fill=bp.NAVY)
    d.text((80, 146), "Class 8 BLE Past Paper", font=bp.font(34, "reg"), fill=bp.INK)
    d.text((78, 236), big, font=bp.fit(d, big, 1100, 96), fill=bp.NAVY)
    d.text((80, 400), yr, font=bp.font(120, "bold"), fill=bp.BLUE)
    d.text((80, 548), sub, font=bp.font(32, "reg"), fill=bp.INK)
    d.text((80, 600), "Full solutions included", font=bp.font(32, "bold"), fill=bp.BLUE)
    d.rectangle([0, 668, 1279, 719], fill=bp.NAVY)
    d.text((80, 680), "nebians.consica.com.np", font=bp.font(24, "semi"), fill=(255, 255, 255))
    t = foot
    d.text((1200 - int(d.textlength(t, font=bp.font(24, "reg"))), 680), t, font=bp.font(24, "reg"), fill=(190, 205, 225))
    img.save(out, "JPEG", quality=88, optimize=True)


def main():
    out = []
    cdir = os.path.join(HERE, "paper_covers")
    os.makedirs(cdir, exist_ok=True)
    for p in PAPERS:
        s, y = p["subject"], p["year_bs"]
        pdf = "notes/papers/pdf/" + p["file"]
        pages = len(pymupdf.open(os.path.join(REPO, pdf)))
        title = "NEB Class 8 %s BLE Past Paper %s (%s) %s with Solutions" % (s, y, p["year_ad"], p["muni"])
        desc = ("The Class 8 Basic Level Examination (BLE) %s paper of %s for %s BS (%s AD), %s marks and %s, re-typeset in %s "
                "with a full worked solution for every question and sub-part, marks shown beside each step and diagrams where the "
                "question needs one. It covers %s. Use it as a timed mock for your BLE and then check each answer against the "
                "solutions. Free to read in the browser."
                % (s, p["muni"], y, p["year_ad"], p["marks"], p["time"], "Nepali, the language of the original paper," if p.get("lang") == "ne" else "English", p["topics"]))
        tags = ["NEB", "BLE", "Class 8", s, "BLE %s %s" % (s, y), p["muni"], "%s past paper" % p["district"], COMMON, y, p["year_ad"]]
        it = {"slug": p["id"], "title": title, "description": desc, "subject": s, "grade_level": "Class 8", "year": y,
              "exam_type": "Final", "type": "Past Paper", "faculty": "", "program": "", "pradesh": p["pradesh"],
              "district": p["district"], "school": "", "author_name": "NEBians",
              "source_label": "BLE paper of %s, re-typeset with NEBians solutions" % p["muni"],
              "tags": ", ".join(tags), "pdf": pdf, "cover": "tools/publish/paper_covers/%s.jpg" % p["id"]}
        cover(s, "%s  ·  %s marks  ·  %s" % (p["muni"], p["marks"], p["time"]), "%d page PDF" % pages,
              os.path.join(REPO, it["cover"]), yr=y)
        out.append(it)
    bpdf = "notes/papers/pdf/bundles/NEBians-BLE-Past-Papers-Grade-8-8-ble-2082-Bundle.pdf"
    if os.path.exists(os.path.join(REPO, bpdf)):
        bpages = len(pymupdf.open(os.path.join(REPO, bpdf)))
        bslug = "8-ble-2082-bundle"
        subs = [p["subject"] for p in PAPERS]
        btitle = "NEB Class 8 BLE Past Papers 2082 (2026) All Subjects Bundle with Solutions: %s" % ", ".join(subs)
        bdesc = ("All six compulsory Class 8 Basic Level Examination (BLE) 2082 BS (2026 AD) past papers in one PDF with full worked "
                 "solutions: Mathematics (Kathmandu Metropolitan City), English (Kathmandu Metropolitan City), Nepali (Pokhara Metropolitan City), "
                 "Science and Technology (Kathmandu Metropolitan City), Social Studies and Human Values (Kathmandu Metropolitan City), and "
                 "Health, Physical and Creative Arts (DMUN). Each paper is 50 marks, 2 hours, and is followed by complete step-by-step "
                 "solutions, diagrams and model answers. Includes a contents table and PDF bookmarks to jump to any subject.")
        btags = ["NEB", "BLE", "Class 8", "BLE 2082 bundle", "Class 8 set solutions", "BLE past papers with solutions"] + subs + [COMMON]
        bit = {"slug": bslug, "title": btitle, "description": bdesc, "subject": "All Compulsory Subjects", "grade_level": "Class 8",
               "year": "2082", "exam_type": "Final", "type": "Past Paper", "faculty": "", "program": "", "pradesh": "Bagmati",
               "district": "Kathmandu", "school": "", "author_name": "NEBians",
               "source_label": "6 BLE 2082 municipality papers re-typeset with NEBians solutions",
               "tags": ", ".join(btags), "pdf": bpdf, "cover": "tools/publish/paper_covers/%s.jpg" % bslug}
        cover("All 6 Subjects Bundle", "6 BLE papers  ·  50 marks each  ·  2 hours each", "%d page PDF" % bpages,
              os.path.join(REPO, bit["cover"]))
        out.append(bit)
    lp = os.path.join(HERE, "papers_listing.json")
    old = json.load(io.open(lp, encoding="utf-8"))
    keep = [x for x in old if x["slug"] not in {y["slug"] for y in out}]
    json.dump(keep + out, io.open(lp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(len(out), "listings merged;", len(keep + out), "total;", [x["slug"] for x in out])


main()
