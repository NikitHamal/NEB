COURSES = [
    {
        'slug': 'living-world',
        'title': 'The Living World',
        'category': 'biology',
        'age_range': '7-12',
        'level': 'Beginner',
        'icon': 'eco',
        'color': '#84CC16',
        'tagline': 'Open up the human body, breathe with a leaf and watch a caterpillar become a butterfly — all in glowing 3D.',
        'description': 'Biology is the story of living things, and the best way to understand it is to see it move. In this course you will lift the skin off a 3D human body to meet the skeleton and organs, feed sunlight to a leaf and watch it make sugar, follow a butterfly through every stage of its transformation, and pace the heartbeat and breathing of your own body. Every model is built to real proportions, every animation follows real biology — so the wonder you feel here is the wonder of how life actually works.',
        'skills': [
            'Major body systems: skeleton, organs, muscles',
            'How plants make food from sunlight (photosynthesis)',
            'Life cycles and metamorphosis',
            'The heart, lungs and the rhythm of breathing',
            'Thinking like a biologist: observe, compare, explain',
        ],
        'lessons': [
            {
                'slug': 'human-body-explorer',
                'title': 'Human Body Explorer',
                'icon': 'accessibility',
                'minutes': 14,
                'sim': 'biology/human-body',
                'sim_type': '3d',
                'summary': 'Peel back the layers of a 3D human body — skin, muscles, skeleton, organs — and tap each part to discover what it does for you every second of the day.',
                'objectives': [
                    'Name the major body layers: skin, muscle, skeleton, organs',
                    'Locate the heart, lungs, brain, liver and stomach in 3D',
                    'Describe one job each major organ does to keep you alive',
                    'Explain how the skeleton and muscles work together to move you',
                ],
                'knowledge': [
                    {
                        'heading': 'You are built in layers',
                        'body': 'Your body is not one solid lump — it is organised in layers, like a Russian doll. On the outside is the skin, your waterproof, sensing suit and the body\'s largest organ. Just beneath sit the muscles, red ropes that can pull your bones to move you. Deeper still is the skeleton, a frame of 206 bones that holds you up and protects soft parts. Tucked inside that frame are the organs — the heart, lungs, brain and gut — each running a different life-support system.\n\nIn the simulation, drag the layer slider to lift each layer away and reveal the next. You cannot see these layers in a mirror, but they are inside you right now, working together.',
                    },
                    {
                        'heading': 'Organs and their jobs',
                        'body': 'Each organ has a specialty. The heart is a muscular pump the size of your fist, pushing blood around your body about 100,000 times a day. The lungs take in the oxygen every cell needs and breathe out waste carbon dioxide. The brain, wrapped safely in the skull, is the control centre — it processes your senses, stores memories and sends the signals that move your muscles.\n\nThe liver is the body\'s chemical factory, cleaning the blood and helping turn food into energy. The stomach churns food into a soup so the intestines can soak up the goodness. Tap each glowing organ in the 3D model to hear its job — none works alone, and not one could keep you alive by itself.',
                    },
                    {
                        'heading': 'Bones and muscles: a tug-of-war',
                        'body': 'Muscles can only pull, never push — so they work in opposing pairs. To bend your elbow, the biceps on the front of your arm contracts and pulls; to straighten it again, the triceps on the back takes its turn. Your skeleton provides the levers: each muscle is anchored across a joint to two bones, so when it shortens, one bone swings.\n\nYou have more than 600 muscles and 206 bones, and almost every movement you make — walking, writing, blinking — is the result of dozens of these tiny tug-of-wars happening in perfect coordination. The 3D model lets you toggle the skeleton and muscles together to see how they line up.',
                    },
                ],
                'fun_fact': 'When you were born you actually had about 300 bones, but as you grew many of them fused together — leaving the 206 that carry you around today.',
                'quiz': [
                    {
                        'q': 'Which layer of the body is the waterproof outer suit and the body\'s largest organ?',
                        'options': ['The skeleton', 'The skin', 'The muscles', 'The lungs'],
                        'answer': 1,
                        'explain': 'Skin is the outermost layer and the largest organ — it keeps water in, germs out and lets you feel the world.',
                    },
                    {
                        'q': 'Muscles can only pull, never push. So how do you straighten a bent arm?',
                        'options': ['The bones push back', 'A different muscle (the triceps) pulls it straight', 'Gravity always does it', 'The skin shrinks back'],
                        'answer': 1,
                        'explain': 'Muscles work in opposing pairs — the biceps bends the arm, the triceps on the other side straightens it.',
                    },
                    {
                        'q': 'What is the main job of the lungs?',
                        'options': ['Pump blood', 'Digest food', 'Take in oxygen and remove carbon dioxide', 'Send signals to muscles'],
                        'answer': 2,
                        'explain': 'Lungs exchange gases: oxygen goes into your blood, and waste carbon dioxide leaves with each breath out.',
                    },
                ],
            },
            {
                'slug': 'plant-power',
                'title': 'Plant Power: Photosynthesis',
                'icon': 'eco',
                'minutes': 13,
                'sim': 'biology/photosynthesis',
                'sim_type': '3d',
                'summary': 'Feed a 3D leaf with sunlight, water and carbon dioxide and watch the green chloroplasts turn them into sugar and the oxygen you breathe.',
                'objectives': [
                    'State the three inputs of photosynthesis: light, water, carbon dioxide',
                    'Name the two products: glucose (sugar) and oxygen',
                    'Explain why leaves are green and where chlorophyll lives',
                    'Connect photosynthesis to the oxygen in every breath you take',
                ],
                'knowledge': [
                    {
                        'heading': 'A leaf is a tiny factory',
                        'body': 'Plants are extraordinary: unlike animals, they can make their own food out of thin air, water and sunlight. The process is called photosynthesis, and it happens inside the leaf in tiny green structures called chloroplasts. The recipe, written as a chemical shorthand, is: carbon dioxide + water + light energy → glucose + oxygen.\n\nIn the simulation you can drag the three ingredients into a leaf and watch green chloroplasts light up as they assemble sugar molecules, releasing oxygen as a gift to the rest of the planet. Without photosynthesis there would be no food chain and no oxygen to breathe — plants literally feed the world.',
                    },
                    {
                        'heading': 'Why are leaves green?',
                        'body': 'Leaves look green because of a pigment called chlorophyll, packed inside those chloroplasts. Chlorophyll\'s superpower is that it is brilliant at soaking up red and blue light from the sun — but it reflects green light straight back, which is why that is the colour your eyes see.\n\nThe energy chlorophyll captures is what powers the whole sugar-making reaction. When autumn comes and a tree reclaims the chlorophyll from its leaves, the hidden yellow and orange pigments that were there all along finally show through. So a leaf\'s green is really the light it could not use.',
                    },
                    {
                        'heading': 'The oxygen you breathe',
                        'body': 'Animals and humans breathe in oxygen and breathe out carbon dioxide. Plants do something beautifully complementary: they take in that carbon dioxide, use the carbon to build sugar, and release the oxygen right back. A single large tree can supply a day\'s oxygen for four people.\n\nThis is why forests are sometimes called the lungs of the Earth — and why cutting them down is dangerous for everyone who breathes. Almost every molecule of oxygen in the air was made by a plant, an alga, or a tiny organism in the ocean called phytoplankton, all running the same photosynthesis reaction.',
                    },
                ],
                'fun_fact': 'Roughly half the oxygen in Earth\'s atmosphere comes not from forests but from microscopic phytoplankton drifting in the oceans — creatures far too small to see without a microscope.',
                'quiz': [
                    {
                        'q': 'What are the three inputs a plant needs for photosynthesis?',
                        'options': ['Soil, worms and rain', 'Light, water and carbon dioxide', 'Sugar, oxygen and salt', 'Heat, wind and soil'],
                        'answer': 1,
                        'explain': 'Photosynthesis turns light energy, water and CO₂ into glucose and oxygen inside the chloroplasts.',
                    },
                    {
                        'q': 'Why do leaves look green to our eyes?',
                        'options': ['They contain green blood', 'Chlorophyll absorbs red and blue light and reflects green', 'They reflect all colours', 'Water inside them is green'],
                        'answer': 1,
                        'explain': 'Chlorophyll soaks up the red and blue light it needs and bounces green light away — that reflected green reaches your eyes.',
                    },
                    {
                        'q': 'What useful gas does a plant release as a result of photosynthesis?',
                        'options': ['Carbon dioxide', 'Nitrogen', 'Oxygen', 'Methane'],
                        'answer': 2,
                        'explain': 'Plants split water to take its hydrogen for sugar, and the leftover oxygen is released — the very gas we breathe.',
                    },
                ],
            },
            {
                'slug': 'become-a-butterfly',
                'title': 'Become a Butterfly',
                'icon': 'flutter_dash',
                'minutes': 12,
                'sim': 'biology/butterfly-life-cycle',
                'sim_type': '3d',
                'summary': 'Spin a 3D model through every stage of a butterfly\'s life — egg, caterpillar, chrysalis and adult — and watch one of nature\'s greatest transformations.',
                'objectives': [
                    'Name the four stages of complete metamorphosis in order',
                    'Describe what happens inside a chrysalis',
                    'Explain why a caterpillar eats so much and an adult butterfly sips nectar',
                    'Compare complete and incomplete metamorphosis',
                ],
                'knowledge': [
                    {
                        'heading': 'Four stages of a miracle',
                        'body': 'A butterfly does not grow up the way you do, getting gradually bigger. Instead it passes through four completely different bodies — a transformation called complete metamorphosis. It begins as a tiny egg glued to a leaf by the mother butterfly. Out of the egg hatches a caterpillar (the larva), whose only job is to eat. The caterpillar stuffs itself with leaves and grows astonishingly fast, shedding its skin several times as it outgrows it.\n\nWhen fully grown, the caterpillar attaches itself to a twig and transforms into a chrysalis (the pupa) — the quiet, magical stage. Finally, the adult butterfly emerges, dries its wings and flies off to find a mate and lay the next generation of eggs. The whole cycle is one animal wearing four completely different outfits.',
                    },
                    {
                        'heading': 'Inside the chrysalis',
                        'body': 'The chrysalis looks still from the outside, but inside it is a rebuild like no other in nature. The caterpillar releases enzymes that digest much of its own body into a kind of nutrient soup, and from that soup special cells called imaginal discs grow the butterfly\'s wings, legs, antennae and eyes.\n\nSo radical is this change that the adult butterfly has almost nothing in common with the caterpillar except its DNA. It does not even eat the same food: the caterpillar chewed leaves with powerful jaws, while the butterfly sips liquid nectar through a long tube called a proboscis. Drag the stage slider in the simulation and watch the body reshape itself.',
                    },
                    {
                        'heading': 'Eat now, fly later',
                        'body': 'Every stage of the life cycle has a different purpose. The egg is for protection and the start of growth. The caterpillar is an eating machine — it can grow to 100 times its birth weight in just two weeks, storing energy for the transformation ahead. The chrysalis is a rebuilding phase, where that stored fuel powers the construction of wings. The adult butterfly is the reproductive stage, whose job is to find a mate and lay eggs on the right kind of plant.\n\nNot all insects transform this completely. Grasshoppers and dragonflies use incomplete metamorphosis: they hatch as miniature wingless adults and simply grow bigger, molting their skin each time. Complete metamorphosis is more dramatic, but it lets the young and adult use completely different foods and habitats without competing.',
                    },
                ],
                'fun_fact': 'A monarch butterfly can migrate up to 4,000 km across North America to a forest in Mexico it has never seen — and no individual makes the trip twice, so the route is somehow carried in its genes.',
                'quiz': [
                    {
                        'q': 'What is the correct order of a butterfly\'s complete metamorphosis?',
                        'options': ['Egg → adult → caterpillar → chrysalis', 'Egg → caterpillar → chrysalis → adult', 'Caterpillar → egg → adult → chrysalis', 'Adult → chrysalis → caterpillar → egg'],
                        'answer': 1,
                        'explain': 'Egg hatches into a caterpillar, which becomes a chrysalis, from which the adult butterfly finally emerges.',
                    },
                    {
                        'q': 'What is the main job of the caterpillar stage?',
                        'options': ['To lay eggs', 'To fly and find a mate', 'To eat and store energy', 'To make honey'],
                        'answer': 2,
                        'explain': 'The caterpillar is an eating machine, growing rapidly and storing the fuel the chrysalis will need to build wings.',
                    },
                    {
                        'q': 'Inside the chrysalis, the caterpillar\'s body is mostly…',
                        'options': ['Asleep and unchanged', 'Broken down into a soup and rebuilt into a butterfly', 'Frozen solid', 'Growing leaves'],
                        'answer': 1,
                        'explain': 'Enzymes digest the caterpillar into a nutrient soup, from which imaginal discs rebuild the wings, legs and eyes of the adult.',
                    },
                ],
            },
            {
                'slug': 'heart-and-lungs',
                'title': 'Heart & Lungs',
                'icon': 'favorite',
                'minutes': 13,
                'sim': 'biology/heart-lungs',
                'sim_type': '3d',
                'summary': 'Watch a 3D heart beat and lungs breathe in real time — turn up the activity and see how fast your body pumps when you run.',
                'objectives': [
                    'Trace the path of blood through the heart and lungs',
                    'Explain why heart rate and breathing rate rise during exercise',
                    'Describe the roles of arteries and veins',
                    'Connect oxygen delivery to every cell in the body',
                ],
                'knowledge': [
                    {
                        'heading': 'A pump that never rests',
                        'body': 'Your heart is a hollow muscular pump about the size of your fist, tucked slightly left of the centre of your chest. It has four chambers: two upper atria that receive blood, and two lower ventricles that pump it out. The right side pumps blood to the lungs to collect oxygen; the left side pumps that oxygen-rich blood out to the rest of the body.\n\nIn one day your heart beats around 100,000 times, moving about 7,000 litres of blood through a network of vessels that, laid end to end, would wrap around the Earth more than twice. The simulation lets you see each chamber squeeze in sequence and watch blood (shown red when oxygen-rich, blue when oxygen-poor) circulate.',
                    },
                    {
                        'heading': 'Breathe in, breathe out',
                        'body': 'The lungs sit either side of the heart, protected by the ribcage. When you breathe in, your diaphragm pulls down and your ribcage expands, sucking air deep into branching tubes that end in millions of tiny air sacs called alveoli. Each alveolus is wrapped in blood vessels so thin that oxygen slips across into the blood, and waste carbon dioxide slips back out to be breathed away.\n\nYou have so many alveoli that, unfolded, their surface would cover roughly half a tennis court — giving your blood a huge area to swap gases. The simulation paces the breathing animation; raise the activity slider and watch both breathing and heartbeat quicken together.',
                    },
                    {
                        'heading': 'Why exercise makes you puff',
                        'body': 'When you run or play hard, your muscles burn glucose for energy far faster — and to do that they need more oxygen and produce more carbon dioxide. Your body detects this and responds on two fronts at once: the heart beats faster to push more blood around each minute, and your breathing speeds up to swap the gases more quickly.\n\nThat is why a resting heart rate of around 70 beats per minute can leap past 150 during hard exercise, and your breaths climb from about 12 a minute to over 40. Athletes train their hearts and lungs so they can deliver oxygen efficiently even at these high rates — which is why regular exercise leaves you less out of breath over time.',
                    },
                ],
                'fun_fact': 'Your heart has its own built-in electrical pacemaker, a patch of cells called the SA node, which fires about once a second even if all nerves to the heart are cut — keeping it beating in a dish.',
                'quiz': [
                    {
                        'q': 'The right side of the heart pumps blood to the…',
                        'options': ['Whole body', 'Lungs, to collect oxygen', 'Brain only', 'Stomach'],
                        'answer': 1,
                        'explain': 'The right side sends oxygen-poor blood to the lungs; the left side then pumps the oxygen-rich blood out to the body.',
                    },
                    {
                        'q': 'Where does oxygen actually enter your blood?',
                        'options': ['In the windpipe', 'In the tiny air sacs called alveoli', 'In the heart', 'In the nose only'],
                        'answer': 1,
                        'explain': 'Alveoli have walls just one cell thick, wrapped in blood vessels, so oxygen diffuses into the blood and CO₂ diffuses out.',
                    },
                    {
                        'q': 'When you run, your heart rate and breathing rate both rise because your muscles need more…',
                        'options': ['Water', 'Oxygen to release energy from glucose', 'Salt', 'Sugar to taste sweet'],
                        'answer': 1,
                        'explain': 'Hard-working muscles burn glucose faster, demanding more oxygen and producing more CO₂ — so the heart and lungs both speed up.',
                    },
                ],
            },
        ],
    },
    {
        'slug': 'neb-biology-practical-11-12',
        'title': 'NEB Biology Practicals — Class 11 & 12',
        'category': 'biology',
        'age_range': '16-18',
        'level': 'Intermediate',
        'icon': 'biotech',
        'color': '#65A30D',
        'tagline': 'Every core NEB biology practical as a working virtual lab — focus the microscope, stain the slide and record your observations like a real biologist.',
        'description': 'This course walks you through the essential NEB Class 11 and 12 biology practicals, each as a realistic virtual lab you can run again and again. Peer through a virtual microscope at dividing cells in an onion root tip and classify the mitotic stages, prepare a leaf peel to count and measure stomata, dissect and label a flower, and run the standard biochemical food tests for starch, sugar, protein and fat. Every step — focusing, staining, observing, tabulating — mirrors what you will do in the school lab and the board practical exam, and every observation matches the standard NEB lab manual.',
        'skills': [
            'Using a compound microscope and preparing temporary slides',
            'Identifying stages of mitosis in onion root tip cells',
            'Counting and measuring stomata in leaf peels',
            'Dissecting and labelling the parts of a flower',
            'Performing biochemical food tests and interpreting colours',
        ],
        'lessons': [
            {
                'slug': 'onion-root-tip-mitosis',
                'title': 'Onion Root Tip — Mitosis',
                'icon': 'biotech',
                'minutes': 18,
                'sim': 'biology/onion-mitosis',
                'sim_type': 'lab',
                'summary': 'Focus a virtual microscope on a stained onion root tip, scan cells and classify each as interphase, prophase, metaphase, anaphase or telophase — then count and compute the mitotic index.',
                'objectives': [
                    'Prepare and focus a temporary slide of an onion root tip',
                    'Identify the phases of mitosis by visible features',
                    'Count cells in each phase and present results in a table',
                    'Compute the mitotic index and explain what it tells you',
                ],
                'knowledge': [
                    {
                        'heading': 'Why the root tip?',
                        'body': 'A plant grows at its tips because the cells there are actively dividing. The very end of a root is called the region of cell division (the meristem), and a high proportion of its cells are caught mid-division in mitosis. That makes the onion root tip the classic preparation for studying mitosis under the microscope.\n\nTo make the dividing cells visible you fix the root in a stain — commonly acetocarmine or aceto-orcein — that darkens the chromosomes. You then squash the tissue gently so the cells spread into a single layer, allowing you to see each one clearly. The simulation walks you through focusing the microscope; the real skill is learning to recognise each phase by its chromosomes.',
                    },
                    {
                        'heading': 'Reading the phases',
                        'body': 'Most cells you see will be in interphase — the long growing phase between divisions — where the nucleus looks grainy and intact, with no obvious individual chromosomes. The rest are in one of four mitotic phases. In prophase the chromosomes condense and appear as distinct threads, while the nuclear membrane fades. In metaphase the chromosomes line up neatly across the middle (the equator) of the cell.\n\nIn anaphase the chromosomes split and the two halves are dragged to opposite poles, looking like two V-shapes pointing in. In telophase two new nuclei form at the ends and the cell pinches in the middle to divide. Scan the root tip in the simulation, tap a cell and use the labelled diagrams to classify each one.',
                    },
                    {
                        'heading': 'Counting and the mitotic index',
                        'body': 'After scanning, you tally the cells you saw in each phase and present the counts in a table. The number of cells in a phase is roughly proportional to how long that phase lasts — interphase is the longest, so the majority of cells will be in it; anaphase is short, so it is rare.\n\nThe mitotic index expresses the fraction of cells actively dividing: mitotic index = (cells in prophase + metaphase + anaphase + telophase) ÷ total cells counted × 100%. For an onion root tip it is typically around 5–10%. A high mitotic index signals rapid growth (or, in a clinical setting, possible cancer); a low one indicates slow tissue renewal. Always count several fields of view and average to reduce sampling error.',
                    },
                ],
                'fun_fact': 'Cancer is essentially mitosis out of control — a tumour is a mass of cells that refuse to stop dividing, which is why the same microscope technique used on your onion slide is also used by pathologists to grade tumours.',
                'quiz': [
                    {
                        'q': 'In which phase do chromosomes line up along the equator of the cell?',
                        'options': ['Prophase', 'Metaphase', 'Anaphase', 'Telophase'],
                        'answer': 1,
                        'explain': 'Meta- means "middle": in metaphase the condensed chromosomes align at the cell equator before being pulled apart.',
                    },
                    {
                        'q': 'Why are most cells you observe in interphase, not mitosis?',
                        'options': ['Interphase is the longest part of the cell cycle', 'Cells hide during mitosis', 'Interphase cells are bigger', 'The stain only colours interphase'],
                        'answer': 0,
                        'explain': 'Interphase lasts far longer than all the mitotic phases combined, so a random snapshot catches most cells there.',
                    },
                    {
                        'q': 'The mitotic index is best defined as…',
                        'options': ['Cells in interphase ÷ total cells', 'Dividing cells ÷ total cells × 100%', 'Total cells × mitosis time', 'Number of chromosomes'],
                        'answer': 1,
                        'explain': 'Mitotic index = cells in mitosis ÷ total cells × 100% — a measure of how actively a tissue is dividing.',
                    },
                    {
                        'q': 'A student finds an unusually high mitotic index in an animal tissue. A possible concern is…',
                        'options': ['The tissue is dead', 'Rapid, possibly uncontrolled cell division (e.g. a tumour)', 'The cells have no nucleus', 'Nothing — it is always normal'],
                        'answer': 1,
                        'explain': 'A high mitotic index can indicate rapid growth; in animals, abnormally high division is a hallmark of cancerous tissue.',
                    },
                ],
            },
            {
                'slug': 'leaf-peel-stomata',
                'title': 'Leaf Peel — Stomata',
                'icon': 'nature',
                'minutes': 15,
                'sim': 'biology/leaf-stomata',
                'sim_type': 'lab',
                'summary': 'Tear a thin peel from a leaf, stain it and focus the microscope to count the stomata and measure the guard cells — comparing upper and lower surfaces.',
                'objectives': [
                    'Prepare a temporary mount of a leaf peel',
                    'Identify stomata, guard cells and epidermal cells',
                    'Count stomata per field of view and estimate density',
                    'Compare stomatal density on upper and lower leaf surfaces',
                ],
                'knowledge': [
                    {
                        'heading': 'What stomata do',
                        'body': 'A leaf is covered in a waxy skin called the epidermis, and scattered across it are thousands of tiny pores called stomata (singular: stoma). Each stoma is a slit between two bean-shaped guard cells that can swell to open the pore or shrink to close it. Open stomata let carbon dioxide flow in for photosynthesis, but they also let water vapour escape — so the plant must balance gas exchange against water loss.\n\nThis is why most plants keep their stomata wide open in the morning when there is light to photosynthesise, and close them at night or in drought to save water. The leaf peel you prepare in the simulation lets you see these pores directly — they look like tiny pairs of green lips.',
                    },
                    {
                        'heading': 'Preparing the slide',
                        'body': 'To see stomata you need a single transparent layer of cells, not a whole leaf. The classic method is to tear a leaf so that a thin film of the lower epidermis peels away — on many leaves this layer comes off like cling film. Float the peel on a drop of water on a slide, add a drop of stain (safranin gives good contrast), lower a cover slip at an angle to avoid air bubbles, and blot gently.\n\nUnder the microscope at 40× to 100× you will see the jigsaw-puzzle epidermal cells and, scattered among them, the pairs of guard cells with the dark stoma between them. The simulation lets you focus through the layers just as you would on a real slide.',
                    },
                    {
                        'heading': 'Counting and comparing',
                        'body': 'To estimate stomatal density, count the stomata in a known field of view and convert to number per square millimetre (the area is fixed by your microscope\'s magnification). A typical leaf has 100–300 stomata per mm² on its lower surface — far more than on the upper surface, because hiding most stomata underneath cuts water loss in direct sun.\n\nThis upper-versus-lower comparison is itself a classic NEB question. Water lilies, which float on water, have stomata only on their upper surface; cacti have very few stomata buried deep in the tissue. The number and position of stomata tells you a great deal about the environment a plant evolved in. Count both surfaces in the simulation and compare your numbers.',
                    },
                ],
                'fun_fact': 'A single wheat leaf can carry more than 20 million stomata — yet each individual pore opens and closes its own microscopic door, every single day, in step with the sun.',
                'quiz': [
                    {
                        'q': 'Each stoma is formed by a pair of cells called…',
                        'options': ['Red blood cells', 'Guard cells', 'Nerve cells', 'Root cells'],
                        'answer': 1,
                        'explain': 'Two bean-shaped guard cells flank each pore; they swell to open the stoma and shrink to close it.',
                    },
                    {
                        'q': 'Why do most land plants have more stomata on the LOWER surface of the leaf?',
                        'options': ['The lower surface is greener', 'To reduce water loss in direct sunlight', 'Stomata cannot form on top', 'Insects eat the top'],
                        'answer': 1,
                        'explain': 'Hiding most stomata underneath, out of direct sun and heat, lets the plant trade gases while limiting water loss.',
                    },
                    {
                        'q': 'Stomata close at night primarily because…',
                        'options': ['The plant is sleeping', 'There is no light for photosynthesis, so CO₂ is not needed and water can be saved', 'They freeze', 'Guard cells die'],
                        'answer': 1,
                        'explain': 'With no light, photosynthesis stops, so the plant closes its stomata to conserve water until dawn.',
                    },
                ],
            },
            {
                'slug': 'flower-dissection',
                'title': 'Flower Dissection',
                'icon': 'local_florist',
                'minutes': 14,
                'sim': 'biology/flower-dissection',
                'sim_type': '3d',
                'summary': 'Dissect and label a 3D Hibiscus flower — peel back the calyx, corolla, androecium and gynoecium and learn what each whorl does.',
                'objectives': [
                    'Identify the four floral whorls: calyx, corolla, androecium, gynoecium',
                    'Locate the male parts (stamen: anther + filament) and female parts (carpel)',
                    'Trace the path of pollen from anther to stigma during pollination',
                    'Explain how a flower becomes a fruit and seeds',
                ],
                'knowledge': [
                    {
                        'heading': 'A flower in four rings',
                        'body': 'A typical flower like Hibiscus or Datura is built from four concentric whorls, like layers of an onion, attached to a swollen base called the thalamus. From outside in, they are the calyx (the green sepals), the corolla (the colourful petals), the androecium (the male parts) and the gynoecium (the female parts). The outer two protect and advertise; the inner two do the actual reproduction.\n\nIn the 3D model you can peel each whorl away to reveal the next. Sepals are usually green and leaf-like, and they protect the bud before it opens. Petals are the bright, often scented flags whose job is to attract pollinators — bees, butterflies and birds drawn by colour and nectar.',
                    },
                    {
                        'heading': 'Male and female',
                        'body': 'The androecium is the male whorl, made of stamens. Each stamen has a thin stalk called the filament topped by an anther — a small box that produces the dust-like pollen grains, each carrying the male sex cells. The gynoecium, at the very centre, is the female whorl, made of one or more carpels. A carpel has three parts: a sticky top called the stigma that catches pollen, a slender tube called the style, and a swollen base called the ovary.\n\nInside the ovary sit the ovules — tiny structures that will become seeds if fertilised. When a grain of pollen lands on the stigma, it grows a tube down the style and into the ovary, where the male cell fuses with an ovule. That fusion is fertilisation. Drag pollen onto the stigma in the simulation to watch the journey begin.',
                    },
                    {
                        'heading': 'From flower to fruit',
                        'body': 'After fertilisation the flower changes utterly. The petals and stamens wither and fall, their jobs done. The ovary swells and its wall thickens to become a fruit, while each fertilised ovule inside becomes a seed. An apple, a mango and a tomato are all swollen ovaries; the pips inside are the seeds, each a tiny plant embryo with its own food store waiting to germinate.\n\nThis is why flowers exist at all: they are the reproductive structures that turn plants\' genetic material into seeds wrapped in fruit, ready to be carried away by wind, water or animal. A flower is, in effect, a plant\'s way of making the next generation — and dissection shows you the machinery up close.',
                    },
                ],
                'fun_fact': 'The world\'s largest single flower, Rafflesia, grows up to a metre across and smells like rotting meat — to attract the flies that pollinate it.',
                'quiz': [
                    {
                        'q': 'Which floral whorl is made of colourful petals?',
                        'options': ['Calyx', 'Corolla', 'Androecium', 'Gynoecium'],
                        'answer': 1,
                        'explain': 'The corolla is the whorl of petals; the calyx is the green sepals outside it.',
                    },
                    {
                        'q': 'The male part of a flower, the stamen, consists of…',
                        'options': ['Stigma and style', 'Anther and filament', 'Ovary and ovules', 'Sepals and petals'],
                        'answer': 1,
                        'explain': 'Each stamen has a stalk (filament) bearing an anther, which produces pollen containing male sex cells.',
                    },
                    {
                        'q': 'After fertilisation, the ovary of a flower develops into a…',
                        'options': ['Root', 'Fruit', 'Leaf', 'Stem'],
                        'answer': 1,
                        'explain': 'The ovary wall thickens and ripens into a fruit, while the ovules inside become seeds.',
                    },
                ],
            },
            {
                'slug': 'food-tests',
                'title': 'Food Tests — Starch, Sugar, Protein, Fat',
                'icon': 'science',
                'minutes': 16,
                'sim': 'biology/food-test',
                'sim_type': 'lab',
                'summary': 'Run the four classic biochemical food tests on everyday samples — iodine for starch, Benedict\'s for sugar, biuret for protein and the spot test for fat — and read the colour changes.',
                'objectives': [
                    'Perform the iodine test for starch and read the colour',
                    'Perform Benedict\'s test for reducing sugar with heat',
                    'Perform the biuret test for protein',
                    'Perform the ethanol/emulsion or spot test for fats',
                ],
                'knowledge': [
                    {
                        'heading': 'Why we test foods',
                        'body': 'The food on your plate is a mixture of biological molecules — chiefly carbohydrates, proteins and fats — and each leaves a characteristic chemical signature when treated with the right reagent. Biochemical food tests let you find out which nutrients a sample contains without tasting it, which matters both in nutrition and in identifying unknown substances in a lab.\n\nFour tests cover the major nutrients: iodine solution turns blue-black in the presence of starch; Benedict\'s solution turns from blue to green, yellow, orange or brick-red with reducing sugars when heated; biuret reagent turns from blue to violet in the presence of protein; and fats leave a translucent spot on paper or form a cloudy emulsion in ethanol. The simulation lets you add each reagent to a range of foods and watch the colour change.',
                    },
                    {
                        'heading': 'Reading the colours',
                        'body': 'Each test works by a specific chemical reaction, but for practical purposes what you need is the colour key. Iodine: yellow-brown → blue-black means starch is present (potato, rice, bread). Benedict\'s: blue → green (trace), yellow (low), orange (moderate) or brick-red (high) sugar; the more sugar, the stronger the colour, so Benedict\'s is semi-quantitative.\n\nBiuret: blue → purple or violet means protein is present (egg white, milk, meat). For fats, the ethanol emulsion test gives a cloudy white layer when the fat-containing sample is mixed with ethanol and then water; the paper spot test leaves a permanent grease mark that does not evaporate. Always run a control — distilled water — alongside each sample to prove the colour change is real.',
                    },
                    {
                        'heading': 'Method and safety',
                        'body': 'Tests need only a small amount of crushed or dissolved food, but the procedure matters. For Benedict\'s you must heat the mixture in a water bath — never directly over a flame, because Benedict\'s solution can spit. Add equal volumes of reagent and sample, mix, and observe. For iodine just two drops on the food are enough; the colour appears instantly.\n\nFor the biuret test, add sodium hydroxide first and then a few drops of copper sulfate — the order matters. For fats, crush the food, shake with ethanol to dissolve any fat, decant into water and look for cloudiness. Record your observations in a table: sample, test, colour observed, conclusion. Mentioning controls and repeating each test earns full marks in the practical exam.',
                    },
                ],
                'fun_fact': 'The iodine test for starch is so sensitive that it is used in forensic labs to detect hidden fingerprints on paper — sweat from fingers leaves faint starch traces from handled food.',
                'quiz': [
                    {
                        'q': 'Iodine solution turns blue-black in the presence of…',
                        'options': ['Glucose', 'Starch', 'Protein', 'Fat'],
                        'answer': 1,
                        'explain': 'Iodine slips into the coiled starch molecule, turning blue-black — a positive test for starch.',
                    },
                    {
                        'q': 'Benedict\'s test is heated with a sample. A brick-red colour means…',
                        'options': ['No sugar', 'A trace of sugar', 'A high concentration of reducing sugar', 'Protein is present'],
                        'answer': 2,
                        'explain': 'Benedict\'s ranges from green (trace) through yellow and orange to brick-red (high), so it estimates sugar concentration.',
                    },
                    {
                        'q': 'The biuret test turns from blue to violet when…',
                        'options': ['Starch is present', 'Sugar is heated', 'Protein is present', 'Fat is dissolved'],
                        'answer': 2,
                        'explain': 'Biuret reagent reacts with the peptide bonds in protein, producing a purple/violet colour.',
                    },
                    {
                        'q': 'Which food would give a positive result in BOTH the iodine test and Benedict\'s test?',
                        'options': ['Pure oil', 'A ripe sweet potato', 'Pure egg white', 'Distilled water'],
                        'answer': 1,
                        'explain': 'A ripe sweet potato contains starch (positive iodine) and free sugars from ripening (positive Benedict\'s), unlike oil, egg or water.',
                    },
                ],
            },
        ],
    },
]
