from .catalog_neb_chemistry_12 import COURSES as _C12

COURSES = [
    {
        'slug': 'neb-chemistry-practical-11',
        'title': 'NEB Chemistry Practicals — Class 11',
        'category': 'chemistry',
        'age_range': '16-17',
        'level': 'Intermediate',
        'icon': 'labs',
        'color': '#059669',
        'tagline': 'The complete Class 11 NEB chemistry practical book — every experiment as a realistic virtual lab.',
        'description': 'Run every practical from the NEB Class 11 chemistry syllabus on a virtual lab bench. Identify apparatus, separate mixtures, titrate acid against base with a real over-shootable endpoint, read flame colours, hunt down anions in unknown salts, prepare and test the classic gases, and determine the water of crystallization in blue vitriol. Each simulation follows the genuine procedure with genuine numbers — record your readings, do the calculation and compare with the true value, exactly as in the board practical exam.',
        'skills': [
            'Naming and handling common laboratory apparatus safely',
            'Choosing the correct separation technique for a mixture',
            'Acid-base titration: technique, endpoint and calculation',
            'Qualitative analysis: flame tests and anion tests',
            'Gas preparation, collection and identification',
            'Gravimetric analysis and the mole calculation',
        ],
        'lessons': [
            {
                'slug': 'lab-apparatus-safety',
                'title': 'Lab Apparatus & Safety',
                'icon': 'science',
                'minutes': 14,
                'sim': 'nebchemistry/lab-apparatus',
                'sim_type': 'lab3d',
                'summary': 'Tour a virtual lab bench: tap every apparatus to learn its name and use, beat the "find the apparatus" quiz, then spot the four safety hazards hiding on the bench.',
                'objectives': [
                    'Identify the common apparatus: beaker, conical flask, burette, pipette, test tube, Bunsen burner, tripod, funnel, wash bottle and watch glass',
                    'Match each apparatus to its correct use, especially accurate versus approximate volume measurement',
                    'State the difference between the Bunsen burner\'s blue and yellow flames and when to use each',
                    'Spot common safety violations: missing goggles, flammables near flames, bad heating technique and uncleaned spills',
                    'Explain why a burette is read at eye level from the bottom of the meniscus',
                ],
                'knowledge': [
                    {
                        'heading': 'Know your glassware — accuracy matters',
                        'body': 'Laboratory glassware is divided by job. Beakers and conical flasks hold and mix; their printed graduations are only approximate, with errors of 5% or more. Volumetric glassware measures: a pipette delivers one fixed volume (commonly 25.0 mL) with an accuracy of about 0.05 mL, and a burette delivers a variable volume readable to 0.1 mL or better.\n\nThis is why titration always uses a pipette for the flask solution and a burette for the titrant — never a beaker for either. In the practical exam, naming the right apparatus for a measurement is a standard question: "accurate fixed volume" means pipette, "accurate variable volume" means burette, "just holding or heating" means beaker or flask.',
                    },
                    {
                        'heading': 'The Bunsen burner and heating technique',
                        'body': 'The Bunsen burner gives two flames. With the air hole open, complete combustion gives the roaring blue flame with a pale inner cone — nearly 1500 °C at the tip of the inner cone, used for strong heating. With the air hole closed, incomplete combustion gives the quiet, luminous yellow flame — cooler, sooty, and used only as the visible "safety flame" between operations.\n\nGlassware never sits directly in the flame: a tripod and wire gauze spread the heat so the glass warms evenly instead of cracking. Test tubes are heated near the surface of the liquid, tilted, constantly moved, and always pointed away from yourself and neighbours — bumping liquid can eject violently from an overheated tube bottom.',
                    },
                    {
                        'heading': 'Safety rules that examiners expect you to know',
                        'body': 'Eye protection comes first: goggles are worn whenever anything is heated or any corrosive liquid is handled, because the eye cannot heal from alkali burns the way skin can. Flammable liquids (ethanol, ether) must be stoppered and kept well away from open flames — their invisible vapour can flash across a bench.\n\nSpills are reported and cleaned immediately; acid spills are neutralised with sodium bicarbonate. Never taste any chemical, never pipette by mouth, and waft vapours toward your nose with a cupped hand rather than sniffing directly. These precautions appear in the viva section of the NEB practical exam, so learn the reason behind each rule, not just the rule itself.',
                    },
                ],
                'fun_fact': 'The conical (Erlenmeyer) flask was invented in 1860 precisely for titration — its sloped sides let you swirl vigorously without a single drop splashing out, which a beaker simply cannot do.',
                'quiz': [
                    {
                        'q': 'Which apparatus delivers one fixed, highly accurate volume of solution?',
                        'options': ['Beaker', 'Pipette', 'Conical flask', 'Wash bottle'],
                        'answer': 1,
                        'explain': 'A pipette is calibrated to deliver a single fixed volume (e.g. 25.0 mL) very accurately. Burettes deliver variable volumes; beakers are only approximate.',
                    },
                    {
                        'q': 'The hottest Bunsen flame is obtained when…',
                        'options': ['The air hole is fully closed', 'The gas is turned low', 'The air hole is fully open, giving a blue flame', 'The flame is yellow and luminous'],
                        'answer': 2,
                        'explain': 'An open air hole gives complete combustion: a roaring blue flame near 1500 °C at the inner cone tip. The yellow flame is cooler and sooty.',
                    },
                    {
                        'q': 'Why is a wire gauze placed between flame and beaker?',
                        'options': ['To make the flame hotter', 'To spread the heat evenly so the glass does not crack', 'To filter the gas', 'To support the burner'],
                        'answer': 1,
                        'explain': 'The gauze distributes the flame\'s heat across the glass base, preventing the local hot spot that would shatter it.',
                    },
                    {
                        'q': 'While heating a liquid in a test tube you should point the mouth…',
                        'options': ['Towards yourself to watch it', 'Straight up', 'Away from everyone, while moving the tube', 'Towards the window'],
                        'answer': 2,
                        'explain': 'Superheated liquid can suddenly "bump" out of the tube. Pointing it away from all people and keeping the tube moving prevents accidents.',
                    },
                ],
            },
            {
                'slug': 'separation-techniques',
                'title': 'Separation Techniques',
                'icon': 'filter_alt',
                'minutes': 16,
                'sim': 'nebchemistry/separation-lab',
                'sim_type': 'lab3d',
                'summary': 'Take five different mixtures apart with the right sequence of techniques — filtration, evaporation, sublimation, distillation and paper chromatography — and watch each apparatus work.',
                'objectives': [
                    'Choose the correct separation technique from the properties of the components',
                    'Separate sand, salt and water by filtration followed by evaporation',
                    'Explain sublimation and use it to separate naphthalene from salt',
                    'Describe simple distillation and what the condenser does',
                    'Run a paper chromatogram and explain why dyes travel different distances',
                ],
                'knowledge': [
                    {
                        'heading': 'Match the technique to the property',
                        'body': 'Every separation exploits a difference in properties. Filtration works when one component is insoluble: the solid stays on the paper as the residue, the liquid passes through as the filtrate. Evaporation recovers a dissolved solid by boiling the solvent away — done gently in an evaporating dish, ideally stopping at the crystallisation point so crystals form slowly and large.\n\nSublimation is the special case for solids like naphthalene, camphor, iodine and ammonium chloride that pass directly from solid to vapour. Heat the mixture and the sublimable component rises as vapour and re-solidifies on a cold surface (an inverted funnel or watch glass), leaving the non-sublimable salt behind.',
                    },
                    {
                        'heading': 'Distillation: when you want the solvent back',
                        'body': 'Evaporation throws the water away — distillation catches it. The solution boils in a distillation flask, the vapour rises into a water-cooled condenser, and pure liquid drips into the receiver. The thermometer sits at the side-arm junction, reading the vapour temperature: a steady 100 °C confirms pure water is coming over.\n\nThe condenser\'s cooling water enters at the bottom and leaves from the top, flowing against the vapour — this counter-current arrangement keeps the coldest water at the coldest end and condenses vapour most efficiently. Distillation separates salt from water completely: the salt cannot evaporate, so it stays in the flask.',
                    },
                    {
                        'heading': 'Chromatography: separating the inseparable-looking',
                        'body': 'Black ink looks like one substance but is usually several dyes. In paper chromatography a spot of ink is placed on a pencil baseline just above the solvent level. As the solvent climbs the paper by capillary action, each dye is carried along at its own rate — dyes that dissolve better in the solvent and stick less to the paper travel further.\n\nThe result is a chromatogram: each dye becomes a separate spot. The ratio of distance moved by the spot to the distance moved by the solvent front is the Rf value, always between 0 and 1, and constant for a given dye in a given solvent — so Rf values identify substances. The baseline must be in pencil, since an ink baseline would chromatograph itself!',
                    },
                ],
                'fun_fact': 'Chromatography means "colour writing" — Russian botanist Mikhail Tsvet invented it in 1903 to separate green plant pigments, and the same principle now powers the drug-testing labs of the Olympics.',
                'quiz': [
                    {
                        'q': 'To get pure salt from a sand-salt-water mixture, the correct order is…',
                        'options': ['Evaporate, then filter', 'Filter, then evaporate the filtrate', 'Distil, then filter', 'Sublime, then evaporate'],
                        'answer': 1,
                        'explain': 'Filtration first removes insoluble sand. Evaporating the filtrate then drives off the water, leaving salt crystals.',
                    },
                    {
                        'q': 'Naphthalene can be separated from salt by sublimation because naphthalene…',
                        'options': ['Dissolves in water', 'Melts at a low temperature', 'Changes directly from solid to vapour on heating', 'Is magnetic'],
                        'answer': 2,
                        'explain': 'Sublimable solids skip the liquid state. Naphthalene vapour rises and re-solidifies on a cold surface; salt does not sublime.',
                    },
                    {
                        'q': 'In simple distillation, the condenser\'s job is to…',
                        'options': ['Boil the solution faster', 'Cool the vapour back to liquid', 'Filter out impurities', 'Measure the temperature'],
                        'answer': 1,
                        'explain': 'The water-cooled condenser turns the rising vapour back into liquid, which is collected as pure distillate.',
                    },
                    {
                        'q': 'In paper chromatography, a dye travels far up the paper when it…',
                        'options': ['Is very dense', 'Dissolves well in the solvent and sticks weakly to the paper', 'Sticks strongly to the paper', 'Has a dark colour'],
                        'answer': 1,
                        'explain': 'Movement is a tug-of-war between solubility in the moving solvent and adsorption on the paper. High solubility + weak sticking = high Rf.',
                    },
                ],
            },
            {
                'slug': 'acid-base-titration',
                'title': 'Acid-Base Titration',
                'icon': 'colorize',
                'minutes': 20,
                'sim': 'nebchemistry/titration',
                'sim_type': 'lab3d',
                'summary': 'Perform a complete titration of unknown NaOH against standard 0.10 M HCl: rinse, fill, pipette, titrate drop by drop to a genuinely over-shootable endpoint, record concordant trials and calculate the concentration.',
                'objectives': [
                    'Carry out the full titration procedure in the correct order, including rinsing the burette with the titrant',
                    'Read a burette to 0.05 mL and record initial and final readings properly',
                    'Approach the endpoint dropwise and recognise the indicator colour change',
                    'Repeat trials until two concordant titres (within 0.2 mL) are obtained',
                    'Calculate the unknown concentration using M₁V₁ = M₂V₂ for a 1:1 reaction',
                ],
                'knowledge': [
                    {
                        'heading': 'Why every step of the procedure exists',
                        'body': 'Titration finds an unknown concentration by reacting it exactly with a standard solution. Each preparation step kills a specific error. The burette is rinsed with the acid it will hold — rinsing with water would leave droplets that dilute the titrant. The pipette is rinsed with the alkali it will measure. The conical flask, however, is rinsed only with distilled water: extra water changes neither the moles of NaOH in the flask nor the titre.\n\nAfter filling, the jet below the tap must be checked for air bubbles — a bubble that escapes mid-titration counts as fake volume. Readings are taken at eye level from the bottom of the meniscus, with the burette vertical. The first titration is always a rough trial run quickly to locate the endpoint; accurate trials then approach it dropwise.',
                    },
                    {
                        'heading': 'The endpoint: one drop decides',
                        'body': 'In this experiment the flask holds 25.0 mL of NaOH with phenolphthalein, which is pink in alkali. As 0.10 M HCl runs in, the reaction NaOH + HCl → NaCl + H₂O consumes the alkali. Near the equivalence point a single drop (about 0.05 mL) swings the solution from alkaline to acidic, and the pink colour vanishes — that decolourisation is the endpoint.\n\nThe skill is anticipation: when the pink starts fading slowly where the acid lands, you are within a millilitre. Slow to single drops, swirl after each, and wash the flask walls with distilled water so every drop reacts. If you overshoot, the trial is not wasted — record it as rough and use it to plan the next one. Methyl orange works too (yellow in alkali → red in acid, orange at the endpoint), but its change is harder to judge by eye.',
                    },
                    {
                        'heading': 'Concordance and the calculation',
                        'body': 'A single titre proves nothing — the examiner wants concordant results: two accurate titres agreeing within 0.2 mL. Their mean is the reliable titre V. For this 1:1 reaction the calculation is M(NaOH) × 25.0 = 0.100 × V, so M(NaOH) = 0.100 × V / 25.0.\n\nSources of error worth quoting in your report: air bubble in the burette jet (titre too high), reading the top of the meniscus, overshooting the endpoint, rinsing the burette with water instead of acid (titre too high because the acid is diluted), and using a wet measuring flask for the pipetted solution. Each links a physical mistake to the direction of the error — exactly the reasoning the practical viva tests.',
                    },
                ],
                'fun_fact': 'The word "titration" comes from the French "titre", meaning the assayed purity of gold coins — 18th-century chemists borrowed the term when they began assaying solutions instead of treasure.',
                'quiz': [
                    {
                        'q': 'Before filling, the burette should be rinsed with…',
                        'options': ['Distilled water only', 'The acid solution it will contain', 'The alkali from the flask', 'Indicator solution'],
                        'answer': 1,
                        'explain': 'Rinsing with the titrant itself ensures leftover droplets are the same solution, so the concentration in the burette is not diluted.',
                    },
                    {
                        'q': 'Extra distilled water added to the conical flask during titration…',
                        'options': ['Increases the titre', 'Decreases the titre', 'Does not change the titre', 'Destroys the indicator'],
                        'answer': 2,
                        'explain': 'The titre depends on the moles of NaOH present, not its volume or concentration in the flask — water adds no moles.',
                    },
                    {
                        'q': 'Two concordant titres means two accurate titres that…',
                        'options': ['Are exactly equal', 'Agree within 0.2 mL', 'Differ by less than 2 mL', 'Include the rough trial'],
                        'answer': 1,
                        'explain': 'Concordant titres agree within 0.2 mL (some books say 0.1 mL). The rough trial is never averaged in.',
                    },
                    {
                        'q': '25.0 mL of NaOH needed a mean titre of 22.5 mL of 0.10 M HCl. The NaOH concentration is…',
                        'options': ['0.10 M', '0.090 M', '0.111 M', '0.225 M'],
                        'answer': 1,
                        'explain': 'M = 0.100 × 22.5 / 25.0 = 0.090 M. The reaction is 1:1, so moles of acid at the endpoint equal moles of base.',
                    },
                ],
            },
            {
                'slug': 'flame-tests',
                'title': 'Flame Tests & Cation Detection',
                'icon': 'local_fire_department',
                'minutes': 14,
                'sim': 'nebchemistry/flame-tests',
                'sim_type': 'lab3d',
                'summary': 'Clean a platinum loop in concentrated HCl, dip it into salt samples and read the flame colours — then identify unknown salts from colour alone, watching out for the sodium contamination trap.',
                'objectives': [
                    'Perform a flame test with the correct clean-dip-flame technique',
                    'Recall the characteristic flame colours: Na golden-yellow, K lilac, Ca brick-red, Cu blue-green, Sr crimson, Ba apple-green',
                    'Explain why a dirty wire loop gives a misleading yellow flame',
                    'Explain the origin of flame colours in terms of electron excitation and emission',
                    'Identify an unknown salt from its flame colour',
                ],
                'knowledge': [
                    {
                        'heading': 'Why metals colour a flame',
                        'body': 'Flame colours are quantum physics you can see. Heat from the Bunsen flame promotes the metal atoms\' outer electrons to higher energy levels. The excited electrons immediately fall back, releasing the energy difference as light. Because each element has its own unique ladder of energy levels, each emits its own fixed wavelengths — sodium\'s famous pair of yellow lines at 589 nm, for example.\n\nThis is the same physics as fireworks (strontium for red, barium for green, copper for blue) and street lamps (sodium\'s orange glow). It is also how astronomers know what stars are made of: the emission and absorption lines in starlight are flame tests performed across light-years.',
                    },
                    {
                        'heading': 'The technique — and the sodium trap',
                        'body': 'The procedure is short but every step matters. The platinum (or nichrome) loop is first dipped in concentrated HCl and held in the flame until it adds no colour of its own. HCl works because it converts surface salts into chlorides, which are relatively volatile and vaporise away — cleaning the wire. Only then is the loop dipped into the salt (often moistened with HCl, again to form the volatile chloride) and held at the edge of the blue flame.\n\nThe classic trap is sodium contamination. Sodium compounds are everywhere — sweat, dust, previous samples — and sodium\'s yellow emission is intensely bright. A dirty loop shows a strong yellow flash that masks everything else, fooling you into reporting sodium. A persistent strong yellow that survives repeated cleaning is genuine; a brief yellow flash from an uncleaned loop is contamination. Real labs view potassium\'s weak lilac through blue cobalt glass, which filters out the yellow sodium glare.',
                    },
                    {
                        'heading': 'The colours you must memorise',
                        'body': 'For the NEB practical the colour table is core knowledge. Sodium: intense golden-yellow, persistent. Potassium: lilac (pale violet), faint and easily masked. Calcium: brick-red (orange-red). Strontium: crimson (deep red, distinguishable from calcium\'s brick shade with practice). Barium: apple-green (pale yellowish green). Copper: blue-green, distinctive and strong.\n\nFlame tests detect the metal cation, not the anion — NaCl, Na₂SO₄ and Na₂CO₃ all give identical yellow. They are also only preliminary evidence: a flame colour suggests a cation, but confirmation needs the wet tests of systematic salt analysis, which you will meet in the Class 12 course.',
                    },
                ],
                'fun_fact': 'Robert Bunsen designed his famous burner in 1855 specifically to give a colourless flame for flame tests — and with it he and Kirchhoff discovered two brand-new elements, caesium (sky-blue line) and rubidium (deep-red line), named after their colours.',
                'quiz': [
                    {
                        'q': 'The wire loop is cleaned in concentrated HCl because…',
                        'options': ['HCl makes the flame hotter', 'Chlorides are volatile and old residues vaporise away', 'HCl is a strong oxidiser', 'It cools the wire down'],
                        'answer': 1,
                        'explain': 'HCl converts residues into volatile chlorides that evaporate in the flame, leaving a clean wire that adds no colour of its own.',
                    },
                    {
                        'q': 'A brick-red flame indicates which cation?',
                        'options': ['Sr²⁺', 'Cu²⁺', 'Ca²⁺', 'K⁺'],
                        'answer': 2,
                        'explain': 'Calcium gives brick-red. Strontium is crimson (deeper red), copper blue-green, potassium lilac.',
                    },
                    {
                        'q': 'The flame colour is produced when excited electrons…',
                        'options': ['Escape the atom completely', 'Fall back to lower energy levels, emitting light', 'Collide with gas molecules', 'Absorb light from the flame'],
                        'answer': 1,
                        'explain': 'Heat excites electrons upward; they emit photons of element-specific wavelengths as they drop back — that light is the flame colour.',
                    },
                    {
                        'q': 'A strong yellow flash from an uncleaned loop most likely means…',
                        'options': ['The salt is potassium', 'Sodium contamination on the wire', 'The flame is too cold', 'Barium is present'],
                        'answer': 1,
                        'explain': 'Sodium traces are everywhere and emit intensely. Always clean the loop until it gives no colour before trusting any yellow.',
                    },
                ],
            },
            {
                'slug': 'anion-tests',
                'title': 'Salt Analysis: Anion Tests',
                'icon': 'biotech',
                'minutes': 16,
                'sim': 'nebchemistry/anion-tests',
                'sim_type': 'lab3d',
                'summary': 'A white unknown salt sits on your bench. Run the dilute acid test, silver nitrate test, barium chloride test and the brown ring test — read the precipitates and gases like an analyst and name the anion.',
                'objectives': [
                    'Test for carbonate with dilute acid and lime water',
                    'Test for chloride with acidified silver nitrate and confirm with ammonia',
                    'Test for sulphate with acidified barium chloride',
                    'Perform and interpret the brown ring test for nitrate',
                    'Write the ionic equations behind each positive observation',
                ],
                'knowledge': [
                    {
                        'heading': 'Gases first: the dilute acid test',
                        'body': 'Systematic anion analysis begins with dilute acid, because the easiest anions to find are those that escape as gases. Add dilute H₂SO₄ (or HCl) to the solid salt: brisk effervescence of a colourless, odourless gas that turns lime water milky proves carbonate. The chemistry: CO₃²⁻ + 2H⁺ → H₂O + CO₂, then CO₂ + Ca(OH)₂ → CaCO₃ (the white milkiness) + H₂O.\n\nA subtle classic: pass the gas through lime water for a long time and the milkiness disappears, because excess CO₂ converts insoluble CaCO₃ into soluble calcium hydrogencarbonate, Ca(HCO₃)₂. If nothing fizzes with cold dilute acid, carbonate is absent and you move to the precipitation tests.',
                    },
                    {
                        'heading': 'Precipitation tests: silver for chloride, barium for sulphate',
                        'body': 'Chloride test: acidify the salt solution with dilute HNO₃, then add AgNO₃. A curdy white precipitate of AgCl that is insoluble in HNO₃ but dissolves in NH₄OH confirms chloride: Ag⁺ + Cl⁻ → AgCl↓. The acidification step matters — it destroys carbonate and sulphite, which would otherwise also give white silver precipitates and a false positive.\n\nSulphate test: acidify with dilute HCl, then add BaCl₂. A heavy white precipitate of BaSO₄, insoluble in the acid, confirms sulphate: Ba²⁺ + SO₄²⁻ → BaSO₄↓. Again the acid is the safeguard: BaCO₃ is also white but dissolves in HCl with fizzing, so only sulphate survives the acid test. In both tests the logic is identical — precipitate plus acid-insolubility equals confirmation.',
                    },
                    {
                        'heading': 'The brown ring test for nitrate',
                        'body': 'Nitrate is the awkward anion: almost all nitrates are soluble, so no simple precipitation test exists. The classic identification is the brown ring test. To the salt solution add freshly prepared FeSO₄ solution, then pour concentrated H₂SO₄ carefully down the inside of the tilted tube. The dense acid forms a separate bottom layer, and at the junction of the two layers a brown ring appears.\n\nThe chemistry happens at that interface: the acid makes the medium strongly acidic, nitrate oxidises Fe²⁺ to Fe³⁺ and is itself reduced to NO (NO₃⁻ + 3Fe²⁺ + 4H⁺ → NO + 3Fe³⁺ + 2H₂O); the NO then binds a remaining Fe²⁺ to form the brown complex [Fe(H₂O)₅NO]²⁺. Shake the tube and the ring vanishes — the layers mix, the local conditions are destroyed. The FeSO₄ must be fresh because air slowly oxidises Fe²⁺ to Fe³⁺, which cannot form the complex.',
                    },
                ],
                'fun_fact': 'AgCl, the white precipitate of the chloride test, darkens to grey-violet in sunlight as light splits it into silver metal and chlorine — the very photoreaction on which 180 years of black-and-white photography was built.',
                'quiz': [
                    {
                        'q': 'A salt fizzes with dilute H₂SO₄ and the gas turns lime water milky. The anion is…',
                        'options': ['Chloride', 'Sulphate', 'Carbonate', 'Nitrate'],
                        'answer': 2,
                        'explain': 'Carbonates release CO₂ with dilute acid, and CO₂ turns lime water milky by forming insoluble CaCO₃.',
                    },
                    {
                        'q': 'In the chloride test, dilute HNO₃ is added before AgNO₃ in order to…',
                        'options': ['Make the precipitate whiter', 'Dissolve the chloride', 'Destroy carbonate and sulphite that would give false white precipitates', 'Speed up the reaction'],
                        'answer': 2,
                        'explain': 'CO₃²⁻ and SO₃²⁻ also precipitate with Ag⁺. Acidifying removes them first, so a surviving white ppt can only be AgCl.',
                    },
                    {
                        'q': 'The white precipitate in a positive sulphate test is…',
                        'options': ['BaSO₄, insoluble in dilute HCl', 'BaCO₃, soluble in HCl', 'AgCl', 'CaSO₄'],
                        'answer': 0,
                        'explain': 'Ba²⁺ + SO₄²⁻ → BaSO₄↓. Its insolubility in dilute HCl distinguishes it from white BaCO₃, which dissolves with effervescence.',
                    },
                    {
                        'q': 'The brown ring in the nitrate test is the complex…',
                        'options': ['Fe(OH)₃', '[Fe(H₂O)₅NO]²⁺', 'Fe₂(SO₄)₃', 'FeCl₃'],
                        'answer': 1,
                        'explain': 'NO produced by reduction of nitrate binds to Fe²⁺ forming the brown nitrosyl complex at the junction of the two layers.',
                    },
                ],
            },
            {
                'slug': 'gas-preparation',
                'title': 'Preparation of Gases',
                'icon': 'bubble_chart',
                'minutes': 16,
                'sim': 'nebchemistry/gas-preparation',
                'sim_type': 'lab3d',
                'summary': 'Set up the classic generators for hydrogen, oxygen and carbon dioxide, collect each gas by the correct method, and confirm its identity with the pop test, glowing splint and lime water.',
                'objectives': [
                    'Prepare H₂ from zinc and dilute HCl, O₂ from H₂O₂ with MnO₂, and CO₂ from marble chips and dilute HCl',
                    'Choose the collection method from the gas\'s density and solubility',
                    'Perform the identifying test for each gas and state the expected result',
                    'Write the balanced equation for each preparation and test',
                    'Explain the role of MnO₂ as a catalyst',
                ],
                'knowledge': [
                    {
                        'heading': 'Three generators, one design',
                        'body': 'All three preparations use the same apparatus logic: a flask holding the solid, a thistle funnel to add the liquid from above (its stem dipping below the liquid surface so gas cannot escape up it), and a delivery tube leading to the collection vessel. Hydrogen: granulated zinc + dilute HCl → ZnCl₂ + H₂. Carbon dioxide: marble chips (CaCO₃) + dilute HCl → CaCl₂ + H₂O + CO₂.\n\nOxygen is the odd one out — no acid needed, just decomposition of hydrogen peroxide: 2H₂O₂ → 2H₂O + O₂, with a pinch of black MnO₂. The MnO₂ is a catalyst: it speeds the decomposition enormously but is chemically unchanged and can be recovered at the end with its mass intact. (The older method, heating KClO₃ with MnO₂, gives the same gas: 2KClO₃ → 2KCl + 3O₂.)',
                    },
                    {
                        'heading': 'Collection: let the gas\'s properties decide',
                        'body': 'How you collect a gas follows from two properties — solubility in water and density relative to air. Hydrogen and oxygen are (almost) insoluble in water, so both are collected over water: the gas bubbles up into an inverted water-filled jar, visibly displacing the water downward. This method has the bonus of showing exactly how full the jar is.\n\nCarbon dioxide is noticeably soluble in water, so water collection wastes it. Instead, being about 1.5 times denser than air, it is collected by upward displacement of air: the jar stands mouth-up and CO₂ sinks in, pushing the lighter air out of the top. (If you ever collect hydrogen by air displacement, the jar must be mouth-down, since H₂ is 14 times lighter than air.) Exam logic: insoluble → over water; soluble and denser than air → upward displacement of air.',
                    },
                    {
                        'heading': 'The identifying tests',
                        'body': 'Each gas has a one-line confirmatory test. Hydrogen: bring a burning splint to the jar mouth — the gas burns with a squeaky pop, the mini-explosion of 2H₂ + O₂ → 2H₂O. Oxygen: a glowing (not burning) splint thrust into the jar relights, because combustion accelerates dramatically in pure O₂. Carbon dioxide: bubble the gas through lime water, which turns milky as insoluble CaCO₃ forms — the same reaction as in the carbonate anion test.\n\nPrecautions worth quoting: keep all flames away from the hydrogen generator (a flame at the delivery tube can flash back into the flask), use dilute acid and add it gradually through the funnel, and never let the thistle funnel\'s stem rise above the liquid or gas escapes unnoticed. These small details are exactly what practical-exam vivas probe.',
                    },
                ],
                'fun_fact': 'The squeaky-pop chemistry of hydrogen is the same reaction that lifted — and destroyed — the airship Hindenburg in 1937; modern airships use helium, which gives no pop because it cannot burn at all.',
                'quiz': [
                    {
                        'q': 'In the preparation of O₂ from H₂O₂, the MnO₂…',
                        'options': ['Is used up as a reactant', 'Acts as a catalyst and is recovered unchanged', 'Provides the oxygen atoms', 'Neutralises the acid'],
                        'answer': 1,
                        'explain': '2H₂O₂ → 2H₂O + O₂. MnO₂ only speeds up the decomposition; the oxygen comes from the peroxide, and the MnO₂ mass is unchanged.',
                    },
                    {
                        'q': 'CO₂ is collected by upward displacement of air because it is…',
                        'options': ['Lighter than air and insoluble', 'Denser than air and fairly soluble in water', 'A coloured gas', 'Explosive over water'],
                        'answer': 1,
                        'explain': 'Its solubility makes water collection wasteful, and being ~1.5× denser than air it sinks into an upright jar.',
                    },
                    {
                        'q': 'A glowing splint relights when thrust into a jar of…',
                        'options': ['Hydrogen', 'Carbon dioxide', 'Oxygen', 'Nitrogen'],
                        'answer': 2,
                        'explain': 'Pure oxygen accelerates combustion so strongly that a merely glowing splint bursts back into flame.',
                    },
                    {
                        'q': 'The balanced equation for preparing hydrogen is…',
                        'options': ['Zn + HCl → ZnCl + H', 'Zn + 2HCl → ZnCl₂ + H₂', '2Zn + 2HCl → 2ZnCl + H₂', 'Zn + H₂SO₄ → ZnSO₄ + 2H'],
                        'answer': 1,
                        'explain': 'One zinc atom displaces two hydrogens from two HCl molecules: Zn + 2HCl → ZnCl₂ + H₂↑.',
                    },
                ],
            },
            {
                'slug': 'water-of-crystallization',
                'title': 'Water of Crystallization',
                'icon': 'scale',
                'minutes': 18,
                'sim': 'nebchemistry/water-crystallization',
                'sim_type': 'lab3d',
                'summary': 'Weigh hydrated copper sulphate into a crucible, heat it until the blue turns white, and reweigh repeatedly until constant mass — then calculate x in CuSO₄·xH₂O from your own readings.',
                'objectives': [
                    'Define water of crystallization and hydrated versus anhydrous salts',
                    'Carry out the heat-cool-weigh cycle to constant mass and explain why it matters',
                    'Record masses correctly and compute the mass of water lost',
                    'Convert masses to moles and determine x in CuSO₄·xH₂O',
                    'List the main sources of error in a gravimetric experiment',
                ],
                'knowledge': [
                    {
                        'heading': 'Water hidden inside a crystal',
                        'body': 'Many salts crystallise with a fixed number of water molecules chemically bonded into their crystal lattice — the water of crystallization. Blue vitriol is the textbook case: CuSO₄·5H₂O, with exactly five water molecules per formula unit. This water is not dampness; it is part of the crystal\'s structure, present in an exact stoichiometric ratio, and the deep blue colour depends on it.\n\nGentle heating drives the water off: CuSO₄·5H₂O → CuSO₄ + 5H₂O, and the blue crystals collapse into a white powder of anhydrous copper sulphate. The change is reversible — add a drop of water to the white powder and it flashes blue again (and warms up!), which is why anhydrous CuSO₄ serves as a chemical test for the presence of water.',
                    },
                    {
                        'heading': 'Heating to constant mass',
                        'body': 'The whole experiment hangs on one technique: heating to constant mass. Weigh the empty crucible, add about 2-3 g of the hydrated salt, and weigh again. Heat gently (strong heating decomposes CuSO₄ itself into black CuO — ruining the result), cool, and weigh. Then heat again, cool, and weigh again. Only when two consecutive weighings agree within about 0.02 g can you be sure all the water has gone.\n\nWhy cool before weighing? A hot crucible sets up convection currents around the balance pan that make the reading drift light, and heat damages the balance. Real labs cool the crucible in a desiccator — a sealed vessel with drying agent — so the anhydrous salt cannot reabsorb moisture from the air while cooling, because anhydrous CuSO₄ is hygroscopic and would silently regain mass.',
                    },
                    {
                        'heading': 'From masses to the formula',
                        'body': 'The arithmetic is two mole calculations. Mass of water lost = (initial crucible + sample) − (final constant mass). Mass of anhydrous CuSO₄ = final mass − empty crucible. Then moles of water = mass lost / 18, moles of CuSO₄ = anhydrous mass / 159.6, and x = moles of water / moles of CuSO₄. With careful work x comes out close to 5.\n\nError analysis is where marks are won. Insufficient heating leaves water behind → x too small. Overheating to black CuO changes the residue\'s identity → calculation invalid. Weighing hot → mass reads low. Letting the residue stand in humid air → it reabsorbs water and x drifts low for the wrong reason. Every error should be stated with its direction — that is the difference between a pass and a distinction in the practical report.',
                    },
                ],
                'fun_fact': 'Silica gel sachets in shoe boxes and phone packaging work on the same principle in reverse — and the orange-to-green colour change of indicating silica gel is itself a hydration colour change, just like white CuSO₄ turning blue.',
                'quiz': [
                    {
                        'q': 'Water of crystallization is…',
                        'options': ['Moisture stuck on the crystal surface', 'A fixed number of water molecules bonded inside the crystal lattice', 'Water used to dissolve the salt', 'Water produced when the salt burns'],
                        'answer': 1,
                        'explain': 'It is structural water present in exact stoichiometric proportion — CuSO₄·5H₂O always has exactly 5 H₂O per CuSO₄.',
                    },
                    {
                        'q': '"Heating to constant mass" guarantees that…',
                        'options': ['The crucible is clean', 'All the water of crystallization has been driven off', 'The salt has melted', 'The balance is calibrated'],
                        'answer': 1,
                        'explain': 'If mass stops changing between successive heat-cool-weigh cycles, no more water is leaving — dehydration is complete.',
                    },
                    {
                        'q': 'A student weighs the crucible while still hot. The recorded mass will be…',
                        'options': ['Too high', 'Too low, due to convection currents', 'Exactly correct', 'Negative'],
                        'answer': 1,
                        'explain': 'Hot air rising around the pan buoys it up, so the balance reads light. Always cool (ideally in a desiccator) before weighing.',
                    },
                    {
                        'q': '2.50 g of CuSO₄·xH₂O leaves 1.60 g of white residue. Moles of water lost ÷ moles of CuSO₄ ≈ (H₂O = 18, CuSO₄ = 159.6)',
                        'options': ['2', '3', '5', '7'],
                        'answer': 2,
                        'explain': 'Water lost = 0.90 g = 0.050 mol; CuSO₄ = 1.60/159.6 = 0.010 mol; x = 0.050/0.010 = 5.',
                    },
                ],
            },
        ],
    },
] + _C12
