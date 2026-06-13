COURSES = [
    {
        'slug': 'neb-biology-practical-11-12',
        'title': 'NEB Biology Practicals — Class 11 & 12',
        'category': 'biology',
        'age_range': '16-18',
        'level': 'Intermediate',
        'icon': 'biotech',
        'color': '#84CC16',
        'tagline': 'Every NEB biology practical as a realistic virtual lab — microscopes, osmosis, mitosis and more.',
        'description': (
            'This course takes you through the essential NEB Class 11 and 12 biology practicals '
            'with one working virtual instrument or simulation per experiment. You will focus a '
            'compound microscope on real slides, measure water movement in potato tissue, step '
            'through every stage of mitosis, count oxygen bubbles from Hydrilla, track a '
            'transpiration bubble in a potometer and plot enzyme activity curves — recording '
            'observations and computing results exactly as you will in the school lab and the '
            'board practical exam. Every formula, technique and source of error matches the '
            'standard NEB lab manual.'
        ),
        'skills': [
            'Operating a compound microscope and computing total magnification',
            'Identifying cell organelles and comparing plant/animal cells',
            'Investigating osmosis and interpreting tonicity',
            'Describing all six stages of mitosis with accurate chromosome behaviour',
            'Measuring photosynthesis rate and identifying limiting factors',
            'Using a potometer and explaining factors affecting transpiration',
            'Plotting and interpreting enzyme activity curves',
        ],
        'lessons': [
            {
                'slug': 'compound-microscope',
                'title': 'Compound Microscope',
                'icon': 'biotech',
                'minutes': 18,
                'sim': 'biology/compound-microscope',
                'sim_type': 'lab',
                'summary': (
                    'Adjust coarse and fine focus knobs, switch between 10×, 40× and 100× '
                    'objectives, and control the diaphragm to bring onion peel or blood smear '
                    'slides into sharp focus. Compute total magnification as eyepiece × objective.'
                ),
                'objectives': [
                    'Name and locate all major parts of a compound microscope',
                    'Compute total magnification as eyepiece (10×) × objective magnification',
                    'Use coarse focus for initial focusing and fine focus for sharp resolution',
                    'Explain how the diaphragm controls contrast and brightness',
                    'Describe what onion peel and blood smear slides look like under different magnifications',
                ],
                'knowledge': [
                    {
                        'heading': 'Parts of the compound microscope',
                        'body': (
                            'A compound microscope uses two sets of lenses to achieve high magnification. '
                            'The eyepiece (ocular lens) is the lens you look through — in school microscopes '
                            'it is almost always 10×. The objective lenses are mounted on a revolving nosepiece '
                            'and come in three powers: low power (10×), high power (40×) and oil immersion (100×). '
                            'Total magnification = eyepiece power × objective power, so the 100× objective gives '
                            '10 × 100 = 1000× total magnification.\n\n'
                            'Other key parts: the stage holds the slide; the condenser focuses light on the '
                            'specimen; the iris diaphragm controls how much light passes through. The arm '
                            'and base support everything. The coarse focus knob moves the stage large '
                            'distances (for initial focusing) while the fine focus knob gives precise '
                            'small-step adjustments needed with high-power objectives.'
                        ),
                    },
                    {
                        'heading': 'Focusing technique and objective switching',
                        'body': (
                            'Always start with the lowest-power objective (10×). Place the slide on the stage, '
                            'use the coarse focus to get the image roughly in view, then fine-tune with the '
                            'fine focus knob. Once sharp at low power, switch to 40× — the image should be '
                            'nearly in focus already (microscopes are designed to be parfocal). Use only the '
                            'fine focus at 40×; using the coarse focus can crash the objective into the slide '
                            'and scratch the lens.\n\n'
                            'At 100× (oil immersion), a drop of immersion oil must be placed between the '
                            'objective and the slide to prevent light from scattering at the glass-air interface. '
                            'The oil has the same refractive index as glass (n ≈ 1.515), maintaining the light '
                            'path and allowing the full resolving power of the objective. Always wipe the lens '
                            'clean with lens tissue after oil-immersion use — never ordinary tissue or cloth, '
                            'which scratches the coating.'
                        ),
                    },
                    {
                        'heading': 'Preparing and viewing slides',
                        'body': (
                            'For an onion peel: peel a thin, transparent epidermal layer from the inner '
                            'surface of a fresh onion scale, mount on a slide in a drop of water, and add '
                            'a cover slip. Optionally stain with iodine solution (turns starch in cell wall '
                            'and nucleus blue-black), which makes the rectangular cells and their nuclei '
                            'clearly visible. The cells are non-living (plasmolysed in stain) but the cell '
                            'walls, nuclei and sometimes vacuoles are clear.\n\n'
                            'For a blood smear: a drop of blood is spread as a thin film across the slide, '
                            'allowed to air-dry, and stained with Leishman\'s or Giemsa stain. You should '
                            'see abundant red blood cells (erythrocytes: biconcave discs, no nucleus), '
                            'occasional white blood cells (leucocytes: larger, with lobed or round nuclei), '
                            'and tiny platelets. The NEB practical exam often asks you to identify and '
                            'draw these cell types at 400× (40× objective).'
                        ),
                    },
                ],
                'fun_fact': (
                    'Antonie van Leeuwenhoek ground lenses by hand in the 1670s and was the first person '
                    'to see living bacteria — with a microscope barely more powerful than a school 10× '
                    'objective. Modern electron microscopes can resolve atoms at 10,000,000× magnification.'
                ),
                'quiz': [
                    {
                        'q': 'A microscope has a 10× eyepiece and a 40× objective. Total magnification = ?',
                        'options': ['40×', '400×', '50×', '4000×'],
                        'answer': 1,
                        'explain': 'Total magnification = eyepiece × objective = 10 × 40 = 400×.',
                    },
                    {
                        'q': 'Which focus knob should you use at high power (40× and above)?',
                        'options': ['Coarse focus only', 'Fine focus only', 'Either coarse or fine', 'No focus is needed'],
                        'answer': 1,
                        'explain': (
                            'At high power the working distance is very small — using the coarse focus '
                            'can drive the objective into the slide and scratch the lens. Use only the fine focus.'
                        ),
                    },
                    {
                        'q': 'Immersion oil is used with the 100× objective because:',
                        'options': [
                            'It lubricates the lens',
                            'Its refractive index matches glass, preventing light scattering at air-glass interfaces',
                            'It stains the specimen',
                            'It makes the slide stick to the stage',
                        ],
                        'answer': 1,
                        'explain': (
                            'Immersion oil (n ≈ 1.515) has the same refractive index as the glass slide, '
                            'so light passes straight through without bending at the air-glass boundary, '
                            'allowing full resolution.'
                        ),
                    },
                ],
            },
            {
                'slug': 'plant-animal-cell',
                'title': 'Plant vs Animal Cell (3D)',
                'icon': 'cell_tower',
                'minutes': 20,
                'sim': 'biology/plant-animal-cell',
                'sim_type': '3d',
                'summary': (
                    'Explore a 3D plant cell and animal cell side by side. Click organelles — '
                    'nucleus, mitochondria, chloroplast, cell wall, vacuole, ER, Golgi, ribosomes — '
                    'to see their name and function. Toggle between plant and animal to compare.'
                ),
                'objectives': [
                    'List the organelles present in plant cells but absent in animal cells',
                    'State the function of at least six organelles common to both cell types',
                    'Explain why chloroplasts are found only in plant cells',
                    'Describe how the central vacuole maintains turgor pressure',
                    'Distinguish lysosomes from the central vacuole in their digestive role',
                ],
                'knowledge': [
                    {
                        'heading': 'Organelles common to plant and animal cells',
                        'body': (
                            'Both cell types share the fundamental toolkit of eukaryotic life. The nucleus '
                            'is the control centre, housing DNA packaged into chromosomes within the nuclear '
                            'envelope. The rough endoplasmic reticulum (rough ER), studded with ribosomes, '
                            'synthesises and folds secretory proteins. The Golgi apparatus (Golgi body) '
                            'receives proteins from the ER, modifies them by adding sugar chains '
                            '(glycosylation), and dispatches them in membrane vesicles.\n\n'
                            'Mitochondria carry out aerobic respiration: glucose + oxygen → CO₂ + water + '
                            'ATP. Their inner membrane is folded into cristae, maximising surface area for '
                            'ATP synthesis. Ribosomes — either free in the cytoplasm or attached to rough ER '
                            '— translate mRNA into protein. A single mammalian cell contains millions of '
                            'ribosomes, reflecting how much protein synthesis life requires.'
                        ),
                    },
                    {
                        'heading': 'Structures unique to plant cells',
                        'body': (
                            'Three major structures distinguish plant from animal cells. The cell wall is a '
                            'rigid layer of cellulose fibres outside the plasma membrane; it provides '
                            'structural support, prevents excessive water uptake (bursting), and '
                            'withstands turgor pressure. Animal cells have no cell wall, relying instead '
                            'on the cytoskeleton and extracellular matrix.\n\n'
                            'Chloroplasts are double-membraned organelles containing the green pigment '
                            'chlorophyll. They carry out photosynthesis: 6CO₂ + 6H₂O + light → '
                            'C₆H₁₂O₆ + 6O₂. The central (large) vacuole, surrounded by the tonoplast '
                            'membrane, can occupy up to 90% of a mature plant cell\'s volume. It stores '
                            'water (maintaining turgor), ions, pigments (anthocyanins), and waste products. '
                            'When the vacuole is full, turgor pressure pushes the cytoplasm against the '
                            'cell wall — this is what keeps herbaceous plants upright; wilting occurs '
                            'when the vacuole loses water.'
                        ),
                    },
                    {
                        'heading': 'Structures unique to animal cells',
                        'body': (
                            'Lysosomes are membrane-bound sacs containing hydrolytic (digestive) enzymes '
                            'at pH ~5. They digest worn-out organelles (autophagy), engulfed bacteria '
                            '(phagocytosis), and cellular debris. Plants use the vacuole for similar '
                            'storage and breakdown functions. Centrioles — pairs of short cylindrical '
                            'microtubule structures — organise the mitotic spindle during cell division. '
                            'Higher plants can divide without centrioles, though lower plants such as '
                            'ferns and mosses retain them.\n\n'
                            'A useful NEB exam summary: plant cells have cell wall + chloroplasts + large '
                            'central vacuole; animal cells have centrioles + lysosomes + no cell wall. '
                            'Both have nucleus, mitochondria, ER, Golgi, ribosomes, and a plasma membrane.'
                        ),
                    },
                ],
                'fun_fact': (
                    'A single chloroplast contains about 200,000 molecules of chlorophyll. Nepal\'s '
                    'Terai forests convert more solar energy per square metre in summer than almost '
                    'any ecosystem on Earth — all driven by chloroplasts.'
                ),
                'quiz': [
                    {
                        'q': 'Which of these is found in a plant cell but NOT in a typical animal cell?',
                        'options': ['Mitochondria', 'Nucleus', 'Chloroplast', 'Ribosome'],
                        'answer': 2,
                        'explain': (
                            'Chloroplasts are the site of photosynthesis and are unique to plant (and algal) '
                            'cells. Mitochondria, nucleus and ribosomes are present in both.'
                        ),
                    },
                    {
                        'q': 'The central vacuole in a plant cell is mainly responsible for:',
                        'options': [
                            'Protein synthesis',
                            'Photosynthesis',
                            'Maintaining turgor pressure and storing water',
                            'Producing ATP',
                        ],
                        'answer': 2,
                        'explain': (
                            'The central vacuole stores water and maintains turgor pressure — the outward '
                            'push of water against the cell wall that keeps plant cells firm and plants upright.'
                        ),
                    },
                    {
                        'q': 'Which organelle modifies proteins and packages them for secretion?',
                        'options': ['Ribosome', 'Mitochondria', 'Golgi apparatus', 'Nucleus'],
                        'answer': 2,
                        'explain': (
                            'The Golgi apparatus receives proteins from the rough ER, adds sugar groups, '
                            'sorts them, and dispatches them in vesicles to their final destinations.'
                        ),
                    },
                ],
            },
            {
                'slug': 'osmosis-potato',
                'title': 'Osmosis — Potato Osmometer',
                'icon': 'opacity',
                'minutes': 16,
                'sim': 'biology/osmosis-potato',
                'sim_type': 'lab',
                'summary': (
                    'Vary external solution concentration from 0-3% (w/v) and watch net water '
                    'movement, mass change percentage, and a live plot. Accurate tonicity '
                    'behaviour: hypotonic swells the potato, hypertonic shrinks it, isotonic '
                    '(~0.9%) causes no change.'
                ),
                'objectives': [
                    'Define osmosis in terms of water potential gradient across a semi-permeable membrane',
                    'Predict whether a potato strip will gain or lose mass in a given concentration',
                    'Distinguish between hypotonic, isotonic and hypertonic solutions',
                    'Explain why the isotonic point of potato is approximately 0.9% sucrose',
                    'Plot mass change % against concentration and identify the isotonic point',
                ],
                'knowledge': [
                    {
                        'heading': 'Osmosis and water potential',
                        'body': (
                            'Osmosis is the net movement of water molecules from a region of higher '
                            'water potential (psi) to lower water potential across a partially (semi-) '
                            'permeable membrane. Water potential is lowered by dissolved solutes '
                            '(solute potential) and raised by pressure (pressure potential). '
                            'Pure water has water potential = 0; adding solute makes it negative.\n\n'
                            'In a typical NEB potato osmosis experiment, cylinders of raw potato are '
                            'placed in a range of sucrose or NaCl solutions for 30-60 minutes, then '
                            'blotted dry and reweighed. A graph of percentage mass change against '
                            'concentration is plotted; the x-intercept (zero change) gives the '
                            'isotonic concentration — the concentration that exactly matches the '
                            'osmolarity of the potato cell sap (approximately 0.9% w/v sucrose for '
                            'potato, equivalent to about 0.25-0.3 M).'
                        ),
                    },
                    {
                        'heading': 'Hypotonic, isotonic and hypertonic',
                        'body': (
                            'A hypotonic solution has a lower solute concentration than the cell sap '
                            '(higher water potential outside). Water moves by osmosis INTO the cell, '
                            'increasing turgor. The potato strip gains mass and becomes firm (turgid). '
                            'If cells were not protected by a rigid cell wall, they would burst '
                            '(lysis) — as red blood cells do in pure water.\n\n'
                            'A hypertonic solution has a higher solute concentration than the cell '
                            '(lower water potential outside). Water moves OUT of the cell, the '
                            'vacuole shrinks and the plasma membrane pulls away from the cell wall '
                            '— a process called plasmolysis. The potato strip loses mass and '
                            'becomes flaccid. In an isotonic solution, water potential is equal on '
                            'both sides, so net water movement is zero and mass stays constant.'
                        ),
                    },
                    {
                        'heading': 'Experiment procedure and sources of error',
                        'body': (
                            'Cut potato cylinders to equal length and diameter using a cork borer '
                            '(approximately 5 cm, 1 cm diameter). Blot excess surface water and record initial '
                            'mass. Prepare sucrose solutions: 0%, 0.2%, 0.4%, 0.6%, 0.8%, 1.0% etc. '
                            'Immerse cylinders for 30 minutes, blot and reweigh. Calculate '
                            'percentage mass change = (final minus initial) / initial × 100.\n\n'
                            'Key sources of error: cutting cylinders to different sizes '
                            '(standardise with a ruler and the same borer), not blotting surface '
                            'water consistently, cylinders drying out in air before measuring, '
                            'and temperature changes affecting membrane permeability. For the '
                            'NEB practical report, state that the semi-permeable membrane here '
                            'is the tonoplast and plasma membrane of the potato cells, not a '
                            'dialysis tube — the potato is its own osmometer.'
                        ),
                    },
                ],
                'fun_fact': (
                    'Cells in a salty pickle become plasmolysed — water moves out by osmosis into '
                    'the brine, shrinking the cell contents away from the wall. This is exactly why '
                    'salt "preserves" food: bacteria also lose water and cannot grow.'
                ),
                'quiz': [
                    {
                        'q': 'A potato strip is placed in 2% sucrose solution and loses mass. The solution is:',
                        'options': ['Hypotonic', 'Isotonic', 'Hypertonic', 'Neutral'],
                        'answer': 2,
                        'explain': (
                            'The potato loses water to the external solution, meaning the solution has '
                            'a lower water potential than the cell sap — a hypertonic solution.'
                        ),
                    },
                    {
                        'q': 'At the isotonic concentration, the mass of the potato strip:',
                        'options': ['Increases', 'Decreases', 'Stays the same', 'Doubles'],
                        'answer': 2,
                        'explain': (
                            'When external and internal water potentials are equal, there is no net '
                            'water movement, so no change in mass.'
                        ),
                    },
                    {
                        'q': 'Plasmolysis occurs when:',
                        'options': [
                            'Water enters the cell and the vacuole swells',
                            'Water leaves the cell and the plasma membrane pulls away from the cell wall',
                            'The cell wall dissolves',
                            'The nucleus divides',
                        ],
                        'answer': 1,
                        'explain': (
                            'In a hypertonic solution the vacuole loses water, shrinks, and the '
                            'plasma membrane detaches from the cell wall — this is plasmolysis.'
                        ),
                    },
                ],
            },
            {
                'slug': 'mitosis-onion-root',
                'title': 'Mitosis in Onion Root Tip',
                'icon': 'cell_merge',
                'minutes': 18,
                'sim': 'biology/mitosis-onion-root',
                'sim_type': 'lab',
                'summary': (
                    'Step through interphase through prophase through metaphase through anaphase through telophase '
                    'through cytokinesis with accurate chromosome behaviour. Labels and descriptions '
                    'appear for each stage. Onion root tip context with simplified 2n = 8.'
                ),
                'objectives': [
                    'Describe the events in each stage of mitosis in the correct order',
                    'Explain what happens to the nuclear envelope, chromosomes and spindle in each phase',
                    'State why the metaphase stage is used to count chromosomes',
                    'Distinguish mitosis from meiosis in terms of chromosome number in daughter cells',
                    'Explain why mitosis is used for growth and repair, not sexual reproduction',
                ],
                'knowledge': [
                    {
                        'heading': 'Why cells divide: the purpose of mitosis',
                        'body': (
                            'Mitosis is cell division that produces two genetically identical daughter '
                            'cells from one parent cell. It is used for: growth (adding new cells to '
                            'developing tissues), repair and replacement (replacing worn-out skin, gut '
                            'lining and blood cells), and asexual reproduction (in plants producing '
                            'runners and tubers).\n\n'
                            'Because the daughter cells are genetically identical, mitosis is NOT used '
                            'for sexual reproduction — that requires meiosis, which halves the chromosome '
                            'number. Mitosis maintains the diploid (2n) number: for Allium cepa (onion), '
                            '2n = 16. The root tip meristem is the classic NEB material because these '
                            'actively dividing cells make it easy to find all stages on one slide.'
                        ),
                    },
                    {
                        'heading': 'The stages in detail',
                        'body': (
                            'INTERPHASE: the stage that appears resting but is actually very active. '
                            'DNA replicates (S phase) so each chromosome becomes two identical sister '
                            'chromatids joined at the centromere. The cell grows and makes proteins. '
                            'Chromosomes are not yet visible (as diffuse chromatin).\n\n'
                            'PROPHASE: chromatin condenses into visible chromosomes. Spindle fibres form '
                            'from MTOCs (centrioles in animals; other structures in plants). The '
                            'nucleolus disappears and the nuclear envelope breaks down.\n\n'
                            'METAPHASE: chromosomes align at the equatorial plate (middle of the cell), '
                            'each attached to spindle fibres from both poles via kinetochores. '
                            'Chromosomes are most condensed here — the ideal stage to count them.\n\n'
                            'ANAPHASE: centromeres split and sister chromatids (now called chromosomes) '
                            'are pulled to opposite poles by shortening spindle fibres. The cell elongates.\n\n'
                            'TELOPHASE: chromosomes reach the poles and decondense. Nuclear envelopes '
                            'reform. The nucleolus reappears.'
                        ),
                    },
                    {
                        'heading': 'Cytokinesis and plant vs animal differences',
                        'body': (
                            'Cytokinesis (cytoplasm division) follows telophase. In ANIMAL cells, a '
                            'cleavage furrow of contractile actin and myosin proteins pinches the cell '
                            'membrane inward from the outside until the cell splits in two.\n\n'
                            'In PLANT cells, a cell plate forms at the cell equator from Golgi vesicles '
                            'filled with pectin and cellulose precursors. The vesicles fuse and lay '
                            'down a new middle lamella and primary cell walls, growing outward until '
                            'they join the existing cell wall — the rigid wall prevents animal-style '
                            'pinching. The result in both cases is two genetically identical daughter '
                            'cells with the full diploid chromosome number (2n).'
                        ),
                    },
                ],
                'fun_fact': (
                    'Your bone marrow produces about 2 million new red blood cells every second by '
                    'mitosis. Over an average lifetime, you produce your body weight in red blood '
                    'cells — all through this same six-stage process.'
                ),
                'quiz': [
                    {
                        'q': 'At which stage do chromosomes line up at the cell\'s equatorial plate?',
                        'options': ['Prophase', 'Anaphase', 'Metaphase', 'Telophase'],
                        'answer': 2,
                        'explain': (
                            'During metaphase, spindle fibres from both poles pull chromosomes to '
                            'the middle of the cell, where they align at the metaphase plate.'
                        ),
                    },
                    {
                        'q': 'Why is metaphase the best stage for counting chromosomes?',
                        'options': [
                            'Chromosomes are most condensed and clearly separate',
                            'The nucleus is visible',
                            'DNA replication occurs here',
                            'Cytokinesis has just finished',
                        ],
                        'answer': 0,
                        'explain': (
                            'Chromosomes are maximally condensed and individually visible at metaphase, '
                            'and each one is still a unit (centromeres have not yet split).'
                        ),
                    },
                    {
                        'q': 'In plant cells, cytokinesis occurs by:',
                        'options': [
                            'A cleavage furrow pinching the membrane',
                            'A cell plate forming from Golgi vesicles at the equator',
                            'The cell wall dissolving and reforming',
                            'Chromosomes moving to the poles',
                        ],
                        'answer': 1,
                        'explain': (
                            'Plant cells cannot pinch inward because of the rigid cell wall, so a '
                            'new cell plate grows outward from the centre using vesicles from the Golgi.'
                        ),
                    },
                ],
            },
            {
                'slug': 'photosynthesis-rate',
                'title': 'Photosynthesis Rate — Hydrilla Experiment',
                'icon': 'eco',
                'minutes': 17,
                'sim': 'biology/photosynthesis-rate',
                'sim_type': 'lab',
                'summary': (
                    'Count O2 bubbles from Hydrilla as you vary light intensity, CO2 '
                    'concentration and temperature. Accurate limiting-factor plateau: '
                    'raising one factor beyond its saturation point does not increase '
                    'rate if another factor is limiting.'
                ),
                'objectives': [
                    'Write the balanced equation for aerobic photosynthesis',
                    'Identify the three main limiting factors of photosynthesis rate',
                    'Explain why rate plateaus when a non-limiting factor is increased',
                    'Describe Blackman\'s law of limiting factors',
                    'Analyse a rate-vs-light intensity graph showing the compensation point and saturation',
                ],
                'knowledge': [
                    {
                        'heading': 'The photosynthesis equation and raw materials',
                        'body': (
                            'Photosynthesis converts light energy into chemical energy stored in glucose: '
                            '6CO2 + 6H2O + light energy -> C6H12O6 + 6O2. The reaction occurs in two '
                            'stages: the light-dependent reactions in the thylakoid membranes of '
                            'chloroplasts (capturing light energy to split water, releasing O2 and '
                            'producing ATP and NADPH), and the light-independent reactions (Calvin '
                            'cycle) in the stroma, which use ATP and NADPH to fix CO2 into glucose.\n\n'
                            'In the Hydrilla experiment, the aquatic plant is placed in a test tube '
                            'of sodium hydrogen carbonate solution (NaHCO3 provides CO2) and '
                            'illuminated. Each O2 bubble released represents a measurable unit of '
                            'photosynthesis. Counting bubbles per minute gives the relative rate.'
                        ),
                    },
                    {
                        'heading': 'Limiting factors and Blackman\'s law',
                        'body': (
                            'Blackman\'s law of limiting factors (1905) states: when a process is '
                            'affected by more than one factor, the rate is limited by the factor '
                            'nearest its minimum. In other words, the slowest step controls the '
                            'overall speed.\n\n'
                            'For photosynthesis, the three main limiting factors are: light intensity '
                            '(drives the light reactions), CO2 concentration (substrate for the '
                            'Calvin cycle), and temperature (affects enzyme speeds of rubisco and '
                            'other Calvin cycle enzymes). On a rate-vs-light-intensity graph, rate '
                            'increases with light up to a plateau — the saturation point — where '
                            'either CO2 or temperature becomes limiting. Increasing light beyond '
                            'this point does nothing until the other factor is also increased.'
                        ),
                    },
                    {
                        'heading': 'Procedure and sources of error',
                        'body': (
                            'Use a fresh sprig of Hydrilla (or Elodea). Prepare sodium hydrogen '
                            'carbonate solution (0.5-1.0%) as a CO2 source. Use a light source at '
                            'known distances (intensity proportional to 1/d squared). Count bubbles per minute at each '
                            'intensity, allowing 2 minutes to equilibrate before counting. Repeat '
                            'three times per distance and average.\n\n'
                            'For temperature: use water baths at 10, 20, 30, 40 degrees C and repeat the '
                            'intensity series. For CO2: vary NaHCO3 concentration.\n\n'
                            'Sources of error: bubbles vary in size (volume not counted), the plant '
                            'adapts to light changes slowly, ambient light contributes, and the '
                            'plant may photosynthesise at different rates at different positions '
                            'within the sprig. Write the precaution that the plant should be '
                            'allowed to equilibrate for at least 2 minutes before counting.'
                        ),
                    },
                ],
                'fun_fact': (
                    'One large tropical tree can absorb up to 22 kg of CO2 per year and release '
                    '16 kg of O2 — the oxygen for roughly one person. Nepal\'s forests collectively '
                    'act as a massive carbon sink, sequestering millions of tonnes of CO2 annually.'
                ),
                'quiz': [
                    {
                        'q': 'You increase light intensity but the photosynthesis rate does not change. The most likely reason is:',
                        'options': [
                            'The plant is dead',
                            'Light is not a factor',
                            'Another factor such as CO2 or temperature is limiting',
                            'Too much light destroys chlorophyll',
                        ],
                        'answer': 2,
                        'explain': (
                            'Blackman\'s law: when one factor is in excess, the rate is limited by '
                            'whichever factor is in shortest supply. Increasing the non-limiting '
                            'factor has no effect.'
                        ),
                    },
                    {
                        'q': 'In the Hydrilla experiment, bubbles are counted as a measure of:',
                        'options': ['CO2 absorbed', 'O2 released', 'Glucose produced', 'Water split'],
                        'answer': 1,
                        'explain': (
                            'Oxygen is the gas product of the light reactions (photolysis of water). '
                            'Bubbles of O2 are released by the underwater plant and counted per minute.'
                        ),
                    },
                    {
                        'q': 'Increasing temperature from 25 to 35 degrees C usually increases photosynthesis rate because:',
                        'options': [
                            'More light energy is available',
                            'Enzyme reactions in the Calvin cycle speed up with temperature (Q10 approximately 2)',
                            'Chlorophyll absorbs more red light',
                            'Water molecules move faster so less water is needed',
                        ],
                        'answer': 1,
                        'explain': (
                            'The Calvin cycle enzymes (especially rubisco) are temperature-sensitive. '
                            'A 10 degree C rise roughly doubles enzyme reaction rates (Q10 approximately 2) up to the '
                            'optimum temperature (about 30-35 degrees C for most C3 plants).'
                        ),
                    },
                ],
            },
            {
                'slug': 'transpiration-potometer',
                'title': 'Transpiration — Bubble Potometer',
                'icon': 'water_drop',
                'minutes': 16,
                'sim': 'biology/transpiration-potometer',
                'sim_type': 'lab',
                'summary': (
                    'Use a bubble potometer to measure water uptake rate. Vary wind speed, '
                    'relative humidity, light intensity and temperature and watch how each '
                    'factor shifts the air bubble along the capillary tube. Accurate '
                    'physiological effects including stomatal response to light.'
                ),
                'objectives': [
                    'Describe the cohesion-tension mechanism of water movement in xylem',
                    'Explain how transpiration creates the driving force for water uptake',
                    'Predict the effect of wind, humidity, light and temperature on transpiration rate',
                    'Describe how to set up and use a potometer correctly',
                    'Explain why potometers measure water uptake rather than transpiration directly',
                ],
                'knowledge': [
                    {
                        'heading': 'Transpiration and the cohesion-tension theory',
                        'body': (
                            'Transpiration is the evaporation of water from the leaves and other '
                            'aerial parts of a plant, primarily through stomata — pores in the leaf '
                            'epidermis surrounded by guard cells. As water evaporates from the '
                            'mesophyll cell surfaces into the air spaces and then out through stomata, '
                            'it creates a water potential gradient that draws water from adjacent '
                            'cells and ultimately from the xylem vessels.\n\n'
                            'The cohesion-tension theory explains how water can be pulled up to the '
                            'tops of 100-metre tall trees against gravity. Water molecules are strongly '
                            'attracted to each other (cohesion, via hydrogen bonds) and to xylem '
                            'cell walls (adhesion). Evaporation at the leaf creates tension (negative '
                            'pressure) that pulls the continuous water column from roots upwards — '
                            'like a chain of molecules being dragged upward from the top.'
                        ),
                    },
                    {
                        'heading': 'Factors affecting transpiration rate',
                        'body': (
                            'Light: light triggers guard cells to open stomata (via blue light '
                            'receptors activating proton pumps, causing K+ influx and guard cell '
                            'swelling). Open stomata allow water vapour to escape. In darkness, '
                            'stomata close and transpiration drops to near zero.\n\n'
                            'Wind: still air around leaves becomes saturated with water vapour, '
                            'reducing the concentration gradient and slowing transpiration. Wind '
                            'removes humid air and restores the gradient — greatly increasing rate.\n\n'
                            'Humidity: high relative humidity means the air is already rich in water '
                            'vapour, reducing the vapour pressure deficit (VPD) between leaf and air '
                            'and slowing evaporation. Low humidity creates a steep gradient, accelerating '
                            'transpiration. Temperature: higher temperatures increase the kinetic energy '
                            'of water molecules (faster evaporation) and reduce air humidity (if '
                            'absolute humidity is constant, warmer air has lower RH).'
                        ),
                    },
                    {
                        'heading': 'Using a potometer: method and limitations',
                        'body': (
                            'A potometer measures the rate of water uptake by a cut shoot, not '
                            'transpiration directly — a small fraction of absorbed water goes to '
                            'photosynthesis and cell expansion. The apparatus consists of a capillary '
                            'tube containing an air bubble, connected to the cut stem via a reservoir. '
                            'As the shoot absorbs water (driven by transpiration), the bubble moves '
                            'along the capillary. Rate = distance moved by bubble per unit time '
                            '(mm/min), or volume if the tube bore is known.\n\n'
                            'Setting up: cut the shoot under water to prevent air entering the xylem '
                            '(an air embolism would block water flow). Ensure all joints are airtight '
                            'with petroleum jelly. Introduce the bubble by opening the tap briefly. '
                            'For NEB: state that this measures water uptake, not transpiration; '
                            'the difference is typically 1-2% for a well-watered plant.'
                        ),
                    },
                ],
                'fun_fact': (
                    'A large oak tree can transpire over 200 litres of water on a hot summer day — '
                    'that is more than 200 kg of water pumped up from the roots purely by the '
                    'tension created at the leaves, with no moving parts at all.'
                ),
                'quiz': [
                    {
                        'q': 'Transpiration rate increases in a breeze because:',
                        'options': [
                            'Wind opens stomata',
                            'Wind removes humid air from around leaves, restoring the water vapour gradient',
                            'Wind cools the leaves and reduces temperature',
                            'Wind brings more CO2',
                        ],
                        'answer': 1,
                        'explain': (
                            'Still air near the leaf saturates with water vapour, reducing the '
                            'concentration gradient that drives evaporation. Wind replaces humid '
                            'air with drier air, keeping the gradient steep and the rate high.'
                        ),
                    },
                    {
                        'q': 'A potometer measures:',
                        'options': [
                            'The exact rate of transpiration',
                            'The rate of water uptake by the cut shoot',
                            'The rate of glucose production',
                            'The concentration of water vapour in air',
                        ],
                        'answer': 1,
                        'explain': (
                            'A potometer records how fast the air bubble moves — i.e., how fast '
                            'the shoot absorbs water. This approximates transpiration rate but '
                            'includes a tiny amount of water used in photosynthesis and growth.'
                        ),
                    },
                    {
                        'q': 'Stomata close in darkness because:',
                        'options': [
                            'CO2 concentration drops',
                            'Blue light receptors in guard cells are no longer activated, so guard cells lose water and shrink',
                            'Temperature drops at night',
                            'Wind speed decreases at night',
                        ],
                        'answer': 1,
                        'explain': (
                            'Guard cells detect blue light via phototropin receptors, which drive '
                            'K+ uptake and guard cell swelling (stomata open). In darkness, this '
                            'signal is absent, K+ leaves, guard cells lose turgor and stomata close.'
                        ),
                    },
                ],
            },
            {
                'slug': 'enzyme-catalysis',
                'title': 'Enzyme Activity — Catalase & Amylase',
                'icon': 'science',
                'minutes': 18,
                'sim': 'biology/enzyme-catalysis',
                'sim_type': 'lab',
                'summary': (
                    'Plot enzyme activity against temperature (bell curve with denaturation above '
                    '50 degrees C), pH (bell curve at optimal pH 7 for catalase, pH 6.8 for amylase), '
                    'and substrate concentration (Michaelis-Menten saturation to Vmax). '
                    'Switch between catalase and amylase.'
                ),
                'objectives': [
                    'Explain enzyme action using the lock-and-key and induced-fit models',
                    'Describe the effect of temperature on enzyme activity including denaturation',
                    'Explain how pH affects enzyme activity in terms of active site shape',
                    'Interpret a Michaelis-Menten substrate concentration curve and define Km and Vmax',
                    'Design an experiment to find the optimum pH of amylase',
                ],
                'knowledge': [
                    {
                        'heading': 'Enzymes as biological catalysts',
                        'body': (
                            'Enzymes are proteins that act as biological catalysts — they speed up '
                            'chemical reactions without being permanently altered. Each enzyme has '
                            'an active site whose three-dimensional shape is complementary to a '
                            'specific substrate (lock-and-key model). In the refined induced-fit '
                            'model, the active site changes shape slightly when the substrate binds, '
                            'improving complementarity and lowering the activation energy more '
                            'effectively.\n\n'
                            'Catalase, found in all aerobic cells (liver, potato, yeast), catalyses '
                            'the breakdown of toxic hydrogen peroxide: 2H2O2 -> 2H2O + O2. Salivary '
                            'amylase begins starch digestion in the mouth: starch -> maltose. Both '
                            'are classic NEB enzyme experiments with well-established optima.'
                        ),
                    },
                    {
                        'heading': 'Effect of temperature: optimum and denaturation',
                        'body': (
                            'As temperature rises, kinetic energy increases and enzyme-substrate '
                            'collisions are more frequent and energetic — rate increases up to the '
                            'optimum temperature. For most human enzymes (catalase, amylase) the '
                            'optimum is close to body temperature, approximately 35-40 degrees C.\n\n'
                            'Above the optimum, heat disrupts the weak hydrogen bonds and '
                            'hydrophobic interactions that maintain the enzyme\'s 3D shape. '
                            'The active site loses its precise geometry — denaturation. Unlike '
                            'inhibition, denaturation is usually irreversible: the active site '
                            'no longer fits the substrate, and activity falls to zero. On an '
                            'activity-vs-temperature graph, the curve is asymmetric: gentle '
                            'rise to the optimum, then steep drop as denaturation accelerates.'
                        ),
                    },
                    {
                        'heading': 'Effect of pH and substrate concentration',
                        'body': (
                            'pH affects the ionisation state of amino acid residues in and around '
                            'the active site. At the optimum pH, the charge distribution is ideal '
                            'for substrate binding and catalysis. Above or below optimum pH, '
                            'H+ or OH- ions disrupt ionic bonds and hydrogen bonds, distorting '
                            'the active site. Extreme pH denatures the enzyme permanently. '
                            'Catalase: optimum pH approximately 7.0; amylase: optimum pH approximately 6.7-7.0.\n\n'
                            'The Michaelis-Menten equation describes how rate (v) depends on '
                            'substrate concentration [S]: v = Vmax[S] / (Km + [S]). At low [S], '
                            'rate is proportional to [S] (most active sites are empty). As [S] '
                            'increases, active sites fill and rate approaches Vmax (all active '
                            'sites occupied at any instant). Km (Michaelis constant) is the [S] '
                            'at which v = Vmax/2 — a low Km means high affinity for substrate.'
                        ),
                    },
                ],
                'fun_fact': (
                    'One molecule of catalase can decompose 40 million hydrogen peroxide molecules '
                    'per second — it is one of the fastest enzymes known. Without catalase, H2O2 '
                    'accumulating in your cells would destroy DNA and proteins within hours.'
                ),
                'quiz': [
                    {
                        'q': 'Enzyme activity drops to zero above 60 degrees C because:',
                        'options': [
                            'The substrate evaporates',
                            'The enzyme denatures — heat disrupts bonds holding the active site shape',
                            'pH becomes neutral',
                            'Substrate concentration is too high',
                        ],
                        'answer': 1,
                        'explain': (
                            'High temperatures break the hydrogen bonds and hydrophobic interactions '
                            'that maintain the enzyme\'s tertiary structure. The active site '
                            'loses its complementary shape — this is irreversible denaturation.'
                        ),
                    },
                    {
                        'q': 'At Vmax in a Michaelis-Menten curve:',
                        'options': [
                            'All substrate molecules are occupied',
                            'All active sites are occupied at any instant — adding more substrate cannot increase rate',
                            'The enzyme is denatured',
                            'Temperature is at its optimum',
                        ],
                        'answer': 1,
                        'explain': (
                            'Vmax is reached when every enzyme active site is already processing a '
                            'substrate molecule. More substrate molecules are simply queuing — '
                            'the enzyme is the bottleneck.'
                        ),
                    },
                    {
                        'q': 'Salivary amylase works best at about pH 6.8 and stops working in the stomach (pH 2). This is because:',
                        'options': [
                            'Substrate runs out in the stomach',
                            'The very low pH denatures amylase by disrupting its active site shape',
                            'Amylase is absorbed into the bloodstream',
                            'Temperature in the stomach is too high',
                        ],
                        'answer': 1,
                        'explain': (
                            'Gastric acid (pH approximately 2) completely disrupts the ionic bonds and hydrogen '
                            'bonds maintaining amylase\'s active site. The denatured enzyme cannot '
                            'bind starch, so digestion of starch pauses until pancreatic amylase '
                            '(which works at pH approximately 7) takes over in the small intestine.'
                        ),
                    },
                ],
            },
        ],
    },
    {
        'slug': 'living-world-explorer',
        'title': 'Living World Explorer',
        'category': 'biology',
        'age_range': '9-13',
        'level': 'Beginner',
        'icon': 'pets',
        'color': '#22c55e',
        'tagline': 'Grow plants, build food chains, watch butterflies hatch and discover the science of living things!',
        'description': (
            'The living world is everywhere — in every leaf, every bubble of oxygen and every '
            'creature that breathes. In this course you get a virtual garden of biology: spin '
            'a 3D plant and click its roots and flowers, tour your own organs, drag organisms '
            'into food chains, watch a butterfly hatch from a chrysalis, tune sunlight and '
            'water to grow your own plant, and sort creatures into the animal kingdom. '
            'Everything is real science, explained for curious 9-to-13-year-olds.'
        ),
        'skills': [
            'Parts of a plant and their jobs',
            'Major human organ systems',
            'Food chains, energy flow and trophic levels',
            'Complete and incomplete metamorphosis',
            'Photosynthesis in simple terms',
            'Classifying living things by key traits',
        ],
        'lessons': [
            {
                'slug': 'plant-parts',
                'title': 'Explore a 3D Plant',
                'icon': 'local_florist',
                'minutes': 12,
                'sim': 'biology/plant-parts',
                'sim_type': '3d',
                'summary': (
                    'Spin a 3D plant and click its roots, stem, leaves and flower to discover '
                    'what each part does. Learn why roots soak up water, why leaves are green '
                    'and what flowers are really for.'
                ),
                'objectives': [
                    'Name the four main parts of a flowering plant',
                    'Describe the job of each part: roots (anchor, absorb), stem (support, transport), leaves (photosynthesis), flower (reproduction)',
                    'Explain why leaves are green (chlorophyll)',
                    'Describe how water moves from roots to leaves',
                ],
                'knowledge': [
                    {
                        'heading': 'Roots: the hidden workers',
                        'body': (
                            'Roots grow underground and do two vital jobs: they anchor the plant '
                            'firmly in the soil so wind cannot blow it over, and they absorb water '
                            'and dissolved minerals from the soil. They do this through millions of '
                            'tiny root hairs — each one is a single cell with a long finger-like '
                            'extension that pokes between soil particles.\n\n'
                            'Root hairs give the roots a huge surface area — like unrolling a piece '
                            'of carpet. Water enters by osmosis (moving from where there is lots '
                            'of water in the wet soil to where there is less water inside the root). '
                            'Some plants also store food in their roots — carrots, radishes and '
                            'cassava are all swollen food-storage roots.'
                        ),
                    },
                    {
                        'heading': 'Stem, leaves and flowers',
                        'body': (
                            'The stem holds the plant upright — like a skeleton — and acts as a '
                            'two-way motorway. Water and minerals travel upwards from the roots '
                            'through thin tubes called xylem vessels. Sugary food (made in the '
                            'leaves) travels downwards (and to all parts of the plant) through '
                            'phloem tubes. In trees, the woody trunk is basically a giant stem.\n\n'
                            'Leaves are the food factories. They contain a green pigment called '
                            'chlorophyll, which captures energy from sunlight. Leaves use that '
                            'energy to combine carbon dioxide from the air and water from the soil '
                            'to make glucose sugar — this process is called photosynthesis. '
                            'Flowers attract insects and birds with bright colours and nectar. '
                            'When pollen is carried from one flower to another (pollination), seeds '
                            'form inside the flower. Seeds grow into new plants — that is how '
                            'flowering plants reproduce.'
                        ),
                    },
                    {
                        'heading': 'How plants are like tiny machines',
                        'body': (
                            'Think of a plant as a solar-powered food factory. The leaves collect '
                            'solar energy. The roots collect water and minerals. The stem pipes '
                            'everything to where it is needed. The flowers make seeds for new '
                            'plants. Each part does one or two specific jobs that keep the whole '
                            'plant alive — just like how your heart, lungs and stomach each have '
                            'their own jobs in your body.\n\n'
                            'In Nepal you can see this beautifully in rice plants: long roots grip '
                            'the flooded paddy soil, the hollow stem keeps the leaves above water, '
                            'and the grain (the seed) is the result of the flower being pollinated '
                            'by wind. Every bowl of dal bhat started as a rice plant doing all four '
                            'of these jobs perfectly!'
                        ),
                    },
                ],
                'fun_fact': (
                    'The world\'s largest flower is the Rafflesia arnoldii from Southeast Asia — '
                    'it grows up to 1 metre wide and weighs up to 11 kg. But it has no roots, '
                    'stem or leaves at all — it is entirely a parasite living inside another plant!'
                ),
                'quiz': [
                    {
                        'q': 'What is the main job of a plant\'s roots?',
                        'options': [
                            'Make food from sunlight',
                            'Attract insects',
                            'Anchor the plant and absorb water and minerals',
                            'Carry food down to the soil',
                        ],
                        'answer': 2,
                        'explain': (
                            'Roots anchor the plant so it does not fall over, and their root hairs '
                            'absorb water and minerals from the soil by osmosis.'
                        ),
                    },
                    {
                        'q': 'Leaves are green because they contain:',
                        'options': ['Sugar', 'Chlorophyll', 'Water', 'Starch'],
                        'answer': 1,
                        'explain': (
                            'Chlorophyll is the green pigment in leaf cells that captures light '
                            'energy for photosynthesis. It absorbs red and blue light but reflects '
                            'green light — which is what we see.'
                        ),
                    },
                    {
                        'q': 'Water travels from roots to leaves through which tubes?',
                        'options': ['Phloem', 'Xylem', 'Root hairs', 'Stomata'],
                        'answer': 1,
                        'explain': (
                            'Xylem vessels carry water (and dissolved minerals) upward from roots '
                            'to leaves. Phloem carries dissolved sugar food down from the leaves.'
                        ),
                    },
                ],
            },
            {
                'slug': 'human-body-systems',
                'title': 'Human Body Systems',
                'icon': 'accessibility_new',
                'minutes': 14,
                'sim': 'biology/human-body-systems',
                'sim_type': '2d',
                'summary': (
                    'Tour four major organ systems — digestive, circulatory, respiratory and '
                    'skeletal. Click any organ on the diagram to read what it does. Switch '
                    'between systems using the panel buttons.'
                ),
                'objectives': [
                    'Name the main organs in the digestive, circulatory, respiratory and skeletal systems',
                    'Describe the job of the heart, lungs, stomach, small intestine and femur',
                    'Explain why the body has different organ systems working together',
                    'Describe how food is broken down from mouth to small intestine',
                ],
                'knowledge': [
                    {
                        'heading': 'The digestive system: turning food into fuel',
                        'body': (
                            'Your digestive system breaks down the food you eat into tiny molecules '
                            'small enough to pass into your blood. It starts in the mouth: teeth '
                            'chew food (mechanical digestion) and saliva adds amylase enzyme to '
                            'begin breaking down starch. Food travels down the oesophagus to the '
                            'stomach — a muscular bag that churns food and adds strong acid (pH 2) '
                            'plus pepsin enzyme to digest proteins.\n\n'
                            'The small intestine is where most digestion and ALL absorption happens. '
                            'It is about 6 metres long and packed with tiny finger-like projections '
                            'called villi that massively increase the absorbing surface area. '
                            'Glucose, amino acids and fatty acids cross through the villi wall '
                            'into the blood and lymph. Whatever cannot be absorbed passes into '
                            'the large intestine, where water is reclaimed, and waste leaves as faeces.'
                        ),
                    },
                    {
                        'heading': 'Circulatory and respiratory systems',
                        'body': (
                            'The heart is a double pump: the right side pumps blood to the lungs '
                            'to collect oxygen and drop off carbon dioxide. The left side — which '
                            'is larger and stronger — pumps oxygen-rich blood to the rest of '
                            'the body. The blood travels in arteries (away from heart, carrying O2), '
                            'through tiny capillaries where it delivers O2 and picks up CO2, then '
                            'returns in veins.\n\n'
                            'The lungs have about 300 million tiny air sacs called alveoli, giving '
                            'a total surface area roughly the size of a tennis court. Oxygen '
                            'diffuses from the air in alveoli into the surrounding blood capillaries; '
                            'CO2 moves the other way. Your diaphragm muscle contracts to increase '
                            'chest volume for inhalation; it relaxes for exhalation.'
                        ),
                    },
                    {
                        'heading': 'Skeletal system: the body\'s scaffold',
                        'body': (
                            'Your skeleton has 206 bones and does much more than just hold you up. '
                            'It protects vital organs: the skull guards the brain, the ribcage '
                            'shields the heart and lungs, and the vertebral column protects the '
                            'spinal cord. Bones also work as levers with muscles attached to them, '
                            'enabling movement.\n\n'
                            'Inside large bones like the femur (thigh bone) is red bone marrow — '
                            'the factory where all blood cells are produced. Red blood cells carry '
                            'oxygen, white blood cells fight infection, and platelets help clotting. '
                            'About 2 million new red blood cells are made every second! Bones are '
                            'also the body\'s calcium reservoir — when blood calcium drops, bones '
                            'release calcium ions to keep the level steady.'
                        ),
                    },
                ],
                'fun_fact': (
                    'Your heart beats about 100,000 times every day and pumps roughly 7,600 litres '
                    'of blood — enough to fill a small swimming pool. Over a 70-year lifetime, '
                    'the heart pumps about 200 million litres of blood, and it never once takes a holiday!'
                ),
                'quiz': [
                    {
                        'q': 'Where does most absorption of nutrients happen?',
                        'options': ['Stomach', 'Large intestine', 'Small intestine', 'Mouth'],
                        'answer': 2,
                        'explain': (
                            'The small intestine has villi and microvilli providing a huge '
                            'surface area for absorbing glucose, amino acids and fatty acids '
                            'into the blood and lymph.'
                        ),
                    },
                    {
                        'q': 'The right side of the heart pumps blood:',
                        'options': ['To the whole body', 'To the liver', 'To the lungs to collect oxygen', 'Back to the mouth'],
                        'answer': 2,
                        'explain': (
                            'The right ventricle pumps deoxygenated blood to the lungs via the '
                            'pulmonary arteries. Oxygen is added and CO2 removed, then the '
                            'oxygenated blood returns to the left side of the heart.'
                        ),
                    },
                    {
                        'q': 'Red blood cells are made in:',
                        'options': ['The liver', 'The lungs', 'Bone marrow inside large bones', 'The heart'],
                        'answer': 2,
                        'explain': (
                            'Red bone marrow inside large bones (like the femur and pelvis) '
                            'produces red blood cells, white blood cells and platelets — '
                            'about 2 million new red blood cells every second!'
                        ),
                    },
                ],
            },
            {
                'slug': 'food-chain-builder',
                'title': 'Food Chain Builder',
                'icon': 'link',
                'minutes': 12,
                'sim': 'biology/food-chain-builder',
                'sim_type': '2d',
                'summary': (
                    'Drag organisms from the organism bank into four chain slots to build a '
                    'valid food chain. Energy flows from producer to apex predator. '
                    'Get instant feedback — correct chain turns green, wrong order explains '
                    'the mistake. Score climbs with each correct chain.'
                ),
                'objectives': [
                    'Define producer, primary consumer, secondary consumer and apex predator',
                    'Explain that energy flows from producers to consumers along a food chain',
                    'Describe why only about 10% of energy passes from one trophic level to the next',
                    'Build at least three different valid food chains using the organism bank',
                ],
                'knowledge': [
                    {
                        'heading': 'What is a food chain?',
                        'body': (
                            'A food chain shows who eats who in an ecosystem, and in which direction '
                            'energy flows. It always starts with a PRODUCER — a green plant or alga '
                            'that makes its own food from sunlight by photosynthesis. The arrows in '
                            'a food chain point in the direction of energy flow: Grass → Grasshopper '
                            '→ Frog → Hawk. Each arrow means "is eaten by".\n\n'
                            'Primary consumers (herbivores) eat producers. Secondary consumers eat '
                            'primary consumers. Tertiary or apex consumers are at the top — nothing '
                            'eats them. Each stage in the chain is called a trophic level. Most '
                            'food chains have 3-5 trophic levels; rarely more, because too much '
                            'energy is lost at each step.'
                        ),
                    },
                    {
                        'heading': 'Energy flow and the 10% rule',
                        'body': (
                            'When a grasshopper eats grass, it does not keep all the energy in '
                            'the grass. Most energy is lost as heat from the grasshopper\'s '
                            'respiration (cellular processes that keep it alive and moving), '
                            'some goes into indigestible parts (faeces), and some is used for '
                            'growth. On average, only about 10% of the energy from one trophic '
                            'level passes to the next.\n\n'
                            'This is why food chains rarely have more than five links — by trophic '
                            'level 5, less than 0.01% of the original producer energy remains. '
                            'It is also why eating plants (being vegetarian) feeds more people '
                            'than eating meat: you get the energy directly from level 1 instead '
                            'of waiting for it to be reduced at levels 2, 3 and 4.'
                        ),
                    },
                    {
                        'heading': 'Food webs and decomposers',
                        'body': (
                            'Real ecosystems have food WEBS, not just chains — most animals eat '
                            'several things and are eaten by several predators, creating a '
                            'complex network. A hawk might eat mice, frogs AND snakes, so it '
                            'is connected to many food chains at once.\n\n'
                            'Decomposers (bacteria and fungi) play a crucial but often forgotten '
                            'role: they break down dead plants and animals, returning nutrients '
                            'like nitrogen and phosphorus to the soil so producers can absorb '
                            'them again. Without decomposers, nutrients would be locked up in '
                            'dead bodies forever and new life could not grow. In Nepal\'s forests, '
                            'decomposers recycle vast amounts of fallen leaves every monsoon season.'
                        ),
                    },
                ],
                'fun_fact': (
                    'The shortest possible food chain has just two links: a cow eating grass. '
                    'The longest food chains are in the deep ocean, where some fish feed on '
                    'creatures that feed on creatures that feed on creatures that originally '
                    'ate bacteria at hydrothermal vents — up to eight trophic levels!'
                ),
                'quiz': [
                    {
                        'q': 'In the food chain: Grass → Rabbit → Fox, the Rabbit is a:',
                        'options': ['Producer', 'Primary consumer', 'Secondary consumer', 'Decomposer'],
                        'answer': 1,
                        'explain': (
                            'The rabbit eats grass (the producer), making it a primary consumer '
                            '(herbivore) at trophic level 2.'
                        ),
                    },
                    {
                        'q': 'Why do food chains rarely have more than 5 links?',
                        'options': [
                            'Animals run out of space',
                            'About 90% of energy is lost at each trophic level, leaving too little energy for higher levels',
                            'Predators kill all prey at level 5',
                            'Photosynthesis only supplies 5 levels of energy',
                        ],
                        'answer': 1,
                        'explain': (
                            'Only about 10% of energy passes from one level to the next. After '
                            '5 levels, less than 0.01% of the original energy remains — not '
                            'enough to support another large animal.'
                        ),
                    },
                    {
                        'q': 'Where does the energy in a food chain originally come from?',
                        'options': ['The soil', 'The Sun, captured by producers through photosynthesis', 'Animals eating each other', 'Rain'],
                        'answer': 1,
                        'explain': (
                            'Producers (green plants and algae) convert solar energy into chemical '
                            'energy (glucose) through photosynthesis. This is the ultimate source '
                            'of energy for almost all food chains on Earth.'
                        ),
                    },
                ],
            },
            {
                'slug': 'life-cycle',
                'title': 'Life Cycles — Butterfly & Frog',
                'icon': 'autorenew',
                'minutes': 12,
                'sim': 'biology/life-cycle',
                'sim_type': '2d',
                'summary': (
                    'Click each stage on an interactive wheel to see what happens — egg, '
                    'caterpillar, chrysalis, butterfly for the butterfly; egg (spawn), '
                    'tadpole, froglet, adult frog for the frog. Switch between animals '
                    'and enable auto-advance to watch the cycle.'
                ),
                'objectives': [
                    'List the four stages of butterfly life cycle in the correct order',
                    'List the four stages of frog life cycle in the correct order',
                    'Explain the difference between complete and incomplete metamorphosis',
                    'Describe what happens inside a chrysalis',
                    'Explain why tadpoles have gills but adult frogs have lungs',
                ],
                'knowledge': [
                    {
                        'heading': 'Complete metamorphosis: butterfly',
                        'body': (
                            'Butterflies (and beetles, flies, bees and moths) undergo complete '
                            'metamorphosis (holometabolism) — four completely different-looking '
                            'stages. The female lays eggs on a suitable food plant. A caterpillar '
                            '(larva) hatches and spends its whole life eating — it may grow to '
                            '100 times its hatching size and moult its skin several times.\n\n'
                            'When ready, the caterpillar forms a protective chrysalis (pupa) and '
                            'appears to "sleep" — but inside, a spectacular transformation is '
                            'happening. The caterpillar\'s body is partly broken down into a '
                            'cellular soup, and the cells reorganise into a completely new body '
                            'plan: six legs, four wings, compound eyes, and a proboscis. The '
                            'adult butterfly emerges, pumps its wings full of fluid to expand '
                            'them, then takes flight to find a mate and lay eggs — completing '
                            'the cycle.'
                        ),
                    },
                    {
                        'heading': 'Frog metamorphosis: from gill to lung',
                        'body': (
                            'Frogs lay hundreds of eggs in water, each protected by a jelly coat '
                            'that keeps them together as frogspawn. Tadpoles hatch and are '
                            'essentially aquatic — they breathe through gills, swim with a tail, '
                            'and eat algae and plant matter. As weeks pass, dramatic changes '
                            'happen: first back legs bud out, then front legs; the tail shrinks '
                            'as it is absorbed for energy; gills shrink and lungs develop.\n\n'
                            'The froglet can breathe both in water (through its moist skin, '
                            'which allows gas exchange) and in air (through lungs). The adult '
                            'frog lives on land but must return to water to reproduce — '
                            'connecting the lifecycle to the pond once more. Frogs are '
                            'amphibians: the word means "double life" in Greek, perfectly '
                            'describing their water-and-land existence.'
                        ),
                    },
                    {
                        'heading': 'Why have a metamorphosis?',
                        'body': (
                            'Complete metamorphosis is brilliant evolutionary design: the larva '
                            '(caterpillar or tadpole) and adult are specialised for completely '
                            'different jobs. The larva specialises in EATING and GROWING — '
                            'storing up energy for the transformation. The adult specialises '
                            'in REPRODUCING and DISPERSING — finding mates, laying eggs in '
                            'new locations.\n\n'
                            'This division of labour means larva and adult do not compete for '
                            'the same food. A caterpillar eating leaves does not compete with '
                            'a butterfly drinking nectar. A tadpole eating algae in a pond '
                            'does not compete with an adult frog catching insects on land. '
                            'This is one reason why insects are the most successful animal '
                            'group on Earth — their metamorphosis splits life into perfectly '
                            'specialised phases.'
                        ),
                    },
                ],
                'fun_fact': (
                    'The monarch butterfly migrates up to 4,800 km from Canada to Mexico each '
                    'autumn — and then butterflies that have never been to Mexico somehow '
                    'navigate back to exactly the same forest patches their great-great-grandparents '
                    'used. Scientists still do not fully understand how they do it!'
                ),
                'quiz': [
                    {
                        'q': 'The correct order of butterfly life cycle is:',
                        'options': [
                            'Egg → Adult → Caterpillar → Chrysalis',
                            'Egg → Caterpillar → Chrysalis → Adult butterfly',
                            'Chrysalis → Egg → Caterpillar → Adult',
                            'Caterpillar → Egg → Adult → Chrysalis',
                        ],
                        'answer': 1,
                        'explain': (
                            'Butterfly: egg → caterpillar (larva) → chrysalis (pupa) → adult. '
                            'This complete metamorphosis has four distinct stages.'
                        ),
                    },
                    {
                        'q': 'Why do tadpoles have gills but adult frogs have lungs?',
                        'options': [
                            'Tadpoles are mammals and adults are reptiles',
                            'Tadpoles live entirely in water (need gills), adults live mostly on land (need lungs)',
                            'Lungs cost too much energy to grow when young',
                            'Adult frogs live in water too',
                        ],
                        'answer': 1,
                        'explain': (
                            'Tadpoles are fully aquatic and extract oxygen dissolved in water '
                            'through gills. As they metamorphose, gills are replaced by lungs '
                            'to breathe atmospheric oxygen when living on land.'
                        ),
                    },
                    {
                        'q': 'What happens inside a chrysalis?',
                        'options': [
                            'Nothing — the caterpillar just sleeps',
                            'The caterpillar\'s body is partly broken down and reorganised into an adult butterfly',
                            'The caterpillar eats food stored inside',
                            'Eggs are fertilised',
                        ],
                        'answer': 1,
                        'explain': (
                            'Inside the chrysalis, histolysis breaks down caterpillar tissues '
                            'into a cell-rich fluid, and histogenesis rebuilds the cells into '
                            'wings, legs and adult organs — a complete body plan transformation.'
                        ),
                    },
                ],
            },
            {
                'slug': 'photosynthesis-basics',
                'title': 'Photosynthesis Basics',
                'icon': 'wb_sunny',
                'minutes': 12,
                'sim': 'biology/photosynthesis-basics',
                'sim_type': '2d',
                'summary': (
                    'Tune sunlight and water sliders and watch your plant grow taller, sprout '
                    'more leaves, and release oxygen bubbles. The photosynthesis equation is '
                    'shown at the bottom. Low light or dry conditions stunt growth; '
                    'bright sun and plenty of water make the plant thrive and flower.'
                ),
                'objectives': [
                    'State the word equation and symbol equation for photosynthesis',
                    'Identify the raw materials (CO2 and water) and products (glucose and oxygen)',
                    'Explain the role of chlorophyll in capturing light energy',
                    'Predict how changing light intensity or water supply affects plant growth',
                ],
                'knowledge': [
                    {
                        'heading': 'Photosynthesis: making food from sunlight',
                        'body': (
                            'Photosynthesis is the process by which plants (and some bacteria and '
                            'algae) make their own food using energy from sunlight. The word '
                            '"photosynthesis" comes from Greek: photo = light, synthesis = putting '
                            'together. Plants are called producers because they produce food; '
                            'animals are consumers because they eat that food.\n\n'
                            'The equation is: carbon dioxide + water + light energy → glucose + oxygen, '
                            'or in symbols: 6CO2 + 6H2O + light → C6H12O6 + 6O2. The process '
                            'happens mainly in the leaves, inside tiny organelles called '
                            'chloroplasts. Chloroplasts contain a green pigment called chlorophyll '
                            'that traps light energy — this is why leaves are green.'
                        ),
                    },
                    {
                        'heading': 'What plants need and what they produce',
                        'body': (
                            'Plants need three things for photosynthesis: sunlight (energy), '
                            'water (absorbed by roots from soil), and carbon dioxide (absorbed '
                            'from air through tiny pores in leaves called stomata). They produce '
                            'two things: glucose (sugar used for energy and to build new cells) '
                            'and oxygen (released into the air as a by-product).\n\n'
                            'The oxygen released by plants and algae is what fills our atmosphere. '
                            'Before plants evolved about 2.5 billion years ago, Earth\'s atmosphere '
                            'had almost no free oxygen. Every breath of air you take was made '
                            'possible by photosynthesis. Glucose made by photosynthesis is also '
                            'the starting material for making cellulose (cell walls), starch '
                            '(storage), proteins and fats — photosynthesis ultimately builds '
                            'every part of the plant\'s body.'
                        ),
                    },
                    {
                        'heading': 'How do we know photosynthesis produces oxygen?',
                        'body': (
                            'The easiest way to see photosynthesis happening is to put an '
                            'aquatic plant (like Hydrilla or Elodea) in a bright light and '
                            'watch tiny oxygen bubbles stream from the leaves — this is exactly '
                            'what the NEB Class 11 practical experiments show. The faster the bubbles, '
                            'the faster the photosynthesis rate.\n\n'
                            'You can also show that leaves need light by covering part of a leaf '
                            'with foil for a few days, then testing the whole leaf for starch with '
                            'iodine solution: the covered area turns pale (no starch made, because '
                            'no light), the uncovered area turns blue-black (starch present). '
                            'This classic experiment was first done in 1779 by Jan Ingenhousz, '
                            'who watched underwater plants produce bubbles only when sunlit.'
                        ),
                    },
                ],
                'fun_fact': (
                    'Every atom of carbon in your body was once CO2 in the air that was pulled '
                    'into a plant leaf through photosynthesis. You literally are made of captured '
                    'sunlight and thin air — the plants ate the sunlight first, and then you ate the plants!'
                ),
                'quiz': [
                    {
                        'q': 'What are the two RAW MATERIALS (inputs) needed for photosynthesis?',
                        'options': [
                            'Glucose and oxygen',
                            'Carbon dioxide and water',
                            'Sunlight and chlorophyll',
                            'Oxygen and starch',
                        ],
                        'answer': 1,
                        'explain': (
                            'Photosynthesis combines CO2 (from air) and H2O (from soil) using '
                            'light energy to make glucose and oxygen. CO2 and water are the raw '
                            'materials; glucose and oxygen are the products.'
                        ),
                    },
                    {
                        'q': 'Why does a plant with no sunlight stop growing?',
                        'options': [
                            'It runs out of soil',
                            'It cannot photosynthesize, so it cannot make glucose for energy and growth',
                            'Its roots stop working',
                            'Oxygen disappears',
                        ],
                        'answer': 1,
                        'explain': (
                            'Without light, photosynthesis stops and the plant cannot make glucose. '
                            'Glucose is needed for energy (respiration) and to build new cells. '
                            'The plant uses up its stored starch and eventually stops growing.'
                        ),
                    },
                    {
                        'q': 'Which gas do plants release as a by-product of photosynthesis?',
                        'options': ['Carbon dioxide', 'Nitrogen', 'Oxygen', 'Hydrogen'],
                        'answer': 2,
                        'explain': (
                            'Oxygen is released when water molecules are split during the '
                            'light reactions of photosynthesis. This O2 enters the atmosphere — '
                            'it is what makes Earth\'s air breathable.'
                        ),
                    },
                ],
            },
            {
                'slug': 'classification-sort',
                'title': 'Classification Sort',
                'icon': 'category',
                'minutes': 12,
                'sim': 'biology/classification-sort',
                'sim_type': '2d',
                'summary': (
                    'Drag 15 organisms into five group boxes: mammals, birds, fish, insects '
                    'and plants. Each correct placement gives a fact about the organism. '
                    'Wrong placements give a hint. Score climbs to 15 as you sort all '
                    'organisms correctly.'
                ),
                'objectives': [
                    'State the key features of mammals, birds, fish, insects and plants',
                    'Correctly classify at least 10 familiar organisms into these groups',
                    'Explain what makes an animal a mammal rather than a bird or fish',
                    'Describe why classification is useful in biology',
                ],
                'knowledge': [
                    {
                        'heading': 'Why we classify living things',
                        'body': (
                            'There are estimated to be over 8 million species of living things on '
                            'Earth (many still undiscovered). Without a system to organise them, '
                            'science would be chaos. Classification (taxonomy) groups organisms '
                            'by shared features, which also tells us about their evolutionary '
                            'relationships — animals in the same group share a common ancestor.\n\n'
                            'Carl Linnaeus invented the modern classification system in 1735. '
                            'He used a hierarchy: Kingdom → Phylum → Class → Order → Family → '
                            'Genus → Species. A human is: Animal → Chordate → Mammal → Primate '
                            '→ Hominidae → Homo → sapiens. Every organism has a two-part Latin '
                            'name (binomial nomenclature): genus + species. Humans are Homo sapiens; '
                            'domestic dogs are Canis lupus familiaris.'
                        ),
                    },
                    {
                        'heading': 'Key features of each group',
                        'body': (
                            'MAMMALS: warm-blooded; body covered in fur or hair; breathe with lungs; '
                            'give birth to live young (mostly); females feed offspring with milk. '
                            'Examples: humans, dogs, bats, whales, dolphins.\n\n'
                            'BIRDS: warm-blooded; body covered in feathers; have a beak (no teeth); '
                            'lay hard-shelled eggs; forelimbs are wings (even penguins that cannot fly). '
                            'Examples: eagles, penguins, parrots.\n\n'
                            'FISH: cold-blooded; live in water; breathe through gills; have scales '
                            'and fins; most lay eggs in water. Examples: salmon, shark, goldfish.\n\n'
                            'INSECTS: cold-blooded; 6 legs; body in 3 parts (head, thorax, abdomen); '
                            'exoskeleton; most have antennae; most undergo metamorphosis. Examples: '
                            'ants, bees, butterflies, beetles.\n\n'
                            'PLANTS: make own food by photosynthesis; cell walls of cellulose; '
                            'cannot move from place to place; have roots, stems, leaves.'
                        ),
                    },
                    {
                        'heading': 'Common classification mistakes',
                        'body': (
                            'Bats look like birds because they fly — but they are mammals: they '
                            'have fur, feed pups with milk and give live birth. Whales and dolphins '
                            'live in the sea like fish — but they are mammals: they breathe air '
                            'with lungs, give live birth and feed young with milk.\n\n'
                            'Spiders are NOT insects: spiders are arachnids with 8 legs and '
                            '2 body segments, not 6 legs and 3 body segments. Millipedes and '
                            'centipedes are also not insects — they belong to completely different '
                            'classes. Sharks are fish (cartilaginous fish), not mammals, even though '
                            'some give live birth. Classification is based on a whole set of features, '
                            'not just one — so always check several traits before deciding which '
                            'group an organism belongs to.'
                        ),
                    },
                ],
                'fun_fact': (
                    'Scientists discover about 15,000-20,000 new species every year — mostly '
                    'insects, fungi and plants from tropical forests like those in Nepal\'s '
                    'Terai. Despite centuries of classification, we may have named fewer than '
                    '20% of all species on Earth!'
                ),
                'quiz': [
                    {
                        'q': 'A bat can fly — so it must be a bird, right?',
                        'options': [
                            'Yes, all flying animals are birds',
                            'No — bats are mammals: they have fur and feed their young with milk',
                            'No — bats are insects: they have wings',
                            'Yes, but a very unusual one',
                        ],
                        'answer': 1,
                        'explain': (
                            'Flight evolved independently in bats, birds AND insects. Bats are '
                            'mammals — they have fur, give live birth and produce milk to feed '
                            'their pups. Classification is based on many features, not just flight.'
                        ),
                    },
                    {
                        'q': 'Which feature is shared by ALL insects?',
                        'options': ['Wings', '8 legs', '6 legs and 3 body segments', 'Living in soil'],
                        'answer': 2,
                        'explain': (
                            '6 legs (3 pairs) and 3 body segments (head, thorax, abdomen) are '
                            'the defining features of all insects. Some insects have no wings '
                            '(e.g. worker ants); some live underground, in water, or in trees.'
                        ),
                    },
                    {
                        'q': 'Why is the whale classified as a mammal and not a fish?',
                        'options': [
                            'Whales are too big to be fish',
                            'Whales breathe air with lungs, are warm-blooded, give live birth and feed calves with milk',
                            'Whales do not have scales',
                            'Whales are too intelligent',
                        ],
                        'answer': 1,
                        'explain': (
                            'Whales share all defining mammal features despite living in the sea. '
                            'Fish are cold-blooded, breathe with gills, usually lay eggs and never '
                            'produce milk — whales do none of these things.'
                        ),
                    },
                ],
            },
        ],
    },
]
