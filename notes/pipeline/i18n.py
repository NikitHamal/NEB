"""Book-furniture strings. Nepali books carry no Latin-script words: every label
the pipeline prints comes from here, selected by the book's subject slug."""
import re

EN = dict(
    lang="en", tagline="Open learning community for Nepal",
    grade="Grade {g} · Science Stream",
    cover_sub=("Complete study notes for the NEB / CDC secondary education "
               "curriculum. Every unit of the official syllabus, with derivations, worked "
               "examples, diagrams, tables, summaries, practice questions and full model "
               "question papers."),
    code="Subject code", edition="Edition 1.0 · 2082 BS (2025–26 AD)",
    contents="Contents", hrs=" hrs", teaching_hours="teaching hours", unit="Unit",
    syl="CDC syllabus — this unit must cover", appendix="Appendix",
    figure="Figure", source="Source:", back="Model Question Papers",
    extras=(("model-questions", "Model Question Papers"), ("formula-sheet", "Formula Sheet"),
            ("answer-key", "Answer Key")),
    credits_h="Picture Credits", credits_sub="Images used in this book",
    unknown_author="Unknown author", lic_unknown="licence unknown", via="via", web="the web",
    no_grid="See the NEB specification grid for the current pattern.",
    boxes={"key": "Key point", "example": "Worked example", "caution": "Common mistake",
           "tip": "Exam tip", "definition": "Definition", "derivation": "Derivation",
           "note": "Note", "memory": "Remember"},
    footer="NEBians — nebians.consica.com.np", digits=False,
    front_title="About this book",
    front_lead=("These notes cover the complete official curriculum for {subject}, Grade {g}, "
                "as published by the Curriculum Development Centre (CDC), Sanothimi, and "
                "examined by the National Examination Board (NEB)."),
    org_h="How this book is organised",
    org_p=("Each chapter maps to one unit of the CDC curriculum and opens with the exact "
           "syllabus points that unit must cover, so you can tick off the syllabus as you "
           "study. Inside a chapter you will find:"),
    org_li=["<strong>Concept sections</strong> following the order of the official curriculum.",
            "<strong>Derivations</strong> set out step by step, the way a full-mark answer should be written.",
            "<strong>Worked examples</strong> with the complete solution method, not just the answer.",
            "<strong>Figures, tables and graphs</strong> drawn to be redrawn by hand in the exam hall.",
            "<strong>Key points, exam tips and common mistakes</strong> pulled out of the running text.",
            "<strong>A chapter summary</strong> and <strong>practice questions with answers</strong>, in NEB question style."],
    cover_h="Syllabus coverage at a glance",
    th=("Content area", "Chapters", "Teaching hours"), exam_h="Examination pattern",
    read="Please read this",
    disclaimer=("This is a community study aid, not an official CDC or NEB publication, and it "
                "does not replace your prescribed textbook. It was prepared from the official CDC "
                "curriculum documents and past NEB question papers. Edition 1.0 is a first "
                "release: if you spot an error, report it in the NEBians app so the next edition "
                "can fix it for everybody."),
    prep="Prepared for the NEBians open learning community · Free to share and print for study purposes.",
    cr_p1=("Schematic diagrams, graphs and derivation figures in this book were drawn for "
           "it and are part of the book. The photographs, micrographs and reference diagrams "
           "listed here came from free-licence sources and remain under their own licences; "
           "they are reproduced with the attribution each licence asks for. Follow a licence "
           "link to see exactly what it permits."),
    cr_p2=("Where a source diagram was published in a numbered or non-English form, the "
           "labels you see over it are ours, added so the terminology matches the CDC "
           "syllabus. The underlying image is unchanged apart from cropping and those labels; "
           "such an annotated version is a derivative work and is offered under the same "
           "licence as the original."),
    cr_foot=("If you believe an image here is wrongly attributed or wrongly licensed, report it "
             "in the NEBians app and it will be corrected or removed in the next edition."),
    summary_re="Chapter summary|Summary|Unit summary",
    qs_re="Practice|Exercise|Review|Model|Self",
)

NE = dict(EN)
NE.update(
    lang="ne", tagline="नेपालका लागि खुला सिकाइ समुदाय",
    grade="कक्षा {g} · विज्ञान संकाय",
    cover_sub=("नेपालको माध्यमिक शिक्षा पाठ्यक्रम (पाठ्यक्रम विकास केन्द्र र राष्ट्रिय परीक्षा बोर्ड) "
               "अनुसारको पूर्ण अध्ययन सामग्री। आधिकारिक पाठ्यक्रमका प्रत्येक एकाइ, उदाहरण, चित्र, "
               "तालिका, सारांश, अभ्यास प्रश्न र पूर्ण नमुना प्रश्नपत्रसहित।"),
    code="विषय सङ्केत", edition="संस्करण १.० · २०८२ साल",
    contents="विषयसूची", hrs=" घण्टा", teaching_hours="शिक्षण घण्टा", unit="एकाइ",
    syl="पाठ्यक्रमअनुसार यस एकाइमा समेटिनुपर्ने विषयवस्तु", appendix="परिशिष्ट",
    figure="चित्र", source="स्रोत:",
    extras=(("model-questions", "नमुना प्रश्नपत्र"), ("formula-sheet", "सूत्र तालिका"),
            ("answer-key", "उत्तरकुञ्जी")),
    credits_h="चित्र श्रेय", credits_sub="यस पुस्तकमा प्रयोग भएका चित्र",
    unknown_author="अज्ञात रचनाकार", lic_unknown="अनुमतिपत्र अज्ञात", via="स्रोत:", web="इन्टरनेट",
    no_grid="हालको ढाँचाका लागि राष्ट्रिय परीक्षा बोर्डको विशिष्टीकरण तालिका हेर्नुहोस्।",
    boxes={"key": "मुख्य बुँदा", "example": "हल गरिएको उदाहरण", "caution": "सामान्य त्रुटि",
           "tip": "परीक्षा सुझाव", "definition": "परिभाषा", "derivation": "व्युत्पत्ति",
           "note": "टिपोट", "memory": "सम्झनुहोस्"},
    footer="नेबियन्स — nebians.consica.com.np", digits=True,
    front_title="यस पुस्तकबारे",
    front_lead=("यी टिपोटले पाठ्यक्रम विकास केन्द्र, सानोठिमीले प्रकाशन गरेको र राष्ट्रिय परीक्षा बोर्डले "
                "परीक्षा लिने {subject}, कक्षा {g} को सम्पूर्ण आधिकारिक पाठ्यक्रम समेट्छन्।"),
    org_h="पुस्तक कसरी व्यवस्थित गरिएको छ",
    org_p=("प्रत्येक अध्याय पाठ्यक्रमको एक एकाइसँग मिल्छ र त्यस एकाइले समेट्नुपर्ने पाठ्यक्रमका बुँदाहरूबाट "
           "सुरु हुन्छ, ताकि पढ्दै जाँदा तपाईँले पाठ्यक्रम पूरा भएको जाँच गर्न सक्नुहुन्छ। अध्यायभित्र यी कुरा पाउनुहुनेछ:"),
    org_li=["<strong>अवधारणा खण्ड</strong> — आधिकारिक पाठ्यक्रमको क्रममा।",
            "<strong>स्पष्टीकरण</strong> — पूर्णाङ्क पाउने उत्तर जसरी लेखिनुपर्छ, त्यसरी चरणबद्ध रूपमा।",
            "<strong>हल गरिएका उदाहरण</strong> — उत्तर मात्र होइन, पूर्ण हल गर्ने विधिसहित।",
            "<strong>चित्र, तालिका र ग्राफ</strong> — परीक्षा हलमा आफैँ बनाउन सकिने गरी तयार पारिएका।",
            "<strong>मुख्य बुँदा, परीक्षा सुझाव र सामान्य त्रुटि</strong> — मूल पाठबाट छुट्याइएका।",
            "<strong>अध्यायको सारांश</strong> र <strong>उत्तरसहित अभ्यास प्रश्न</strong> — राष्ट्रिय परीक्षा बोर्डको प्रश्न शैलीमा।"],
    cover_h="पाठ्यक्रम समावेश एक नजरमा",
    th=("विषयक्षेत्र", "अध्याय सङ्ख्या", "शिक्षण घण्टा"), exam_h="परीक्षा ढाँचा",
    read="कृपया यो पढ्नुहोस्",
    disclaimer=("यो सामुदायिक अध्ययन सामग्री हो, पाठ्यक्रम विकास केन्द्र वा राष्ट्रिय परीक्षा बोर्डको आधिकारिक "
                "प्रकाशन होइन, र तपाईँको तोकिएको पाठ्यपुस्तकको विकल्प पनि होइन। यो आधिकारिक पाठ्यक्रम "
                "दस्तावेज र विगतका परीक्षाका प्रश्नपत्रका आधारमा तयार पारिएको हो। यो पहिलो संस्करण भएकाले "
                "कतै त्रुटि भेट्नुभयो भने नेबियन्स एपमा जानकारी दिनुहोस्, ताकि अर्को संस्करणमा सबैका लागि सुधार गर्न सकियोस्।"),
    prep="नेबियन्स खुला सिकाइ समुदायका लागि तयार पारिएको · अध्ययन प्रयोजनका लागि निःशुल्क बाँड्न र छाप्न पाइन्छ।",
    cr_p1=("यस पुस्तकका रेखाचित्र, ग्राफ र व्युत्पत्तिका चित्र पुस्तकका लागि नै बनाइएका हुन्। यहाँ सूचीबद्ध "
           "फोटो र सन्दर्भ चित्र निःशुल्क अनुमतिपत्र भएका स्रोतबाट लिइएका हुन् र तिनका आफ्नै अनुमतिपत्रअन्तर्गत रहन्छन्; "
           "प्रत्येक अनुमतिपत्रले मागेबमोजिम श्रेय दिएर प्रयोग गरिएको छ। अनुमतिपत्रको सम्पर्कसूत्र हेरेर "
           "के-के अनुमति छ भन्ने ठ्याक्कै थाहा पाउन सकिन्छ।"),
    cr_p2=("कुनै स्रोत चित्र अरू भाषामा प्रकाशित भएको भए, त्यसमाथि देखिने नेपाली नामाङ्कन हाम्रो हो; पाठ्यक्रमको शब्दावलीसँग "
           "मिलाउन थपिएको हो। काटछाँट र यी नामाङ्कन बाहेक मूल चित्र जस्ताको तस्तै छ; यसरी नामाङ्कन थपिएको संस्करण "
           "व्युत्पन्न कृति हो र मूल चित्रकै अनुमतिपत्रमा उपलब्ध गराइएको छ।"),
    cr_foot=("यहाँको कुनै चित्रको श्रेय वा अनुमतिपत्र गलत छ भन्ने लागेमा नेबियन्स एपमा जानकारी दिनुहोस्; "
             "अर्को संस्करणमा सच्याइनेछ वा हटाइनेछ।"),
    summary_re="अध्यायको सारांश|एकाइको सारांश|सारांश|Chapter summary|Summary|Unit summary",
    qs_re="अभ्यास|प्रश्न|नमुना|पुनरावलोकन|Practice|Exercise|Review|Model|Self",
)

CUR = EN

# The same pipeline prints the books for the basic level (grades 1-8) and for
# the secondary level (grades 9-12). The furniture differs where it matters:
# a Grade 8 book is basic level, examined by the local level, not a "Science
# Stream" NEB book, and saying otherwise on the cover would be wrong.
BASIC_EN = dict(
    grade="Grade {g} · Basic Level (Grades 1–8)",
    cover_sub=("Complete study notes for the CDC basic level curriculum, "
               "Grades 1–8. Every unit of the official syllabus, with worked "
               "examples, diagrams, tables, summaries, practice questions and "
               "full answer keys."),
    front_lead=("These notes cover the complete official curriculum for "
                "{subject}, Grade {g}, as published by the Curriculum "
                "Development Centre (CDC), Sanothimi. Grade 8 is assessed by "
                "the Basic Education Examination, conducted by the local level "
                "under the CDC assessment scheme."),
    exam_h="Assessment pattern",
    no_grid=("The basic level assessment scheme gives continuous (internal) "
             "assessment 50 % weight and the written paper 50 %; confirm your "
             "local level's grid."),
)

BASIC_NE = dict(
    grade="कक्षा {g} · आधारभूत तह (कक्षा १–८)",
    cover_sub=("पाठ्यक्रम विकास केन्द्रको आधारभूत तह (कक्षा १–८) पाठ्यक्रममा "
               "आधारित सम्पूर्ण अध्ययन टिपोट — हल गरिएका उदाहरण, चित्र, तालिका, "
               "सारांश, अभ्यास प्रश्न र पूर्ण उत्तरकुञ्जीसहित।"),
    front_lead=("यी टिपोटले पाठ्यक्रम विकास केन्द्र, सानोठिमीले प्रकाशन गरेको "
                "{subject}, कक्षा {g} को सम्पूर्ण आधिकारिक पाठ्यक्रम समेट्छन्। "
                "कक्षा ८ को मूल्याङ्कन स्थानीय तहबाट सञ्चालित आधारभूत तह "
                "परीक्षाबाट हुन्छ।"),
    exam_h="मूल्याङ्कन ढाँचा",
    no_grid=("आधारभूत तहको मूल्याङ्कन योजनाअनुसार आन्तरिक (निरन्तर) मूल्याङ्कनको "
             "भार ५० प्रतिशत र लिखित परीक्षाको भार ५० प्रतिशत हुन्छ; आफ्नो "
             "स्थानीय तहको विशिष्टीकरण तालिका पुष्टि गर्नुहोस्।"),
)


SEC_EN = dict(
    grade="Grade {g} · Secondary Level (SEE)",
    cover_sub=("Complete study notes for the CDC secondary education "
               "curriculum (Grades 9–10), examined by the Secondary Education "
               "Examination. Every unit of the official syllabus, with "
               "derivations, worked examples, diagrams, tables, summaries and "
               "practice questions with full model question papers."),
    front_lead=("These notes cover the complete official curriculum for "
                "{subject}, Grade {g}, as published by the Curriculum "
                "Development Centre (CDC), Sanothimi, and examined by the "
                "Secondary Education Examination (SEE) of the National "
                "Examination Board."),
)

SEC_NE = dict(
    grade="कक्षा {g} · माध्यमिक तह (कक्षा ९–१०)",
    cover_sub=("पाठ्यक्रम विकास केन्द्रको माध्यमिक तह (कक्षा ९–१०) पाठ्यक्रममा "
               "आधारित सम्पूर्ण अध्ययन टिपोट — व्युत्पत्ति, हल गरिएका उदाहरण, "
               "चित्र, तालिका, सारांश र पूर्ण नमुना प्रश्नपत्रसहित अभ्यास प्रश्न।"),
    front_lead=("यी टिपोटले पाठ्यक्रम विकास केन्द्र, सानोठिमीले प्रकाशन गरेको र "
                "राष्ट्रिय परीक्षा बोर्डको माध्यमिक शिक्षा परीक्षाबाट "
                "परीक्षा लिइने {subject}, कक्षा {g} को सम्पूर्ण आधिकारिक "
                "पाठ्यक्रम समेट्छन्।"),
)


# Books the CDC publishes and the boards examine in Nepali. Their furniture,
# their cover and every label the pipeline prints must be Nepali too — a
# student reading सामाजिक अध्ययन should not meet a single Latin word.
NEPALI_MEDIUM = ("nep", "soc", "health")


def set_book(slug):
    global CUR
    m = re.match(r"([a-z]+)(\d+)", slug or "")
    grade = int(m.group(2)) if m else 12
    base = NE if (slug or "").startswith(NEPALI_MEDIUM) else EN
    if grade <= 8:
        CUR = dict(base, **(BASIC_NE if base is NE else BASIC_EN))
    elif grade <= 10:
        CUR = dict(base, **(SEC_NE if base is NE else SEC_EN))
    else:
        CUR = base
    return CUR

_D = str.maketrans("0123456789", "०१२३४५६७८९")
def num(x):
    s = str(x)
    return s.translate(_D) if CUR["digits"] else s

def for_title(title, book):
    """A chapter whose title is Devanagari gets Nepali furniture even inside an English book."""
    return NE if re.match(r"\W*[\u0900-\u097F]", title or "") else book
