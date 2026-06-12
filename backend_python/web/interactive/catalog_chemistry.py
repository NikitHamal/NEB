COURSES = [
    {
        'slug': 'kitchen-chemistry',
        'title': 'Kitchen Chemistry',
        'category': 'chemistry',
        'age_range': '8-12',
        'level': 'Beginner',
        'icon': 'skillet',
        'color': '#10B981',
        'tagline': 'Your kitchen is secretly a science lab — let\'s mix, fizz, float and melt!',
        'description': 'Did you know real chemistry happens every day in your kitchen? In this course you will mix salt, sand, oil and colour into a virtual beaker, build a rainbow tower out of liquids, make a bottle fizz with baking soda and vinegar, and melt chocolate with a virtual heater. Everything is safe, everything is playful, and every experiment uses real science numbers — so what you learn here works in your real kitchen too (with a grown-up nearby, of course!).',
        'skills': [
            'Mixing: dissolve, float, sink and spread',
            'Density and why liquids make layers',
            'Chemical reactions that make gas',
            'Melting and freezing points',
            'Thinking like a scientist: predict, test, observe',
        ],
        'lessons': [
            {
                'slug': 'mix-it-up',
                'title': 'Mix It Up!',
                'icon': 'blender',
                'minutes': 10,
                'sim': 'chemistry/mixing-lab',
                'sim_type': 'lab',
                'summary': 'Drop water, oil, salt, sand and food colouring into a virtual beaker and discover what dissolves, what floats, what sinks and what spreads.',
                'objectives': [
                    'Predict whether something will dissolve, float, sink or spread before you add it',
                    'Explain why salt seems to vanish in water but sand never does',
                    'Show that oil always floats on top of water',
                    'Use stirring to speed up dissolving and diffusion',
                ],
                'knowledge': [
                    {
                        'heading': 'Four things can happen',
                        'body': 'When you add something to water, only a few things can happen. It can dissolve and seem to disappear, like salt or sugar. It can float on top, like oil. It can sink to the bottom, like sand. Or it can slowly spread out, like a drop of food colouring.\n\nScientists call spreading out diffusion. Try every ingredient in the beaker and watch which of the four things happens!',
                    },
                    {
                        'heading': 'Where does the salt go?',
                        'body': 'Salt does not really disappear — it just breaks into pieces far too small to see. Water particles surround each tiny piece of salt and carry it away into the liquid. That is what dissolving means.\n\nHere is the proof it is still there: taste sea water (yuck, salty!) or let salty water dry in the sun. The water leaves, and the salt comes back as white crystals. Nothing was lost!',
                    },
                    {
                        'heading': 'Sand is stubborn',
                        'body': 'Sand never dissolves, no matter how hard you stir. Its particles hold on to each other too tightly for water to pull them apart. So sand just sinks to the bottom and sits there.\n\nA mixture like sand in water is easy to separate again — you can pour it through a filter or just wait for the sand to settle. A dissolved mixture like salt water is much trickier!',
                    },
                    {
                        'heading': 'Stirring is a speed boost',
                        'body': 'Stirring does not make impossible things happen — it only makes possible things happen faster. Salt dissolves quicker when you stir because fresh water keeps rushing past each salt grain. Food colouring spreads in seconds instead of minutes.\n\nBut stir sand all day and it still will not dissolve. Stirring is a speed boost, not a magic wand!',
                    },
                ],
                'fun_fact': 'A single drop of food colouring will spread through a whole glass of still water all by itself — it just takes hours. The particles are always moving, even when the water looks perfectly still!',
                'quiz': [
                    {
                        'q': 'You stir salt into water and it seems to vanish. What really happened?',
                        'options': ['The salt was destroyed', 'The salt dissolved into pieces too small to see', 'The salt turned into water', 'The salt floated away'],
                        'answer': 1,
                        'explain': 'Dissolving breaks salt into invisibly small pieces that mix into the water — let the water dry up and the salt comes back!',
                    },
                    {
                        'q': 'Why does oil sit on top of water?',
                        'options': ['Oil is sticky', 'Oil is less dense than water', 'Oil is afraid of water', 'Oil is hotter than water'],
                        'answer': 1,
                        'explain': 'Oil is lighter than the same amount of water — less dense — so water sinks below it and oil floats on top.',
                    },
                    {
                        'q': 'What does stirring do to sand in water?',
                        'options': ['Makes it dissolve', 'Turns it into salt', 'Mixes it for a moment, but it still sinks', 'Makes it float'],
                        'answer': 2,
                        'explain': 'Stirring only speeds up things that can already happen. Sand cannot dissolve, so it always settles back to the bottom.',
                    },
                ],
            },
            {
                'slug': 'density-tower',
                'title': 'Density Tower',
                'icon': 'layers',
                'minutes': 12,
                'sim': 'chemistry/density-tower',
                'sim_type': 'lab',
                'summary': 'Pour honey, syrup, water, oil and alcohol into one tall glass and watch them sort themselves into a rainbow of layers — then drop in objects and guess where they will stop!',
                'objectives': [
                    'Explain what density means using grams per millilitre',
                    'Predict the order of liquid layers before pouring',
                    'Show that pouring order does not change the final tower',
                    'Predict which layer an object will float on from its density',
                ],
                'knowledge': [
                    {
                        'heading': 'What is density?',
                        'body': 'Density tells you how much stuff is squeezed into a space. Imagine two identical spoons: one full of honey, one full of alcohol. The honey spoon is heavier because honey packs more material into the same space.\n\nWe measure density in grams per millilitre (g/mL). Honey is about 1.42 g/mL, water is exactly 1.00, and alcohol is only about 0.79. The bigger the number, the heavier each spoonful.',
                    },
                    {
                        'heading': 'Liquids sort themselves',
                        'body': 'Pour several liquids into one glass and something magical happens: they line up by density, all by themselves! The densest liquid (honey, 1.42) pushes its way to the bottom, and the lightest (alcohol, 0.79) floats to the very top.\n\nTry pouring them in a silly order in the simulation — water first, then honey, then oil. The tower always ends up the same: honey, syrup, water, oil, alcohol from bottom to top.',
                    },
                    {
                        'heading': 'Objects pick their floor',
                        'body': 'Now drop an object in. It sinks past every liquid that is lighter than itself and stops on the first liquid that is denser. A grape (about 1.1 g/mL) sinks through oil and water but floats on syrup (1.37).\n\nA cork is so light (about 0.24 g/mL) it floats on everything, while a metal coin (almost 9 g/mL!) zooms straight to the bottom. Every object finds its own floor in the tower.',
                    },
                    {
                        'heading': 'Density in real life',
                        'body': 'Density explains so much of the world! Ships made of heavy steel float because their shape traps light air inside, making the whole ship less dense than water. Hot air balloons rise because hot air is less dense than cold air.\n\nAnd when you shake a salad dressing of oil and vinegar, watch it afterwards: the oil patiently climbs back to the top, every single time.',
                    },
                ],
                'fun_fact': 'The Dead Sea is so salty that its water is about 1.24 g/mL — denser than your body! People float on it like corks, reading newspapers while lying on the water.',
                'quiz': [
                    {
                        'q': 'Which liquid sits at the BOTTOM of the density tower?',
                        'options': ['Alcohol (0.79 g/mL)', 'Water (1.00 g/mL)', 'Oil (0.92 g/mL)', 'Honey (1.42 g/mL)'],
                        'answer': 3,
                        'explain': 'The densest liquid always sinks below the rest — honey at 1.42 g/mL beats them all and takes the bottom floor.',
                    },
                    {
                        'q': 'If you pour the liquids in a different order, the tower will…',
                        'options': ['Stack in pouring order', 'Sort itself by density just the same', 'Mix into one colour', 'Explode'],
                        'answer': 1,
                        'explain': 'Density is the boss, not pouring order! Each liquid slides up or down until it sits between a denser one below and a lighter one above.',
                    },
                    {
                        'q': 'A grape has a density of about 1.1 g/mL. Where does it stop?',
                        'options': ['Floating on top of everything', 'On the syrup layer, below the water', 'At the very bottom', 'Inside the oil layer'],
                        'answer': 1,
                        'explain': 'The grape sinks through alcohol, oil and water (all less dense than 1.1) and floats on syrup, the first liquid denser than itself.',
                    },
                ],
            },
            {
                'slug': 'solids-liquids-fizz',
                'title': 'Solids, Liquids... Fizz!',
                'icon': 'bubble_chart',
                'minutes': 10,
                'sim': 'chemistry/fizzy-reactions',
                'sim_type': 'lab',
                'summary': 'Mix virtual baking soda and vinegar, watch CO₂ bubbles erupt into foam, and inflate a balloon with the gas you make — then find out which ingredient ran out first.',
                'objectives': [
                    'Recognise a chemical reaction: new things are made that were not there before',
                    'Name the gas made by baking soda and vinegar: carbon dioxide (CO₂)',
                    'Explain why the fizzing stops when one ingredient runs out',
                    'Use the balloon to show that an invisible gas still takes up space',
                ],
                'knowledge': [
                    {
                        'heading': 'A real chemical reaction',
                        'body': 'Mixing salt into water is just mixing — you can always get the salt back. But baking soda and vinegar do something much more exciting: they react and turn into brand-new substances that were not there before!\n\nThe fizz you see is carbon dioxide gas, called CO₂ for short — the same gas that makes soft drinks bubbly. Once it is made, you cannot un-fizz it back into baking soda and vinegar. That is the sign of a true chemical reaction.',
                    },
                    {
                        'heading': 'Where do the bubbles come from?',
                        'body': 'Baking soda is a base and vinegar is a weak acid. When they meet, they swap parts and build three new things: a salt dissolved in the liquid, plain water, and CO₂ gas.\n\nThe gas has nowhere to go, so it forms bubbles that race upward and burst into foam at the surface. More ingredients means more gas — and a bigger, foamier eruption!',
                    },
                    {
                        'heading': 'The one that runs out first wins',
                        'body': 'A reaction is like making sandwiches: if you have lots of bread but only two slices of cheese, you can only make two sandwiches. The cheese ran out first, so the cheese decides when you stop.\n\nChemists call the ingredient that runs out first the limiting reactant. In the simulation, try lots of vinegar with a tiny pinch of soda — the fizz stops early because the soda ran out. The leftover vinegar just sits there with no one to react with.',
                    },
                    {
                        'heading': 'Catching an invisible gas',
                        'body': 'CO₂ is invisible — so how do we know it is real? Trap it! Stretch a balloon over the bottle and the gas has nowhere to escape. As the reaction fizzes, the balloon swells up, blown up by a gas you cannot even see.\n\nThis is a famous and totally safe kitchen experiment. Ask a grown-up to try it with you for real: a bottle, a spoon of baking soda, a splash of vinegar and a balloon. Science magic!',
                    },
                ],
                'fun_fact': 'Volcano models at science fairs use exactly this reaction — baking soda, vinegar and a little red colouring. Real volcanoes also release CO₂, so the model is more scientific than it looks!',
                'quiz': [
                    {
                        'q': 'What gas do baking soda and vinegar make when they react?',
                        'options': ['Oxygen', 'Carbon dioxide (CO₂)', 'Hydrogen', 'Steam'],
                        'answer': 1,
                        'explain': 'The acid in vinegar reacts with baking soda to make carbon dioxide — the same gas that puts the fizz in soft drinks.',
                    },
                    {
                        'q': 'You mix LOTS of vinegar with a tiny pinch of baking soda. Why does the fizzing stop quickly?',
                        'options': ['The vinegar got bored', 'The gas escaped before forming', 'The baking soda ran out — it was the limiting reactant', 'Vinegar stops working after a minute'],
                        'answer': 2,
                        'explain': 'Fizzing needs BOTH ingredients. The tiny pinch of soda gets used up fast, and the leftover vinegar has nothing left to react with.',
                    },
                    {
                        'q': 'The balloon over the bottle inflates because…',
                        'options': ['The bottle gets hot', 'The reaction makes CO₂ gas that needs space', 'Vinegar evaporates into the balloon', 'The balloon sucks in air'],
                        'answer': 1,
                        'explain': 'The reaction creates new gas inside a closed bottle. The gas takes up space, and the only place to go is into the balloon!',
                    },
                ],
            },
            {
                'slug': 'hot-and-cold',
                'title': 'Hot and Cold',
                'icon': 'device_thermostat',
                'minutes': 10,
                'sim': 'chemistry/melt-freeze',
                'sim_type': 'lab',
                'summary': 'Heat and cool ice, chocolate, butter and candle wax, watch their particles break free or lock back together, and catch the thermometer pausing right at the melting point.',
                'objectives': [
                    'Describe melting and freezing using the particle picture',
                    'Match each substance to its real melting point',
                    'Explain why the thermometer pauses while something melts',
                    'Show that freezing is just melting in reverse, at the same temperature',
                ],
                'knowledge': [
                    {
                        'heading': 'Solid or liquid? Ask the particles',
                        'body': 'Everything is made of tiny particles, far too small to see. In a solid like ice or a chocolate bar, the particles hold hands in a neat pattern and only wiggle in place. That is why solids keep their shape.\n\nHeat the solid up and the particles wiggle harder and harder — until they break free and start sliding past each other. Now it flows: it has melted into a liquid!',
                    },
                    {
                        'heading': 'Every substance has its own magic number',
                        'body': 'Each substance melts at its own special temperature, called its melting point. Ice melts at exactly 0 °C. Chocolate melts at about 34 °C and butter at about 35 °C — just below your body temperature of 37 °C. Candle wax needs about 60 °C.\n\nThat is why chocolate melts in your hand and on your tongue, but a candle stays solid on a warm day. Try all four substances in the simulation and check their numbers!',
                    },
                    {
                        'heading': 'The thermometer takes a break',
                        'body': 'Heat ice steadily and watch the thermometer climb: −10, −5, 0… and then it stops! While the ice is melting, the temperature stays stuck at 0 °C even though you keep adding heat.\n\nWhy? All that energy is busy breaking the particles out of their neat solid pattern. Only when the very last bit has melted does the temperature start climbing again. Scientists call this hidden energy latent heat.',
                    },
                    {
                        'heading': 'Freezing: the movie in reverse',
                        'body': 'Cooling does exactly the opposite. Slow the particles down and, at the very same magic number, they snap back into their neat pattern — the liquid freezes solid. Water freezes at 0 °C, the same temperature ice melts.\n\nMelting and freezing are the same doorway, just walked through in opposite directions. Melted chocolate left on the counter hardens again because the room is colder than 34 °C.',
                    },
                ],
                'fun_fact': 'Chocolate is one of very few foods designed to melt at just below body temperature — that is why it stays snappy in the packet but melts smoothly the moment it touches your tongue!',
                'quiz': [
                    {
                        'q': 'What are the particles doing in a solid?',
                        'options': ['Flying around freely', 'Sliding past each other', 'Wiggling in place in a neat pattern', 'Not moving at all'],
                        'answer': 2,
                        'explain': 'Solid particles are locked in a tidy pattern and can only vibrate in place — that is why a solid keeps its shape.',
                    },
                    {
                        'q': 'Chocolate melts at about 34 °C. What happens to it on your tongue (37 °C)?',
                        'options': ['It freezes harder', 'It melts, because your tongue is warmer than 34 °C', 'Nothing happens', 'It turns into gas'],
                        'answer': 1,
                        'explain': 'Your tongue is warmer than chocolate\'s melting point, so the chocolate melts smoothly — exactly as the chocolate makers planned!',
                    },
                    {
                        'q': 'While ice is melting at 0 °C, the thermometer stays stuck because the heat energy is…',
                        'options': ['Leaking out of the box', 'Busy breaking particles out of their solid pattern', 'Making the ice colder', 'Broken'],
                        'answer': 1,
                        'explain': 'During melting, every bit of added energy goes into freeing particles from the lattice instead of raising the temperature. That pause is latent heat at work.',
                    },
                ],
            },
        ],
    },
    {
        'slug': 'virtual-chemistry-lab',
        'title': 'Virtual Chemistry Lab',
        'category': 'chemistry',
        'age_range': '12-19',
        'level': 'Intermediate',
        'icon': 'experiment',
        'color': '#10B981',
        'tagline': 'Build atoms particle by particle, spin real molecules in 3D and titrate acids without splashing a drop.',
        'description': 'Chemistry comes alive when you can touch it. In this course you assemble atoms from protons, neutrons and electrons, rotate accurate ball-and-stick molecules, melt and boil substances particle by particle, run a full acid-base titration with a live pH curve, and balance chemical equations until the atom scales sit level. Every model follows the real chemistry — correct electron shells, true bond angles, genuine titration mathematics — straight from the NEB science syllabus.',
        'skills': [
            'Atomic structure: protons, neutrons, electrons and shells',
            'Elements, isotopes and ions',
            'Molecular geometry and chemical bonding',
            'The particle model and changes of state',
            'pH, indicators and acid-base titration',
            'Balancing equations and conservation of mass',
        ],
        'lessons': [
            {
                'slug': 'atom-builder',
                'title': 'Atom Builder',
                'icon': 'token',
                'minutes': 16,
                'sim': 'chemistry/atom-builder',
                'sim_type': '3d',
                'summary': 'Add protons, neutrons and electrons to a live 3D atom and watch it become a new element, an isotope or an ion.',
                'objectives': [
                    'Name the three subatomic particles and where each lives in the atom',
                    'Show that the proton count alone decides which element an atom is',
                    'Build isotopes by changing neutrons and ions by changing electrons',
                    'Fill electron shells in the 2, 8, 8 pattern for the first twenty elements',
                ],
                'knowledge': [
                    {
                        'heading': 'Inside the atom',
                        'body': 'Every atom is built from just three particles. Protons (positive) and neutrons (neutral) are packed into a tiny, dense nucleus at the centre. Electrons (negative), nearly two thousand times lighter, occupy the space around it arranged in shells.\n\nThe scale is hard to imagine: if the nucleus were a football placed at the centre of a stadium, the nearest electrons would orbit out by the far stands, and everything between would be empty space. Almost all of an atom\'s mass sits in the nucleus, yet almost all of its size comes from the electron cloud.',
                    },
                    {
                        'heading': 'Protons define the element',
                        'body': 'The single number that decides an atom\'s identity is its proton count, called the atomic number Z. One proton makes hydrogen, six make carbon, eight make oxygen — no exceptions, ever. Change the proton count and you have literally changed the element.\n\nThe mass number A is protons plus neutrons, since both weigh about one atomic mass unit. In the simulation, watch the element name flip the instant you add or remove a proton, while adding neutrons changes only the mass number. The periodic table is simply all the elements lined up in order of Z.',
                    },
                    {
                        'heading': 'Isotopes and ions',
                        'body': 'Atoms of the same element can still differ. Isotopes have the same protons but different neutrons: carbon-12 and carbon-14 are both carbon, but the heavier one is radioactive and lets archaeologists date ancient remains. Too many or too few neutrons makes a nucleus unstable.\n\nIons differ in electrons instead. A neutral atom has equal protons and electrons; strip an electron away and the atom becomes a positive ion (cation), add an extra and it becomes a negative ion (anion). Sodium losing one electron to become Na⁺ is the first step in forming common salt.',
                    },
                    {
                        'heading': 'Electron shells: 2, 8, 8',
                        'body': 'Electrons cannot crowd anywhere they like — they fill shells of fixed capacity, starting nearest the nucleus. The first shell holds 2 electrons, the second 8, and the third 8 (for the first twenty elements). So sodium\'s eleven electrons arrange as 2, 8, 1.\n\nThe outermost electrons, called valence electrons, decide an element\'s chemistry. Atoms with full outer shells (helium, neon, argon) are famously unreactive, while atoms one electron away from a full shell — like sodium or chlorine — react eagerly. Chemistry is, at heart, the story of atoms chasing complete shells.',
                    },
                ],
                'fun_fact': 'You are partly made of stardust quite literally: every atom heavier than helium in your body — the carbon, oxygen, calcium and iron — was forged by nuclear fusion inside stars that exploded long before the Sun existed.',
                'quiz': [
                    {
                        'q': 'What single property decides which element an atom is?',
                        'options': ['Its number of neutrons', 'Its number of protons', 'Its number of electrons', 'Its total mass'],
                        'answer': 1,
                        'explain': 'The atomic number (proton count) defines the element. Neutrons give isotopes and electrons give ions, but the element never changes unless protons do.',
                    },
                    {
                        'q': 'Carbon-12 and carbon-14 are both carbon atoms. They differ in their number of…',
                        'options': ['Protons', 'Electrons', 'Neutrons', 'Shells'],
                        'answer': 2,
                        'explain': 'Isotopes share the same proton count (6 for carbon) but have different neutron counts: 6 neutrons in C-12, 8 in C-14.',
                    },
                    {
                        'q': 'An atom with 11 protons and 10 electrons is…',
                        'options': ['A neutral sodium atom', 'A sodium ion with charge +1', 'A neon atom', 'A sodium ion with charge −1'],
                        'answer': 1,
                        'explain': '11 protons means sodium. With one electron missing, positive charge wins by one: Na⁺, a cation.',
                    },
                    {
                        'q': 'How do the 17 electrons of chlorine arrange into shells?',
                        'options': ['8, 8, 1', '2, 8, 7', '2, 7, 8', '17 in one shell'],
                        'answer': 1,
                        'explain': 'Shells fill from the inside: 2 in the first, 8 in the second, leaving 7 in the third — one short of full, which is why chlorine is so reactive.',
                    },
                ],
            },
            {
                'slug': 'molecule-gallery',
                'title': 'Molecule Gallery',
                'icon': 'hub',
                'minutes': 15,
                'sim': 'chemistry/molecule-viewer',
                'sim_type': '3d',
                'summary': 'Rotate accurate 3D models of water, methane, glucose and more — and tap any atom to meet the element behind it.',
                'objectives': [
                    'Recognise common molecules by their 3D shapes: bent, linear, tetrahedral, pyramidal',
                    'Read ball-and-stick models and standard CPK element colours',
                    'Connect bond angles like water\'s 104.5° to the molecule\'s properties',
                    'Explain why molecular shape matters for smell, taste and life itself',
                ],
                'knowledge': [
                    {
                        'heading': 'Molecules have shape',
                        'body': 'A chemical formula like H₂O tells you the ingredients, but molecules are three-dimensional objects with definite geometry. Water is not a straight line: its two hydrogen atoms sit at an angle of 104.5°, making the molecule bent. Carbon dioxide really is linear, methane is a perfect tetrahedron with 109.5° angles, and ammonia is a low pyramid.\n\nThese shapes arise because pairs of electrons around the central atom repel each other and spread as far apart as possible — a rule known as VSEPR. Water is bent precisely because two invisible lone pairs on the oxygen squeeze the hydrogens together.',
                    },
                    {
                        'heading': 'Reading the model',
                        'body': 'Chemists colour atoms by a convention called CPK colouring, used in this gallery: hydrogen is white, carbon dark grey, oxygen red, nitrogen blue, chlorine green and sodium purple. The sticks between balls are covalent bonds — shared pairs of electrons. A double line of sticks, as in O₂ or CO₂, is a double bond: two shared pairs, shorter and stronger than a single bond.\n\nNot everything bonds this way. The salt fragment in the gallery is an ionic lattice: Na⁺ and Cl⁻ ions held by electrostatic attraction in an endlessly repeating grid, which is why salt forms cubic crystals.',
                    },
                    {
                        'heading': 'Why shape matters',
                        'body': 'Water\'s bent shape makes one side of the molecule slightly negative and the other slightly positive — it is polar. That tiny asymmetry is why water dissolves salt and sugar, why ice floats, and why water can climb up plant stems. Straighten the molecule and none of that would work; life as we know it depends on 104.5°.\n\nShape rules biology everywhere: enzymes recognise molecules the way a lock recognises a key, your nose tells smells apart largely by molecular shape, and a drug works only if it fits its target protein. Glucose\'s ring shape is exactly what your cells\' transporters are built to grab.',
                    },
                ],
                'fun_fact': 'Carbon monoxide is dangerous because of shape and fit: it latches onto the iron in your blood\'s haemoglobin more than 200 times more tightly than oxygen does, quietly taking oxygen\'s seat.',
                'quiz': [
                    {
                        'q': 'What is the shape of a water molecule?',
                        'options': ['Linear', 'Bent, with an angle of about 104.5°', 'Tetrahedral', 'A flat triangle'],
                        'answer': 1,
                        'explain': 'Two lone pairs on the oxygen push the O–H bonds together, bending the molecule to 104.5° — the source of water\'s polarity.',
                    },
                    {
                        'q': 'In CPK colouring, a red ball bonded to two white balls represents…',
                        'options': ['Carbon dioxide', 'Water', 'Ammonia', 'Methane'],
                        'answer': 1,
                        'explain': 'Red is oxygen and white is hydrogen, so one red with two whites is H₂O.',
                    },
                    {
                        'q': 'Methane (CH₄) has its four hydrogens arranged…',
                        'options': ['In a flat square', 'In a straight line', 'At the corners of a tetrahedron', 'In a ring'],
                        'answer': 2,
                        'explain': 'Four bonding pairs spread as far apart as possible in 3D, giving a tetrahedron with 109.5° between bonds.',
                    },
                    {
                        'q': 'The NaCl model looks different from the others because salt is…',
                        'options': ['A single giant molecule', 'An ionic lattice of Na⁺ and Cl⁻ ions', 'A metal', 'Made of double bonds'],
                        'answer': 1,
                        'explain': 'Salt has no individual molecules — oppositely charged ions stack in a repeating cubic lattice held by electrostatic attraction.',
                    },
                ],
            },
            {
                'slug': 'states-of-matter',
                'title': 'States of Matter',
                'icon': 'thermostat',
                'minutes': 15,
                'sim': 'chemistry/states-matter',
                'sim_type': 'lab',
                'summary': 'Heat and cool a box of particles to watch solids vibrate, liquids flow and gases fly — and find the melting plateaus.',
                'objectives': [
                    'Describe solids, liquids and gases using the particle model',
                    'Link temperature to the kinetic energy of particles',
                    'Explain why temperature pauses at the melting and boiling points',
                    'Compare melting and boiling points across different substances',
                ],
                'knowledge': [
                    {
                        'heading': 'The particle model',
                        'body': 'All matter is made of tiny particles in constant motion, and the three common states differ only in how those particles are arranged and how much they move. In a solid, particles sit in a fixed, regular lattice and merely vibrate in place — that is why solids hold their shape. In a liquid, particles still touch but can slide past one another, letting the liquid flow and take its container\'s shape. In a gas, particles break free entirely and fly in straight lines until they collide, filling every corner of whatever space they are given.\n\nWatch the simulation switch between all three as you drag the temperature slider.',
                    },
                    {
                        'heading': 'Temperature is particle motion',
                        'body': 'Temperature measures the average kinetic energy of the particles. Heat a substance and its particles vibrate, jostle or fly faster; cool it and they slow down. At −273 °C, absolute zero, particle motion reaches its minimum — nothing can be colder.\n\nThis explains everyday observations: gases expand when heated because faster particles hit the walls harder and more often; smells spread faster in a warm room because the gas particles carrying them travel faster; and sugar dissolves quicker in hot tea because energetic water particles break the crystal apart sooner.',
                    },
                    {
                        'heading': 'Plateaus: the hidden energy of melting',
                        'body': 'Heat ice steadily and its temperature climbs — until 0 °C, where it sticks. The thermometer pauses while the ice melts, then resumes climbing through the liquid range, and pauses again at 100 °C while the water boils. These flat sections of the heating curve are the plateaus you can see in the simulation\'s graph.\n\nDuring a plateau the added energy, called latent heat, is spent breaking the bonds between particles instead of speeding them up. That is why steam at 100 °C scalds far worse than water at 100 °C: it carries the entire latent heat of vaporisation, ready to release into your skin.',
                    },
                    {
                        'heading': 'Every substance has its own thresholds',
                        'body': 'Melting and boiling points are fingerprints of a substance, set by how strongly its particles attract one another. Water melts at 0 °C and boils at 100 °C. Oxygen\'s molecules attract so weakly that it is a gas until −183 °C and only freezes at −218 °C. Iron\'s atoms grip each other so strongly that it stays solid until 1538 °C and boils at a furious 2862 °C.\n\nSwitch substances in the simulation and notice that the behaviour is identical — only the temperatures shift. The particle model is universal; the bond strength is what changes.',
                    },
                ],
                'fun_fact': 'On high Himalayan peaks water boils well below 100 °C — around 86 °C at Everest Base Camp — because air pressure is lower, which is why climbers struggle to brew properly hot tea.',
                'quiz': [
                    {
                        'q': 'In which state do particles vibrate about fixed positions in a regular pattern?',
                        'options': ['Gas', 'Liquid', 'Solid', 'All three'],
                        'answer': 2,
                        'explain': 'Solid particles are locked in a lattice and can only vibrate in place, which is why solids keep a fixed shape and volume.',
                    },
                    {
                        'q': 'While ice is melting at 0 °C, the energy being added goes into…',
                        'options': ['Raising the temperature', 'Breaking bonds between particles', 'Making the particles heavier', 'Creating new particles'],
                        'answer': 1,
                        'explain': 'During a phase change the temperature plateaus: the latent heat is spent separating particles from the lattice, not speeding them up.',
                    },
                    {
                        'q': 'Heating a gas in a sealed rigid box increases its pressure because the particles…',
                        'options': ['Get bigger', 'Multiply in number', 'Hit the walls faster and more often', 'Stick to the walls'],
                        'answer': 2,
                        'explain': 'Higher temperature means higher particle speed, so collisions with the walls are harder and more frequent — that is pressure rising.',
                    },
                    {
                        'q': 'Oxygen boils at −183 °C while iron boils at 2862 °C. This is because…',
                        'options': ['Iron particles are smaller', 'The attraction between iron atoms is much stronger', 'Oxygen has no particles', 'Iron contains more heat'],
                        'answer': 1,
                        'explain': 'Boiling requires enough energy to fully separate particles. Stronger interparticle attraction means far more energy — a far higher boiling point.',
                    },
                ],
            },
            {
                'slug': 'acid-base-lab',
                'title': 'Acid-Base Lab',
                'icon': 'water_drop',
                'minutes': 17,
                'sim': 'chemistry/acid-base',
                'sim_type': 'lab',
                'summary': 'Run a real titration: drip NaOH into acid, watch the indicator change colour and catch the dramatic pH jump on a live graph.',
                'objectives': [
                    'Place everyday substances on the pH scale from 0 to 14',
                    'Carry out a virtual titration and read the equivalence point from the pH curve',
                    'Choose between universal indicator, litmus and phenolphthalein',
                    'Write the neutralisation reaction: acid + base → salt + water',
                ],
                'knowledge': [
                    {
                        'heading': 'The pH scale',
                        'body': 'Acidity is measured on the pH scale, which runs from 0 (strongly acidic) through 7 (neutral) to 14 (strongly alkaline). It tracks the concentration of hydrogen ions, H⁺: acids release H⁺ in water, while bases release OH⁻ ions that mop H⁺ up.\n\nThe scale is logarithmic — each step is a tenfold change. Lemon juice at pH 2 is ten times more acidic than vinegar at pH 3 and a hundred times more than tomato juice at pH 4. Your stomach works near pH 2, your blood holds remarkably steady at 7.4, and soap sits around pH 9 to 10.',
                    },
                    {
                        'heading': 'Neutralisation',
                        'body': 'Mix an acid with a base and they destroy each other\'s character in a neutralisation reaction: acid + base → salt + water. With hydrochloric acid and sodium hydroxide, HCl + NaOH → NaCl + H₂O — the products are simply table salt and water.\n\nAt the heart of every neutralisation the same tiny event repeats: H⁺ + OH⁻ → H₂O. Farmers neutralise acidic soil with lime, antacid tablets neutralise excess stomach acid, and toothpaste neutralises the acids made by mouth bacteria. The simulation runs this reaction drop by drop so you can watch the pH respond.',
                    },
                    {
                        'heading': 'Titration and the equivalence point',
                        'body': 'Titration is chemistry\'s precision technique for measuring concentration: add base from a burette, drop by drop, into a measured volume of acid containing an indicator. At first the pH creeps up slowly because plenty of acid remains. Then, near the equivalence point — where moles of base exactly match moles of acid — a single drop sends the pH leaping several units almost vertically.\n\nThat steep jump is the signature you will see on the live graph. For a strong acid and strong base the equivalence point sits at pH 7. Past it, extra base accumulates and the curve flattens again in alkaline territory.',
                    },
                    {
                        'heading': 'Indicators: chemistry you can see',
                        'body': 'Indicators are dyes that change colour with pH. Universal indicator shows the whole rainbow — red in strong acid, green at neutral, violet in strong alkali — so it estimates pH at a glance. Litmus is simpler: red below 7, blue above, making it a quick acid-or-base test.\n\nPhenolphthalein is the titration specialist: colourless in acid and suddenly pink above about pH 8.3. Because its colour snaps on right where the equivalence jump happens, a single drop of excess base turns the whole flask pink — an unmistakable stop signal. Choose each indicator in the simulation and compare.',
                    },
                ],
                'fun_fact': 'Rainwater is naturally slightly acidic, around pH 5.6, because carbon dioxide in the air dissolves into it to form weak carbonic acid — the same gas that gives soft drinks their fizzy bite.',
                'quiz': [
                    {
                        'q': 'A solution has pH 3. Compared with a pH 5 solution it is…',
                        'options': ['Twice as acidic', '100 times more acidic', 'Slightly more alkaline', '100 times less acidic'],
                        'answer': 1,
                        'explain': 'pH is logarithmic: each unit is a factor of ten in H⁺ concentration, so two units means 10 × 10 = 100 times more acidic.',
                    },
                    {
                        'q': 'What are the products when hydrochloric acid reacts with sodium hydroxide?',
                        'options': ['Hydrogen gas and chlorine', 'Sodium chloride and water', 'Carbon dioxide and water', 'Sodium and hydrochloric acid'],
                        'answer': 1,
                        'explain': 'Neutralisation: HCl + NaOH → NaCl + H₂O — salt and water.',
                    },
                    {
                        'q': 'Near the equivalence point of a strong acid-strong base titration, the pH…',
                        'options': ['Stays exactly constant', 'Falls sharply', 'Jumps steeply over a tiny added volume', 'Rises in a perfectly straight line'],
                        'answer': 2,
                        'explain': 'Once the acid is almost used up, each extra drop of base swings the H⁺ concentration enormously, producing the near-vertical jump on the curve.',
                    },
                    {
                        'q': 'Phenolphthalein in an acidic solution appears…',
                        'options': ['Pink', 'Blue', 'Green', 'Colourless'],
                        'answer': 3,
                        'explain': 'Phenolphthalein is colourless below about pH 8.3 and pink above it — which is exactly why it marks the end point of an acid-base titration so crisply.',
                    },
                ],
            },
            {
                'slug': 'reaction-balancer',
                'title': 'Reaction Balancer',
                'icon': 'balance',
                'minutes': 14,
                'sim': 'chemistry/reaction-balancer',
                'sim_type': 'lab',
                'summary': 'Tip the atomic scales: set coefficients, count atoms on both sides and balance real reactions from combustion to photosynthesis.',
                'objectives': [
                    'State the law of conservation of mass and what it means for equations',
                    'Balance chemical equations by adjusting coefficients — never subscripts',
                    'Count atoms of each element on both sides of a reaction',
                    'Balance real reactions including combustion and photosynthesis',
                ],
                'knowledge': [
                    {
                        'heading': 'Atoms are never lost',
                        'body': 'In 1789 Antoine Lavoisier weighed everything entering and leaving sealed reactions and found the totals always matched: mass is conserved. The modern explanation is simple — chemical reactions only rearrange atoms into new groupings; they never create or destroy them.\n\nBurn a candle and the wax seems to vanish, but weigh the carbon dioxide and water vapour produced and every atom is accounted for. This law is the foundation of all chemical arithmetic: whatever atoms enter a reaction must come out the other side, just wearing different molecular outfits.',
                    },
                    {
                        'heading': 'Coefficients, not subscripts',
                        'body': 'A balanced equation respects conservation by showing equal atoms of each element on both sides. You balance it by placing coefficients — the big numbers in front of formulas that multiply the whole molecule. 2H₂O means two complete water molecules: four H atoms and two O atoms.\n\nThe golden rule: never change the subscripts. Turning H₂O into H₂O₂ does not balance anything — it silently swaps water for hydrogen peroxide, a completely different chemical. The formulas are fixed by nature; your only legal move is choosing how many of each molecule take part.',
                    },
                    {
                        'heading': 'A strategy that works',
                        'body': 'Balance like a detective, not by random guessing. Start with the element that appears in the fewest formulas — usually a metal or carbon — and leave lone elements like O₂ or H₂ for last, since their coefficients can be set freely at the end without disturbing anything else.\n\nTry it on methane combustion: CH₄ + O₂ → CO₂ + H₂O. Carbon is already balanced. Four hydrogens on the left demand 2H₂O on the right. Now count oxygens on the right: 2 + 2 = 4, so the left needs 2O₂. Done: CH₄ + 2O₂ → CO₂ + 2H₂O. Finally, check the coefficients cannot all be divided down.',
                    },
                    {
                        'heading': 'Balanced equations run the world',
                        'body': 'Balancing is not exam decoration — it is the recipe book of industry and life. Photosynthesis, 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂, tells you a plant must capture exactly six CO₂ molecules for every glucose it builds, and that six O₂ come out — the oxygen you are breathing now.\n\nEngineers use balanced equations to compute exactly how much oxygen a rocket must carry, how much lime neutralises a polluted lake, and how much CO₂ a power station emits per tonne of fuel. Every one of those calculations starts from the same idea you are practising here: count the atoms.',
                    },
                ],
                'fun_fact': 'Lavoisier, who gave chemistry the law of conservation of mass, proved it using sealed glass vessels and the most precise balances of his century — showing that even burning, the most dramatic "disappearance" of all, loses nothing.',
                'quiz': [
                    {
                        'q': 'The law of conservation of mass says that in a chemical reaction…',
                        'options': ['Mass always decreases slightly', 'Atoms are rearranged but never created or destroyed', 'New atoms can form if there is energy', 'Gases have no mass'],
                        'answer': 1,
                        'explain': 'Reactions only regroup existing atoms into new molecules, so total mass before and after is identical.',
                    },
                    {
                        'q': 'To balance an equation you may only change the…',
                        'options': ['Subscripts inside formulas', 'Coefficients in front of formulas', 'Chemical symbols', 'Products into different chemicals'],
                        'answer': 1,
                        'explain': 'Coefficients multiply whole molecules. Changing a subscript changes the substance itself — H₂O and H₂O₂ are different chemicals.',
                    },
                    {
                        'q': 'In the balanced equation 2H₂ + O₂ → 2H₂O, how many hydrogen atoms are on each side?',
                        'options': ['2', '4', '6', '8'],
                        'answer': 1,
                        'explain': '2H₂ contains 2 × 2 = 4 hydrogen atoms, and 2H₂O also contains 2 × 2 = 4. Balanced.',
                    },
                    {
                        'q': 'What coefficient of O₂ balances CH₄ + ?O₂ → CO₂ + 2H₂O?',
                        'options': ['1', '2', '3', '4'],
                        'answer': 1,
                        'explain': 'The right side holds 2 oxygens in CO₂ plus 2 in 2H₂O, four in total, so the left needs 2O₂.',
                    },
                ],
            },
        ],
    },
]
