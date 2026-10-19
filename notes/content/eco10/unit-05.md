---
subject: Economics
grade: 10
unit: 5
title: Nepal's Economy (नेपालको अर्थतन्त्र)
hours: 15
area: Nepal's Economy
---

This unit looks at Nepal itself, sector by sector. Four sectors carry the country: **agriculture**, which still employs most Nepalis; **industry**, which is small and struggles to compete; **tourism**, which earns foreign exchange from the mountains, the culture and the pilgrimage sites; and **foreign employment**, which earns more foreign exchange than everything else put together and has changed Nepali villages more than any policy of the last thirty years. For each one, the same four questions are asked: what is its role, what are its features, what are its problems, and what are its prospects.

::: key What the examiner tests here
Group A asks: "What is the contribution of agriculture to Nepal's GDP?", "Write any two features of Nepali agriculture", "What is a cottage industry?", "Write any two problems of tourism in Nepal", "What is meant by foreign employment?". Group B asks for the role, features, problems and prospects of any one of the four sectors — this is the most predictable Group B question in the paper. Group C may ask for the same at length, or for the role of remittance in the Nepali economy. Learn each sector as **role, features, problems, prospects**, four short paragraphs of which any two are worth five marks.
:::

## 5.1 Agriculture

**Role and importance.** Agriculture is the backbone of the Nepali economy, and its importance is out of all proportion to its share of output.

1. **Contribution to GDP.** Agriculture and its related activities provide roughly a fifth to a quarter of the country's Gross Domestic Product.
2. **Employment.** It employs about three-fifths of the working population — by far the largest employer in the country. It is also, in the hills, the only employer the village has.
3. **Food supply.** It feeds the population and supplies the raw materials of the agro-processing industry — rice, wheat, maize, millet, oilseed, sugar cane, jute, tea, coffee, ginger, cardamom, tobacco.
4. **Foreign exchange.** Tea, coffee, ginger, cardamom, lentils, pulses, hides and essential oils are exported, and several of them are among Nepal's few competitive exports.
5. **Market for industry.** The rural population is the market for the goods that industry makes — fertiliser, tools, cloth, bicycles, processed food.
6. **Capital and labour for other sectors.** Agriculture supplies the saving, the labour and the food that let industry and services grow. If agriculture is stagnant, the rest of the economy starves.
7. **Way of life.** It carries the culture, the festivals and the settlement pattern of the country, and it is the sector to which hundreds of thousands of migrant workers return.

**Features.** Subsistence farming, with most of the produce consumed by the household; small and **fragmented** holdings, averaging less than a hectare and often split into several scattered plots; heavy **dependence on the monsoon**, with only about a third of the cultivated area under assured irrigation; **low productivity** per hectare and per worker; **traditional technology** — the wooden plough, hand tools, animal power, farmyard manure; a **dual structure**, with a large low-yielding subsistence sector and a small commercial sector producing tea, coffee, cardamom, ginger and vegetables for the market; **unequal distribution of land**; and a large number of people **under-employed** on the land, whose departure would not reduce output.

**Problems.** Low productivity per hectare and per worker; the risk of the monsoon and the small share of irrigated land; small and fragmented holdings with no scope for machinery; the high cost of inputs — seed, fertiliser, pesticide, fuel — and the shortage of timely credit; the poor condition and high cost of roads, storage and market yards in the hills; the **middleman**, who takes a large share of the price the consumer pays; weak extension and training services, so that improved varieties and techniques do not reach the farmer; the low price the farmer receives and the poor market information he has; land fragmentation and the growing number of unviable holdings; the shortage and rising cost of farm labour, since the young have gone abroad; the loss of fertile land to housing and roads in the Terai; and the damage done by floods, landslides, hailstorms and drought.

**Land reform.** Land reform means the state's intervention to change the ownership and use of agricultural land, so that the cultivator owns more of what he tills. Its **objectives** are to end absentee landlordism and exploitation, to give land to the tiller, to reduce inequality, to raise production by making the farmer secure and able to invest, and to create a market in land.

In Nepal land reform began with the abolition of the **Birta** system in 2019 B.S. and the **Zamindari** system, and the **Land Reform Act, 2021 B.S. (1964 A.D.)** introduced a ceiling on holdings, security of tenure for tenants, and redistribution of surplus land. Its results were partial: the **ceiling was evaded** by transferring land to relatives, the **tenancy records were manipulated** so that many real tenants were recorded as ordinary cultivators, the redistribution was small, and **scientific land reform** — land consolidation, cooperative farming, proper tenancy records on the land information system — still remains largely unfinished.

**Prospects.** Assured irrigation; improved seed, balanced fertiliser and the timely supply of both; agricultural **marketing** through cooperatives, contract farming and cold storage; **high-value crops** — tea, coffee, ginger, cardamom, vegetables, fruit, dairy — for the domestic market and for export; **agro-processing** industry to add value where it is grown; agricultural **insurance** against crop loss; land consolidation and cooperative farming; and agricultural **credit** at reasonable rates through the Agricultural Development Bank and cooperatives.

```photo id="eco10/terraces" caption="Terrace farming in Ramechhap. Steep land, small plots and heavy dependence on the monsoon describe Nepali agriculture better than any table does." width="84"
```

```figure caption="Nepal's sectoral structure. Agriculture still employs about three-fifths of the workers while producing only about a quarter of output — the widest such gap in the economy."
import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots(figsize=(5.0,2.6))
sectors = ["Agriculture","Industry","Services"]
gdp = [24, 14, 62]
emp = [60, 15, 25]
x = np.arange(3); w = 0.36
ax.bar(x-w/2, gdp, w, color=ACCENT, label="Share of GDP (%)")
ax.bar(x+w/2, emp, w, color=SERIES[1], label="Share of employment (%)")
ax.set_xticks(x); ax.set_xticklabels(sectors, fontsize=7.5, color=INK)
ax.set_ylabel("Per cent", color=INK)
ax.set_ylim(0,72)
for i,(a,b) in enumerate(zip(gdp,emp)):
    ax.text(i-w/2,a+1.5,str(a),ha='center',fontsize=6.4,color=INK)
    ax.text(i+w/2,b+1.5,str(b),ha='center',fontsize=6.4,color=INK)
ax.grid(color=GRID, lw=0.5, axis='y'); ax.spines[['top','right']].set_visible(False)
ax.legend(fontsize=6.4, frameon=False)
```

::: example Agriculture in the economy
**Problem.** In a year Nepal's GDP was Rs. 4,800 billion, of which agriculture contributed Rs. 1,152 billion. The employed labour force was 16 million, of whom 9.6 million worked in agriculture. Find (a) agriculture's share of GDP, (b) agriculture's share of employment, (c) the average output per worker in the whole economy and (d) the average output per worker in agriculture. What does the comparison show?

**Solution.**
Step 1 — $Share\ of\ GDP = \frac{1{,}152}{4{,}800} \times 100 = 24\%$.
Step 2 — $Share\ of\ employment = \frac{9.6}{16} \times 100 = 60\%$.
Step 3 — Whole economy, output per worker $= \frac{4{,}800\ billion}{16\ million} = Rs.\ 3{,}00{,}000$.
Step 4 — Agriculture, output per worker $= \frac{1{,}152\ billion}{9.6\ million} = Rs.\ 1{,}20{,}000$.
Step 5 — Compare: the average agricultural worker produces Rs. 1,20,000 while the average worker in the rest of the economy produces $\frac{4{,}800 - 1{,}152}{6.4\ million} = Rs.\ 5{,}70{,}000$ — nearly five times as much.

**Answer.** (a) 24 %, (b) 60 %, (c) Rs. 3,00,000, (d) Rs. 1,20,000; the agricultural worker produces about a fifth of what a worker outside agriculture produces.
**What it means.** Nine and a half million people are working very hard for very little, because each of them has too little land, too little water and too little capital. Raising agricultural productivity is not a separate problem from reducing poverty; it is the same problem.
:::

## 5.2 Industry

**Role and importance.** Industry manufactures goods, and manufactures are the fastest route to higher productivity and higher wages. Industry provides **employment** for the labour that agriculture cannot absorb; **higher value added** than the sale of raw material; **diversified exports** and so relief from the trade deficit; **raw material demand** that gives the farmer a market for tea, milk, sugar cane and jute; **foreign exchange**; **linkages** with transport, banking, insurance and trade; **technological skill** and the training of the workforce; and **balanced regional development** when it is spread beyond Kathmandu.

**Types.** By size, industry is **cottage and small**, **medium** and **large**. By raw material or product, Nepal's common classes are **agro-based** (rice, oil, sugar, tea, dairy, fruit processing, jute), **forest-based** (timber, furniture, plywood, paper), **mineral-based** (cement, brick, lime, slate), **energy-based** (electricity, LPG bottling), **tourism-based** (handicrafts, curio, trekking equipment, hotel and food), **construction-based** (metal and fabricated products, pipes) and **textile-based** (garments, pashmina, woollen carpets).

**Cottage and small industries** deserve separate mention. They need little capital, use local raw material and local skill, can be set up anywhere, create employment at low cost, keep artisan skills alive, and spread earnings across regions. Nepal's handicrafts, pashmina, carpets, pottery, metalwork, handloom cloth, incense and *dhaka* cloth are its recognised strength.

**Regulation and policy.** The **Industrial Enterprises Act** protects and promotes investment and classifies enterprises; the **Foreign Investment and Technology Transfer Act** governs foreign investment; **special economic zones** (as at Bhairahawa) offer infrastructure and facilities to export industries; and industrial policy aims at export promotion, import substitution where it is economic, small and cottage industry promotion, agricultural and tourism linkages, and balanced regional development.

**Problems.** Shortage of capital and the high cost of borrowing; out-dated technology, because machinery must be imported and few firms can afford the latest; irregular supply and high cost of energy; the high cost of transport, worsened by being landlocked; the shortage of skilled labour and of technical education; raw material that must be imported, and dependence on India for it; a small domestic market with low purchasing power; **stiff competition** from Indian and Chinese goods and smuggling across the open border; labour unrest and industrial disputes; weak marketing, branding and quality certification; bureaucratic delay and frequent policy change; and the crowding of industry into Kathmandu and the Terai while the hills get little.

**Prospects.** Hydroelectricity to end the power constraint and to make electricity itself an export; **Special Economic Zones** and industrial corridors; **agro-processing** built on Nepali tea, coffee, ginger, cardamom, fruit, herbs and milk; cement, hydro equipment, steel fabrication and construction materials for the home market and for export; commercialisation of **herbal and traditional medicine** and of handicrafts; skill development and technical education to supply the workers industry needs; and simplification of registration, taxation and customs.

```photo id="eco10/tea" caption="A tea garden in Ilam. Tea is Nepal's clearest industrial success story: a hill crop, processed locally as orthodox tea, and sold abroad — agriculture and industry together." width="82"
```

## 5.3 Tourism

**Role and importance.** Tourism sells a country's mountains, culture and hospitality to people who live somewhere else. For Nepal its importance is very great.

1. **Foreign exchange** — a tourist spends in foreign currency inside Nepal, so tourism is an export that needs no ship and no port. For a landlocked country, that is unusual and valuable.
2. **Employment** — it employs hotel and restaurant staff, trekking guides, porters, cooks, drivers, shopkeepers, travel agents, and — indirectly — farmers who sell vegetables and milk, and artisans who make handicrafts. Much of the employment is in areas that have little else.
3. **Income for remote areas** — the trekking routes of Solukhumbu, Manang, Mustang, Langtang, Annapurna and Dolpa are among the few places where money comes from outside.
4. **Linkage effects** — it builds hotels, roads and airports, and it creates a market for handicrafts, agriculture and transport.
5. **Promotion of art, culture and heritage** — the temples, stupas, festivals and crafts of Kathmandu, Lumbini, Janakpur and the districts are protected partly because visitors come to see them.
6. **Balance of payments** — tourism receipts are one of the few sizeable items in the invisibles of the current account.

**Features.** Nepal's tourism is based on **mountains**, **trekking and mountaineering**, **religious pilgrimage** (Pashupatinath, Lumbini, Janakpur, Muktinath, Gosainkunda, Pathibhara), **culture and heritage** (the Kathmandu valley's world heritage sites), and **adventure sports** (rafting, paragliding, bungee, jungle safari in Chitwan and Bardia). It is **seasonal**, with two peak seasons; it is **concentrated** on a few routes and on Kathmandu, Pokhara and Chitwan; it is **small in scale**, with tourist arrivals in the low hundreds of thousands a year against millions in comparable destinations; and it earns far less per visitor than it could, because visitors spend fewer nights and less money than in competing countries.

**Problems.** Poor air connectivity and few direct international flights, so that many visitors enter through India; inadequate and expensive internal transport; shortage of good hotels, resorts and trained staff outside the main centres; poor sanitation, waste management and trail maintenance; the **seasonality** that leaves the industry idle for months; weak marketing and promotion abroad; the dominance of Indian visitors, so that earnings are low and unsteady; the lack of a **tourism policy that is actually implemented** and of coordination among government, the private sector and local communities; safety concerns — air crashes, road accidents, strikes — which discourage bookings; the leakage of earnings to foreign-owned hotels and airlines; and the **environmental damage** that mass trekking can cause to trails, forests and mountain ecosystems.

**Prospects.** Diversification beyond trekking — health and wellness tourism, yoga and meditation, adventure sports, homestay tourism, village and community tourism, festivals and events, the Great Himalaya Trail, mountain biking, and religious circuits; effective **marketing** in Europe, China, Korea, Japan and the Gulf; direct air links and an improvement of Tribhuvan and Gautam Buddha airports; **community homestays** so that the money stays in the village; **training** in hospitality, guiding and languages; **conservation** of heritage, trails and parks; and **regional and seasonal spread** with new destinations such as Karnali, Sudurpashchim and the eastern hills.

```photo id="eco10/phewa" caption="Phewa Lake, Pokhara. Tourism is Nepal's most valuable invisible export: the visitor spends foreign currency inside the country, and no port is needed." width="84"
```

```photo id="eco10/ama-dablam" caption="Ama Dablam, seen from near Pheriche on the Everest trail. The mountain is the resource; the guided trek, the lodge and the porter are the industry built on it." width="80"
```

::: example The weight of tourism
**Problem.** In a year Nepal received 1,200,000 foreign visitors, each staying on average 12 days and spending on average 45 US dollars a day. The exchange rate was Rs. 133 to one US dollar. Take the country's GDP as Rs. 4,800 billion and merchandise exports as Rs. 250 billion. Find (a) gross tourist spending in rupees, (b) its value as a percentage of GDP, and (c) how it compares with merchandise exports.

**Solution.**
Step 1 — Total visitor-days $= 1{,}200{,}000 \times 12 = 14{,}400{,}000$ days.
Step 2 — Gross spending in dollars $= 14{,}400{,}000 \times 45 = 648{,}000{,}000$ US dollars.
Step 3 — In rupees $= 648{,}000{,}000 \times 133 = Rs.\ 86{,}184$ million, that is about **Rs. 86.2 billion**.
Step 4 — $Share\ of\ GDP = \frac{86.2}{4{,}800} \times 100 = 1.8\%$.
Step 5 — Compared with merchandise exports of Rs. 250 billion, tourist spending is about **34 per cent** of the goods Nepal exports.

**Answer.** Rs. 86.2 billion; 1.8 % of GDP; about a third of merchandise exports.
**What it means.** Tourism is important but not yet transformative. Doubling the average stay or the daily spend would add more to the economy than several new export factories, which is why length of stay and spending per visitor matter more than the headline number of arrivals.
:::

## 5.4 Foreign employment

**Foreign employment (वैदेशिक रोजगारी)** means the employment of Nepali citizens in a foreign country. In thirty years it has become the largest single source of foreign exchange in Nepal and the largest single influence on village life.

**Role and importance.**

1. **Remittance.** The money that migrant workers send home is the country's largest source of foreign exchange — roughly a quarter of the Gross Domestic Product. It has kept the balance of payments in surplus despite a huge trade deficit.
2. **Employment for the surplus labour force.** The domestic economy cannot create jobs fast enough for the young people who enter the labour market each year; foreign employment absorbs them and relieves open unemployment and under-employment at home.
3. **Poverty reduction.** Remittance is money received directly by households, and a large part of it goes to consumption, health, education and housing. It has done more to lift household living standards than any single public programme.
4. **Foreign exchange reserves and the exchange rate.** The steady inflow keeps the reserves comfortable and stabilises the rate.
5. **Capital and investment at home.** Remittance finances land, houses, education, small shops, transport, and cooperative and bank deposits, which are then available for lending.
6. **Skill acquisition.** Workers abroad learn trades, machinery, discipline and languages, and some bring both skill and capital back with them.
7. **Relief of the pressure on land and public services**, as the number of people depending on a fixed area of farmland falls.

**Features.** Destinations are dominated by **Malaysia and the Gulf states** (Qatar, Saudi Arabia, the UAE, Kuwait, Bahrain, Oman), with smaller numbers in Korea (under the EPS scheme), Japan, Israel, Europe, Australia and the United States. Most migrants are **unskilled or semi-skilled**, going for two to three years on contracts; a minority are professionals and students. The flow is **large and continuous**, with more than half a million labour permits issued in a year in recent years. The migrant is usually **male, young and from a rural district**, and the strongest migration districts are in the eastern hills, the mid-west and the far-west. Remittance is used mainly for **consumption, education, health, repayment of the loan taken to go, house construction and land purchase**.

**Problems.** **Recruitment costs and debt** — a worker often borrows Rs. 1.5 to 2 lakh to pay an agent, and repays it from his first year's earnings. **Exploitation** by unlicensed manpower agencies, with false promises of wages and jobs. **Unsafe work and accidents**, illness, and deaths that are neither compensated nor properly investigated; and the difficulty of bringing the body, or the wages, home. **Low wages and long hours** in jobs for which the worker had no training. **Skill mismatch** — the jobs are unskilled, so no skill is gained. **Social costs at home**: wives left to run the household alone, children without a parent, the neglect of the elderly, and increasing alcoholism and family breakdown. **Agricultural neglect**, because the young men who would farm have gone. **Brain drain**, when educated and well-trained Nepalis settle abroad. **Fraudulent agents and an ineffective regulation** of the recruitment business. **Miserable conditions at the destination** and, in some countries, the withholding of passports and wages by the employer. And **reintegration difficulties** for those who return with money but no skill, no plan and no business.

**Prospects.** **Skill-based migration** — training Nepali workers as masons, plumbers, welders, electricians, drivers, nurses and caregivers *before* they go, so that they earn three or four times as much; **bilateral labour agreements** with destination countries to fix wages and conditions; **strict regulation and prosecution** of fraudulent manpower agencies; a **single and honest recruitment charge**; **insurance and a welfare fund** for migrant workers, with a compensation mechanism; **consular support** and a help desk in every destination country; **financial literacy** so that remittance is invested rather than consumed; **reintegration programmes** to help returnees set up enterprises; and the development at home of the jobs that would let young people stay.

```photo id="eco10/porter" caption="A porter on the trail above Namche. Foreign employment is not only the Gulf and Malaysia: trekking work is the same phenomenon in a different form — a Nepali selling his labour abroad for foreign currency, close to home." width="76"
```

::: example Remittance and the economy
**Problem.** In a year Nepal received remittance of Rs. 1,220 billion. The Gross Domestic Product was Rs. 4,800 billion and merchandise exports were Rs. 250 billion while merchandise imports were Rs. 1,320 billion. Find (a) remittance as a percentage of GDP, (b) the trade deficit, and (c) what the trade deficit would have done to the foreign exchange reserves if there had been no remittance.

**Solution.**
Step 1 — $Remittance\ as\ a\ share\ of\ GDP = \frac{1{,}220}{4{,}800} \times 100 = 25.4\%$.
Step 2 — $Trade\ deficit = imports - exports = 1{,}320 - 250 = Rs.\ 1{,}070$ billion.
Step 3 — Without remittance, the current account would show a deficit of about Rs. 1,070 billion (before services and other transfers) instead of a small surplus of about Rs. 150 billion.
Step 4 — That deficit would have had to be financed by **borrowing abroad or running down the reserves** — and given the level of reserves, the reserves would have been exhausted in about a year.

**Answer.** (a) 25.4 % of GDP; (b) a trade deficit of Rs. 1,070 billion; (c) without remittance the deficit would swamp the reserves and force foreign borrowing or a sharp devaluation.
**What it means.** Remittance is not a comfort; it is the single item that makes Nepal's external accounts add up. That is also its danger: if a destination country changes its labour policy, the shock reaches every district in the country at once.
:::

::: caution The common mistake
"Agriculture contributes most to Nepal's GDP, because most people work in it" is wrong on two counts. Agriculture employs about three-fifths of the workers but produces only about a quarter of GDP — the **service sector contributes the largest share of output**. Getting the shares of *employment* and *output* the right way round is the commonest single error in answers on the Nepali economy. A second error is to treat remittance as development: it raises household consumption, which is real and important, but unless it is invested it does not raise the country's productive capacity.
:::

## Chapter summary

- **Agriculture** contributes about a fifth to a quarter of GDP while employing about three-fifths of the workers. Its importance lies in food, employment, raw material for agro-processing, exports, the market it provides to industry and the saving and labour it releases. Its features are subsistence farming, small and fragmented holdings, dependence on the monsoon, low productivity, traditional technology, a dual commercial and subsistence structure and unequal land ownership. Its problems are low yields, unirrigated land, small holdings, costly inputs and credit, poor roads and markets, the middleman, weak extension and the loss of fertile land. **Land reform** — abolition of Birta and Zamindari, and the **Land Reform Act, 2021 B.S.** with ceilings, tenancy security and redistribution — achieved only part of its aim, and scientific land reform remains unfinished. Prospects: irrigation, improved seed, high-value crops, marketing and cooperatives, agro-processing, insurance and credit.
- **Industry** provides employment, value added, diversified exports, a market for farm produce, linkages and skills. It is classified by size (cottage, small, medium, large) and by raw material. **Cottage and small industries** need little capital, use local material and skill and spread employment. Its problems are capital shortage, old technology, costly and irregular energy, high transport cost, shortage of skilled labour, imported raw material, a small market, competition and smuggling from India and China, labour unrest, weak marketing and bureaucratic delay. Prospects: hydropower, special economic zones, agro-processing, cement and construction materials, herbal products and handicrafts, and skill development.
- **Tourism** brings foreign exchange without needing a port, employs guides, porters, hotel staff, drivers and artisans — much of it in remote areas — builds infrastructure and helps preserve heritage. It is based on mountains, trekking, pilgrimage and culture; it is seasonal and concentrated; and its problems are poor air links, weak infrastructure, shortage of hotels and trained staff, sanitation, seasonality, weak marketing, dependence on Indian visitors, safety concerns, leakage of earnings and environmental damage. Prospects: diversification, community homestays, training, better air links, marketing abroad and regional spread.
- **Foreign employment** and **remittance** are the largest source of foreign exchange — about a quarter of GDP — and the main reason Nepal's external accounts balance despite a trade deficit several times its exports. Remittance reduces poverty, finances consumption, education, health, housing and small business, and relieves unemployment at home. Its problems are recruitment debt and exploitation, unsafe work, accidents and deaths, unskilled jobs, social costs at home, agricultural neglect, brain drain and difficult reintegration. Prospects: skill-based migration, bilateral agreements, strict regulation of agencies, insurance and a welfare fund, consular support, financial literacy, reintegration programmes and the creation of jobs at home.
- The two figures to keep straight: **agriculture employs about 60 per cent of the workers but produces about 24 per cent of output**, and **remittance is about a quarter of GDP and is what makes the balance of payments add up**.

## Practice questions

**Group A — Very short answer (1 mark each)**

1. What is the contribution of agriculture to Nepal's GDP? <span class="marks">[1]</span>
2. Write any two features of Nepali agriculture. <span class="marks">[1]</span>
3. What is a cottage industry? <span class="marks">[1]</span>
4. Write any two problems of the industrial sector in Nepal. <span class="marks">[1]</span>
5. Write any two importance of tourism in Nepal. <span class="marks">[1]</span>
6. Write any two problems of tourism in Nepal. <span class="marks">[1]</span>
7. What is meant by foreign employment? <span class="marks">[1]</span>
8. Write any two destinations of Nepali migrant workers. <span class="marks">[1]</span>
9. What is remittance? <span class="marks">[1]</span>
10. Write any two uses of remittance by a Nepali household. <span class="marks">[1]</span>
11. What is land reform? <span class="marks">[1]</span>
12. Write any two importance of agriculture in Nepal. <span class="marks">[1]</span>

::: note Answers to Group A
**1.** Roughly a fifth to a quarter of the Gross Domestic Product (and it employs about three-fifths of the working population).
**2.** Any two of: subsistence farming; small and fragmented holdings; heavy dependence on the monsoon; low productivity; traditional technology; unequal ownership of land; a dual subsistence and commercial structure.
**3.** A cottage industry is a small-scale, usually household or family, industry that uses local raw material and local skill, needs little capital, and is often carried on in the home — for example handloom cloth, pottery, metalwork or handicrafts.
**4.** Any two of: shortage of capital; old technology; irregular and costly energy; high transport cost; shortage of skilled labour; dependence on imported raw material; a small domestic market; competition from imported goods; labour unrest; weak marketing; bureaucratic delay.
**5.** Any two of: foreign exchange earnings; employment; income for remote areas; linkage effects; preservation of art and culture; improvement of the balance of payments.
**6.** Any two of: poor air connectivity; inadequate transport and infrastructure; shortage of hotels and trained staff; poor sanitation and waste management; seasonality; weak marketing; dependence on Indian visitors; safety concerns; leakage of earnings; environmental damage.
**7.** Foreign employment means the employment of a country's citizens in a foreign country; for Nepal it is mainly the employment of unskilled and semi-skilled workers in Malaysia and the Gulf states on contracts of two to three years.
**8.** Any two of: Malaysia, Qatar, Saudi Arabia, the United Arab Emirates, Kuwait, Bahrain, Oman, South Korea, Japan.
**9.** Remittance is the money sent home by a person working away from home, usually abroad.
**10.** Any two of: daily consumption; education; health; repayment of the loan taken to go abroad; house construction; purchase of land; small business.
**11.** Land reform is the state's intervention to change the ownership and use of agricultural land, so that the cultivator obtains security and ownership and inequality is reduced.
**12.** Any two of: contribution to GDP; employment; food supply; raw material for industry; export earnings; the market it provides to industry; the saving and labour it supplies to other sectors.
:::

**Group B — Short answer (5 marks each)**

1. Explain the importance of agriculture in the Nepali economy. <span class="marks">[5]</span>
2. Explain the features of Nepali agriculture. <span class="marks">[5]</span>
3. Explain the problems of Nepali agriculture and state the measures to solve them. <span class="marks">[5]</span>
4. What is land reform? Explain its objectives and the progress of land reform in Nepal. <span class="marks">[5]</span>
5. Explain the role and importance of industry in the economic development of Nepal. <span class="marks">[5]</span>
6. Explain the problems of industrial development in Nepal and state its prospects. <span class="marks">[5]</span>
7. Explain the role of tourism in the Nepali economy and its problems. <span class="marks">[5]</span>
8. What is foreign employment? Explain its role and importance in the Nepali economy. <span class="marks">[5]</span>
9. Explain the problems of foreign employment in Nepal and state the measures to make it safe and productive. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Agriculture provides about a fifth to a quarter of GDP and employs about three-fifths of the workers; it supplies the country's food and the raw material for agro-processing; it earns foreign exchange through tea, coffee, ginger, cardamom, lentils and pulses; it is the market for industrial goods; it supplies labour, saving and food to the other sectors; it carries the culture and settlement pattern of the country; and it is the sector to which migrant workers return. (Any five, each explained in a sentence.)
**2.** Subsistence farming with most produce consumed at home; small and fragmented holdings of less than a hectare; dependence on the monsoon, with only about a third of the area assuredly irrigated; low productivity per hectare and per worker; traditional technology and farmyard manure; a dual structure of a large low-yielding subsistence sector and a small commercial sector; unequal distribution of land; and heavy under-employment on the land.
**3.** Problems: low yields; unirrigated and rain-dependent land; small fragmented holdings; costly inputs and scarce credit; poor roads, storage and markets; the middleman taking the consumer's price; weak extension services; low prices and poor market information; land fragmentation; shortage of farm labour as the young go abroad; loss of fertile Terai land to housing; and natural disasters. Measures: assured irrigation; improved seed and balanced fertiliser supplied on time; cooperatives, contract farming, cold storage and market yards; high-value and export crops; agro-processing; crop insurance; land consolidation and cooperative farming; and cheap agricultural credit.
**4.** Definition as in Group A answer 11. Objectives: to end absentee landlordism and exploitation; to give land to the tiller; to reduce inequality; to raise production by making the farmer secure; and to create a proper land market. Progress in Nepal: the abolition of the Birta system in 2019 B.S. and of Zamindari; the Land Reform Act 2021 B.S. (1964) with a ceiling on holdings, security of tenure and redistribution of surplus land. Results were partial — the ceiling was evaded by transfers to relatives, tenancy records were manipulated so that tenants were recorded as ordinary cultivators, and redistribution was small. Scientific land reform — consolidation, cooperative farming and accurate tenancy records on the land information system — remains unfinished.
**5.** Industry provides employment to the labour that agriculture cannot absorb; it adds value to raw material, so the country earns more from the same crop; it diversifies exports and eases the trade deficit; it creates demand for farm produce; it earns foreign exchange; it builds linkages with transport, banking, insurance and trade; it trains a skilled workforce; and it supports balanced regional development when it is spread beyond the Kathmandu valley and the Terai.
**6.** Problems as in Group A answer 4, plus dependence on India for raw material and for transit, an open border with smuggling, and concentration of industry in a few districts. Prospects: hydropower to end the power constraint and to be exported; special economic zones and industrial corridors; agro-processing of tea, coffee, ginger, cardamom, fruit, herbs and milk; cement, steel fabrication, hydro equipment and construction materials; herbal medicine and handicrafts; skill development and technical education; and simpler registration, taxation and customs.
**7.** Role: foreign exchange without needing a port; employment for guides, porters, hotel staff, drivers and artisans, much of it in remote areas; income for the trekking regions; construction of hotels, roads and airports; a market for handicrafts and farm produce; preservation of heritage; and improvement of the invisible earnings of the balance of payments. Problems as in Group A answer 6.
**8.** Definition as in Group A answer 7. Role: remittance of about a quarter of GDP is the largest source of foreign exchange and keeps the balance of payments in surplus despite the trade deficit; it absorbs the surplus labour that the domestic economy cannot employ; it reduces poverty because it reaches households directly; it finances consumption, education, health, housing and small business; it supports the exchange rate and the reserves; migrant workers acquire skills abroad; and it relieves pressure on land and public services at home.
**9.** Problems: heavy recruitment cost and debt; exploitation by unlicensed manpower agencies; unsafe work, accidents, illness and uncompensated deaths; low wages and long hours in unskilled jobs; no skill gained; social costs at home — wives alone, children without a parent, neglect of the elderly; neglect of agriculture; brain drain; ineffective regulation of the recruitment business; and difficult reintegration on return. Measures: skill-based migration with training before departure; bilateral labour agreements fixing wages and conditions; strict regulation and prosecution of fraudulent agencies; a single honest recruitment charge; insurance and a welfare fund for migrants and their families; consular support and help desks in destination countries; financial literacy so that remittance is invested; reintegration programmes for returnees; and the creation of jobs at home.
:::

**Group C — Long answer (8 marks each)**

1. Explain the importance, features, problems and prospects of Nepali agriculture, and state the objectives and progress of land reform in Nepal. <span class="marks">[8]</span>
2. What is remittance? Explain the role and importance of foreign employment in the Nepali economy, its problems, and the measures needed to make it safe and productive. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** *Importance (2).* Contribution to GDP and to employment; food and raw material; export earnings; the market for industry; the supply of labour, saving and food to other sectors; and the culture and settlement it carries.
*Features (1.5).* Subsistence farming; small fragmented holdings; monsoon dependence with only a third of the area irrigated; low productivity; traditional technology; a dual structure; unequal land ownership; under-employment.
*Problems (1.5).* Low yields; unirrigated land; small holdings; costly inputs and scarce credit; poor roads, storage and markets; the middleman; weak extension; low prices; labour shortage; loss of fertile land; natural disasters.
*Land reform (1.5).* Definition; objectives — end exploitation, land to the tiller, reduce inequality, raise production, create a land market; progress — abolition of Birta (2019 B.S.) and Zamindari, and the Land Reform Act 2021 B.S. with ceiling, tenancy security and redistribution; partial results and the manipulation of records; scientific land reform unfinished.
*Prospects (1.5).* Irrigation; improved seed and fertiliser; cooperatives, contract farming and cold storage; high-value crops; agro-processing; crop insurance; land consolidation and cooperative farming; agricultural credit.
**2.** *Remittance (1).* Money sent home by a person working away from home, usually abroad.
*Role and importance (3).* The largest source of foreign exchange, about a quarter of GDP; keeps the balance of payments in surplus despite a trade deficit several times the value of exports; absorbs the surplus labour that the domestic economy cannot employ; reduces poverty because it reaches households directly; finances consumption, education, health, housing, land and small business; supports the reserves and the exchange rate; teaches skills abroad; relieves pressure on land and on public services.
*Problems (2.5).* Recruitment cost and debt of Rs. 1.5 to 2 lakh; exploitation by unlicensed agencies; unsafe work, accidents, illness and uncompensated deaths; low wages and long hours; no skill gained; social costs at home; neglect of agriculture; brain drain; weak regulation; difficult reintegration.
*Measures (1.5).* Skill-based migration with pre-departure training; bilateral labour agreements; strict regulation and prosecution of fraudulent agencies; a single recruitment charge; insurance and a welfare fund; consular support; financial literacy and productive investment of remittance; reintegration programmes; and creation of jobs at home.
:::


## Retrieval practice and investigation

::: key Work before reading the key
Answer these short retrieval questions without consulting the chapter. Explain the reason, not only the result. These are revision checks, not a prediction of the examination paper.
:::

**1.** Is every rupee of tourist spending pure national profit?

**2.** Give one benefit and one risk of remittance dependence.

**3.** Does a higher farm selling price always mean higher real farm profit?

::: note Reasoned key
**1.** No. Costs, imported inputs, leakage and environmental impacts must also be considered.

**2.** Benefit: household purchasing power and foreign-exchange receipts. Risk: vulnerability to foreign labour-market changes; families may also face social costs.

**3.** No. Input costs, output quantities, transport and losses may also change.

:::

::: tip Investigation — Follow a local value chain
Trace a fictional vegetable crop from farmer to collection centre, transport, retailer and household. Identify where storage loss occurs and how better irrigation, storage or market information might help. Discuss costs as well as benefits.

Submit a one-page record: your method, working or evidence, conclusion, and one limitation. Exchange it with a classmate and check the reasoning against the chapter.
:::
