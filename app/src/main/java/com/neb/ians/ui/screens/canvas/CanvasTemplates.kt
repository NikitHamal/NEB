package com.neb.ians.ui.screens.canvas

object CanvasTemplates {
    fun getTemplates(): List<CanvasTemplate> {
        return listOf(
            CanvasTemplate(
                key = "blank",
                name = "Blank Canvas",
                subtitle = "Freeform exploration",
                description = "Start with a single seed topic and branch concepts outwards in any direction.",
                iconName = "space_dashboard",
                initialNodes = listOf(
                    CanvasNode(
                        id = "node_seed",
                        boardId = "",
                        parentId = null,
                        prompt = "My First Idea",
                        title = "Central Concept",
                        kind = "topic",
                        color = "blue",
                        x = 120f,
                        y = 80f,
                        content = CanvasNodeContent(
                            title = "Central Concept",
                            summary = "This is your starting point. Use the connector ports on any side to link related cards, or ask a follow-up question below.",
                            sections = listOf(
                                CanvasSection(
                                    type = "bullets",
                                    title = "How to explore",
                                    bulletItems = listOf(
                                        "Tap connector ports to link related cards together.",
                                        "Drag cards by their header to position them freely.",
                                        "Ask Neby to visualize diagrams, comparisons, or deep dives."
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            CanvasTemplate(
                key = "concept-master",
                name = "Concept Mastery",
                subtitle = "Feynman Technique",
                description = "Master any tricky topic by explaining simply, mapping mechanics, working examples, and self-testing.",
                iconName = "psychology",
                initialNodes = listOf(
                    CanvasNode(
                        id = "cm_root",
                        boardId = "",
                        parentId = null,
                        prompt = "The Core Concept",
                        title = "Core Concept",
                        kind = "topic",
                        color = "blue",
                        x = 230f,
                        y = 40f,
                        content = CanvasNodeContent(
                            title = "The Core Concept",
                            summary = "Define the subject in **plain, jargon-free English** as if explaining to a 12-year-old.",
                            sections = listOf(
                                CanvasSection(
                                    type = "text",
                                    content = "A good mental model eliminates obscurity. What is the fundamental intuition behind this phenomenon?"
                                ),
                                CanvasSection(
                                    type = "bullets",
                                    title = "Mastery criteria",
                                    bulletItems = listOf(
                                        "Can you explain it without checking notes?",
                                        "Where does the metaphor break down?",
                                        "What problem did its discovery solve?"
                                    )
                                )
                            )
                        )
                    ),
                    CanvasNode(
                        id = "cm_how",
                        boardId = "",
                        parentId = "cm_root",
                        prompt = "How it Works & Mechanism",
                        title = "Mechanisms & Components",
                        kind = "summary",
                        color = "purple",
                        x = 40f,
                        y = 560f,
                        content = CanvasNodeContent(
                            title = "Internal Mechanics",
                            summary = "Break the concept into **interacting parts** and inspect cause and effect.",
                            sections = listOf(
                                CanvasSection(
                                    type = "diagram",
                                    title = "Component Flow",
                                    nodes = listOf(
                                        DiagramNodeItem("p1", "Input Signal", "Raw observation or stimulus"),
                                        DiagramNodeItem("p2", "Transformation", "Mathematical or logical filter"),
                                        DiagramNodeItem("p3", "Latent State", "Internal compressed model"),
                                        DiagramNodeItem("p4", "Output", "Synthesized response or action")
                                    )
                                )
                            )
                        )
                    ),
                    CanvasNode(
                        id = "cm_example",
                        boardId = "",
                        parentId = "cm_root",
                        prompt = "Worked Example",
                        title = "Worked Example",
                        kind = "practice",
                        color = "green",
                        x = 420f,
                        y = 560f,
                        content = CanvasNodeContent(
                            title = "Worked Real-World Case",
                            summary = "Walk through a concrete problem from initial state to final verified solution.",
                            sections = listOf(
                                CanvasSection(
                                    type = "cards",
                                    title = "Step-by-step breakdown",
                                    cardItems = listOf(
                                        CardRefItem("Phase 1: Setup", "Define boundaries", listOf("List givens and unknowns", "Choose reference frame")),
                                        CardRefItem("Phase 2: Execution", "Apply principles", listOf("Compute intermediate values", "Sanity-check units"))
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            CanvasTemplate(
                key = "exam-sprint",
                name = "Exam Sprint",
                subtitle = "Syllabus to 100%",
                description = "High-yield revision board: topic weightage, formulas, active recall questions, and past paper traps.",
                iconName = "school",
                initialNodes = listOf(
                    CanvasNode(
                        id = "es_syllabus",
                        boardId = "",
                        parentId = null,
                        prompt = "High-Yield Topics",
                        title = "Syllabus Breakdown",
                        kind = "goal",
                        color = "amber",
                        x = 230f,
                        y = 40f,
                        content = CanvasNodeContent(
                            title = "Exam Weightage & Priority",
                            summary = "Cluster topics into **Must Master (60%)**, **High Probability (30%)**, and **Edge Cases (10%)**.",
                            sections = listOf(
                                CanvasSection(
                                    type = "comparison",
                                    title = "Topic Prioritization",
                                    headers = listOf("Topic", "Exam Weight", "Difficulty"),
                                    rows = listOf(
                                        listOf("Thermodynamics & Heat", "High (12 marks)", "Medium"),
                                        listOf("Wave Optics & Interference", "High (10 marks)", "Challenging"),
                                        listOf("Modern Physics & Nuclei", "Guaranteed (8 marks)", "Direct")
                                    )
                                )
                            )
                        )
                    ),
                    CanvasNode(
                        id = "es_traps",
                        boardId = "",
                        parentId = "es_syllabus",
                        prompt = "Common Mistakes & Traps",
                        title = "Examiner Traps",
                        kind = "warning",
                        color = "rose",
                        x = 40f,
                        y = 560f,
                        content = CanvasNodeContent(
                            title = "Mistakes That Cost Marks",
                            summary = "Review the top slip-ups students make under exam time pressure.",
                            sections = listOf(
                                CanvasSection(
                                    type = "bullets",
                                    title = "Watch out for",
                                    bulletItems = listOf(
                                        "Sign conventions in lens and mirror formulas.",
                                        "Forgetting SI conversions (cm -> m, kJ -> J).",
                                        "Skipping intermediate algebraic steps in 4-mark questions."
                                    )
                                )
                            )
                        )
                    ),
                    CanvasNode(
                        id = "es_practice",
                        boardId = "",
                        parentId = "es_syllabus",
                        prompt = "Must-Solve Problems",
                        title = "Practice Drill",
                        kind = "practice",
                        color = "blue",
                        x = 420f,
                        y = 560f,
                        content = CanvasNodeContent(
                            title = "High-Probability Questions",
                            summary = "Work through these recurring patterns from previous NEB question banks.",
                            sections = listOf(
                                CanvasSection(
                                    type = "cards",
                                    title = "Target Questions",
                                    cardItems = listOf(
                                        CardRefItem("Derivation 1", "Young's Double Slit", listOf("Fringe width beta = lambda*D/d", "Angular fringe width condition")),
                                        CardRefItem("Numerical 2", "Carnot Cycle Efficiency", listOf("eta = 1 - T2/T1", "Entropy change calculation"))
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            CanvasTemplate(
                key = "research-map",
                name = "Research Map",
                subtitle = "Evidence & Synthesis",
                description = "Structure an academic inquiry: central thesis, supporting empirical evidence, and counter-arguments.",
                iconName = "travel_explore",
                initialNodes = listOf(
                    CanvasNode(
                        id = "rm_thesis",
                        boardId = "",
                        parentId = null,
                        prompt = "Central Research Question",
                        title = "Research Question",
                        kind = "question",
                        color = "blue",
                        x = 230f,
                        y = 40f,
                        content = CanvasNodeContent(
                            title = "Central Thesis & Hypothesis",
                            summary = "State the core question clearly: **What relationship are we examining, and why does it matter?**",
                            sections = listOf(
                                CanvasSection(
                                    type = "text",
                                    content = "Ground the question in context, establishing the existing consensus and current open problems."
                                )
                            )
                        )
                    ),
                    CanvasNode(
                        id = "rm_evidence",
                        boardId = "",
                        parentId = "rm_thesis",
                        prompt = "Supporting Evidence",
                        title = "Supporting Data",
                        kind = "source",
                        color = "green",
                        x = 40f,
                        y = 560f,
                        content = CanvasNodeContent(
                            title = "Key Studies & Metrics",
                            summary = "Empirical findings that back up the hypothesis.",
                            sections = listOf(
                                CanvasSection(
                                    type = "comparison",
                                    title = "Source Matrix",
                                    headers = listOf("Study", "Methodology", "Finding"),
                                    rows = listOf(
                                        listOf("Smith et al. (2024)", "Randomized Trial", "32% performance boost"),
                                        listOf("Sharma & Khan (2025)", "Longitudinal Cohort", "Strong positive correlation (r=0.74)")
                                    )
                                )
                            )
                        )
                    ),
                    CanvasNode(
                        id = "rm_counter",
                        boardId = "",
                        parentId = "rm_thesis",
                        prompt = "Counter-Arguments & Limitations",
                        title = "Counterpoints & Nuance",
                        kind = "comparison",
                        color = "amber",
                        x = 420f,
                        y = 560f,
                        content = CanvasNodeContent(
                            title = "Limitations & Alternate Views",
                            summary = "A strong inquiry directly addresses counter-evidence.",
                            sections = listOf(
                                CanvasSection(
                                    type = "bullets",
                                    title = "Confounds & Biases",
                                    bulletItems = listOf(
                                        "Selection bias in initial cohort sampling.",
                                        "Correlation does not establish causal direction without mechanism.",
                                        "External validity across diverse demographics."
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            CanvasTemplate(
                key = "essay-builder",
                name = "Essay & Report Builder",
                subtitle = "From Prompt to Polish",
                description = "Craft rigorous argumentative essays with hook, thesis, topic sentences, citations, and punchy conclusion.",
                iconName = "edit_note",
                initialNodes = listOf(
                    CanvasNode(
                        id = "eb_prompt",
                        boardId = "",
                        parentId = null,
                        prompt = "Essay Prompt & Thesis",
                        title = "Thesis Statement",
                        kind = "topic",
                        color = "blue",
                        x = 230f,
                        y = 40f,
                        content = CanvasNodeContent(
                            title = "The Core Argument",
                            summary = "State your thesis in one sentence with a clear **claim**, **reasoning**, and **counter-concession**.",
                            sections = listOf(
                                CanvasSection(
                                    type = "bullets",
                                    title = "Structural Checklist",
                                    bulletItems = listOf(
                                        "Hook: Engaging opening observation or provocative stat.",
                                        "Bridge: Connecting background context to specific scope.",
                                        "Thesis: Unambiguous road map for the body paragraphs."
                                    )
                                )
                            )
                        )
                    ),
                    CanvasNode(
                        id = "eb_body",
                        boardId = "",
                        parentId = "eb_prompt",
                        prompt = "Body Paragraphs Blueprint",
                        title = "Body Paragraphs",
                        kind = "summary",
                        color = "purple",
                        x = 230f,
                        y = 560f,
                        content = CanvasNodeContent(
                            title = "Point - Evidence - Analysis",
                            summary = "Each paragraph must advance a single pillar of your central thesis.",
                            sections = listOf(
                                CanvasSection(
                                    type = "cards",
                                    title = "Paragraph Blueprints",
                                    cardItems = listOf(
                                        CardRefItem("Body 1: Foundational Claim", "The primary driver", listOf("Topic sentence", "Evidence quote", "Tie-back to thesis")),
                                        CardRefItem("Body 2: Deep Analysis", "The nuance", listOf("Comparative contrast", "Secondary source backing"))
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            CanvasTemplate(
                key = "project-plan",
                name = "Project Roadmap",
                subtitle = "Milestones & Actions",
                description = "Plan learning projects, hackathon prototypes, or science fair experiments with clear milestones and risks.",
                iconName = "account_tree",
                initialNodes = listOf(
                    CanvasNode(
                        id = "pp_goal",
                        boardId = "",
                        parentId = null,
                        prompt = "Project Outcome",
                        title = "Outcome & Definition of Done",
                        kind = "goal",
                        color = "blue",
                        x = 230f,
                        y = 40f,
                        content = CanvasNodeContent(
                            title = "Project North Star",
                            summary = "What does the final deliverable look like, and who does it serve?",
                            sections = listOf(
                                CanvasSection(
                                    type = "bullets",
                                    title = "Success criteria",
                                    bulletItems = listOf(
                                        "Working demo submitted before deadline.",
                                        "Comprehensive report with references.",
                                        "Peer presentation slides ready."
                                    )
                                )
                            )
                        )
                    ),
                    CanvasNode(
                        id = "pp_milestones",
                        boardId = "",
                        parentId = "pp_goal",
                        prompt = "Milestones & Timeline",
                        title = "Phased Milestones",
                        kind = "task",
                        color = "green",
                        x = 40f,
                        y = 560f,
                        content = CanvasNodeContent(
                            title = "Execution Phases",
                            summary = "Chronological roadmap with clear checkpoints.",
                            sections = listOf(
                                CanvasSection(
                                    type = "timeline",
                                    title = "Sprint schedule",
                                    timelineItems = listOf(
                                        TimelineItem(1, "Phase 1: Research & Discovery", "Gather sources, interview stakeholders"),
                                        TimelineItem(2, "Phase 2: Prototype & Draft", "Build rough model, test core mechanics"),
                                        TimelineItem(3, "Phase 3: Polish & Review", "Incorporate feedback, finalize artifacts")
                                    )
                                )
                            )
                        )
                    ),
                    CanvasNode(
                        id = "pp_risks",
                        boardId = "",
                        parentId = "pp_goal",
                        prompt = "Key Risks & Mitigations",
                        title = "Risk Register",
                        kind = "warning",
                        color = "rose",
                        x = 420f,
                        y = 560f,
                        content = CanvasNodeContent(
                            title = "Known Risks & Safety Margins",
                            summary = "Anticipate blockers before they derail the project.",
                            sections = listOf(
                                CanvasSection(
                                    type = "comparison",
                                    title = "Risk Matrix",
                                    headers = listOf("Risk", "Impact", "Mitigation"),
                                    rows = listOf(
                                        listOf("API rate limits", "High", "Local mock caching + batching"),
                                        listOf("Scope creep", "Medium", "Lock MVP feature list on Day 2"),
                                        listOf("Hardware delay", "High", "Simulate inputs via software stubs")
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    }
}
