---
subject: E-Governance
grade: BCA Semester 8 (Elective III)
unit: 4
title: Applications of Data Warehousing and Data Mining in Government
hours: 6
area: BCA 453 · E-Governance · Unit 4
---

A government that serves people also collects data about them every day: births, school enrolments, vaccinations, taxes, imports, land sales, complaints. For decades these records lived in separate systems that were good at answering "what is the status of this one file?" and bad at answering "which districts are falling behind, and why?" **Data warehousing** gathers the records into one consistent store built for questions across places and years. **Data mining** searches that store for patterns that nobody asked for in advance. Together they turn e-governance from *service delivery* into *evidence-based policy*, which is the last of the objectives listed in Unit 1.

::: key What this unit gives you
- The warehouse idea: subject-oriented, integrated, time-variant, non-volatile; OLTP versus OLAP; ETL; star schema; marts; cubes.
- Data mining tasks (classification, clustering, association, anomaly detection, forecasting) and the knowledge-discovery process.
- **National data warehouses**: census data and the prices of essential commodities, each worked through a small program.
- Uses in agriculture, rural development, health, planning, education, commerce and trade, and other sectors.
- Privacy and ethics: what must be protected when government data are mined, with a k-anonymity check.
:::

## 4.1 Introduction

### 4.1.1 From operational systems to a warehouse

Government applications are **OLTP** systems (on-line transaction processing): they record one transaction at a time, quickly and safely (register a birth, post a payment). A **data warehouse** is built for **OLAP** (on-line analytical processing): reading millions of past records at once to summarise, compare and trend.

| Feature | OLTP (operational system) | Data warehouse (OLAP) |
|---|---|---|
| Purpose | Run day-to-day services | Support analysis and decisions |
| Data | Current, detailed, one application | Historical, integrated, many sources |
| Typical query | "Status of citizenship file 4521" | "Births by district and year for ten years" |
| Update | Constantly, by many users | Loaded in batches, not changed afterwards |
| Design | Normalised tables, few joins | Star schema, summaries, few tables |
| Users | Clerks, citizens | Analysts, planners, managers |

A data warehouse is commonly defined (after W. H. Inmon) as a **subject-oriented, integrated, time-variant and non-volatile** collection of data in support of management decisions. *Subject-oriented*: organised around population, health or trade, not around applications. *Integrated*: one code for each district, one date format. *Time-variant*: every record carries a date, so trends can be studied. *Non-volatile*: data are added, not overwritten.

### 4.1.2 Architecture

```svgfig label="4.1" caption="Architecture of a government data warehouse: source systems feed an ETL stage; the warehouse serves subject-wise data marts, and analysts reach them with OLAP, reports and mining tools. A metadata layer and security cover the whole chain."
f = Fig(680, 300)
f.box(15, 30, 120, 60, "Census\nsystem", fill=BLUE, stroke=NAVY, size=10)
f.box(15, 105, 120, 60, "Tax and\ncustoms", fill=BLUE, stroke=NAVY, size=10)
f.box(15, 180, 120, 60, "Health, school,\nland records", fill=BLUE, stroke=NAVY, size=10)
f.box(175, 65, 100, 130, "ETL\nextract\ntransform\nload", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(315, 65, 110, 130, "Central\ndata\nwarehouse", fill=MINT, stroke=TEAL, size=12, bold=True)
f.box(465, 30, 90, 50, "Health mart", fill=SOFT, stroke=TEAL, size=9.5)
f.box(465, 125, 90, 50, "Trade mart", fill=SOFT, stroke=TEAL, size=9.5)
f.box(465, 205, 90, 50, "Education\nmart", fill=SOFT, stroke=TEAL, size=9.5)
f.box(590, 80, 80, 110, "OLAP\nreports\nmining\ndashboards", fill=ROSE, stroke=RED, size=9.5)
f.box(15, 262, 655, 30, "Metadata, data quality rules, security and privacy controls span all stages", fill=SOFT, stroke=SLATE, size=10.5, color=SLATE)
for y in (60, 135, 210):
    f.arrow([(135, y), (175, 130)], color=NAVY)
f.arrow([(275, 130), (315, 130)], color=AMBER)
for y in (55, 150, 230):
    f.arrow([(425, 130), (465, y)], color=TEAL)
    f.arrow([(555, y), (590, 135)], color=RED)
```

**ETL** has three steps. *Extract* copies data from sources. *Transform* cleans and conforms it: fixes spellings, converts codes, removes duplicates, checks ranges and fills or rejects missing values. *Load* writes the result into the warehouse. Transformation is the largest part of the work; a warehouse of dirty data is a fast way to wrong answers.

### 4.1.3 Star schema, cube and OLAP

The usual design is a **star schema**: a central **fact table** of measurable events (population count, number of births, price, value of imports) surrounded by **dimension tables** that describe the context (place, time, age group, product). A **cube** is the same data seen along several dimensions at once. OLAP operations: **roll-up** (district to province), **drill-down** (province to district), **slice** (fix one dimension, such as the year 2021), **dice** (select ranges on several), and **pivot** (turn the axes).

```svgfig label="4.2" caption="A star schema for population data: one fact table (counts of people) and three dimensions (place, time, age and sex). Roll-up moves up the place hierarchy: ward, municipality, district, province, country."
f = Fig(680, 270)
f.box(240, 95, 200, 80, "FACT_POPULATION\ngeo_key, year_key, age_key,\npersons, households", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(20, 20, 190, 70, "DIM_GEOGRAPHY\ngeo_key, ward, municipality,\ndistrict, province", fill=BLUE, stroke=NAVY, size=9.5)
f.box(470, 20, 190, 70, "DIM_TIME\nyear_key, census year,\ndecade", fill=BLUE, stroke=NAVY, size=9.5)
f.box(245, 195, 190, 60, "DIM_AGE_SEX\nage_key, age group, sex", fill=BLUE, stroke=NAVY, size=9.5)
f.arrow([(160, 90), (260, 105)], color=NAVY)
f.arrow([(520, 90), (420, 105)], color=NAVY)
f.arrow([(340, 195), (340, 175)], color=NAVY)
```

The program builds exactly this schema in an in-memory SQLite database with synthetic counts for six districts, then runs roll-up, drill-down and slice queries. The numbers are invented; only the *method* is the point.

```python
import sqlite3, random
random.seed(11)
db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE dim_geo (geo_key INTEGER PRIMARY KEY, district TEXT, province TEXT);
CREATE TABLE dim_age (age_key INTEGER PRIMARY KEY, age_group TEXT, sex TEXT);
CREATE TABLE fact_pop (geo_key INT, year INT, age_key INT, persons INT);
""")
districts = [("Kathmandu", "Bagmati"), ("Lalitpur", "Bagmati"), ("Morang", "Koshi"),
             ("Jhapa", "Koshi"), ("Kaski", "Gandaki"), ("Humla", "Karnali")]
db.executemany("INSERT INTO dim_geo VALUES (?,?,?)", [(i, d, p) for i, (d, p) in enumerate(districts)])
groups = ["0-14", "15-59", "60+"]
ages = [(i, g, s) for i, (g, s) in enumerate((g, s) for g in groups for s in ("M", "F"))]
db.executemany("INSERT INTO dim_age VALUES (?,?,?)", ages)
base = {0: 1900, 1: 480, 2: 960, 3: 820, 4: 600, 5: 55}      # thousands of people, invented
mix = {"0-14": 0.27, "15-59": 0.63, "60+": 0.10}
rows = []
for g, b in base.items():
    for year, mult in ((2011, 1.00), (2021, 1.08)):
        for k, grp, sex in ages:
            rows.append((g, year, k, round(b * mult * mix[grp] * (0.97 if sex == "M" else 1.03) / 2 * random.uniform(0.98, 1.02))))
db.executemany("INSERT INTO fact_pop VALUES (?,?,?,?)", rows)

print("ROLL-UP: persons (thousands) by province and year")
for r in db.execute("""SELECT province, year, SUM(persons) FROM fact_pop f JOIN dim_geo g USING (geo_key)
                       GROUP BY province, year ORDER BY province, year"""):
    print("  %-8s %d %6d" % r)
print("DRILL-DOWN: Bagmati districts, 2021")
for r in db.execute("""SELECT district, SUM(persons) FROM fact_pop f JOIN dim_geo g USING (geo_key)
                       WHERE province='Bagmati' AND year=2021 GROUP BY district"""):
    print("  %-10s %6d" % r)
print("SLICE 2021, DICE age group x province (thousands)")
for r in db.execute("""SELECT province,
        SUM(CASE WHEN age_group='0-14' THEN persons END), SUM(CASE WHEN age_group='15-59' THEN persons END),
        SUM(CASE WHEN age_group='60+' THEN persons END)
        FROM fact_pop f JOIN dim_geo g USING (geo_key) JOIN dim_age a USING (age_key)
        WHERE year=2021 GROUP BY province"""):
    print("  %-8s %6d %6d %6d" % r)
```
```output
ROLL-UP: persons (thousands) by province and year
  Bagmati  2011   2389
  Bagmati  2021   2569
  Gandaki  2011    598
  Gandaki  2021    647
  Karnali  2011     56
  Karnali  2021     59
  Koshi    2011   1780
  Koshi    2021   1924
DRILL-DOWN: Bagmati districts, 2021
  Kathmandu    2057
  Lalitpur      512
SLICE 2021, DICE age group x province (thousands)
  Bagmati     690   1625    254
  Gandaki     176    406     65
  Karnali      16     37      6
  Koshi       517   1215    192
```
Each query is a three-table join with one `GROUP BY`; that is what "analysis-ready" means. The same queries on the operational tables would need dozens of joins and would slow down the services that run on them.

### 4.1.4 Cleaning data in the ETL stage

Government data from different offices disagree on spelling, units and missing values. The program applies the usual transformations to a small raw extract: standard district names, trimming, removing duplicates, rejecting impossible values and reporting each rejection for correction at the source.

```python
raw = [("Kathmandu ", "2021", "1,200"), ("KATHMANDU", "2021", "1200"), ("Katmandu", "2021", "1200"),
       ("Lalitpur", "2021", "-35"), ("Morang", "2021", ""), ("Jhapa", "2021", "980"),
       ("Kaski", "21", "610"), ("Humla", "2021", "55"), ("Humla", "2021", "55")]
alias = {"katmandu": "Kathmandu", "kathmandu": "Kathmandu"}
clean, rejects, seen = [], [], set()
for district, year, persons in raw:
    d = district.strip().title()
    d = alias.get(d.lower(), d)
    p = persons.replace(",", "").strip()
    if not p:
        rejects.append((district, "missing value")); continue
    p = int(p)
    if p < 0:
        rejects.append((district, "negative count")); continue
    y = int(year) + (2000 if len(year) == 2 else 0)
    key = (d, y)
    if key in seen:
        rejects.append((district, "duplicate of %s %d" % key)); continue
    seen.add(key)
    clean.append((d, y, p))
print("loaded %d of %d rows" % (len(clean), len(raw)))
for r in clean:
    print("  load  ", r)
for r in rejects:
    print("  reject", r)
```
```output
loaded 4 of 9 rows
  load   ('Kathmandu', 2021, 1200)
  load   ('Jhapa', 2021, 980)
  load   ('Kaski', 2021, 610)
  load   ('Humla', 2021, 55)
  reject ('KATHMANDU', 'duplicate of Kathmandu 2021')
  reject ('Katmandu', 'duplicate of Kathmandu 2021')
  reject ('Lalitpur', 'negative count')
  reject ('Morang', 'missing value')
  reject ('Humla', 'duplicate of Humla 2021')
```
Two lessons. First, the check *rule* belongs to the data owner, who must repair the source, otherwise the same defects return every month. Second, rejecting is better than guessing: a "fixed" negative count that is wrong is harder to find later than a rejected one.

## 4.2 National data warehouses

A **national data warehouse** is a shared, governed store of a subject on which many agencies and the public rely. The outline names two: **census data** and the **prices of essential commodities**. Both show the pattern: a source collected under law, a standard definition, a time dimension, publication at several levels of detail.

### 4.2.1 Census data

**What it is.** The population and housing census counts every person and household on a reference day. In Nepal the Central Bureau of Statistics (CBS) conducts it every ten years; the 2021 census (2078 BS) counted **29,164,578** people against **26,494,504** in 2011. Because the census covers everyone, it is the frame for sampling, for the allocation of seats and grants, and for the denominators of nearly every rate (births per thousand, enrolment per hundred children).

**Warehouse design.** Facts: persons, households, literacy, disability, migration, housing quality. Dimensions: geography (ward to country, the hierarchy of Figure 4.2), time (census years), sex, age group, caste or ethnic group, mother tongue, religion, occupation. The same cube feeds the planner (how many children of school age in each ward?), the election body (constituency delimitation), the health department (population at risk) and researchers.

**Uses of mining.** Clustering of local levels with similar profiles, to target programmes; prediction of the population for school and hospital planning; detection of out-migration areas; small-area estimates of poverty by combining census and survey data.

The program computes standard census indicators. The annual growth rate of the two national totals uses the exact length of the intercensal period (22 June 2011 to 25 November 2021, 10.43 years), and the age-structure indicators use invented age counts to show the calculation.

```python
import math
p1, p2, t = 26494504, 29164578, 10.43      # 2011 and 2021 totals (CBS), years between the census dates
r = math.log(p2 / p1) / t
print("exponential growth rate : %.2f%% a year" % (100 * r))
print("doubling time           : %.0f years" % (math.log(2) / r))
print("projection to 2031      : %.2f million (same rate, 9.6 more years)" % (p2 * math.exp(r * 9.6) / 1e6))
# Age structure of a (made-up) district, persons
young, adult, old = 310_000, 640_000, 80_000
male, female = 478_000, 552_000
print("\nyouth dependency ratio  : %.1f per 100 adults" % (100 * young / adult))
print("old-age dependency ratio: %.1f per 100 adults" % (100 * old / adult))
print("total dependency ratio  : %.1f per 100 adults" % (100 * (young + old) / adult))
print("sex ratio               : %.1f males per 100 females" % (100 * male / female))
```
```output
exponential growth rate : 0.92% a year
doubling time           : 75 years
projection to 2031      : 31.86 million (same rate, 9.6 more years)

youth dependency ratio  : 48.4 per 100 adults
old-age dependency ratio: 12.5 per 100 adults
total dependency ratio  : 60.9 per 100 adults
sex ratio               : 86.6 males per 100 females
```
A sex ratio far below 100 in a district is a data signal to mine, not a conclusion: in hill districts it usually reflects the **absence of working-age men abroad**, which then explains labour shortages in agriculture and the weight of remittances. The mining step is to link the census cube to labour-migration and household records and test the explanation.

### 4.2.2 Prices of essential commodities

**What it is.** A regular, dated record of the prices of rice, pulses, edible oil, vegetables, milk, fuel and other necessities, collected from markets or wholesale centres. In Nepal the sources include the Department of Commerce, Supplies and Consumer Protection, the Kalimati Fruit and Vegetable Market Development Board (daily wholesale prices), Nepal Rastra Bank's consumer price statistics and CBS.

**Warehouse design.** Fact: price per unit (and quantity). Dimensions: commodity (with unit and grade), market, date (day, week, month, festival season), source. Derived measures: a **consumer price index (CPI)**, inflation rate, regional price gaps.

**Uses.** Inflation and cost-of-living monitoring; price stabilisation and food-security decisions; setting minimum support prices; flood and festival-season warnings; consumer protection against profiteering; the real value of social allowances.

A Laspeyres price index measures the cost of a fixed basket relative to the base period:

$$I_t=\frac{\sum p_t\,q_0}{\sum p_0\,q_0}\times 100$$

The program builds a six-item household basket with invented prices, computes the index and the inflation rate, and then runs a simple **anomaly detector** on a weekly series of a vegetable price: a price above the mean of the previous four weeks by more than two standard deviations is flagged for review (festival demand, a road blockage, or a possible cartel).

```python
import statistics
basket = {   # item: (monthly quantity q0, base price p0, current price pt) in NPR per unit, invented
    "rice (kg)": (40, 90, 108), "lentil (kg)": (6, 190, 215), "vegetables (kg)": (25, 60, 78),
    "cooking oil (litre)": (4, 220, 245), "milk (litre)": (20, 100, 112), "LPG cylinder": (1, 1700, 1900),
}
base_cost = sum(q * p0 for q, p0, pt in basket.values())
now_cost = sum(q * pt for q, p0, pt in basket.values())
index = 100 * now_cost / base_cost
print("basket cost: base NPR %d, now NPR %d" % (base_cost, now_cost))
print("price index: %.1f  -> inflation %.1f%% over the period" % (index, index - 100))
share = {k: 100 * q * pt / now_cost for k, (q, p0, pt) in basket.items()}
top = max(share, key=share.get)
print("largest weight now: %s (%.0f%% of the basket cost)" % (top, share[top]))
series = [62, 64, 63, 65, 66, 64, 67, 95, 92, 70, 68, 66]   # weekly tomato price, NPR/kg, invented
for i in range(4, len(series)):
    w = series[i - 4:i]
    mu, sd = statistics.mean(w), statistics.stdev(w)
    if series[i] > mu + 2 * sd:
        print("week %2d: price %d vs mean of last 4 weeks %.1f (sd %.1f) -> FLAG" % (i + 1, series[i], mu, sd))
```
```output
basket cost: base NPR 10820, now NPR 12680
price index: 117.2  -> inflation 17.2% over the period
largest weight now: rice (kg) (34% of the basket cost)
week  8: price 95 vs mean of last 4 weeks 65.5 (sd 1.3) -> FLAG
```
Note two things. The code flags week 8 but **not week 9**: the spike has already entered the four-week window and inflated its standard deviation, so a real system would use a longer baseline or the median, which a spike cannot distort. And the code does not say *why* the price jumped. The mining output is a question for a market inspector, who may find a festival, a landslide on a highway or a hoarding trader. The warehouse (dated prices by market) is what lets the question be asked in minutes.

## 4.3 Other areas for data warehousing and data mining

Each sector below follows the same four questions: what is the **source**, what are the **facts and dimensions** of its warehouse, what **mining question** pays off, and what is a **typical use**.

| Sector | Sources | Warehouse facts and dimensions | Mining questions | Typical use |
|---|---|---|---|---|
| Agriculture | Crop and livestock statistics, farmer registers, market prices, weather, soil and satellite data | Area, yield, price; by crop, district, season, input | Which areas share yield problems? What price will tomatoes fetch next month? Which farmers miss subsidy? | Advisory by SMS, price forecasts, crop insurance, targeted subsidy |
| Rural development | Local-level plans, allowance and employment-scheme registers, road and water-supply inventories, poverty surveys | Beneficiaries, funds, assets; by ward, scheme, year | Which wards are poor but get little? Which scheme sites stall? Are there duplicate beneficiaries? | Targeting, monitoring of payments, social audit |
| Health | Facility reports (HMIS using DHIS2 in Nepal), immunisation and maternal records, laboratory reports | Cases, visits, stock; by facility, disease, month, age | Early outbreak signals, facilities with stock-outs, high-risk pregnancies | Surveillance, vaccine planning, drug supply |
| Planning | Census, surveys, national accounts, budget and project data | Indicators, spending, results; by sector, district, year | Which districts lag on several goals at once? Does spending change outcomes? | Resource allocation, monitoring of national plans and the SDGs |
| Education | School census and flash reports, examination results, teacher records, scholarship data | Enrolment, pass rate, teachers; by school, grade, sex, year | Which schools lose girls after grade 8? Link between teacher numbers and results | Teacher deployment, dropout alerts, scholarships |
| Commerce and trade | Customs declarations, company and tax registers, price data, remittance flows | Value, quantity, duty; by product code, country, border point, month | Under-invoicing patterns, risky consignments, export potential | Risk-based customs inspection, trade policy |
| Other sectors | Tax returns, police and court records, vehicle registers, land transactions, disaster reports | Cases, revenues, incidents; by place, type, time | Tax non-filers; accident black-spots; flood-prone settlements | Tax compliance, road safety, disaster preparedness |

**Data mining in one sentence each.** *Classification* assigns a record to a known class (will this declaration need inspection?). *Clustering* groups similar records without labels (districts with similar profiles). *Association analysis* finds items that occur together (services used in one visit). *Anomaly detection* finds records unlike the rest (a price spike, a suspicious bid). *Forecasting* projects a series (demand, revenue, cases). The knowledge-discovery steps are: select data, clean and transform, mine, **interpret and validate with domain experts**, act.

### 4.3.1 Clustering districts for targeting

The planning commission wants to group districts by two indicators (adult literacy and health posts per 10,000 people) so that a single package fits each group. The program standardises the indicators (so that one scale does not dominate) and runs k-means with three clusters on twelve invented districts.

```python
import numpy as np
names = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"]
X = np.array([[88, 3.1], [85, 2.8], [90, 3.4], [62, 1.2], [58, 1.0], [65, 1.5],
              [60, 2.9], [57, 3.2], [63, 3.0], [80, 1.1], [78, 1.4], [82, 1.2]], dtype=float)   # literacy %, posts per 10,000
Z = (X - X.mean(0)) / X.std(0)
centres = Z[[0, 3, 6]].copy()                      # fixed starting points so the run is repeatable
for it in range(20):
    d = ((Z[:, None, :] - centres[None]) ** 2).sum(2)
    lab = d.argmin(1)
    new = np.array([Z[lab == k].mean(0) for k in range(3)])
    if np.allclose(new, centres):
        break
    centres = new
for k in range(3):
    m = X[lab == k]
    print("cluster %d: %-22s mean literacy %.1f%%, posts %.1f per 10,000" %
          (k, ",".join(n for n, l in zip(names, lab) if l == k), m[:, 0].mean(), m[:, 1].mean()))
print("iterations:", it + 1)
```
```output
cluster 0: D1,D2,D3               mean literacy 87.7%, posts 3.1 per 10,000
cluster 1: D4,D5,D6,D10,D11,D12   mean literacy 70.8%, posts 1.2 per 10,000
cluster 2: D7,D8,D9               mean literacy 60.0%, posts 3.0 per 10,000
iterations: 2
```
Reading the clusters as a planner: cluster 0 (D1 to D3) has high literacy and good health coverage and needs the least; cluster 1 (six districts) has the weakest health coverage, 1.2 posts per 10,000, although its literacy ranges from 58 to 82 per cent, so a health-infrastructure package fits; cluster 2 (D7 to D9) has good health coverage but the lowest literacy, so an education and adult-literacy package fits. Without the clustering a single national programme would be an average that fits nobody.

### 4.3.2 Association analysis of service use

At a municipal one-stop counter, a log records which services each citizen used in one visit. Association rules reveal which services to place together or to offer in one online flow. For a rule A -> B: *support* is the share of visits containing both, *confidence* is the share of A-visits that also contain B, and *lift* is confidence divided by the share of B-visits (lift above 1 means a real association).

```python
from itertools import combinations
visits = [{"birth cert", "citizenship rec"}, {"citizenship rec", "tax clearance"}, {"birth cert", "citizenship rec", "ward rec"},
          {"business reg", "tax clearance"}, {"citizenship rec", "ward rec"}, {"birth cert", "citizenship rec"},
          {"business reg", "tax clearance", "ward rec"}, {"tax clearance"}, {"birth cert", "ward rec"}, {"citizenship rec", "ward rec"}]
n = len(visits)
items = sorted(set().union(*visits))
sup = lambda s: sum(1 for v in visits if s <= v) / n
rules = []
for a, b in combinations(items, 2):
    for x, y in ((a, b), (b, a)):
        s_xy = sup({x, y})
        if s_xy >= 0.3:
            conf = s_xy / sup({x})
            rules.append((conf / sup({y}), conf, s_xy, x, y))
for lift, conf, s, x, y in sorted(rules, reverse=True):
    print("%-15s -> %-15s support %.2f confidence %.2f lift %.2f" % (x, y, s, conf, lift))
```
```output
citizenship rec -> birth cert      support 0.30 confidence 0.50 lift 1.25
birth cert      -> citizenship rec support 0.30 confidence 0.75 lift 1.25
ward rec        -> citizenship rec support 0.30 confidence 0.60 lift 1.00
citizenship rec -> ward rec        support 0.30 confidence 0.50 lift 1.00
```
The strongest pair is birth certificate and citizenship record (lift 1.25; 75 per cent of birth-certificate visits also ask for the citizenship record), so one combined form and one payment would save a second visit. Note the *minimum support* of 0.3: without it the code lists accidental pairs of one or two visits.

## 4.4 Privacy, ethics and governance of government data

A warehouse that links many registers is a strong tool and a strong risk. Linkage lets planners see a district in full; it also lets an intruder or an insider see a person in full.

- **Purpose limitation and legal basis**: data are used for the purpose they were given for, under law (in Nepal, the Individual Privacy Act and the RTI Act set the frame; check the current rules).
- **Minimisation and aggregation**: planners need rates by ward, not names; publish aggregates and release microdata only under controlled access.
- **De-identification and k-anonymity**: a released table is *k-anonymous* if every combination of quasi-identifiers (age band, sex, ward) is shared by at least k people. Small groups must be merged or hidden.
- **Access control and audit**: role-based access, logs of who queried what, regular review.
- **Fairness**: models trained on past decisions inherit past bias; test results by gender, caste, region and income before using a score to allocate benefits, and keep a human appeal.
- **Transparency**: tell citizens which data are held and how decisions based on them are made.

```python
from collections import Counter
rows = [("20-29", "F", "Ward 1"), ("20-29", "F", "Ward 1"), ("20-29", "M", "Ward 1"), ("30-39", "M", "Ward 2"),
        ("30-39", "M", "Ward 2"), ("30-39", "F", "Ward 2"), ("60-69", "F", "Ward 3"), ("40-49", "M", "Ward 3")]
def k_of(table):
    return min(Counter(table).values())
print("k before generalising:", k_of(rows))
small = [g for g, c in Counter(rows).items() if c < 2]
print("groups of size 1:", small)
# generalise: widen age bands to 30 years and drop sex for the small groups' wards
gen = []
for a, s, w in rows:
    band = {"20-29": "20-39", "30-39": "20-39", "40-49": "40-69", "60-69": "40-69"}[a]
    gen.append((band, w if w != "Ward 3" else "Wards 3", "*"))
print("k after generalising :", k_of(gen))
```
```output
k before generalising: 1
groups of size 1: [('20-29', 'M', 'Ward 1'), ('30-39', 'F', 'Ward 2'), ('60-69', 'F', 'Ward 3'), ('40-49', 'M', 'Ward 3')]
k after generalising : 2
```
The price of privacy is lost detail; the skill is to lose just enough. Each release of a table should state its k and the generalisation applied.

## 4.5 Summary and exercises

**Summary.** A data warehouse integrates historical data from operational (OLTP) systems into a subject-oriented, time-variant, non-volatile store designed for analysis (OLAP) through a star schema; ETL extracts, transforms and loads. Data mining adds classification, clustering, association, anomaly detection and forecasting. National warehouses such as census data (CBS, 2021 count 29,164,578) and prices of essential commodities (CPI, inflation, market price series) serve planning and policy. The same approach applies to agriculture, rural development, health, planning, education, commerce and trade, taxation, police and disasters. The risks are privacy, bias and misuse, handled by purpose limitation, minimisation, k-anonymity, access control and transparency.

1. Differentiate OLTP and a data warehouse. List the four properties of a warehouse.
2. Draw and explain the architecture of a government data warehouse.
3. What are ETL steps? Give four typical transformations of government data.
4. Draw a star schema for the prices of essential commodities (fact and three dimensions). Name two OLAP operations on it.
5. Explain the role of census data as a national data warehouse. Which dimensions and which uses?
6. Nepal's population was 26,494,504 in 2011 and 29,164,578 in 2021 (10.43 years apart). Compute the annual exponential growth rate and the doubling time.
7. Define the Laspeyres price index. Compute it for a basket with base cost NPR 5,000 and current cost NPR 5,600, and give the inflation rate.
8. A weekly price series reads 40, 42, 41, 43 and then 60. Is 60 flagged by the two-standard-deviation rule on the previous four weeks (use the sample standard deviation)?
9. Explain five uses of data warehousing and mining in agriculture, health or education.
10. Define support, confidence and lift. For 100 visits, A occurs in 40, B in 50 and both in 30, compute the three measures of A -> B.
11. A district has 200,000 children (0-14), 500,000 adults (15-59) and 50,000 older people. Compute the total dependency ratio.
12. Explain k-means clustering with a district example and say why indicators are standardised.
13. List five privacy safeguards for a national data warehouse. What is k-anonymity?
14. Discuss the benefits and risks of linking census, tax and health data.
15. Write notes on the use of data mining in commerce and trade (customs).

**Answers to the numerical items.** (6) r = ln(29,164,578 / 26,494,504)/10.43 = ln(1.10078)/10.43 = 0.09600/10.43 = **0.92 per cent a year**; doubling time = ln 2 / r = 0.6931/0.00920 = **about 75 years**. (7) Index = 5,600/5,000 x 100 = **112**, inflation **12 per cent**. (8) Mean of the four = 41.5; sample sd = 1.29; mean + 2 sd = 44.1; 60 exceeds it, so **yes, it is flagged**. (10) Support = 30/100 = **0.30**; confidence = 30/40 = **0.75**; lift = 0.75/0.50 = **1.5**. (11) (200,000 + 50,000)/500,000 = **0.50, i.e. 50 dependents per 100 adults**.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is a data warehouse? How does it differ from an operational database?**

A data warehouse is a subject-oriented, integrated, time-variant and non-volatile collection of data that supports management decisions. It differs from an operational (OLTP) database in purpose (analysis, not daily transactions), content (historical, integrated across sources, not current and single-application), design (star schema with few joins, not normalised tables), update pattern (batch loading, no changes after loading) and users (planners and analysts, not clerks). Government example: a warehouse of births by ward and year answers trend questions that the birth-registration system cannot answer quickly.

**Q2 (5 marks). Explain census data as a national data warehouse.**

The census counts all persons and households on a reference day, under law, at intervals of ten years. As a warehouse it has facts (persons, households, literacy, disability, migration) and dimensions (geography from ward to country, time, sex, age, caste or ethnicity, language, occupation). It supplies denominators for rates, the frame for surveys, constituency delimitation and grant formulas, school and health planning, and (with mining) clustering of areas and small-area poverty estimates. Control needs: confidentiality of individual records, consistent definitions between censuses and publication of aggregates at ward level.

**Q3 (10 marks). Explain the application of data warehousing and data mining in government sectors: agriculture, health, education and commerce.**

Introduce the warehouse and mining tasks. For each sector give source data, warehouse facts and dimensions, a mining question and a use, following the table in 4.3: agriculture (yield and price by crop, district and season; price forecasting, advisory, targeted subsidy), health (facility reports in the HMIS; outbreak signals, stock-outs, high-risk pregnancy), education (enrolment, pass rate, teachers by school; dropout alerts, teacher deployment), commerce and trade (customs declarations by product, country and border; risk-based inspection, under-invoicing patterns). Add one example result (clusters of districts, an anomaly flag or an association rule), the requirement to validate with domain experts, and the privacy and fairness controls.

**Q4 (10 marks). Discuss the issues in using data mining in government and how they can be controlled.**

Issues: privacy and linkage risk; misuse of data for purposes other than collected; poor data quality leading to wrong conclusions; bias in models trained on past decisions; opaque scores that citizens cannot challenge; security of a single large store; dependence on vendors; weak skills. Controls: legal basis and purpose limitation; data minimisation and aggregation; de-identification with a stated k; access control, logging and audit; data-quality rules owned by data custodians; testing for bias by group and a human appeal route; transparency about what is held and how decisions are made; security measures and back-up; open standards and capacity building. Close with the principle that mining output is a question for experts to investigate, not a verdict.
