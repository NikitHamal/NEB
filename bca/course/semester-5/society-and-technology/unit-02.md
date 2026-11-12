---
subject: Society and Technology
grade: BCA Semester 5
unit: 2
title: Organizing Social Life
hours: 6
area: BCA 305 · Society and Technology · Unit 2
---

Unit 1 asked what sociology is. This unit looks at how social life is *organised*: how many people there are and where they live, how they share a way of life (culture), what rules guide them (norms and values), what positions they hold (status and role), and which institutions and groups hold everything together (marriage, family, kinship and groups). These are the building blocks that the later units use to describe Nepali society and the effect of technology on it.

::: key What this unit gives you
- Society and community: definitions, characteristics and types; population size and distribution, with Nepal's census figures.
- Culture: elements, types, cultural lag, ethnocentrism and cultural relativism.
- Norms and values: folkways, mores, laws, taboos; sanctions and social control.
- Status and role: ascribed and achieved status, role conflict and role strain.
- Institutions: marriage, family and kinship in Nepal; primary and secondary groups, reference groups and Nepali community groups.
:::

## 2.1 Society and population

A **society** is a *system of social relationships* among people who share a territory and a way of life (MacIver and Page: "a web of social relationships"). Its main characteristics are: people living together; mutual awareness and interdependence; cooperation and also conflict; likeness and difference; and a shared culture. A **community** is a smaller, territorially bounded group whose members share a common life and a sense of belonging (a village, a tole, a municipality); the key difference is that a community has *locality* and *community sentiment*, while a society is a wider network of relationships that need not be local (the "Nepali society", the "global society"). In the digital age, an online community has sentiment but not locality, which is why sociologists speak of *virtual communities*.

Societies are classified by their main way of producing a living: **hunting and gathering, pastoral, horticultural (simple farming), agrarian, industrial and post-industrial (information) societies**. Nepal is a mixed case: subsistence farming for many households, growing services, remittance and tourism economies, and a rapidly growing digital sector.

### Population size and distribution

Population is a basic social fact because it sets the demand for schools, jobs, land and services. Sociologists look at **size** (how many), **composition** (age, sex, ethnicity, literacy) and **distribution** (where; density, urban and rural). *Demography* is the statistical study of these. Three processes change the population: **fertility** (births), **mortality** (deaths) and **migration** (movement in or out). Nepal conducts a census every ten years. The 2021 census (BS 2078) recorded:

| Indicator, Census 2021 | Value |
|---|---|
| Total population | 29,164,578 |
| Female / male | 14,911,027 / 14,253,551 (more females than males) |
| Annual growth rate (2011 to 2021) | 0.92 per cent |
| Average household size | 4.37 persons |
| Density | 198 persons per square km (29,164,578 / 147,516 km²) |

The distribution is uneven. The hills hold much of the area but the Tarai (Madhesh province) and the Kathmandu valley hold the highest densities, and the population is shifting from the hills and mountains to the Tarai and to towns.

```svgfig label="2.1" caption="Population of Nepal's seven provinces, Census 2021 (millions). Bagmati and Madhesh have about 21 per cent each; Karnali, the largest province by area in the west, has less than 6 per cent. The seven values sum to 29,164,578."
f = Fig(580, 270)
data = [("Koshi", 4.961), ("Madhesh", 6.115), ("Bagmati", 6.117), ("Gandaki", 2.466), ("Lumbini", 5.122), ("Karnali", 1.688), ("Sudur-\npashchim", 2.695)]
base, scale = 215, 26
f.line(40, base, 560, base, color=SLATE, sw=1.4)
for i, (n, v) in enumerate(data):
    x = 62 + i * 72
    h = v * scale
    f.box(x, base - h, 48, h, "", fill=BLUE if v < 6 else MINT, stroke=NAVY if v < 6 else TEAL)
    f.text(x + 24, base - h - 8, "%.2f" % v, size=10, color=SLATE, bold=True)
    f.text(x + 24, base + 14, n, size=9.5, color=SLATE)
f.text(290, 14, "Population in millions", size=10, color=SLATE, bold=True)
```

::: example Why distribution matters for IT
A telemedicine or e-learning project needs to know that Karnali province has fewer than 1.7 million people spread across rough terrain, whereas Bagmati has more than 6 million, much of it in one valley. Network cost per user, language mix and device ownership differ widely, so one national design will not fit all districts.
:::

## 2.2 Culture and community

**Culture** is the *whole way of life* of a society: the knowledge, beliefs, art, morals, law, custom, language and habits acquired as a member of society (E. B. Tylor, 1871). It is *learned* (not inherited), *shared*, *transmitted* across generations, *cumulative*, *symbolic* (language above all) and *adaptive*.

**Elements.** *Material culture* is the physical objects (tools, buildings, a smartphone, a dhaka topi); *non-material culture* covers ideas and behaviour: beliefs, values, norms, language, symbols, rituals and knowledge.

**Types and related terms.**
- **Subculture:** a group within a culture with its own patterns while sharing the main culture (gamers, Newar guthi communities, hackers, students of a campus).
- **Counterculture:** a group that rejects dominant values (some youth movements).
- **Cultural diffusion:** spread of cultural traits between societies (Western-style weddings, momo and pizza, K-pop, Facebook).
- **Cultural lag** (W. F. Ogburn): non-material culture changes more slowly than material culture, creating gaps. Laws on data privacy trail behind the spread of apps; many people own smartphones before they learn online safety.
- **Culture shock:** disorientation on meeting an unfamiliar culture, familiar to students moving to Kathmandu or abroad.
- **Ethnocentrism:** judging other cultures by the standards of one's own, assuming one's own is superior. **Cultural relativism:** understanding a practice within its own cultural context, without moral approval of every practice. Relativism is a method for understanding, not a reason to ignore human-rights standards.

Nepal's culture is a *mosaic*: more than 120 caste and ethnic groups and over a hundred languages were recorded in recent censuses, with Nepali as the largest mother tongue (by about 44 per cent), followed by Maithili, Bhojpuri, Tharu and Tamang. Festivals such as Dashain, Tihar, Chhath, Eid, Buddha Jayanti, Lhosar and Christmas are celebrated by different communities.

## 2.3 Norms and values

**Values** are *general beliefs about what is good, desirable and important* (honesty, hospitality, respect for elders, equality, success). They give direction. **Norms** are *specific rules* that tell people how to behave in a situation; they put values into practice. A value ("respect for teachers") produces many norms (stand when the teacher enters, use *sir* or *miss*, say *namaste*).

William Graham Sumner classified norms by their strength:

| Type | Meaning | Example | Sanction if broken |
|---|---|---|---|
| **Folkways** | Everyday habits and conventions; not morally serious | Removing shoes before entering a house or temple; eating with the right hand | Mild disapproval, raised eyebrows |
| **Mores** | Norms with moral weight; essential to group welfare | Honesty, respect for parents, not cheating in exams | Strong disapproval, social exclusion |
| **Taboos** | Strongest mores; unthinkable acts | Incest, killing a cow in many Hindu communities | Horror, severe punishment |
| **Laws** | Norms formalised and enforced by the state | The Muluki Criminal Code, Electronic Transactions Act | Fine, imprisonment |

**Sanctions** are the rewards and punishments that enforce norms: *positive* (praise, awards, promotion) and *negative* (ridicule, fine, expulsion), *formal* (imposed by institutions) or *informal* (by peers). **Social control** is the sum of means by which society secures conformity, from the internalised conscience and family upbringing (informal) to school discipline, police and courts (formal). Behaviour that violates norms is **deviance**; what counts as deviant varies by time and place (Merton's typology: conformity, innovation, ritualism, retreatism, rebellion).

::: example Norms in digital life
*Netiquette* is a set of folkways for online behaviour (no ALL CAPS, reply promptly, tag with permission). Plagiarism and online harassment violate mores. Hacking and identity theft violate laws. A team's code review rules are norms within a workplace subculture.
:::

## 2.4 Status and role

A **status** is a *position* a person holds in a group or society; a **role** is the *behaviour expected* from the holder of that position. Status is what you *are*, role is what you *do* (Ralph Linton: "status is a collection of rights and duties; role is the dynamic aspect: putting the rights and duties into effect").

- **Ascribed status:** assigned at birth or by automatic processes, not chosen: sex, age, caste or ethnicity, kinship (son, daughter), in some societies royal descent.
- **Achieved status:** earned through effort and choice: doctor, engineer, programmer, team leader, champion.
- **Master status:** the status that dominates the others in how a person is seen (for example, "minister", or in discrimination, caste or disability).
- **Status set:** all statuses a person holds at once; a student may also be a daughter, a part-time developer, a club treasurer and a Facebook-group admin.
- **Role set:** the set of roles linked to one status. A *teacher* acts with students, colleagues, the principal and parents (Merton).

| Concept | Meaning | Example |
|---|---|---|
| **Role conflict** | Demands of *two different* roles clash | A manager must fire an employee who is also her friend; a student needs to study but also earn |
| **Role strain** | Demands *within one* role clash or are too many | A teacher expected to teach, grade, run activities and handle paperwork |
| **Role exit** | Leaving an important role | Retirement, divorce, leaving a job |
| **Role performance** | Actual behaviour versus the expected role | A developer who delivers late despite the role of "dependable" |

Status and role are links between the individual and society: society needs tasks done, so it defines positions and attaches expectations, while individuals learn the expectations through **socialisation** (Unit 3).

::: example Roles on a software project
A project manager, analyst, developer, tester and client each hold a status with expected roles. Conflict arises when a developer is also the client's relative and is asked to hide a bug (role conflict), or when one person is asked to be developer, tester and support (role strain). Clear role definitions reduce both.
:::

## 2.5 Institutions: marriage, family and kinship

An **institution** is an *organised, established system of norms, statuses and roles built around a basic social need* (Unit 1's functionalists call these the organs of society). The five major institutions are family, economy, polity (state), education and religion. Here we study the family complex: marriage, family, kinship.

### Marriage

**Marriage** is a *socially approved union* between persons that establishes rights and duties between them, their children and their kin. Its functions include regulation of sexual relations, legitimate childbearing, division of labour, economic cooperation and linking of families.

**Forms by number of spouses:** *monogamy* (one spouse at a time; legally the only form in Nepal today), *polygyny* (one husband, several wives), *polyandry* (one wife, several husbands; found historically in some Himalayan communities) and *group marriage* (rare). **Forms of selection:** *arranged* (families choose or approve), *love* (the couple choose), and *mixed*, increasingly common in Nepal with arranged introductions after consent; *endogamy* (marry within a group such as caste or ethnicity) versus *exogamy* (marry outside a group, such as one's clan or gotra); *hypergamy* and *hypogamy* (marriage into a higher or lower group). Other practices of marriage by capture, by elopement, by service exist among some groups.

In Nepal the **Muluki Civil Code, 2074** (in force since 2075 BS) sets the minimum age of marriage at **20 years** for both women and men; the **Muluki Criminal Code, 2074** criminalises child marriage and dowry-related harassment. Child marriage and dowry persist in practice in some regions, which is a good example of the gap between law (formal norm) and custom (informal norm).

### Family

A **family** is a *group of persons related by marriage, blood or adoption, living together (usually), cooperating economically and raising children*. It is the *primary* institution of socialisation.

| Basis | Types |
|---|---|
| **Structure** | *Nuclear* (couple and unmarried children); *joint or extended* (several married couples and generations sharing hearth, property and authority); *single-parent*; *reconstituted* |
| **Authority** | *Patriarchal* (father or senior male heads; the common form in Nepal), *matriarchal*, *egalitarian* |
| **Descent and residence** | *Patrilineal* (descent traced through father; *patrilocal* residence: wife moves to husband's home), *matrilineal*, *bilateral* |
| **Marriage form** | *Monogamous*, *polygynous*, *polyandrous* |

**Functions of the family:** biological (reproduction), economic (shared income, care), socialisation (language, values), protective (care of children, sick and elderly), status ascription (caste, surname), religious and emotional (ritual, affection, rites of passage).

**Change in the Nepali family.** The traditional ideal is the joint family, but the average household is 4.37 persons (Census 2021), and nuclear households are increasing owing to urbanisation, education, employment and migration. Foreign employment creates *transnational* families: one spouse or both abroad, grandparents raising children, and money and video calls connecting the household. Women manage land, farming and finance in many "left-behind" households; mobile phones, remittance apps and social media are the medium of family life.

### Kinship

**Kinship** is the *system of social relationships based on blood (consanguineal kin) and marriage (affinal kin)*. Kin are classified in *degrees*: **primary** (parent, child, sibling, spouse), **secondary** (primary kin's primary kin: grandparent, uncle, aunt, in-laws) and **tertiary** (cousins and further). Terms of address and reference in Nepali are detailed and mark side and age: *mama* (mother's brother), *kaka* or *thulo-bua* (father's brothers), *phupu* (father's sister), *maiju* (mother's sister), *bhanja* and *bhanji* (sister's children), *bhatija* (brother's children). Descent groups (lineage, clan) matter for inheritance, ritual obligations (death rites) and in many communities for marriage rules (clan exogamy).

::: note Functions of kinship
Kinship regulates marriage, gives identity and a social network of mutual support (credit, labour exchange, job references), organises inheritance, and defines ritual duty. In Nepal, kin networks often work as informal social security and as the first source of migration contacts and loans.
:::

## 2.6 Groups

A **social group** is *two or more people who interact on the basis of shared expectations and a sense of belonging*. A crowd waiting at a bus stop is a *category* or *aggregate*, not a group, because there is no interaction or shared identity.

| Classification | Types | Notes |
|---|---|---|
| **Primary and secondary** (Cooley) | *Primary*: small, face-to-face, intimate, lasting (family, close friends, village peer group). *Secondary*: larger, impersonal, goal-oriented (company, political party, university) | Primary groups form the self and values; secondary groups perform specific tasks |
| **In-group and out-group** (Sumner) | "We" and "they" | Loyalty inside, rivalry outside; the source of ethnocentrism |
| **Reference group** (Merton, Hyman) | Group a person uses as a standard to evaluate themselves, even without belonging | Aspirations of a student to join a tech company; fashion following |
| **Formal and informal** | *Formal*: rules, offices, written goals (a company, campus student union). *Informal*: spontaneous, unwritten (friends at lunch) | Informal groups often decide how formal organisations really work |
| **Gemeinschaft and Gesellschaft** (Toennies) | Community of personal bonds versus society of contract and interest | Village versus city or corporation |

**Nepali community groups.** The same functions are served by traditional and modern groups: **guthi** (Newar trusts for religious and social duties and funeral help), **parma** (traditional labour exchange among neighbours, "labour for labour"), **dhukuti** (rotating savings and credit association among members, a forerunner of cooperatives), **aama samuha** (mothers' groups in health and community programmes), **community forest user groups**, cooperatives, and *tole* development committees. Digital counterparts include WhatsApp and Viber family groups, Facebook community pages and online savings circles.

## 2.7 Technology and the organisation of social life

Each building block of this unit is touched by digital technology. The table shows how; the later units study the changes in detail.

| Block | Effect of technology | Example in Nepal |
|---|---|---|
| Population | Better data (census tablets, national ID), targeting of services, new migration patterns | Digital census tools; online job and foreign-employment portals |
| Culture | Diffusion and mixing of culture; cultural lag in law and etiquette | Short videos spreading songs and trends; slow privacy law |
| Norms | New online folkways and new forms of deviance | Netiquette; cyber-bullying; loan-app harassment |
| Status and role | New statuses (influencer, freelancer, admin); role conflict between work and home when always online | Remote work for foreign firms |
| Family | Transnational families kept together by calls; remittance transfer by wallets | Daily video calls with relatives in the Gulf |
| Kinship | Kin networks move to group chats | Family groups share news and organise rituals |
| Groups | Virtual communities, crowdsourcing, online fund-raising | Earthquake relief and lockdown mutual aid groups |

## Chapter summary

- A society is a web of social relationships; a community adds locality and community sentiment. Nepal (Census 2021) has 29,164,578 people, 4.37 per household and an uneven distribution across provinces.
- Culture is learned, shared, cumulative, symbolic and adaptive; material and non-material parts change at different speeds (cultural lag). Avoid ethnocentrism; use relativism to understand.
- Values give direction; norms (folkways, mores, taboos, laws) enforce them through sanctions and social control.
- Status is a position (ascribed, achieved, master), role the expected behaviour; role conflict is between roles, role strain within one.
- Marriage, family and kinship are the core institutions of social life; the Nepali family is shifting from joint to nuclear and transnational forms.
- Groups: primary and secondary, in-group and out-group, reference and formal and informal groups; Nepal has guthi, parma, dhukuti and aama samuha.

## Practice

1. Differentiate society and community.
2. What is demography? Name three processes that change a population.
3. Write down four characteristics of culture.
4. What is cultural lag? Give a digital example.
5. Distinguish ethnocentrism from cultural relativism.
6. Differentiate folkways, mores, taboos and laws with examples.
7. Distinguish ascribed and achieved status; role conflict and role strain.
8. What is marriage? State two functions and name two forms.
9. List the types of family by structure; why are nuclear families rising in Nepal?
10. Differentiate primary and secondary groups. Give Nepali examples of community groups.

::: note Answers and worked solutions
**1.** Society is a wide web of social relationships (need not be local); community is a smaller group in a locality sharing a common life and sentiment.
**2.** Demography is the statistical study of population size, composition and distribution. Fertility, mortality and migration.
**3.** Learned, shared, transmitted across generations, cumulative, symbolic (language), adaptive (any four).
**4.** Non-material culture (laws, habits) changes more slowly than material culture (technology). Example: many users own smartphones before learning safe online behaviour, and privacy laws arrive later.
**5.** Ethnocentrism judges others by one's own standards; relativism understands a practice in its own context.
**6.** Folkways: removing shoes at a doorway. Mores: honesty in exams. Taboo: incest. Law: Muluki Criminal Code provisions on theft or cyber-crime.
**7.** Ascribed: given at birth (sex, caste); achieved: earned (engineer). Role conflict: two roles clash (manager and friend); role strain: strain inside a single role (overloaded teacher).
**8.** A socially approved union with rights and duties. Functions: regulating sexual relations, legitimate childbearing, economic cooperation. Forms: monogamy, polygyny, polyandry, arranged or love.
**9.** Nuclear, joint (extended), single-parent, reconstituted. Reasons: urbanisation, education, jobs and migration, housing cost.
**10.** Primary: small, intimate, face-to-face (family); secondary: large, impersonal, goal-oriented (company, party). Examples: guthi, parma, dhukuti, aama samuha, community forest user groups.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Define norms and values. Explain the types of norms with examples.**

*Definition.* Values are general beliefs about what is good and desirable (honesty, respect). Norms are specific rules of behaviour that put values into practice.

*Types (Sumner).* **Folkways** are everyday conventions without moral force, such as removing shoes before entering a temple; breaking them brings mild disapproval. **Mores** are norms with moral force, such as honesty and respect for parents; breach brings strong disapproval. **Taboos** are the strongest prohibitions, such as incest. **Laws** are norms made and enforced by the state, such as the Electronic Transactions Act 2063. Enforced through positive and negative, formal and informal sanctions, norms provide social control.

**Q2 (10 marks). What is a family? Describe its types and functions, and discuss changes in the Nepali family.**

*Definition.* A family is a group related by marriage, blood or adoption, usually sharing a home and cooperating economically and in raising children; it is the primary agency of socialisation.

*Types.* By structure: nuclear, joint, single-parent, reconstituted. By authority: patriarchal, matriarchal, egalitarian. By descent: patrilineal, matrilineal, bilateral. By marriage: monogamous, polygynous, polyandrous.

*Functions.* Reproduction, economic support, socialisation, protection and care, status ascription, religious and emotional support.

*Change in Nepal.* Average household size is 4.37 (Census 2021), nuclear forms are increasing because of urbanisation, education, jobs and migration. Foreign employment creates transnational families that stay connected by phone and wallet; women manage many households; the legal minimum marriage age is 20 under the Muluki Civil Code 2074. Joint-family values (respect for elders, shared obligations) persist, but practice is more flexible.

*Conclusion.* The family has not disappeared; it has adapted, and technology is a medium for the adapted form.

**Q3 (5 marks). Explain status and role with types and examples. Differentiate role conflict from role strain.**

*Status* is a position; *role* is the behaviour expected from it. Ascribed status is given (age, sex, caste); achieved status is earned (doctor, engineer); a master status dominates others. A person has a *status set*, and each status has a *role set*. *Role conflict* arises between two roles (a manager who must discipline a friend); *role strain* arises within one role (a teacher overloaded with conflicting duties).
