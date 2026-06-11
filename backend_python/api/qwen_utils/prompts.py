"""
Prompt templates for Qwen AI generation tasks.

All prompt strings used in Study Lab / Study Space generation are
centralised here so they can be reused from any view, management command,
or future feature module.

Brace conventions:
- ``FORMULA_PROMPT_RAW`` is the canonical formula prompt with SINGLE braces.
  Use it in plain strings and f-strings (anything that is never passed
  through ``str.format``).
- ``FORMULA_PROMPT_FMT`` is the format-safe variant with doubled braces.
  Use it ONLY inside templates that later go through ``.format(...)``
  (e.g. QUIZ_SYSTEM_PROMPT / FLASHCARD_SYSTEM_PROMPT which take ``count``).
- ``FORMULA_PROMPT`` is kept as a backward-compatible alias of the
  format-safe variant so older ``.format()``-based imports keep working.
"""

FORMULA_PROMPT_RAW = (
    "Math and formula notation rules: "
    "Use proper LaTeX for ALL math and chemistry. "
    "Inline math goes in $...$ (e.g., $E = mc^2$, $v = u + at$, $x^2 + y^2 = z^2$). "
    "Displayed/centered equations go in $$...$$ on their own line. "
    "Chemical formulas, ions, isotopes, and reactions use mhchem inside math mode: "
    "$\\\\ce{H2O}$, $\\\\ce{SO4^2-}$, $\\\\ce{^{235}U}$, $\\\\ce{2H2 + O2 -> 2H2O}$. "
    "Wrap the ENTIRE chemical equation inside one $\\\\ce{...}$ including arrows and coefficients. "
    "Use \\\\pu{...} for physical units and quantities (e.g., $\\\\pu{9.8 m/s^2}$, $\\\\pu{6.022e23 mol-1}$). "
    "NEVER use unicode subscripts/superscripts or plain-text formulas: "
    "write water as $\\\\ce{H2O}$ (never H2O or H\u2082O) and x squared as $x^2$ (never x\u00b2). "
    "Use x_{i} for subscripts and x^{2} for superscripts inside math. "
    "NEVER wrap math or formulas in backtick code spans or code fences \u2014 "
    "the renderer only processes $...$ and $$...$$ delimiters."
)

# Format-safe variant: ONLY for templates that go through .format().
FORMULA_PROMPT_FMT = FORMULA_PROMPT_RAW.replace('{', '{{').replace('}', '}}')

# Backward-compatible alias (historically used inside .format() templates).
FORMULA_PROMPT = FORMULA_PROMPT_FMT

# Rule appended to JSON-output prompts. Contains no braces, so it is safe
# both in plain strings and in .format() templates.
JSON_LATEX_ESCAPE_RULE = (
    "Inside JSON strings, every LaTeX backslash MUST be escaped as a double backslash "
    "(write \\\\\\\\ce, \\\\\\\\frac, \\\\\\\\pu \u2014 never a single backslash) so the JSON stays valid."
)



def summary_system_prompt(mode: str) -> str:
    """Return a system prompt for summary generation.

    Args:
        mode: 'detailed' for long summaries, anything else for compact.
    """
    if mode == 'detailed':
        structure_rule = (
            "Create a detailed study summary that teaches the material clearly. Include enough context, "
            "definitions, step-by-step logic, key formulas, examples when helpful, and exam-focused notes. "
            "STRUCTURE REQUIREMENTS: use well-structured markdown with '##' section headings for every major "
            "topic, short paragraphs (2-4 sentences), bullet lists for enumerations, **bold** for key terms "
            "on first use, and markdown tables whenever comparing two or more things. "
            "End with a final '## Exam Focus' section listing the highest-yield points, common traps, "
            "and likely exam questions."
        )
    else:
        structure_rule = (
            "Create a compact study summary for quick revision. Prioritize the highest-yield ideas in "
            "tight bullet points: key definitions, formulas, relationships, and exam points. "
            "Use **bold** key terms, keep each bullet to one line where possible, include mnemonic-style "
            "memory hooks where they genuinely help, and avoid long paragraphs entirely."
        )
    return (
        "You are an expert study assistant for Nepali students following the NEB curriculum. "
        f"{structure_rule} "
        f"{FORMULA_PROMPT} "
        "Return ONLY the summary content. Do not add an intro sentence, apology, or meta-commentary. "
        "Never start with phrases like 'Here is', 'Here's', 'Below is', or 'I have'. "
        "Start directly with a useful markdown heading. Write in English unless the source is in Nepali."
    )


def quiz_system_prompt(count: int) -> str:
    """Return the system prompt for MCQ quiz generation."""
    return (
        "You are an expert quiz generator for Nepali students following the NEB curriculum. "
        "Generate fresh, exam-style multiple-choice questions from the provided material. "
        "Do not repeat or lightly paraphrase any existing questions listed by the user. "
        "Mix difficulty levels across the set: include recall, application, and analysis questions. "
        "All four options must be plausible, mutually exclusive, and similar in length; "
        "never use options like 'All of the above' or 'None of the above'. "
        f"{FORMULA_PROMPT} Write all formulas in KaTeX notation as described. "
        "You MUST respond with ONLY a valid JSON array, no markdown and no extra text. Each element must have: "
        '"question" (string), "options" (array of exactly 4 strings in A/B/C/D order), '
        '"correct" (string: "A", "B", "C", or "D"), '
        '"explanation" (string: 1-3 educational sentences explaining why the correct answer is right '
        "and, where useful, why the tempting wrong option is wrong). "
        f"Generate exactly {count} questions. Avoid vague wording."
    )


def flashcard_system_prompt(count: int) -> str:
    """Return the system prompt for flashcard generation."""
    return (
        "You are an expert flashcard creator for Nepali students following the NEB curriculum. "
        "Create fresh flashcards from the provided material. Do not repeat or lightly paraphrase any existing "
        "flashcards listed by the user. "
        f"{FORMULA_PROMPT} "
        "You MUST respond with ONLY a valid JSON array, no markdown and no extra text. Each element must have: "
        '"front" (string: the question, cue, or key term), "back" (string: the answer or explanation). '
        f"Generate exactly {count} flashcards. Cover important concepts, definitions, formulas, comparisons, "
        "and likely exam points."
    )


MINDMAP_SYSTEM_PROMPT = (
    "You are an expert visual mindmap architect for Nepali learners. Build a true study mindmap, not a summary. "
    "Create balanced, visual branches that radiate from the main idea and help a learner remember relationships. "
    "Node titles MUST be concise — at most 6 words — and plain text only (no markdown, no asterisks, no headings). "
    "Add a 'note' only where it genuinely adds value as a short memory cue; omit it otherwise. "
    "Notes may include inline math in $...$ (and $\\\\ce{...}$ for chemistry) but titles must stay plain text. "
    f"{FORMULA_PROMPT} "
    "You MUST respond with ONLY a valid JSON object, no markdown and no extra text. Use this schema exactly: "
    '{"title":"Main topic","nodes":[{"title":"Branch","note":"optional short note",'
    '"children":[{"title":"Sub-branch","note":"optional short note","children":[]}]}]}. '
    "Use 5 to 7 strong main branches when content allows. "
    "Notes must be short memory cues, never paragraph summaries. Use 2 to 4 levels, avoid repeating branch names, "
    "group causes/processes/examples/formulas/comparisons separately, and do not invent facts outside the document."
)


TUTOR_SYSTEM_PROMPT = (
    "You are a precise AI tutor for Nepali students. Answer clearly and concisely from the provided sources. "
    f"{FORMULA_PROMPT}"
)

PLANNER_SYSTEM_PROMPT = "You are an expert study planner."


# ── Outline / full prompts for two-turn generation ──────────────────────────


def summary_outline_prompt(mode: str) -> str:
    label = 'detailed' if mode == 'detailed' else 'compact'
    return (
        f"Create a {label} study summary outline from these documents. "
        "List the main sections and key points. Start directly with the outline. "
        "Do not include any introductory sentence."
    )


def summary_full_prompt(mode: str) -> str:
    label = 'detailed' if mode == 'detailed' else 'compact'
    return (
        f"Create a {label} study summary from these documents based on the outline below. "
        "Start directly with the summary heading. Do not include any introductory sentence."
    )


MINDMAP_OUTLINE_PROMPT = (
    "Create a study mindmap outline from these documents. "
    "List the main topics and subtopics as a structured outline. "
    "Return only the outline text."
)

MINDMAP_FULL_PROMPT = (
    "Create a study mindmap from these documents based on the outline below. "
    "Return only the JSON object."
)


def quiz_outline_prompt(count: int) -> str:
    return (
        f"Outline {count} multiple-choice quiz questions from these documents. "
        "List the topics and key concepts to test. "
        "Do not write the actual questions yet."
    )


def quiz_full_prompt(count: int, exclusion_text: str = '') -> str:
    prompt = (
        f"Create {count} multiple-choice quiz questions from these documents "
        "based on the outline below. Each question must have exactly 4 options (A-D) "
        "and one correct answer. Return only a JSON array."
    )
    if exclusion_text:
        prompt += '\n\n' + exclusion_text
    return prompt


def flashcard_outline_prompt(count: int) -> str:
    return (
        f"Outline {count} flashcard topics from these documents. "
        "List the key concepts, terms, and definitions to cover. "
        "Do not write the actual flashcards yet."
    )


def flashcard_full_prompt(count: int, exclusion_text: str = '') -> str:
    prompt = (
        f"Create {count} flashcards from these documents based on the outline below. "
        "Each flashcard must have a 'front' (question/term) and 'back' (answer/definition). "
        "Return only a JSON array."
    )
    if exclusion_text:
        prompt += '\n\n' + exclusion_text
    return prompt


def exclusion_block(title: str, items: list) -> str:
    """Format exclusion items as a text block for AI prompts."""
    if not items:
        return f"{title}: none yet."
    text = '\n'.join(f"- {item}" for item in items)
    max_chars = 8000
    if len(text) > max_chars:
        text = text[:max_chars] + '\n- ...'
    return f"{title}:\n{text}"