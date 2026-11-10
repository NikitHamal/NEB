---
file: NEBians-IOE-Past-Paper-Project-Engineering-and-Management-ENEE301-2082-Chaitra.pdf
subject: Project Engineering and Management
level: BE · Year III / Part I
code: ENEE 301
year_bs: 2082 Chaitra
cal: BS
year_ad: 2026
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular exam (new course), BE Electrical (BEL), Year III / Part I. Full marks 60, pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) Define the term project management. Compare the traditional vs. agile project management methods. Explain on triple constraints in a project. [[2+2+2]]

b) Starting from the process of project closure, explain how is it archived, either success or failure, for the future reference. [[6]]

@q 2
a) What do you understand by the feasibility analysis of a project? Elaborate how feasibility analysis of an engineering project is carried out. [[6]]

b) Define NPV and payback period of project and discuss its significance in project appraisal. Calculate simple payback period for the following cash flow: [[3+3]]

| Year | Cash flow (Rs.) |
|---|---|
| 0 | −10,00,000 |
| 1 | 1,20,000 |
| 2 | 1,50,000 |
| 3 | 3,00,000 |
| 4 | 5,00,000 |
| 5 | 5,00,000 |

@q 3
a) Explain the application of bar chart in project management. [[4]]

b) Draw the CPM diagram and calculate all the components (EST, EFT, LST, LFT, TF, FF, IF1 and IF2) of CPM from the following information. [[8]]

| Activity | Duration (days) | Predecessor | Successor |
|---|---|---|---|
| A | 1 | – | D, E |
| B | 6 | – | F, J |
| C | 2 | – | G |
| D | 2 | A | H |
| E | 4 | A | H |
| F | 3 | B | I |
| G | 4 | C | J |
| H | 2 | D, E | K |
| I | 5 | F | L |
| J | 3 | B, G | – |
| K | 3 | H | L |
| L | 4 | I, K | – |

@q 4
a) Explain the stage of project procurement. Include the stages such as notice of expression of interest, request of proposal, and bid evaluation, in your analysis. [[6]]

b) Starting from the concept of project procurement, explain how dispute resolution is settled in contract administration. [[6]]

@q 5
a) What do you understand by project evaluation and how project evaluation is carried out during the execution phase of project? Explain with an aid of hydropower project. [[6]]

b) A project is undertaken where the work has to be completed within 60 days with a budget of Rs. 20,00,000. According to the progress reports, at the end of the first month, only 25% of the total work has been completed and 50% of the total budget has been spent. Also, for the completion of 25% work, the actual cost incurred is 50% of the total budgeted cost. Perform EVA and comment on performance. [[6]]

<!-- SOLUTIONS -->

@s 1
**(a) Project management.** The **application of knowledge, skills, tools and techniques to the project activities in order to meet the project requirements** (PMBOK): planning, organising, directing, monitoring and controlling the resources of a **temporary endeavour with a definite start and end** so that a unique product, service or result (a hydropower plant, a substation, a transmission line) is delivered within the scope, time, cost and quality. The five process groups are initiating, planning, executing, monitoring and controlling, and closing.

**Traditional (waterfall / predictive) vs agile.**

| Basis | Traditional (waterfall) | Agile (Scrum, Kanban) |
|---|---|---|
| Approach | Sequential phases: requirements → design → build → test → hand-over | Iterative, incremental **sprints** (1 to 4 weeks) each giving a working increment |
| Scope | **Fixed early**, change is controlled and costly | **Flexible**, the backlog is re-prioritised after each sprint |
| Planning | Detailed up-front plan (WBS, Gantt, CPM) | Rolling-wave, adaptive planning |
| Customer role | At the start (requirements) and the end (acceptance) | **Continuous** involvement and feedback |
| Documentation | Heavy and formal | Light, working product over documents |
| Risk | Found late (at testing), high cost of change | Found early, low cost of change |
| Team | Hierarchical, the project manager commands | Self-organising, cross-functional, the project manager is a facilitator |
| Best for | Civil, hydropower, construction and other projects with stable scope and large physical work | Software, product development, uncertain and changing requirements |

**Triple constraints.** Every project is bounded by three interdependent constraints, the **project management triangle**:

1. **Scope** (quality and performance): what is to be delivered, the specifications and the quality;
2. **Time** (schedule): the duration and the completion date;
3. **Cost** (budget, resources).

A change in one affects at least one of the others: adding scope increases the time or cost, shortening the schedule (crashing) increases the cost, cutting the cost reduces the scope or quality. The **quality** (and the risk and the resources) is at the centre, being the result of balancing the three; the project manager's job is to keep them in balance.

```figure caption="Question 1(a): the triple constraint (project management triangle): scope, time and cost, with quality at the centre. A change in any one forces a change in at least one of the others."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(3.9,3.0)); ax.axis("off")
tri=np.array([[0,0],[4,0],[2,3.4],[0,0]])
ax.plot(tri[:,0],tri[:,1],color=ACCENT,lw=2); ax.fill(tri[:,0],tri[:,1],color=ACCENT,alpha=0.08)
ax.text(2,3.65,"SCOPE",ha="center",fontsize=9,fontweight="bold"); ax.text(-0.1,-0.35,"TIME",ha="center",fontsize=9,fontweight="bold"); ax.text(4.1,-0.35,"COST",ha="center",fontsize=9,fontweight="bold")
ax.text(2,1.0,"QUALITY\n(risk, resources)",ha="center",va="center",fontsize=8,color=INK)
ax.text(0.45,1.8,"schedule\nslips",fontsize=6.5,color=MUTED,ha="center",rotation=60); ax.text(3.6,1.8,"budget\noverrun",fontsize=6.5,color=MUTED,ha="center",rotation=-60)
ax.set_xlim(-0.8,4.9); ax.set_ylim(-0.7,4.0)
```

**(b) Project closure and archiving of the project record.** Closure is the last process group: **all the work is formally completed, the product is accepted by the owner and the project is released**, whether it ended in success, in early termination or in failure. The steps are:

1. **Scope verification and formal acceptance:** inspection, tests and commissioning (e.g. the trial run of the power plant), **punch-list** completion, the **taking-over certificate** and the defects liability period, and the hand-over of the as-built drawings, the O&M manuals and the training.
2. **Administrative closure:** the final payment and the release of the retention money and the performance security, the settlement of claims and the **contract closure** (the formal written notice that the contract is complete), the release of the staff and the equipment, and the closing of the project accounts.
3. **Lessons learned / post-implementation review** (the project audit): what worked and what failed, the **cost and the schedule variances against the baseline**, the quality results, the risk and the issue logs, the performance of contractors and the suppliers, and the **root causes of any failure** (the reasons for cancellation if terminated early).
4. **Archiving of the project records** for future reference:
   - collect and **index** all documents: the feasibility study, the design and drawings, the contract documents, the correspondence, the change orders and variations, the progress and the inspection reports, the test results, the financial records, the as-built records and the **lessons-learned report**;
   - store them in the **organisation's repository / knowledge base** (the project management information system, and a document control system) under the **retention period** set by the law and the policy, with the access control and backup, in the physical and the digital form;
   - feed the lessons and the **historical data** (the unit costs, the productivity, the durations, the risk register) into the organisational process assets for the estimating and planning of the **future similar projects**, for both the **successful** project (the best practices) and the **failed** one (the mistakes to avoid, the claims and the dispute record).
5. **Celebrate and release** the team, and a **final project report** to the stakeholders.

@s 2
**(a) Feasibility analysis.** A **systematic study done before the commitment of resources to decide whether the proposed project is technically possible, economically and financially viable, legally and socially acceptable and environmentally sound**, and which of the alternatives is the best. The outcome is the **feasibility study report** with the recommendation to go, to modify or not to go. It reduces the risk of failure and is the basis of the financing (the bank, the donor).

**How it is carried out for an engineering project** (e.g. a small hydropower or a transmission line):

1. **Pre-feasibility / identification:** the need, the objectives, the alternatives and the screening (the map study).
2. **Technical feasibility:** the site investigation and the surveys (the topographic, geological, hydrological), the capacity, the technology, the layout and design alternatives, the availability of the materials, the manpower and the equipment, the construction method and the schedule, and the O&M.
3. **Economic feasibility:** the **cost–benefit analysis** over the project life: the capital and the O&M costs, the benefits (energy sales, the avoided cost, the employment) at the shadow prices, with the economic indicators $B/C$, **EIRR, ENPV**.
4. **Financial feasibility:** the funding sources and the structure (the equity, the loan, the grant), the cash flows, the revenue (the PPA tariff), the **NPV, IRR, payback period, B/C**, the debt service coverage ratio, and the **sensitivity analysis** (cost +10 %, the delay, the revenue −10 %) and the risk.
5. **Environmental and social feasibility:** the IEE/EIA, the land acquisition and the resettlement, the community benefits, the gender and the social inclusion, and the climate resilience.
6. **Legal and institutional / managerial feasibility:** the licences and the permits (the generation licence, the water rights), the policies and the regulations, the organisation and the capacity to implement and to operate.
7. **Market / commercial feasibility** (the demand forecast, the off-taker) and the **risk assessment**.
8. **Decision:** compare the alternatives (the matrix of the criteria), prepare the report with the recommendation, and the approval by the decision makers.

**(b) NPV.** The **net present value** is the sum of the present values of all the cash inflows minus the outflows over the project life, discounted at the required rate of return (the opportunity cost of capital, the MARR) $i$:

$$ \text{NPV} = \sum_{t=0}^{n}\frac{C_t}{(1+i)^t} = -C_0 + \sum_{t=1}^{n}\frac{B_t - O_t}{(1+i)^t} $$

*Significance:* it accounts for the **time value of money** and for all the cash flows of the whole life, and it gives the **absolute value added** to the owner. **Decision rule:** accept if $\text{NPV} > 0$ (the return is above $i$), reject if $\text{NPV} < 0$, indifferent if zero; among mutually exclusive alternatives choose the **highest NPV**. It is additive, but it needs a discount rate and favours the large projects (so use it with the B/C ratio or the IRR).

**Payback period.** The time (in years) needed to **recover the initial investment from the net cash inflows**: the simple payback ignores the time value, the discounted payback discounts the flows at $i$.

*Significance:* a simple measure of **liquidity and risk** (the shorter, the less exposed to uncertainty), easy to understand, and used to **screen** the projects; its weakness is that it **ignores the cash flows after the payback** and (for the simple form) the time value of money, so it is not a measure of profitability, and it is used together with NPV or IRR.

**Simple payback for the given cash flow.**

| Year | Cash flow (Rs.) | Cumulative (Rs.) |
|---|---|---|
| 0 | −10,00,000 | −10,00,000 |
| 1 | 1,20,000 | −8,80,000 |
| 2 | 1,50,000 | −7,30,000 |
| 3 | 3,00,000 | −4,30,000 |
| 4 | 5,00,000 | **+70,000** |
| 5 | 5,00,000 | +5,70,000 |

The cumulative cash flow changes sign during year 4; the balance to recover at the end of year 3 is Rs. 4,30,000:

$$ \text{Payback} = 3 + \frac{4{,}30{,}000}{5{,}00{,}000} = 3.86\ \text{years} \approx 3\ \text{years } 10\frac{1}{2}\ \text{months} $$

$$ \boxed{\text{Simple payback period} \approx 3.86\ \text{years}} $$

*Additional appraisal at a 10 % discount rate (not asked, for information):* $\text{NPV} = -10{,}00{,}000 + \dfrac{1{,}20{,}000}{1.1} + \dfrac{1{,}50{,}000}{1.1^2} + \dfrac{3{,}00{,}000}{1.1^3} + \dfrac{5{,}00{,}000}{1.1^4} + \dfrac{5{,}00{,}000}{1.1^5} = \text{Rs. } 1{,}10{,}420$, and the IRR is about 13.3 %. The discounted payback is a little under 5 years (the cumulative discounted balance is −2,00,041 at year 4 and +1,10,420 at year 5), so the project is acceptable at 10 %.

@s 3
**(a) Bar (Gantt) chart in project management.** A bar chart (Gantt chart, Henry Gantt 1910s) shows the activities in the rows and the **time on the horizontal axis**, each activity as a horizontal bar from its start to its finish whose length is proportional to its duration. Applications:

1. **Planning and scheduling:** the sequence and the timing of the activities of the WBS and the project duration at a glance, simple to prepare and to understand even by non-technical people and workers.
2. **Resource planning and levelling:** the labour, equipment and material needs are summed along the time axis (the resource histogram under the chart) and the peaks are smoothed.
3. **Progress monitoring and control:** the **planned bars are compared with the actual progress bars** (the shading of the completed part and the "today" line), so the delay is seen immediately; the cash flow and the **S-curve** are derived from it.
4. **Communication and reporting** to the client and the management, **milestones** (diamonds) and the contract deadlines, and the **look-ahead (weekly) programmes** at the site.
5. With **links (dependencies)** it works as a simple network, and it is the output format of CPM/PERT software (MS Project, Primavera).

*Limitations:* it does not show the **interdependencies** and the critical path clearly (unless linked), is difficult to update for a large project and has no probabilistic information.

The bar chart of the given project is drawn in part (b) (earliest start, with the float of the non-critical activities shown by the pale extension).

**(b) CPM network** (activity-on-node form; the node shows EST, EFT above and LST, LFT below). Forward pass: $EST = \max(EFT\ \text{of predecessors})$, $EFT = EST + D$. The project duration is the largest EFT, $T = 18$ days (activity L; J also finishes at day 9, early). Backward pass: $LFT = \min(LST\ \text{of successors})$, $LST = LFT - D$, with $LFT = 18$ for the activities with no successor (J and L).

**Floats.**

- Total float: $TF = LST - EST = LFT - EFT$.
- Free float: $FF = \min(EST_{succ}) - EFT$.
- **IF1, interfering float** (the "head" part of the total float): $IF_1 = TF - FF$ (the part of TF that, if used, reduces the float of the following activities).
- **IF2, independent float:** $IF_2 = \max\big[0,\ \min(EST_{succ}) - \max(LFT_{pred}) - D\big]$ (the float that is not affected by the float of any other activity; it exists only when the activity may be shifted without any effect on the predecessors or successors).

| Act. | D | EST | EFT | LST | LFT | TF | FF | IF1 = TF − FF | IF2 |
|---|---|---|---|---|---|---|---|---|---|
| A | 1 | 0 | 1 | 4 | 5 | 4 | 0 | 4 | 0 |
| **B** | 6 | 0 | 6 | 0 | 6 | **0** | 0 | 0 | 0 |
| C | 2 | 0 | 2 | 9 | 11 | 9 | 0 | 9 | 0 |
| D | 2 | 1 | 3 | 7 | 9 | 6 | 2 | 4 | 0 |
| E | 4 | 1 | 5 | 5 | 9 | 4 | 0 | 4 | 0 |
| **F** | 3 | 6 | 9 | 6 | 9 | **0** | 0 | 0 | 0 |
| G | 4 | 2 | 6 | 11 | 15 | 9 | 0 | 9 | 0 |
| H | 2 | 5 | 7 | 9 | 11 | 4 | 0 | 4 | 0 |
| **I** | 5 | 9 | 14 | 9 | 14 | **0** | 0 | 0 | 0 |
| J | 3 | 6 | 9 | 15 | 18 | 9 | 9 | 0 | 0 |
| K | 3 | 7 | 10 | 11 | 14 | 4 | 4 | 0 | 0 |
| **L** | 4 | 14 | 18 | 14 | 18 | **0** | 0 | 0 | 0 |

(Examples: for D, $FF = EST_H - EFT_D = 5 - 3 = 2$; for J, $FF = 18 - 9 = 9$; for K, $FF = EST_L - EFT_K = 14 - 10 = 4$; for E, $FF = 5 - 5 = 0$ and $TF = 4$ is shared with H and K on the path A–E–H–K–L.)

**Critical path** (all floats zero): $B \to F \to I \to L$, with duration $6 + 3 + 5 + 4 = 18$ days.

$$ \boxed{\text{Project duration} = 18\ \text{days; critical path B–F–I–L}} $$

The second-longest path is A–E–H–K–L, with $1 + 4 + 2 + 3 + 4 = 14$ days (4 days of float), then C–G–J (9 days; it ends at day 9 against the project end 18, so 9 days of float).

```figure caption="Question 3(b): CPM network (activity-on-node). Each box: top EST | EFT, middle activity and duration, bottom LST | LFT. The critical path B–F–I–L (blue, bold) has zero total float and a length of 18 days."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(6.6,4.0)); ax.axis("off")
pos={"A":(0,4.4),"B":(0,2.2),"C":(0,0),"D":(2.7,5.5),"E":(2.7,3.8),"F":(2.7,2.2),"G":(2.7,0),"H":(5.4,4.6),"I":(5.4,2.2),"J":(5.4,0),"K":(8.1,4.6),"L":(8.1,2.2)}
D={'A':1,'B':6,'C':2,'D':2,'E':4,'F':3,'G':4,'H':2,'I':5,'J':3,'K':3,'L':4}
ES=dict(A=0,B=0,C=0,D=1,E=1,F=6,G=2,H=5,I=9,J=6,K=7,L=14); LS=dict(A=4,B=0,C=9,D=7,E=5,F=6,G=11,H=9,I=9,J=15,K=11,L=14)
crit=set("BFIL")
W,H=1.7,1.2
for a,(x,y) in pos.items():
    c=ACCENT if a in crit else INK
    ax.add_patch(mp.Rectangle((x,y),W,H,fc="#e8effc" if a in crit else "white",ec=c,lw=1.6 if a in crit else 0.9))
    ax.plot([x,x+W],[y+H*0.33,y+H*0.33],color=c,lw=0.6); ax.plot([x,x+W],[y+H*0.67,y+H*0.67],color=c,lw=0.6)
    ax.text(x+W/2,y+H*0.835,f"{ES[a]}  |  {ES[a]+D[a]}",ha="center",va="center",fontsize=7.5)
    ax.text(x+W/2,y+H*0.5,f"{a} ({D[a]})",ha="center",va="center",fontsize=8.5,fontweight="bold",color=c)
    ax.text(x+W/2,y+H*0.165,f"{LS[a]}  |  {LS[a]+D[a]}",ha="center",va="center",fontsize=7.5)
E=[("A","D"),("A","E"),("B","F"),("B","J"),("C","G"),("D","H"),("E","H"),("F","I"),("G","J"),("H","K"),("I","L"),("K","L")]
for u,v in E:
    (x1,y1),(x2,y2)=pos[u],pos[v]; c=ACCENT if (u in crit and v in crit) else MUTED
    ax.annotate("",xy=(x2,y2+H/2),xytext=(x1+W,y1+H/2),arrowprops=dict(arrowstyle="-|>",color=c,lw=1.8 if c==ACCENT else 0.9,shrinkA=0,shrinkB=0))
ax.text(9.9,2.8,"project end\nday 18",fontsize=7.5,color=MUTED,va="center")
ax.set_xlim(-0.3,10.9); ax.set_ylim(-0.3,6.9)
```

```figure caption="Question 3(b): bar chart (earliest-start Gantt chart) of the same project; dark bars are the activity durations, pale extensions the total float, and the critical activities B, F, I, L are blue."
D={'A':1,'B':6,'C':2,'D':2,'E':4,'F':3,'G':4,'H':2,'I':5,'J':3,'K':3,'L':4}
ES=dict(A=0,B=0,C=0,D=1,E=1,F=6,G=2,H=5,I=9,J=6,K=7,L=14); TF=dict(A=4,B=0,C=9,D=6,E=4,F=0,G=9,H=4,I=0,J=9,K=4,L=0)
fig,ax=plt.subplots(figsize=(5.8,3.1))
acts=list("ABCDEFGHIJKL")
for i,a in enumerate(acts):
    y=len(acts)-1-i; c=ACCENT if TF[a]==0 else INK
    ax.barh(y,D[a],left=ES[a],color=c,height=0.55)
    if TF[a]: ax.barh(y,TF[a],left=ES[a]+D[a],color=c,alpha=0.22,height=0.55)
    ax.text(ES[a]+D[a]/2,y,str(D[a]),ha="center",va="center",color="white",fontsize=7)
ax.set_yticks(range(len(acts))); ax.set_yticklabels(acts[::-1],fontsize=7.5); ax.set_xticks(range(0,19,2)); ax.tick_params(labelsize=7)
ax.axvline(18,color=MUTED,lw=0.8,ls="--"); ax.set_xlabel("days",fontsize=8); ax.grid(True,axis="x",color=GRID,lw=0.5)
fig.tight_layout()
```

@s 4
**(a) Stages of project procurement.** Procurement is the process of **acquiring goods, works, and consulting / non-consulting services from the outside the organisation** (in Nepal under the Public Procurement Act 2063 and Rules 2064, the PPMO). The main stages:

1. **Procurement planning:** the need identification, the **procurement plan and the packaging** (the lots, the method, the schedule, the budget), the cost estimate, and the approval.
2. **Choice of the procurement method:** works and goods by **open competitive bidding (NCB/ICB)**, limited, RFQ (shopping) or direct; consultants by QCBS, QBS, FBS, LCS or the single source, according to the value and the nature.
3. **Notice of expression of interest (EOI) (for consulting services):** a public **invitation (published in the national newspapers and the PPMO portal, 15 days)** asking the consultants to express their interest with a short document on their experience, the capacity, the staff and the legal status; the **evaluation of the EOIs** (the criteria, the scores) prepares the **short list of 3 to 7 consultants**.
4. **Preparation of the bidding / RFP documents:** the **request for proposal (RFP)** for consultants (the letter of invitation, the instructions to consultants, the terms of reference, the data sheet, the evaluation criteria and the weights, the draft contract); for works and goods the **bidding documents** (the invitation for bids, the instructions to bidders (ITB), the bid data sheet, the conditions of contract, the specifications, the drawings, the BOQ, the forms), with the **bid security** and the **performance security** requirements.
5. **Invitation, pre-bid meeting, the clarifications and the amendments;** the bid / proposal **submission** by a fixed deadline.
6. **Bid opening:** the **public opening** in the presence of the bidders (technical proposals first for QCBS; the financial proposals only for the technically qualified), the record of the bid prices and securities.
7. **Bid evaluation:**

   - *preliminary (responsiveness) examination:* the completeness, the signatures, the security, the eligibility;
   - *technical evaluation:* the qualification (the experience, the financial capacity, the equipment, the personnel) and the technical compliance, **pass/fail** for works, or scoring for the consultants (e.g. the minimum technical score 70 %);
   - *financial evaluation:* the **arithmetical correction**, the conversion to the single currency, the adjustment and the **ranking of the evaluated costs**, the **lowest evaluated substantially responsive bid** for the works and goods; for the QCBS the combined score $S = w_tS_t + w_fS_f$ with the lowest-cost proposal at $S_f = 100$;
   - the **evaluation report** and the **post-qualification**.
8. **Award:** the notice of the intention to award, the **standstill period (7 days) for the complaints**, the **negotiation** (consultants, within limits), the **approval**, the **letter of acceptance** and the **contract agreement** after the performance security.
9. **Contract administration:** the procurement ends with the contract signing and the commencement; and the monitoring and closure (see Q4(b)).

```figure caption="Question 4(a): the stages of project procurement from the plan to the contract award; the EOI and RFP stages are for consulting services, the bid stages for the works and goods."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(6.6,2.6)); ax.axis("off")
st=["Procurement\nplan & packaging","Select method\n(open / RFQ / QCBS)","Notice of EOI\n+ shortlist","RFP / bidding\ndocuments","Invite, pre-bid\nmeeting, submit","Open bids\n(public)","Evaluate: prelim,\ntechnical, financial","Award, standstill,\nnegotiate, contract"]
for i,t in enumerate(st):
    x=(i%4)*2.6; y=1.6 if i<4 else 0.0
    ax.add_patch(mp.FancyBboxPatch((x,y),2.1,1.0,boxstyle="round,pad=0.04",fc="#eef2fb" if i not in (2,3) else "#fdf1dd",ec=INK,lw=0.9)); ax.text(x+1.05,y+0.5,f"{i+1}. "+t,ha="center",va="center",fontsize=6.6)
    if i%4<3: ax.annotate("",xy=(x+2.55,y+0.5),xytext=(x+2.14,y+0.5),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.2))
ax.annotate("",xy=(0.2,1.0),xytext=(10.0,1.6),arrowprops=dict(arrowstyle="-|>",color=MUTED,lw=0.8,connectionstyle="arc3,rad=0.0",ls="--"))
ax.set_xlim(-0.2,10.6); ax.set_ylim(-0.2,2.8)
```

**(b) Dispute resolution in contract administration.** After the contract is awarded, the **contract administration** (monitoring the performance, the variations, the payments, the claims, and the closure) is done by the engineer / project manager under the **conditions of contract** (e.g. the PPMO standard bidding documents, FIDIC). Because the procurement documents fix the **dispute clauses in advance**, a dispute (about the time extension, the variation, the payment, the quality, or the termination) is settled in the **escalating steps**:

1. **Notice of the claim / dispute:** the party gives the written notice within the time limit (e.g. 28 days), with the particulars; the **Engineer (Project Manager) makes a determination / decision** on the claim after consulting both the parties, **within 28 days**.
2. **Amicable settlement / negotiation:** if a party is dissatisfied, the parties try to settle the matter **by mutual discussion** (the senior management) within a period (28 days).
3. **Dispute Board / Adjudicator (DAB):** for large works, the standing or ad-hoc board of the independent experts gives a **non-final, binding-in-the-interim decision** within 84 days; it is valid unless one party gives the **notice of dissatisfaction**.
4. **Conciliation / mediation:** a neutral third person helps to reach the settlement (non-binding).
5. **Arbitration:** the final step under the **Arbitration Act 2055 of Nepal** (the ICC rules or the national arbitration for the international contracts): the **arbitral tribunal (1 or 3 arbitrators)** hears the parties and gives the **final and binding award**, enforceable like a court decree; the place, the language and the law are fixed in the contract.
5. **Court:** only in the limited cases (the challenge or the enforcement of the award, or if the contract has no arbitration clause) the dispute goes to the **District/High Court**.

During the dispute the contractor must **continue the work** and the Engineer continues to certify the undisputed payments. The best practice is **to avoid the disputes** by the clear contract documents, the regular meetings, the proper records and the early notice and the early settlement, which is cheaper and faster.

@s 5
**(a) Project evaluation.** The **systematic and objective assessment of an ongoing or completed project: its design, its implementation and its results**, against the planned objectives, the schedule, the cost and the quality, to judge its **relevance, efficiency, effectiveness, impact and sustainability** (the OECD-DAC criteria), and to draw lessons and corrective actions. Monitoring is the routine tracking of the inputs and the progress; evaluation is the periodic judgement of the performance. The evaluation can be **ex-ante** (the appraisal), **during the execution (mid-term / concurrent)** and **ex-post** (the completion and the impact evaluation).

**Evaluation during the execution phase** is done by:

1. Fixing the **baseline** (the scope, the schedule, the budget, the quality plan) and the **indicators** (the physical progress %, the cost, the time, the quality, the safety).
2. **Collecting the data** regularly: the site progress reports, the measurement and the running-bill (IPC) records, the inspection and the test results, the site meetings and the visits, the financial records.
3. **Comparing the actual with the plan:** the schedule variance (the bar chart / S-curve, the critical path update), the **cost variance** and the **earned value analysis** (SPI, CPI, EAC), the quality (the test results and the non-conformance reports), the safety and the environmental compliance (EMP), and the risks.
4. **Evaluation meetings and the mid-term review** with the client, the consultant and the lenders, the **forecast of the completion time and cost**, the identification of the causes of the deviation.
5. **Corrective action:** the recovery plan (the crashing, the additional resources, the re-sequencing), the variation orders, the re-allocation of the budget, the contract notices (the delay and the penalty), and the reporting to the stakeholders.

**Illustration with a hydropower project** (e.g. a 20 MW run-of-river project):

- *Relevance and design:* is the energy still needed (the PPA with NEA), is the design (the intake, the headrace tunnel, the powerhouse) adequate against the hydrological data and the geology found during the construction (the poor rock in the tunnel).
- *Efficiency (time and cost):* the physical progress of each package: the access road, the **headworks (weir, intake, desander)**, the **headrace tunnel (the metres excavated per month against the plan, the support quantities)**, the penstock, the powerhouse civil works, the **electro-mechanical (turbine, generator, transformer, transmission line)**. The cumulative S-curve of the planned against the actual progress and cost, the **SPI and CPI** and the critical path (usually the tunnel and the E&M delivery) are updated monthly; the delay due to the monsoon, the landslides, the blockades and the late EM delivery is analysed and the recovery (the additional tunnel faces, the night shifts) is decided.
- *Effectiveness and quality:* the concrete cube tests, the penstock welding inspection, the turbine factory tests and the specified output $P = \eta\rho gQH$ (the net head and the discharge) against the design.
- *Safety, environment and social:* the environmental management plan (the minimum environmental flow release, the muck disposal), the benefit sharing and the compensation, the lost-time injuries.
- *Financial:* the payments, the IDC (the interest during construction) that rises with the delay, the **forecast IRR and NPV** with the updated cost and the COD (the commercial operation date), and the lender's technical advisor's reports. Based on this the decisions (the time extension, the variation, the re-financing) are taken.

**(b) Earned value analysis (EVA).** Data: budget at completion $BAC = $ Rs. 20,00,000; planned duration 60 days; at the end of month 1 (day 30).

- **Planned value** $PV$ = budgeted cost of the work scheduled. Assuming the uniform plan, at 30 of 60 days the planned progress is 50 %: $PV = 0.50 \times 20{,}00{,}000 = \text{Rs. } 10{,}00{,}000$.
- **Earned value** $EV$ = budgeted cost of the work performed $= 0.25 \times 20{,}00{,}000 = \text{Rs. } 5{,}00{,}000$.
- **Actual cost** $AC = 0.50 \times 20{,}00{,}000 = \text{Rs. } 10{,}00{,}000$ (the 50 % of the budget spent, for the 25 % work).

| Measure | Formula | Value |
|---|---|---|
| Schedule variance $SV$ | $EV - PV$ | $5{,}00{,}000 - 10{,}00{,}000 = -5{,}00{,}000$ |
| Cost variance $CV$ | $EV - AC$ | $5{,}00{,}000 - 10{,}00{,}000 = -5{,}00{,}000$ |
| Schedule performance index $SPI$ | $EV/PV$ | $0.50$ |
| Cost performance index $CPI$ | $EV/AC$ | $0.50$ |
| Estimate at completion $EAC$ | $BAC/CPI$ | Rs. 40,00,000 |
| Estimate to complete $ETC$ | $EAC - AC$ | Rs. 30,00,000 |
| Variance at completion $VAC$ | $BAC - EAC$ | −Rs. 20,00,000 |
| To-complete performance index $TCPI$ | $\dfrac{BAC - EV}{BAC - AC}$ | $\dfrac{15{,}00{,}000}{10{,}00{,}000} = 1.5$ |
| Forecast duration | $60/SPI$ | 120 days |

**Comment on the performance.** $SV < 0$ and $SPI = 0.5$: the project is **behind the schedule**, doing only half of the planned work, and at this rate it will take about **120 days instead of 60** (a 100 % delay). $CV < 0$ and $CPI = 0.5$: the project is **over the budget**, each rupee spent gives only 50 paisa of work, and if the trend continues the final cost will be **Rs. 40,00,000, i.e. twice the budget**, a shortfall of Rs. 20,00,000. The $TCPI = 1.5$ shows that, to finish within the original budget, the remaining work would have to be done at **1.5 times the budgeted efficiency**, which is unrealistic. The project is in serious trouble (both behind the schedule and over the budget): the corrective actions are an urgent review of the causes, a recovery schedule (the additional resources and the crashing, re-sequencing), tighter cost control, and a re-baseline or the re-negotiation of the scope/budget with the client.

```figure caption="Question 5(b): earned value at the end of month 1 (day 30): planned value 10 lakh, earned value 5 lakh, actual cost 10 lakh; both the schedule and cost variances are −5 lakh (SPI = CPI = 0.5)."
fig,axs=plt.subplots(1,2,figsize=(6.2,2.6))
a=axs[0]; a.bar(["PV","EV","AC","BAC"],[10,5,10,20],color=[MUTED,ACCENT,INK,"#c9d4e8"],width=0.55)
for i,v in enumerate([10,5,10,20]): a.text(i,v+0.4,f"{v}",ha="center",fontsize=8)
a.set_ylabel("Rs. lakh",fontsize=8); a.tick_params(labelsize=7.5); a.set_ylim(0,23); a.set_title("at day 30",fontsize=8)
b=axs[1]; t=np.array([0,30,60,90,120]); pv=np.array([0,10,20,20,20]); b.plot([0,60],[0,20],color=MUTED,lw=1.6,label="planned value (PV)")
b.plot([0,30],[0,5],color=ACCENT,lw=1.8,label="earned value (EV)"); b.plot([0,30],[0,10],color=INK,lw=1.4,label="actual cost (AC)")
b.plot([30,120],[5,20],color=ACCENT,lw=1.2,ls="--"); b.plot([30,120],[10,40],color=INK,lw=1.2,ls="--")
b.text(104,40.5,"EAC = 40",fontsize=7); b.text(104,16,"EV = 20 at 120 d",fontsize=7,color=ACCENT)
b.set_xlabel("days",fontsize=8); b.set_ylabel("Rs. lakh",fontsize=8); b.legend(fontsize=6.5,loc="upper left"); b.tick_params(labelsize=7.5); b.grid(True,color=GRID,lw=0.5); b.set_ylim(0,45); b.set_title("trend (forecast dashed)",fontsize=8)
fig.tight_layout()
```
