---
subject: Social Studies and Human Value Education
grade: 10
unit: 5
title: Civic Consciousness
hours: 0
area: Units
---

Civic consciousness is the awareness of how our country is governed, of the rights and duties of citizens and of the way citizens can take part. In a democracy the power belongs to the people, but the people use it through institutions: a legislature that makes laws, an executive that carries them out, a judiciary that decides disputes, political parties that organise the contest for power, and elections that let citizens choose. This unit studies each of these as set up by the **Constitution of Nepal, 2072 (2015)**, and then the rights that protect every person — human rights and consumer rights. The facts here are numbers, names and procedures, so the unit is high-scoring for those who revise it carefully.

::: key What the SEE paper expects from this unit
Frequent questions: "Write any four functions of the legislature / the judiciary" (2–4 marks); "How is the Prime Minister appointed?" (2 marks); "What is human rights? Write any four human rights" (2 marks); "Explain the role of citizens in elections" (4 marks); "What are consumer rights? Write any four" (2–4 marks). Know the **numbers**: 275 and 59 members of the Federal Parliament; five-year and six-year terms; 3 levels of courts; 18 years for voting; 30 articles of the UDHR; 10 December Human Rights Day.
:::

### The separation of powers

No single person or body should hold all the power of the state. The constitution divides it among three organs, which check each other.

```figure caption="The three organs of the state and how they check one another."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8,3.2))
ax.set_xlim(0,12); ax.set_ylim(0,8); ax.axis('off')
def box(x,y,w,h,t,s,c):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.05',fc=c,ec='none'))
    ax.text(x+w/2,y+h*0.68,t,ha='center',va='center',color='white',fontsize=9,weight='bold')
    ax.text(x+w/2,y+h*0.28,s,ha='center',va='center',color='white',fontsize=7.5)
box(3.8,5.2,4.4,2.3,'Legislature','makes laws,\napproves budget',ACCENT)
box(0.2,0.6,4.4,2.3,'Executive','carries out laws,\nruns government','#2e6da4')
box(7.4,0.6,4.4,2.3,'Judiciary','interprets laws,\ngives justice','#4f8bbf')
kw=dict(arrowstyle='<->',color=INK,lw=1.1)
ax.annotate('',xy=(3.6,5.5),xytext=(2.4,2.95),arrowprops=kw)
ax.annotate('',xy=(8.4,5.5),xytext=(9.6,2.95),arrowprops=kw)
ax.annotate('',xy=(4.7,1.75),xytext=(7.3,1.75),arrowprops=kw)
ax.text(0.2,4.6,'questions,\nno-confidence,\nbudget control',fontsize=7,color=INK,ha='left',va='center')
ax.text(11.8,4.6,'judicial review,\nimpeachment',fontsize=7,color=INK,ha='right',va='center')
ax.text(6,1.2,'courts check\nexecutive acts',fontsize=7,color=INK,ha='center',va='center')
```

## 5.1 Legislature

### Meaning

::: definition Legislature
The legislature is the organ of government that makes laws, approves the budget and controls the executive on behalf of the people.
:::

### Federal Parliament

The legislature of Nepal at the federal level is the **Federal Parliament** (*Sangheeya Sansad*), made up of the **President** and two Houses: the **House of Representatives** (*Pratinidhi Sabha*) and the **National Assembly** (*Rastriya Sabha*).

| | House of Representatives | National Assembly |
|---|---|---|
| Nature | Lower house, the main house | Upper house, permanent house |
| Members | **275** | **59** |
| How elected | 165 by first-past-the-post from single-member constituencies; 110 by proportional representation (party lists) from the whole country | 56 elected, eight from each province, by an electoral college of provincial assembly members and the chiefs and deputy chiefs of local levels; 3 nominated by the President on the government's recommendation |
| Term | 5 years (unless dissolved earlier) | 6 years; one-third of members retire every 2 years |
| Minimum age | 25 | 35 |
| Head | Speaker | Chairperson |
| Special role | The Prime Minister must have its majority support; money bills start here | Reviews bills passed by the House of Representatives; represents the provinces |

Among the National Assembly's 56 elected members, from each province there are at least three women, one Dalit and one person with a disability or from a minority. Each political party must make sure that at least **one-third of its elected members** in the federal parliament are women.

```photo id="soc10/parliament" caption="The Federal Parliament building (Sansad Bhawan) at New Baneshwor, Kathmandu, where the House of Representatives and the National Assembly meet." width="80"
```

### Provincial and local legislatures

Each province has a **Provincial Assembly**, whose members are elected by the people (a mixture of first-past-the-post and proportional seats). Each municipality and rural municipality has an **Assembly** (*Gaun/Nagar Sabha*) made up of the elected chief, deputy chief, ward chairs and ward members, and it makes local laws. Thus all three tiers of the federal system have lawmaking bodies.

### Functions of the legislature

1. **Makes laws** (*kanun nirman*) and amends or repeals old ones.
2. **Approves the budget** and controls government spending and taxation.
3. **Controls the executive** through questions, discussion, committees and the power to remove a government by a vote of no confidence.
4. **Elects or confirms people**: the Speaker, the Prime Minister (by majority support), and takes part in electing the President and Vice-President together with the provincial assemblies.
5. **Approves treaties** and agreements with other countries.
6. **Amends the constitution** by a two-thirds majority of each house.
7. **Hears impeachment** of the President, Vice-President, judges and holders of constitutional posts, and **represents the people** by discussing public issues.

### How a bill becomes law

```figure caption="Steps for a bill to become a law in the Federal Parliament."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8,2.4))
ax.set_xlim(0,12.4); ax.set_ylim(0,5.2); ax.axis('off')
steps=['Bill\nintroduced','Discussion,\ncommittee','Vote,\nfirst house','Second\nhouse','President\nassents']
for i,s in enumerate(steps):
    x=0.1+i*2.5
    ax.add_patch(FancyBboxPatch((x,2.0),2.1,1.6,boxstyle='round,pad=0.05',fc='#e8f0f8',ec=ACCENT,lw=1))
    ax.text(x+1.05,2.8,s,ha='center',va='center',fontsize=7,color=INK)
    if i<4:
        ax.annotate('',xy=(x+2.48,2.8),xytext=(x+2.17,2.8),arrowprops=dict(arrowstyle='->',color=MUTED,lw=1))
ax.annotate('',xy=(11.15,1.0),xytext=(11.15,1.9),arrowprops=dict(arrowstyle='->',color=ACCENT,lw=1.2))
ax.text(11.15,0.55,'Becomes an Act (law)',ha='right',va='center',fontsize=9,weight='bold',color=ACCENT)
ax.text(6.2,4.5,'A money bill starts only in the House of Representatives',ha='center',va='center',fontsize=7.5,color=MUTED)
```

A bill is first introduced, discussed in principle, studied clause by clause (often in a committee) and voted on. After the first house passes it, the second house considers it. A bill passed by both houses is presented to the **President**, who gives assent within fifteen days; after assent it becomes an **Act**. Money bills (such as the finance bill) may be introduced only in the House of Representatives, and the National Assembly can only give suggestions.

### Importance

The legislature is the voice of the people, the guardian of the budget, the maker of the rules that all must follow and the place where the government is made answerable. A parliament can work well only when members attend regularly, discuss seriously and listen to the opposition.

## 5.2 Federal executive

### Meaning

::: definition Executive
The executive is the organ of government that carries out the laws, runs the administration and makes and implements policies and plans.
:::

### The federal executive of Nepal

Under the Constitution (Article 75) the executive power of Nepal is vested in the **Council of Ministers**. The structure is as follows.

| Post | How selected | Main role |
|---|---|---|
| **President** (head of state) | Elected for **5 years** by an electoral college of the members of the Federal Parliament and the provincial assemblies; a person may hold the post for at most two terms | The symbol of national unity; formal acts of the state are done in the President's name; gives assent to bills; appoints the Prime Minister and judges on recommendation; Supreme Commander of the army on the Prime Minister's advice; acts on the advice of the Council of Ministers |
| **Vice-President** | Elected with the President | Acts for the President in the President's absence |
| **Prime Minister** (head of government) | The President appoints the leader of the parliamentary party that commands a majority in the House of Representatives. If no party has a majority, a leader who can win the support of members of two or more parties is appointed | Leads the Council of Ministers and runs the government |
| **Council of Ministers** | Appointed by the President on the recommendation of the Prime Minister; not more than **25** members including the Prime Minister | Makes policies, prepares the budget and carries out laws; collectively responsible to the House of Representatives |

The Prime Minister must keep the confidence of the House of Representatives. If the House passes a motion of no confidence, the Prime Minister loses office.

The President is the **head of state** and the Prime Minister is the **head of government**; this system is called the *parliamentary system*, because the government is formed from, and answerable to, the parliament.

### Provincial and local executives

| Level | Executive |
|---|---|
| Province | Chief Minister and Council of Ministers; the Governor is the federal representative and head of the province |
| Local | Mayor and Deputy Mayor (municipality) or Chair and Vice-chair (rural municipality) and ward chairs, who form the local executive |

### Functions of the federal executive

1. **Implements laws** and decisions of parliament throughout the country.
2. **Prepares policy and plans** and presents them to parliament.
3. **Prepares and presents the annual budget** (the Finance Minister presents it on **Jestha 15** each year) and collects revenue.
4. **Maintains peace, law and order** through the Nepal Police, Armed Police Force and the Nepal Army, as needed.
5. **Conducts foreign relations**: embassies, treaties, trade and aid.
6. **Runs the civil service**: ministries, departments and the appointment of officers.
7. **Provides services**: roads, electricity, health and education policy, disaster relief.
8. **Manages emergencies**: advises the President on declaring a state of emergency under the constitution's rules.

```photo id="soc10/singha-durbar" caption="Singha Durbar, Kathmandu, the main secretariat of the Government of Nepal, where ministries and the office of the Prime Minister work." width="76"
```

::: caution Do not mix up the roles
The **President** gives formal assent but does not run the government day by day. The **Prime Minister and Council of Ministers** hold the real executive power. Questions that ask "Who is the head of government?" want the Prime Minister.
:::

## 5.3 Judiciary

### Meaning

::: definition Judiciary
The judiciary is the organ of government that interprets the law, decides disputes and gives justice, and protects the constitution and the rights of citizens.
:::

Justice in Nepal is delivered in the name of the people. The constitution declares that the judiciary is **independent**: judges are to decide cases only on the basis of law, evidence and conscience, free from pressure from the executive, legislature or anybody else.

### Structure of the courts

```figure caption="Structure of the judiciary of Nepal."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8,3.0))
ax.set_xlim(0,12); ax.set_ylim(0,7.4); ax.axis('off')
rows=[(5.5,'Supreme Court','1 court, Kathmandu; Chief Justice and other judges',ACCENT),(3.3,'High Courts','7 courts, in each province; hear appeals from district courts','#2e6da4'),(1.1,'District Courts','77 courts, one in each district; first hearing of most cases','#4f8bbf')]
for y,t,s,c in rows:
    ax.add_patch(FancyBboxPatch((0.4,y),11.2,1.6,boxstyle='round,pad=0.04',fc=c,ec='none'))
    ax.text(6,y+1.1,t,ha='center',va='center',color='white',fontsize=10,weight='bold')
    ax.text(6,y+0.45,s,ha='center',va='center',color='white',fontsize=7.5)
ax.text(6,0.5,'Alongside: Judicial Committees of local levels, Special Court, tribunals',ha='center',va='center',fontsize=7.5,color=MUTED)
```

| Court | Notes |
|---|---|
| **Supreme Court** | The highest court, in Kathmandu. Headed by the **Chief Justice** with not more than 20 other judges. Its decisions bind all other courts. It hears appeals, decides constitutional questions and issues writs |
| **High Courts** | One in each province (seven). Hear appeals against district court decisions and certain cases of their own |
| **District Courts** | One in each of the 77 districts. The first court for most civil and criminal cases |
| **Judicial Committees** | Elected committees at each municipality and rural municipality, led by the deputy chief, with power to settle certain local disputes and to mediate |
| **Special Court and tribunals** | Special Court hears cases of corruption filed by the CIAA; other tribunals handle revenue, administrative and labour cases |

```photo id="soc10/supreme-court" caption="The Supreme Court of Nepal at Ramshahpath, Kathmandu, the highest court of the country and the final interpreter of the constitution." width="76"
```

### Appointment and independence

The **Chief Justice** is appointed by the President on the recommendation of the **Constitutional Council**. Other judges of the Supreme Court, the High Courts and the District Courts are appointed on the recommendation of the **Judicial Council**, which also supervises discipline. A Supreme Court judge retires at 65 years. Salaries and conditions are protected, and judges may be removed only by a process of impeachment or by the Judicial Council for stated reasons.

### Functions

1. **Gives justice** — hears civil, criminal and administrative cases and punishes the guilty.
2. **Interprets the law and the constitution**, and gives binding decisions that other courts follow.
3. **Judicial review** — the Supreme Court may declare a law or an act of government void if it conflicts with the constitution.
4. **Protects fundamental rights** by issuing **writs** such as *habeas corpus* (to produce a detained person before the court), *mandamus* (to order an official to perform a duty), *certiorari*, *prohibition* and *quo warranto*.
5. **Hears public interest litigation:** anyone may go to the court on a matter of public interest, such as environment or the rights of the disadvantaged. For example, the Supreme Court has issued directives against chhaupadi and for the rights of women and sexual minorities.
6. **Punishes contempt of court** to keep respect for the judiciary.
7. **Settles disputes** between governments of different levels.

### Principles of fair justice

- Everyone is equal before the law.
- A person is **presumed innocent** until proven guilty.
- The accused has the right to a lawyer, to be told the reason for arrest and to be produced before a court within 24 hours of arrest (excluding journey time).
- Trials are open and decisions are reasoned; the right of appeal.
- Free legal aid is given to those who cannot pay.

### Problems and improvement

Delays in cases, many pending cases, high cost, weak access in remote areas, corruption in the system, poor enforcement of decisions. Improvements: more judges and staff, e-filing and e-courts, mediation, legal aid, circuit benches of High Courts and honest, independent appointments.

## 5.4 Political parties

### Meaning

::: definition Political party
A political party is an organised group of people with common ideas about how the country should be governed, who seek to win elections, to form or influence the government and to put their policies into effect.
:::

### Features of a political party

- A common **ideology, programme and policy**
- An **organisation** from the centre to the ward
- **Members, leaders and rules** (constitution of the party)
- Aim to **win power by elections**
- **Registration** with the Election Commission and a **symbol** for elections

### Party systems

| System | Meaning | Example |
|---|---|---|
| One-party | Only one party is allowed | China, North Korea |
| Two-party | Two main parties compete | The United States, United Kingdom (in practice) |
| Multi-party | Many parties compete; coalition governments are common | **Nepal**, India |

Nepal follows the **multi-party** system. The Constitution allows any group of citizens to form a political party, provided that its rules and aims respect the constitution and democracy, that its membership is open and that it has an internal democratic process. All political parties must register with the **Election Commission**, as laid down in the Political Parties Act, 2073 (2017). The Election Commission gives "national party" recognition to parties that win a minimum of 3% of the proportional votes and at least one directly elected seat in the House of Representatives. Examples of parties that have shaped Nepal's politics include the **Nepali Congress** (founded 1947), several parties of the communist tradition, the **Rastriya Prajatantra Party**, and newer parties such as the **Rastriya Swatantra Party** (registered 2022). New parties form and old ones change; focus on how parties work, not on memorising lists.

### Functions of political parties

1. **Contest elections** by nominating candidates and publishing manifestos.
2. **Form the government** (the winning party or alliance) and **act as the opposition** (the others), who check the government.
3. **Make policies and laws** through their members in parliament.
4. **Form public opinion** and educate citizens about issues.
5. **Link people and the government**: carry the people's problems to the state.
6. **Train and bring forward leaders.**
7. **Social service** and relief work in disasters.
8. **Protect democracy** by giving the people a choice.

### Merits and demerits

| Merits | Demerits |
|---|---|
| Give citizens a choice | Frequent split and changing of governments cause instability |
| Make government accountable through opposition | Money and muscle power in elections |
| Provide stable policy and leadership | Lack of internal democracy; leadership of the same persons for long |
| Teach citizens about politics | Narrow party interest placed above national interest |
| Make coalition and compromise possible | Political interference in civil service, schools and justice |

### How can political parties be improved?

Internal democracy and regular elections within the party; transparent funds and accounts; a code of ethics for leaders; ticket to candidates on merit; inclusion of women, youth and marginalised groups; programmes made on evidence; strict observation of the election code by the Election Commission; and informed voters who reward good performance.

::: tip The opposition is not an enemy
In exam answers, say that the **opposition** has a constructive role: it questions the government, offers alternatives and protects the rights of citizens. A government and an opposition both serve the people.
:::

## 5.5 Election process and the role of citizens

### Meaning and importance

::: definition Election
An election is the process by which the citizens choose their representatives to make laws and run the government, by voting at regular intervals.
:::

Elections are the base of democracy. Through them the people give power to leaders and also take it back; they make rulers answerable. Without free and fair elections no democracy is real.

### Elections in Nepal

| Level | Body elected | Term |
|---|---|---|
| Federal | House of Representatives (275) | 5 years |
| Province | Provincial Assemblies | 5 years |
| Local | Mayor/Deputy Mayor, Chair/Vice-chair, ward chairs and members in 753 local levels | 5 years |
| Indirect | National Assembly (6 years), President and Vice-President (5 years) | By electoral colleges |

After the Constitution of 2072, elections to all three levels were first held in 2074 BS (2017). Local elections were held again in 2079 BS (May 2022), and House of Representatives elections were held in 2079 (November 2022) and, as early elections, on 5 March 2026.

### Electoral system

Nepal uses a **mixed system** for the House of Representatives and the provincial assemblies.

- **First-past-the-post (FPTP):** the country is divided into constituencies; each elects one member, and the candidate who gets the most votes wins, even without a majority. 165 members of the House of Representatives are elected this way.
- **Proportional representation (PR):** parties' share of seats follows their share of the national vote, using party lists. 110 members are elected this way. The PR lists must be inclusive: women, Dalit, Adivasi Janajati, Khas Arya, Tharu, Madhesi, Muslims and backward areas.
- A voter casts **two votes** (two ballot papers): one for a candidate and one for a party.

### Who can vote and who can stand?

| | Condition |
|---|---|
| Voter | A Nepali citizen aged **18** or above, whose name is on the voter list, and who is not disqualified by law |
| Candidate (House of Representatives) | Citizen aged 25 or above, name on the voter list, not disqualified by law, not holding a profit office |

### The Election Commission

The **Election Commission** is a constitutional body (Article 245) that conducts, supervises, directs and controls elections to the federal parliament, provincial assemblies and local levels, and the elections of the President and Vice-President. It has five commissioners, one of whom is the Chief Election Commissioner, appointed for six years. It prepares the voter list, registers parties, sets the code of conduct, appoints polling officers and observers, and announces results. Its independence guarantees fair elections.

### Steps of an election

```figure caption="The main steps of an election."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8,2.6))
ax.set_xlim(0,12.4); ax.set_ylim(0,6.2); ax.axis('off')
steps=['1. Voter list','2. Election\nschedule','3. Candidate\nnomination','4. Campaign\n(code of conduct)','5. Voting\n(secret ballot)','6. Counting\nand result']
for i,s in enumerate(steps):
    col=i%3; row=i//3
    x=0.2+col*4.1; y=3.5-row*3.0
    ax.add_patch(FancyBboxPatch((x,y),3.3,2.1,boxstyle='round,pad=0.05',fc='#e8f0f8',ec=ACCENT,lw=1))
    ax.text(x+1.65,y+1.05,s,ha='center',va='center',fontsize=7.5,color=INK)
    if col<2:
        ax.annotate('',xy=(x+4.05,y+1.05),xytext=(x+3.4,y+1.05),arrowprops=dict(arrowstyle='->',color=MUTED,lw=1))
ax.plot([9.85,9.85,1.85],[3.45,3.05,3.05],color=MUTED,lw=1)
ax.annotate('',xy=(1.85,2.65),xytext=(1.85,3.05),arrowprops=dict(arrowstyle='->',color=MUTED,lw=1))
```

1. **Voter list:** the Commission registers eligible citizens and publishes the list for correction.
2. **Election schedule:** the date is announced; the code of conduct comes into force.
3. **Nomination:** parties and independent candidates file nominations, which are checked for eligibility.
4. **Campaign:** manifestos, meetings and house visits within the code of conduct, with limits on spending.
5. **Voting:** at the polling station the voter's name is checked, the voter marks the ballot in secret and drops it in the box. Security forces keep peace.
6. **Counting and results:** votes are counted at the counting centre in front of party agents and observers; the winner is declared and given a certificate.

```photo id="soc10/voter" caption="A voter casts a ballot in the local elections of 2022. The secret ballot and an independent Election Commission protect free choice." width="62"
```

### Role of citizens

1. **Register and vote** — vote in every election, and vote freely and by conscience.
2. **Know the candidates and their programmes**, and choose on merit, not on caste, money, force or relation.
3. **Never sell or buy votes**, and refuse gifts, threats and pressure.
4. **Follow the election code of conduct**; do not spread false rumour or hate speech.
5. **Report** violations to the Election Commission or police.
6. **Take part** as polling officer, observer or volunteer; those who are eligible may stand as candidates.
7. **Accept the result peacefully**, and hold the winners to their promises.
8. **Educate others** — help first-time voters and the elderly to vote.

::: caution FPTP and PR are not the same
In FPTP the winner needs only more votes than the others in a constituency (a "plurality"), and only one person is elected. In PR the parties win seats according to their share of votes. The House of Representatives has 165 FPTP and 110 PR members: total 275.
:::

## 5.6 Human rights

### Meaning

::: definition Human rights
Human rights are the basic rights and freedoms that every person has simply because he or she is a human being, regardless of nationality, sex, caste, religion, language or any other status, and which no one may take away.
:::

### Features

| Feature | Meaning |
|---|---|
| Universal | They belong to all persons everywhere |
| Inherent and inalienable | We are born with them; they cannot be sold or taken away |
| Equal and non-discriminatory | Same for everyone |
| Indivisible and interdependent | All rights, civil and economic, are linked |
| Come with responsibilities | Respecting others' rights is a duty |

### Universal Declaration of Human Rights

After the horrors of the Second World War, the United Nations General Assembly adopted the **Universal Declaration of Human Rights (UDHR)** on **10 December 1948**; it has **30 articles**. Its first article says, "All human beings are born free and equal in dignity and rights." **10 December** is celebrated every year as **Human Rights Day**. The commission that drafted it was led by **Eleanor Roosevelt**.

```photo id="soc10/roosevelt-udhr" caption="Eleanor Roosevelt, who chaired the UN Commission on Human Rights that drafted the Universal Declaration of Human Rights, reads the Declaration." width="64"
```

### Kinds of human rights

| Kind | Examples |
|---|---|
| Civil and political | Right to life, liberty, equality before the law, freedom of expression, religion, vote |
| Economic, social and cultural | Education, health, work, food, housing, social security, language and culture |
| Collective and environmental rights | Right to a clean environment, right to development, rights of indigenous peoples |

### Human rights in the Constitution of Nepal

Part 3 of the Constitution (Articles 16 to 46) lists **31 fundamental rights**. Some of the main ones are:

| Right | Article | Meaning |
|---|---|---|
| Right to live with dignity | 16 | Every person has the right to live with dignity; no law shall provide for the death penalty |
| Right to freedom | 17 | Freedom of opinion and expression, peaceful assembly, forming organisations and parties, movement and profession |
| Right to equality | 18 | All citizens equal before the law; no discrimination on grounds of origin, religion, race, caste, sex or ideology; equal pay for equal work |
| Right to justice | 20 | Fair trial, a lawyer, to be informed of the reason for arrest |
| Right against torture | 22 | No one may be tortured during arrest or detention |
| Right against untouchability and discrimination | 24 | Caste-based untouchability is a crime |
| Right to property | 25 | Every citizen may acquire, own and sell property |
| Right to religious freedom | 26 | Freedom to practise one's religion; conversion by force or temptation is not allowed |
| Right against exploitation | 29 | No trafficking, slavery, bonded labour or forced work |
| Right to a clean environment | 30 | Right to live in a clean and healthy environment |
| Right to education | 31 | Free and compulsory basic education, free secondary education |
| Right of women | 38 | Equal lineage rights, safe motherhood, no violence |
| Right of the child | 39 | Name, identity, care, no child labour, marriage or army recruitment |
| Right to health | 35 | Free basic health service |
| Right to food, housing, employment, social security | 36, 37, 33, 43 | Basic needs |
| Right of the consumer | 44 | Quality goods and services |
| Right to constitutional remedy | 46 | Go to the Supreme Court if a fundamental right is violated |

Fundamental **duties** (Article 48) go with these rights: to protect the nation's independence, to obey the constitution and law, to serve the nation when required by law and to protect public property.

### Violations of human rights

Caste-based discrimination and untouchability, trafficking, child labour and child marriage, domestic violence and violence against women, torture in custody, forced disappearances during the armed conflict (1996–2006), the lack of food and shelter for some people and discrimination against persons with disabilities and sexual and gender minorities.

### How to protect human rights

Know our rights and respect those of others; teach human rights in school and family; strong laws and independent courts; an active National Human Rights Commission, press and NGOs; international monitoring; punishment of offenders; and victims' support through compensation and rehabilitation.

## 5.7 Role of organisations in the protection of human rights

Human rights can be protected only if some bodies watch, inquire and speak up. Four groups work in Nepal.

| Level | Institution | Role |
|---|---|---|
| State | **Courts** (especially the Supreme Court) | Protect rights by writs, public interest litigation and punishment of violators |
| State | **National Human Rights Commission (NHRC)** | A constitutional body (Article 248) that protects and promotes human rights, receives complaints, investigates violations on its own initiative or on complaint, and recommends action and compensation |
| State | **Other commissions** | National Women Commission, National Dalit Commission, National Inclusion Commission, Indigenous Nationalities Commission and others, for their groups |
| State | **Police and Attorney General** | Investigate and prosecute offences |
| Civil society | **NGOs** (INSEC, Advocacy Forum, WOREC, CWIN, Maiti Nepal and others) | Monitor and report violations, give legal aid, run awareness and rehabilitation programmes |
| Media | Press and radio | Expose violations and inform citizens |
| International | **UN bodies** (UN Human Rights Council, Office of the High Commissioner for Human Rights, UNICEF, UN Women, ILO) | Make standards (conventions), monitor Nepal's reports, support the NHRC and government |
| International | **International NGOs** such as Amnesty International and the International Committee of the Red Cross | Research, campaign and humanitarian work, including visits to prisons |

### The NHRC at work

The NHRC was formed under a law in 2000 and became a constitutional commission in the constitutions that followed. It has a chairperson and members, and it can visit prisons and police custody, summon officials, and recommend punishment and compensation. Its recommendations carry strong moral weight and the government is expected to implement them. Citizens can send a complaint to the NHRC in writing or through its offices in the regions.

### International conventions Nepal is party to

The International Covenant on Civil and Political Rights (ICCPR); the International Covenant on Economic, Social and Cultural Rights (ICESCR); the Convention on the Elimination of All Forms of Discrimination against Women (CEDAW); the Convention on the Rights of the Child (CRC); the Convention on the Elimination of Racial Discrimination (CERD); and the Convention against Torture (CAT). By signing these, Nepal promises to bring its laws and practice into line and to report regularly.

### What citizens can do

Report violations; support victims; take part in human rights clubs and awareness campaigns; refuse to join in discrimination and rumour; and ask the courts and commission for remedy.

::: tip A complete answer
For "Role of organisations in protecting human rights", cover **government** (courts, NHRC), **NGOs and media**, and **international** bodies (UN, INGOs) with one example for each.
:::

## 5.8 Consumer rights

### Who is a consumer?

::: definition Consumer
A consumer is a person who buys or uses goods or services for personal or family use, and not for resale. A person who buys vegetables, a mobile phone, a bus ticket, an electricity connection or a school's tuition is a consumer.
:::

Consumers are often at a disadvantage because sellers know more about the product than buyers do. Consumer rights try to correct this. Article 44 of the Constitution of Nepal says that every consumer has the right to obtain quality goods and services and to be informed about the quality and the cost of goods and services, and that a consumer who suffers loss or damage from goods or services is entitled to compensation. The **Consumer Protection Act, 2075 (2018)** puts this into detail.

```photo id="soc10/market" caption="A vegetable seller at the market in Asan, Kathmandu. Honest weights, fair prices and fresh, safe goods are the basic rights of buyers in every market." width="72"
```

### Consumer rights

Consumers International, the world federation of consumer groups, lists eight basic rights, which are largely reflected in Nepal's law.

| Right | Meaning | Everyday example |
|---|---|---|
| Right to basic needs | Access to essential goods and services: food, clothing, shelter, health, education, water | Safe drinking water in every home |
| Right to safety | Protection from goods and services that may harm health or life | Not selling expired medicines, unsafe toys or adulterated food |
| Right to information | Correct facts about quality, quantity, price, ingredients, date of manufacture and expiry | Labels, price tag (MRP), expiry date |
| Right to choice | Freedom to select from a variety of goods at fair prices | No forced buying or tying one product to another |
| Right to be heard | Consumers' views are taken into account in policy and complaints are heard | Consumer forums and complaint desks |
| Right to redress (compensation) | Compensation or replacement for loss from bad goods or service | Replacement of a faulty mobile phone |
| Right to consumer education | Knowledge and skill to be an informed consumer | School lessons and media campaigns |
| Right to a healthy environment | A clean and safe environment | Controlling pollution from factories |

### Problems faced by consumers in Nepal

- **Adulteration** of food, milk, oil, spices and medicine.
- **Overcharging** above the printed price and **underweighing** or short measure.
- **Black marketing and hoarding** of goods, such as fuel or sugar, in time of shortage.
- **Expired, fake and substandard goods**, and tampered dates.
- **Misleading advertisements.**
- **Not giving a bill**, which also hides the seller's tax.
- **Online fraud** and the sale of unsafe goods on social media.
- **Weak monitoring** and slow action.

### Consumer responsibilities

1. **Check the label**: manufacturing and expiry date, price, weight, ingredients and the quality mark (**Nepal Standard "NS" mark** of the Nepal Bureau of Standards and Metrology) for goods that need it.
2. **Take a bill** (with **13% VAT**) for every purchase, and keep it as proof.
3. **Check weights, change and the price** before paying.
4. **Complain** to the proper office when cheated; do not accept injustice silently.
5. **Do not buy** smuggled, banned or doubtful goods and do not encourage hoarding.
6. **Be careful in online buying**: use known sellers and safe payment.
7. **Protect the environment**: avoid wasteful packaging, plastic bags and over-consumption.

### Institutions that protect consumers

| Institution | Role |
|---|---|
| **Department of Commerce, Supplies and Consumer Protection** | Monitors the market, controls prices and black marketing, handles complaints and enforces the Consumer Protection Act |
| **Local governments** | Market monitoring and action under their powers in their local area |
| **Nepal Bureau of Standards and Metrology** | Sets national standards, awards the NS mark, checks weights and measures |
| **Department of Food Technology and Quality Control** | Tests food quality and enforces food laws |
| **Department of Drug Administration** | Controls the quality of medicines |
| **Consumer rights organisations and the media** | Advocate, give education, test goods and expose frauds |
| **Courts and consumer complaint bodies** | Hear complaints and order compensation and punishment |

**World Consumer Rights Day** is observed every year on **15 March**, in memory of the 1962 message of US President John F. Kennedy to the US Congress on consumer rights.

### How to complain

```figure caption="How a consumer can seek redress."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8,2.2))
ax.set_xlim(0,12.4); ax.set_ylim(0,4.0); ax.axis('off')
steps=['Keep the bill\nand proof','Talk to the\nseller first','Complain to\nlocal office or\nDepartment','Case and\ncompensation\nunder law']
for i,s in enumerate(steps):
    x=0.1+i*3.1
    ax.add_patch(FancyBboxPatch((x,0.8),2.6,2.4,boxstyle='round,pad=0.05',fc='#e8f0f8',ec=ACCENT,lw=1))
    ax.text(x+1.3,2.0,s,ha='center',va='center',fontsize=7,color=INK)
    if i<3:
        ax.annotate('',xy=(x+3.08,2.0),xytext=(x+2.72,2.0),arrowprops=dict(arrowstyle='->',color=MUTED,lw=1))
```

::: example Worked example: a consumer case
**Problem.** Rita buys a packet of biscuits for Rs 50 from a shop. At home she finds that the packet expired three months ago. What should she do?

**Solution.** She should (1) keep the packet and the bill as proof; (2) return to the shop and ask for a refund or exchange, because selling an expired product violates her right to safety and information; (3) if the shopkeeper refuses, complain to the ward office or municipality's market monitoring team or to the Department of Commerce, Supplies and Consumer Protection with the proof; (4) report the manufacturer if the date was tampered with; and (5) share the experience with others so that they check the dates. This protects her and other consumers.
:::

## Chapter summary

- The **Constitution of Nepal 2072** divides state power among the **legislature** (makes laws), the **executive** (implements them) and the **judiciary** (interprets them and gives justice).
- **Federal Parliament** = President + **House of Representatives** (275: 165 FPTP + 110 PR; term 5 years) + **National Assembly** (59; term 6 years; one-third retire every 2 years). Bills need passage in both houses and the President's assent.
- **Federal executive:** the President (head of state, 5-year term), the **Prime Minister** (leader of the majority in the House of Representatives) and a **Council of Ministers** of not more than 25. The budget is presented on 15 Jestha.
- **Judiciary:** Supreme Court (Chief Justice + up to 20 judges), 7 High Courts, 77 District Courts and local Judicial Committees; it gives justice, does judicial review and protects rights by writs.
- **Political parties** organise the contest for power, form the government and the opposition, and shape opinion; Nepal has a multi-party system, with parties registered with the Election Commission.
- **Elections:** every citizen of 18 years may vote; the Election Commission (5 members, 6 years) conducts them; mixed FPTP + PR system; citizens must vote wisely, refuse bribes and accept results.
- **Human rights** are inherent rights of all; UDHR adopted 10 December 1948 (30 articles); Part 3 of Nepal's Constitution gives 31 fundamental rights; the NHRC, courts, NGOs and UN bodies protect them.
- **Consumer rights:** basic needs, safety, information, choice, being heard, redress, education and a healthy environment; Consumer Protection Act 2075; World Consumer Rights Day is 15 March.

## Practice questions

**Group A — Objective questions (1 mark each)**

1. The total number of members of the House of Representatives is <span class="marks">[1]</span>
   (a) 165 (b) 110 (c) 275 (d) 59
2. The term of the National Assembly members is <span class="marks">[1]</span>
   (a) 4 years (b) 5 years (c) 6 years (d) 8 years
3. Who appoints the Prime Minister of Nepal? <span class="marks">[1]</span>
   (a) Chief Justice (b) The President (c) Speaker (d) Election Commission
4. The highest court of Nepal is <span class="marks">[1]</span>
   (a) High Court (b) District Court (c) Supreme Court (d) Special Court
5. In Nepal, the minimum age for voting is <span class="marks">[1]</span>
   (a) 16 (b) 18 (c) 20 (d) 25
6. The Universal Declaration of Human Rights was adopted in <span class="marks">[1]</span>
   (a) 1945 (b) 1948 (c) 1966 (d) 1990
7. World Consumer Rights Day is observed on <span class="marks">[1]</span>
   (a) 15 March (b) 8 March (c) 10 December (d) 5 June
8. Which is a constitutional body that conducts elections in Nepal? <span class="marks">[1]</span>
   (a) Election Commission (b) CIAA (c) Public Service Commission (d) National Planning Commission

::: note Answers to Group A
**1.** (c) — 275 (165 FPTP + 110 PR).
**2.** (c) — six years; one-third retire every two years.
**3.** (b) — the President appoints the leader of the party with a majority in the House of Representatives.
**4.** (c) — Supreme Court.
**5.** (b) — 18 years.
**6.** (b) — 10 December 1948.
**7.** (a) — 15 March.
**8.** (a) — the Election Commission.
:::

**Group B — Short answer (2 marks each)**

1. Write any two functions of the legislature. <span class="marks">[2]</span>
2. Who is the head of state and who is the head of government in Nepal? <span class="marks">[2]</span>
3. What is judicial review? <span class="marks">[2]</span>
4. What is a political party? Give any two of its functions. <span class="marks">[2]</span>
5. Write any two duties of a voter. <span class="marks">[2]</span>
6. Define human rights. Write any two human rights guaranteed by the Constitution of Nepal. <span class="marks">[2]</span>
7. Write any four rights of consumers. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Makes laws; approves the budget; controls the executive; amends the constitution (any two).
**2.** The President is the head of state; the Prime Minister is the head of government.
**3.** It is the power of the Supreme Court to declare a law or government act void if it conflicts with the constitution.
**4.** An organised group of people with common ideas who seek power by elections. Functions: contest elections, form government or opposition, form public opinion (any two).
**5.** Be registered and vote freely and wisely; do not sell or buy votes; follow the code of conduct (any two).
**6.** Human rights are basic rights every person has by being human. Examples: right to equality, right to freedom, right to education, right against untouchability (any two).
**7.** Right to safety; information; choice; to be heard; redress; consumer education; basic needs; healthy environment (any four).
:::

**Group C — Long answer (4 marks each)**

1. Describe the structure of the Federal Parliament of Nepal and write any four functions of the legislature. <span class="marks">[4]</span>
2. Explain how the Prime Minister is appointed and write any four functions of the federal executive. <span class="marks">[4]</span>
3. Describe the structure of the courts of Nepal and explain any three functions of the judiciary. <span class="marks">[4]</span>
4. Explain the role of political parties in a democracy and suggest ways of improving them. <span class="marks">[4]</span>
5. Write about the role of citizens in an election. <span class="marks">[4]</span>
6. What are human rights? Explain the role of the National Human Rights Commission and other organisations in protecting human rights. <span class="marks">[4]</span>
7. Explain the rights and responsibilities of consumers. What would you do if you were cheated by a seller? <span class="marks">[4]</span>

::: note Answers to Group C
**1.** The Federal Parliament = President + House of Representatives (275 members, 5-year term) + National Assembly (59 members, 6-year term). Functions: make laws, approve budget, control the executive, approve treaties, amend the constitution, hold impeachment.
**2.** The President appoints the leader of the parliamentary party with a majority in the House of Representatives as Prime Minister (if no majority, a leader who can get the support of two or more parties). The Prime Minister forms a Council of Ministers of up to 25. Functions: implement laws, prepare policy and budget, maintain law and order, conduct foreign relations, run administration.
**3.** Supreme Court (Chief Justice and up to 20 judges), 7 High Courts, 77 District Courts, Judicial Committees at local level. Functions: give justice; interpret the constitution and law; judicial review; issue writs to protect rights; public interest litigation (any three).
**4.** Role: contest elections; form government and opposition; make policies; educate and unite citizens; link people with government. Improvement: internal democracy, financial transparency, ethical leaders, inclusion, obeying the code of conduct.
**5.** Register and vote; choose by merit; refuse bribes and pressure; follow the code; report violations; take part as observer or volunteer; accept results peacefully.
**6.** Human rights are the basic rights of all people. NHRC: receives complaints, investigates, recommends action and compensation. Courts: writs and public interest litigation. NGOs and media: monitor and report. UN bodies and INGOs: set standards, monitor and support.
**7.** Rights: safety, information, choice, to be heard, redress, education, basic needs, healthy environment. Responsibilities: check labels and dates, take a bill, check weights, complain, avoid fake goods. If cheated: keep the bill and proof, speak to the seller, complain to the local government or the Department of Commerce, Supplies and Consumer Protection and seek compensation.
:::
