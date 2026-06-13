def _lesson(slug, title, icon, minutes, sim_mode, summary, objectives, knowledge, quiz, fun_fact=None):
    lesson = {
        'slug': slug,
        'title': title,
        'icon': icon,
        'minutes': minutes,
        'sim': 'biology/biology-lab',
        'sim_type': 'lab',
        'summary': summary,
        'objectives': objectives,
        'knowledge': knowledge,
        'quiz': quiz,
        'sim_mode': sim_mode,
    }
    if fun_fact:
        lesson['fun_fact'] = fun_fact
    return lesson


COURSES = [
    {
        'slug': 'neb-biology-practical-11',
        'title': 'NEB Biology Practicals — Class 11',
        'category': 'biology',
        'age_range': '16-17',
        'level': 'Intermediate',
        'icon': 'biotech',
        'color': '#65A30D',
        'tagline': 'Class 11 botany and zoology practicals as a virtual microscope, wet lab, field notebook and specimen bench.',
        'description': 'This course turns core Class 11 biology practical skills into interactive labs: using a compound microscope, preparing temporary mounts, observing stomata and plasmolysis, testing food biomolecules, measuring photosynthesis and respiration, dissecting flower parts, sampling vegetation and identifying animal specimens. The simulations emphasize real lab handling, observation, labelled diagrams, tabulation, conclusion and precautions.',
        'skills': [
            'Use microscope parts, focus and magnification correctly',
            'Prepare and observe temporary mounts',
            'Record biological observations with labelled diagrams',
            'Run controlled botany and zoology investigations',
            'Identify specimens using diagnostic features',
        ],
        'lessons': [
            _lesson(
                'compound-microscope',
                'Compound Microscope Handling',
                'microscope',
                14,
                'microscope',
                'Assemble the light path, choose objective lenses, focus a slide and identify common handling errors.',
                [
                    'Name the major parts of a compound microscope',
                    'Use coarse and fine adjustment in the correct sequence',
                    'Calculate total magnification from eyepiece and objective power',
                    'List precautions for safe microscope handling',
                ],
                [
                    {
                        'heading': 'The microscope is an optical system',
                        'body': 'A compound microscope uses an objective lens near the specimen and an eyepiece lens near your eye. The total magnification is objective power multiplied by eyepiece power, so a 10x eyepiece with a 40x objective gives 400x total magnification.\n\nGood microscopy is not only magnification. The mirror or lamp, condenser and diaphragm control light. The stage holds the slide. Coarse adjustment brings the image near focus under low power; fine adjustment sharpens it. Under high power, rough coarse adjustment can crash the objective into the slide.',
                    },
                    {
                        'heading': 'Focusing procedure',
                        'body': 'Start with low power and the stage lowered. Place the slide, center the specimen, watch from the side while raising the stage close to the objective, then look through the eyepiece and lower the stage slowly until the image appears. Use fine adjustment for clarity, then move to higher power only after the object is centered.\n\nA practical record should include a labelled microscope diagram, magnification used, observed structures and precautions such as carrying the microscope with both hands and keeping lenses clean with lens paper.',
                    },
                ],
                [
                    {
                        'q': 'Total magnification with a 10x eyepiece and 40x objective is:',
                        'options': ['40x', '50x', '400x', '4x'],
                        'answer': 2,
                        'explain': 'Total magnification = eyepiece power x objective power = 10 x 40 = 400x.',
                    },
                    {
                        'q': 'Why should high power focusing use fine adjustment?',
                        'options': ['To avoid crashing the objective into the slide', 'To change the stain', 'To heat the specimen', 'To reduce magnification to zero'],
                        'answer': 0,
                        'explain': 'The high-power objective is close to the slide, so coarse movement can break the slide or damage the lens.',
                    },
                ],
                'Most school microscopes invert the image, so moving a slide left often makes the image appear to move right.',
            ),
            _lesson(
                'onion-cell-mount',
                'Temporary Mount of Onion Epidermis',
                'grid_view',
                15,
                'cell-mount',
                'Peel onion epidermis, stain it virtually and inspect cell wall, cytoplasm, nucleus and vacuole.',
                [
                    'Prepare a temporary mount without air bubbles',
                    'Identify plant-cell wall, cytoplasm, nucleus and vacuole',
                    'Explain why iodine or safranin improves contrast',
                ],
                [
                    {
                        'heading': 'Preparing a thin mount',
                        'body': 'Onion epidermis is used because it peels into a single-cell-thick transparent layer. A small piece is placed in water or glycerine on a slide, stained lightly and covered with a cover slip. Lowering the cover slip at an angle pushes air out and prevents bubbles from hiding cells.\n\nUnder the microscope, onion cells appear rectangular because of their rigid cellulose cell walls. The nucleus becomes easier to see after staining. The large central vacuole pushes cytoplasm toward the edge.',
                    },
                    {
                        'heading': 'Observation and record',
                        'body': 'A good biological drawing is large, clean, labelled and based on what is actually seen. Draw only a few representative cells, not the whole field. Labels should point to visible structures: cell wall, cell membrane region, cytoplasm, nucleus and vacuole.\n\nPrecautions include using a thin peel, avoiding folded tissue, using only a small amount of stain and removing extra stain with blotting paper.',
                    },
                ],
                [
                    {
                        'q': 'Why is onion epidermis useful for a temporary mount?',
                        'options': ['It is thin and transparent', 'It has bones', 'It produces oxygen bubbles only', 'It has no cells'],
                        'answer': 0,
                        'explain': 'A thin transparent epidermal peel lets light pass through and shows individual plant cells clearly.',
                    },
                    {
                        'q': 'What prevents air bubbles under a cover slip?',
                        'options': ['Lowering it gently at an angle', 'Dropping it flat from a height', 'Heating the lens', 'Using no water at all'],
                        'answer': 0,
                        'explain': 'Angled lowering lets air escape as the cover slip settles.',
                    },
                ],
            ),
            _lesson(
                'leaf-stomata',
                'Stomata in Leaf Epidermis',
                'eco',
                15,
                'stomata',
                'Prepare a leaf peel and compare open and closed stomata by changing light and water conditions.',
                [
                    'Identify guard cells, stomatal pore and surrounding epidermal cells',
                    'Relate stomatal opening to gas exchange and transpiration',
                    'Explain how light and water availability affect guard-cell turgor',
                ],
                [
                    {
                        'heading': 'Guard cells control the pore',
                        'body': 'Stomata are microscopic pores mostly found in leaf epidermis. Each pore is surrounded by two guard cells. When guard cells take up water and become turgid, their curved walls pull the pore open. When they lose water, the pore closes.\n\nOpen stomata allow carbon dioxide to enter for photosynthesis, but they also let water vapour escape. Plants constantly balance carbon gain against water loss.',
                    },
                    {
                        'heading': 'Observation in a practical',
                        'body': 'A thin lower epidermal peel is mounted in water and observed under low and then high power. Students count stomata in a microscope field or draw a labelled stomatal complex.\n\nPrecautions include taking a very thin peel, keeping the peel moist, avoiding thick veins and using fine focus under high power.',
                    },
                ],
                [
                    {
                        'q': 'Which cells surround a stomatal pore?',
                        'options': ['Guard cells', 'Red blood cells', 'Root hairs', 'Xylem vessels only'],
                        'answer': 0,
                        'explain': 'Two guard cells surround each stomatal pore and regulate opening and closing.',
                    },
                    {
                        'q': 'Open stomata help photosynthesis mainly by allowing entry of:',
                        'options': ['Carbon dioxide', 'Sand', 'Proteins', 'Starch grains'],
                        'answer': 0,
                        'explain': 'Carbon dioxide enters through stomata and is used to build sugars during photosynthesis.',
                    },
                ],
            ),
            _lesson(
                'plasmolysis-osmosis',
                'Osmosis and Plasmolysis',
                'water_drop',
                16,
                'osmosis',
                'Move cells between hypotonic and hypertonic solutions and watch the protoplast shrink or recover.',
                [
                    'Define osmosis as water movement through a selectively permeable membrane',
                    'Distinguish turgid, flaccid and plasmolysed plant cells',
                    'Explain why concentrated salt or sugar solution causes plasmolysis',
                ],
                [
                    {
                        'heading': 'Water moves down water potential',
                        'body': 'Osmosis is the movement of water through a selectively permeable membrane from higher water potential to lower water potential. In dilute solution, plant cells gain water, become turgid and press against the cell wall. In concentrated solution, water leaves and the protoplast pulls away from the wall: plasmolysis.\n\nThe cell wall remains rigid while the living membrane and cytoplasm shrink inward. Returning the cell to water can reverse early plasmolysis by endosmosis.',
                    },
                    {
                        'heading': 'Practical method',
                        'body': 'A coloured epidermal peel, such as Rhoeo or Tradescantia, is mounted first in water and then irrigated with concentrated salt or sugar solution from one side while blotting from the other. Students observe the gradual shrinkage of the protoplast.\n\nThe correct conclusion is not that the wall shrinks; it is that water leaves the vacuole and cytoplasm through the membrane while the cell wall keeps its shape.',
                    },
                ],
                [
                    {
                        'q': 'Plasmolysis happens when a plant cell is placed in:',
                        'options': ['A hypertonic solution', 'Pure oxygen gas', 'A vacuum only', 'A magnet field'],
                        'answer': 0,
                        'explain': 'A hypertonic solution draws water out of the cell, shrinking the protoplast away from the wall.',
                    },
                    {
                        'q': 'Which structure remains rigid during plasmolysis?',
                        'options': ['Cell wall', 'Vacuole only', 'Cytoplasm only', 'Nucleus only'],
                        'answer': 0,
                        'explain': 'The cellulose cell wall keeps its shape while the living contents shrink inward.',
                    },
                ],
            ),
            _lesson(
                'food-tests',
                'Biomolecule Food Tests',
                'science',
                16,
                'food-test',
                'Run iodine, Benedict, Biuret and emulsion tests and record positive and negative results.',
                [
                    'Detect starch, reducing sugar, protein and lipid with standard qualitative tests',
                    'Use a control sample to compare colour changes',
                    'Record observations and conclusions accurately',
                ],
                [
                    {
                        'heading': 'Qualitative tests detect groups of molecules',
                        'body': 'Food tests use reagents that change appearance when a chemical group is present. Iodine turns blue-black with starch. Benedict reagent becomes green, yellow, orange or brick-red when heated with reducing sugar. Biuret reagent turns violet with proteins. The ethanol emulsion test gives a milky suspension when lipids are present.\n\nThese tests are qualitative or semi-quantitative. They show presence and approximate amount, not exact concentration unless calibrated carefully.',
                    },
                    {
                        'heading': 'Controls and safety',
                        'body': 'A proper practical includes a negative control such as distilled water and a positive control such as glucose or egg albumin. Controls prove that the reagent and procedure work.\n\nUse a water bath for heating Benedict reagent, avoid direct flame on test tubes and label tubes before adding reagents. Record initial colour, final colour and inference in a table.',
                    },
                ],
                [
                    {
                        'q': 'Iodine solution gives a blue-black colour with:',
                        'options': ['Starch', 'Protein', 'Lipid', 'Oxygen'],
                        'answer': 0,
                        'explain': 'Iodine forms a blue-black complex with starch.',
                    },
                    {
                        'q': 'Biuret reagent tests for:',
                        'options': ['Protein', 'Starch', 'Carbon dioxide', 'Chlorophyll'],
                        'answer': 0,
                        'explain': 'Biuret reagent turns violet in the presence of peptide bonds in proteins.',
                    },
                ],
            ),
            _lesson(
                'photosynthesis-rate',
                'Photosynthesis Rate in Aquatic Plant',
                'wb_sunny',
                16,
                'photosynthesis',
                'Change light intensity and carbon dioxide supply, then count oxygen bubbles from Hydrilla or Elodea.',
                [
                    'Measure photosynthesis rate using oxygen bubble count',
                    'Explain light intensity and carbon dioxide as limiting factors',
                    'Design a fair test by controlling temperature and plant size',
                ],
                [
                    {
                        'heading': 'Oxygen bubbles reveal photosynthesis',
                        'body': 'Aquatic plants such as Hydrilla or Elodea release oxygen bubbles during photosynthesis. Counting bubbles per minute gives a simple estimate of photosynthesis rate. More light usually increases the rate until another factor becomes limiting.\n\nCarbon dioxide concentration, temperature, chlorophyll and leaf area also affect the rate. A fair test changes one factor while keeping the others constant.',
                    },
                    {
                        'heading': 'Limiting factors',
                        'body': 'If light is very low, increasing carbon dioxide will not help much because light is limiting. If light is strong but carbon dioxide is low, extra light will not increase the rate. This idea of limiting factors explains why real plant growth depends on several resources together.\n\nThe simulation lets you adjust light and bicarbonate supply, then watch oxygen output and a live data table.',
                    },
                ],
                [
                    {
                        'q': 'Bubble count in this experiment estimates the rate of:',
                        'options': ['Photosynthesis', 'Digestion', 'Blood clotting', 'Sound production'],
                        'answer': 0,
                        'explain': 'Oxygen is released during photosynthesis, so bubble count estimates photosynthetic rate.',
                    },
                    {
                        'q': 'A limiting factor is:',
                        'options': ['The factor in shortest supply that restricts the rate', 'Any label on the beaker', 'Only the colour of the plant', 'A microscope part'],
                        'answer': 0,
                        'explain': 'The limiting factor is the resource or condition that currently prevents the process from going faster.',
                    },
                ],
            ),
            _lesson(
                'flower-dissection',
                'Flower Dissection and Floral Formula',
                'local_florist',
                17,
                'flower',
                'Dissect a bisexual flower, identify whorls and assemble a floral formula from symmetry, ovary and merosity.',
                [
                    'Identify calyx, corolla, androecium and gynoecium',
                    'Distinguish complete/incomplete and bisexual/unisexual flowers',
                    'Relate ovary position and symmetry to a floral formula',
                ],
                [
                    {
                        'heading': 'A flower is a reproductive shoot',
                        'body': 'Typical flowers have four whorls: sepals in the calyx, petals in the corolla, stamens in the androecium and carpels in the gynoecium. A complete flower has all four whorls. A bisexual flower has both stamens and carpels.\n\nDissection should proceed from outer to inner whorls. Count parts carefully, note fusion or free parts, observe ovary position and draw a labelled floral diagram.',
                    },
                    {
                        'heading': 'Floral formula summarizes structure',
                        'body': 'A floral formula is a compact symbolic description. It can show actinomorphic or zygomorphic symmetry, bisexual or unisexual condition, numbers of sepals, petals, stamens and carpels, fusion and ovary position.\n\nThis practical builds classification skills because floral characters are major clues in identifying plant families.',
                    },
                ],
                [
                    {
                        'q': 'The androecium is made of:',
                        'options': ['Stamens', 'Sepals only', 'Petals only', 'Roots'],
                        'answer': 0,
                        'explain': 'The androecium is the male reproductive whorl made of stamens.',
                    },
                    {
                        'q': 'A flower with both stamens and carpels is:',
                        'options': ['Bisexual', 'Sterile by definition', 'A leaf', 'Always incomplete'],
                        'answer': 0,
                        'explain': 'Bisexual flowers contain both male and female reproductive structures.',
                    },
                ],
            ),
            _lesson(
                'animal-specimen-identification',
                'Zoology Specimen Identification',
                'pets',
                17,
                'specimen',
                'Inspect earthworm, cockroach, fish and frog models and identify phylum/class characters without dissection.',
                [
                    'Use observable characters to identify common animal specimens',
                    'Distinguish annelid, arthropod, fish and amphibian features',
                    'Record habitat, diagnostic characters and classification',
                ],
                [
                    {
                        'heading': 'Identification uses diagnostic characters',
                        'body': 'Zoology practicals often ask students to identify preserved specimens and give reasons. The reason matters: segmentation and setae suggest earthworm as an annelid; jointed appendages and chitinous exoskeleton suggest cockroach as an arthropod; fins and gills indicate fish; moist skin and limbs indicate frog as an amphibian.\n\nA correct answer names the specimen, its classification, habitat and at least two visible identifying characters.',
                    },
                    {
                        'heading': 'Ethical virtual observation',
                        'body': 'Virtual specimen study cannot replace all real biological handling, but it can reduce repeated harm, prepare students before lab day and help schools without enough preserved material. It is especially useful for learning external morphology and classification before advanced dissections.\n\nThe simulation lets you rotate 2D/3D specimen models and reveal labels only after attempting identification.',
                    },
                ],
                [
                    {
                        'q': 'Jointed appendages and chitinous exoskeleton indicate:',
                        'options': ['Arthropoda', 'Annelida', 'Mollusca only', 'Bryophyta'],
                        'answer': 0,
                        'explain': 'Arthropods such as cockroaches have jointed appendages and a chitinous exoskeleton.',
                    },
                    {
                        'q': 'A fish is identified externally by:',
                        'options': ['Fins and gills', 'Petals and stamens', 'Root hairs', 'Only feathers'],
                        'answer': 0,
                        'explain': 'Fins and gills are key external features of fish.',
                    },
                ],
            ),
        ],
    },
    {
        'slug': 'neb-biology-practical-12',
        'title': 'NEB Biology Practicals — Class 12',
        'category': 'biology',
        'age_range': '17-18',
        'level': 'Advanced',
        'icon': 'genetics',
        'color': '#15803D',
        'tagline': 'Advanced Class 12 botany and zoology practicals: anatomy, physiology, genetics, biotechnology and human biology.',
        'description': 'This course covers advanced biology practical work for Class 12 science students. Learners examine dicot and monocot anatomy, measure transpiration, observe pollen germination, model mitosis and genetics, isolate DNA, inspect animal tissues, interpret blood grouping and explore human physiology with realistic instruments, labelled diagrams and data tables.',
        'skills': [
            'Interpret plant and animal tissue slides',
            'Measure physiological rates and explain limiting factors',
            'Model heredity, mitosis and biotechnology procedures',
            'Use clinical observations responsibly',
            'Connect microscopic structure with biological function',
        ],
        'lessons': [
            _lesson(
                'plant-anatomy-sections',
                'Dicot and Monocot Anatomy',
                'grain',
                17,
                'anatomy',
                'Compare transverse sections of dicot stem, monocot stem, dicot root and monocot root with labelled tissue layers.',
                [
                    'Identify epidermis, cortex, endodermis, pericycle, vascular bundles, xylem and phloem',
                    'Distinguish dicot and monocot stem/root anatomy',
                    'Relate vascular arrangement to plant function',
                ],
                [
                    {
                        'heading': 'Internal structure reveals plant type',
                        'body': 'Dicot stems usually show vascular bundles arranged in a ring with cambium, allowing secondary growth. Monocot stems have scattered vascular bundles and usually lack cambium. In roots, xylem and phloem arrangement differs from stems, and the endodermis controls entry into the vascular cylinder.\n\nA practical slide observation should begin under low power to locate tissue regions, then high power to inspect details. Draw only the sector needed for clarity and label tissues accurately.',
                    },
                    {
                        'heading': 'Function follows arrangement',
                        'body': 'Xylem conducts water and minerals, phloem conducts organic food, cortex stores material and endodermis regulates movement. Tissue arrangement is not random; it supports transport, strength and growth.\n\nThe simulation lets students switch sections and rotate a 3D tissue cylinder while the 2D view keeps the exact labelled transverse-section layout.',
                    },
                ],
                [
                    {
                        'q': 'Vascular bundles in a typical dicot stem are arranged:',
                        'options': ['In a ring', 'Randomly everywhere only', 'Only outside the epidermis', 'Inside flowers only'],
                        'answer': 0,
                        'explain': 'Dicot stems usually show vascular bundles in a ring and often have cambium.',
                    },
                    {
                        'q': 'Xylem mainly conducts:',
                        'options': ['Water and minerals', 'Nerve impulses', 'Carbon dioxide only', 'Antibodies'],
                        'answer': 0,
                        'explain': 'Xylem transports water and dissolved minerals from roots upward.',
                    },
                ],
            ),
            _lesson(
                'transpiration-potometer',
                'Transpiration With Potometer',
                'air',
                17,
                'transpiration',
                'Use a Ganong-style potometer to track bubble movement under wind, light and humidity changes.',
                [
                    'Measure water uptake as an estimate of transpiration rate',
                    'Explain effects of light, wind, humidity and leaf area',
                    'Recognize experimental errors in potometer setup',
                ],
                [
                    {
                        'heading': 'Water uptake estimates water loss',
                        'body': 'A potometer measures how quickly a leafy shoot takes up water. Because most absorbed water is lost by transpiration, bubble movement in the capillary tube estimates transpiration rate. The setup must be airtight; any leak ruins the measurement.\n\nLight and wind usually increase transpiration, while high humidity decreases it. Leaf area also matters because more stomata mean more evaporating surface.',
                    },
                    {
                        'heading': 'Precautions',
                        'body': 'Cut the shoot under water to prevent air entering xylem. Fit joints tightly with petroleum jelly if needed. Let the shoot acclimatize before readings and reset the air bubble carefully.\n\nThe simulation shows bubble displacement, elapsed time and calculated rate so students practice tabulation and unit conversion.',
                    },
                ],
                [
                    {
                        'q': 'A potometer directly measures:',
                        'options': ['Water uptake by the shoot', 'Exact glucose production', 'DNA length', 'Blood pressure'],
                        'answer': 0,
                        'explain': 'Potometers measure water uptake, which estimates transpiration under controlled conditions.',
                    },
                    {
                        'q': 'Why must the apparatus be airtight?',
                        'options': ['Leaks break the link between bubble movement and water uptake', 'To change leaf color', 'To kill the plant instantly', 'To increase microscope power'],
                        'answer': 0,
                        'explain': 'Air leaks let water movement occur outside the measured capillary path.',
                    },
                ],
            ),
            _lesson(
                'pollen-germination',
                'Pollen Germination',
                'bubble_chart',
                16,
                'pollen',
                'Grow pollen tubes on sucrose-boric acid medium and measure tube length under changing conditions.',
                [
                    'Explain pollen-tube formation during fertilization',
                    'Prepare a suitable germination medium',
                    'Measure germination percentage and tube length',
                ],
                [
                    {
                        'heading': 'Pollen tube carries male gametes',
                        'body': 'When compatible pollen lands on a stigma, it germinates and forms a pollen tube. The tube grows through style tissue toward the ovule, carrying male gametes for fertilization. In the lab, pollen can germinate on a slide using sucrose solution with small amounts of boric acid and minerals.\n\nGermination percentage and tube length depend on species, pollen freshness, sucrose concentration, temperature and time.',
                    },
                    {
                        'heading': 'Observation and calculation',
                        'body': 'Students count total pollen grains and germinated grains in microscope fields. Germination percentage = germinated grains / total grains x 100. Tube length can be estimated with an eyepiece scale if calibrated.\n\nThe virtual microscope shows how concentration affects tube growth and why counting multiple fields gives a better estimate.',
                    },
                ],
                [
                    {
                        'q': 'A pollen tube helps carry:',
                        'options': ['Male gametes toward the ovule', 'Xylem sap to leaves', 'Starch to roots only', 'Blood cells'],
                        'answer': 0,
                        'explain': 'The pollen tube transports male gametes through the style to the ovule.',
                    },
                    {
                        'q': 'Germination percentage equals:',
                        'options': ['Germinated pollen divided by total pollen times 100', 'Tube length minus slide length', 'Objective power only', 'Number of petals'],
                        'answer': 0,
                        'explain': 'The percentage is calculated from germinated grains relative to all counted grains.',
                    },
                ],
            ),
            _lesson(
                'mitosis-root-tip',
                'Mitosis in Onion Root Tip',
                'cycle',
                18,
                'mitosis',
                'Scan a root-tip squash, classify cells into mitotic stages and compute mitotic index.',
                [
                    'Identify prophase, metaphase, anaphase and telophase',
                    'Explain why root tips are used for mitosis observation',
                    'Calculate mitotic index from counted cells',
                ],
                [
                    {
                        'heading': 'Root tips divide actively',
                        'body': 'Onion root tips contain meristematic cells that divide rapidly. After fixing, hydrolysing, staining and squashing, chromosomes become visible under the microscope. Different cells show different stages of mitosis.\n\nProphase shows condensing chromosomes, metaphase aligns chromosomes at the equator, anaphase separates sister chromatids and telophase forms daughter nuclei.',
                    },
                    {
                        'heading': 'Mitotic index',
                        'body': 'Mitotic index = number of cells in mitosis / total observed cells x 100. It estimates how actively a tissue is dividing. Counting many cells reduces random error.\n\nThe simulation lets students classify cells and checks whether they confuse metaphase alignment with anaphase separation.',
                    },
                ],
                [
                    {
                        'q': 'Chromosomes align at the equator during:',
                        'options': ['Metaphase', 'Anaphase', 'Telophase', 'Interphase only'],
                        'answer': 0,
                        'explain': 'In metaphase, chromosomes line up at the cell equator before sister chromatids separate.',
                    },
                    {
                        'q': 'Mitotic index measures:',
                        'options': ['Fraction of cells undergoing mitosis', 'Leaf water loss only', 'Pollen tube diameter only', 'Blood type'],
                        'answer': 0,
                        'explain': 'Mitotic index is the percentage or fraction of observed cells currently in mitosis.',
                    },
                ],
            ),
            _lesson(
                'mendelian-cross',
                'Mendelian Genetics Simulator',
                'family_history',
                17,
                'genetics',
                'Set parent genotypes, build Punnett squares and compare predicted ratios with random offspring counts.',
                [
                    'Use genotype and phenotype correctly',
                    'Construct monohybrid and dihybrid Punnett squares',
                    'Explain why observed ratios vary in small samples',
                ],
                [
                    {
                        'heading': 'Alleles segregate into gametes',
                        'body': 'Mendelian inheritance models genes as allele pairs. During gamete formation, alleles segregate so each gamete receives one allele from each pair. Fertilization combines gametes, producing predictable genotype probabilities.\n\nA monohybrid heterozygous cross Aa x Aa gives a 1:2:1 genotype ratio and often a 3:1 dominant-to-recessive phenotype ratio if A is completely dominant.',
                    },
                    {
                        'heading': 'Probability needs sample size',
                        'body': 'Punnett squares give expected probabilities, not guaranteed counts. Ten offspring may not show a perfect 3:1 ratio. Hundreds are usually closer.\n\nThe simulation rolls virtual offspring and compares observed counts with expected ratios, showing why practical genetics relies on probability and statistics.',
                    },
                ],
                [
                    {
                        'q': 'Aa x Aa gives which genotype ratio?',
                        'options': ['1 AA : 2 Aa : 1 aa', '3 AA : 1 aa only', 'All aa', 'No offspring'],
                        'answer': 0,
                        'explain': 'Each parent makes A and a gametes, giving AA, Aa, Aa and aa combinations.',
                    },
                    {
                        'q': 'Observed ratios vary most when sample size is:',
                        'options': ['Small', 'Very large', 'Infinite', 'Not counted'],
                        'answer': 0,
                        'explain': 'Small samples are strongly affected by chance.',
                    },
                ],
            ),
            _lesson(
                'dna-isolation',
                'DNA Isolation From Plant Tissue',
                'genetics',
                18,
                'dna',
                'Break cells with detergent and salt, filter extract and precipitate DNA with cold alcohol.',
                [
                    'Explain why detergent, salt and alcohol are used in DNA extraction',
                    'Sequence the main steps of plant DNA isolation',
                    'Identify sources of contamination and poor yield',
                ],
                [
                    {
                        'heading': 'Chemistry releases DNA',
                        'body': 'Plant tissue is crushed to break cell walls. Detergent disrupts cell and nuclear membranes. Salt helps neutralize charges on DNA and proteins. Filtering removes solids. Cold ethanol or isopropanol makes DNA precipitate as white threads because DNA is not very soluble in alcohol.\n\nThis is a safe school-level extraction, not a clinical genetic test. The product is crude DNA mixed with other molecules.',
                    },
                    {
                        'heading': 'Yield and precautions',
                        'body': 'Fresh soft tissue, careful grinding, cold alcohol and gentle layering improve visible DNA yield. Vigorous shaking after alcohol can shear DNA into tiny fragments.\n\nThe simulation lets students adjust detergent, salt and alcohol temperature, then see whether DNA precipitates clearly or remains contaminated.',
                    },
                ],
                [
                    {
                        'q': 'Detergent helps DNA extraction by:',
                        'options': ['Breaking lipid membranes', 'Making chromosomes invisible', 'Turning DNA into protein', 'Creating pollen tubes'],
                        'answer': 0,
                        'explain': 'Detergent disrupts cell and nuclear membranes, releasing DNA.',
                    },
                    {
                        'q': 'Cold alcohol is used to:',
                        'options': ['Precipitate DNA', 'Grow roots', 'Open stomata', 'Boil Benedict reagent'],
                        'answer': 0,
                        'explain': 'DNA is poorly soluble in cold alcohol and appears as white threads.',
                    },
                ],
            ),
            _lesson(
                'animal-tissue-histology',
                'Animal Tissue Histology',
                'biotech',
                17,
                'histology',
                'Compare epithelial, connective, muscular and nervous tissue slides with labelled diagnostic features.',
                [
                    'Identify four basic animal tissue types',
                    'Relate tissue structure to function',
                    'Use microscope evidence for identification',
                ],
                [
                    {
                        'heading': 'Tissues are specialized cell groups',
                        'body': 'Epithelial tissue covers surfaces and lines cavities. Connective tissue supports and binds. Muscle tissue contracts. Nervous tissue conducts impulses. Each tissue type has visible structural clues: cell arrangement, matrix, fibres, striations or branching neurons.\n\nHistology practicals require careful observation rather than memorizing names. The reason for identification should point to visible characters.',
                    },
                    {
                        'heading': 'Structure supports function',
                        'body': 'Squamous epithelium is thin for diffusion, cartilage has a firm matrix for support, skeletal muscle has striations for voluntary contraction and neurons have long processes for signal transmission.\n\nThe simulation provides slide fields and a 3D tissue block so learners can link microscopic texture with biological role.',
                    },
                ],
                [
                    {
                        'q': 'Which tissue conducts nerve impulses?',
                        'options': ['Nervous tissue', 'Cartilage only', 'Xylem', 'Cork'],
                        'answer': 0,
                        'explain': 'Neurons in nervous tissue conduct electrical impulses.',
                    },
                    {
                        'q': 'Striations are a diagnostic feature of:',
                        'options': ['Skeletal muscle', 'Simple squamous epithelium only', 'Blood plasma', 'Pollen'],
                        'answer': 0,
                        'explain': 'Skeletal muscle fibres show cross-striations under the microscope.',
                    },
                ],
            ),
            _lesson(
                'blood-grouping',
                'ABO and Rh Blood Grouping',
                'hematology',
                18,
                'blood',
                'Mix simulated blood with anti-A, anti-B and anti-D sera, observe agglutination and infer blood group safely.',
                [
                    'Explain antigen-antibody agglutination in ABO and Rh typing',
                    'Interpret anti-A, anti-B and anti-D reactions',
                    'State why real blood work needs strict biosafety',
                ],
                [
                    {
                        'heading': 'Agglutination reveals antigens',
                        'body': 'Red blood cells may carry A antigen, B antigen, both or neither. Anti-A serum agglutinates cells with A antigen. Anti-B agglutinates cells with B antigen. Anti-D detects the Rh factor. The reaction pattern identifies blood group.\n\nFor example, agglutination with anti-A and anti-D but not anti-B indicates A positive blood.',
                    },
                    {
                        'heading': 'Safety and ethics',
                        'body': 'Real blood grouping must use sterile lancets, gloves, proper disposal and consent. No student should share lancets or handle blood casually. Virtual practice helps students learn interpretation before supervised real work.\n\nThe simulation randomizes samples and requires learners to record all three reactions before revealing the group.',
                    },
                ],
                [
                    {
                        'q': 'Agglutination with anti-A only means the ABO group is:',
                        'options': ['A', 'B', 'AB', 'O'],
                        'answer': 0,
                        'explain': 'Anti-A agglutination shows A antigen is present; no anti-B reaction means B antigen is absent.',
                    },
                    {
                        'q': 'Anti-D serum tests for:',
                        'options': ['Rh factor', 'Starch', 'Pollen germination', 'Xylem'],
                        'answer': 0,
                        'explain': 'Anti-D detects the D antigen, commonly called Rh positive when present.',
                    },
                ],
            ),
        ],
    },
]
