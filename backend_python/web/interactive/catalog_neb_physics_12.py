COURSES = [
    {
        'slug': 'neb-physics-practical-12',
        'title': 'NEB Physics Practicals — Class 12',
        'category': 'physics',
        'age_range': '17-18',
        'level': 'Advanced',
        'icon': 'electric_meter',
        'color': '#B45309',
        'tagline': 'Sound, electricity and optics — the full Class 12 NEB practical set as hands-on virtual experiments with real instruments.',
        'description': 'The Class 12 NEB practical exam is all about waves, circuits and light: resonance tubes, sonometers, meter bridges, potentiometers, galvanometers, optical benches and prisms. This course gives you a working virtual version of each apparatus. You hunt for resonance by ear, chase galvanometer nulls with a jockey, remove parallax on an optical bench and sweep a ray through minimum deviation — recording data tables and computing results exactly as the board examiner expects.',
        'skills': [
            'Locating resonance and null points precisely',
            'Wiring and reading electrical meters',
            'Tabulating V-I, balance-length and u-v data',
            'Graphical analysis: slopes, intercepts and minima',
            'Error analysis and standard precautions',
        ],
        'lessons': [
            {
                'slug': 'resonance-air-column',
                'title': 'Resonance Tube: Speed of Sound',
                'icon': 'graphic_eq',
                'minutes': 16,
                'sim': 'nebphysics/resonance-tube',
                'sim_type': '3d',
                'summary': 'Strike a tuning fork, slide the water level down the tube and catch the two loudness peaks — then v = 2f(l₂ − l₁) gives the speed of sound in the room.',
                'objectives': [
                    'Explain resonance of a closed air column at odd quarter-wavelengths',
                    'Locate the first and second resonance lengths by loudness',
                    'Compute v = 2f(l₂ − l₁) and compare with 331.4 + 0.6t m/s',
                    'Explain why the difference method cancels the end correction',
                ],
                'knowledge': [
                    {
                        'heading': 'Standing waves in a closed pipe',
                        'body': 'A tube closed at the bottom by water supports standing waves with a node at the water surface and an antinode just above the open top. That happens when the air column length is an odd number of quarter wavelengths: l = λ/4, 3λ/4, 5λ/4… So as you lower the water with a fork of frequency f singing above the tube, the sound swells dramatically at l₁ ≈ λ/4 and again at l₂ ≈ 3λ/4.\n\nSubtracting, l₂ − l₁ = λ/2 exactly, so v = fλ = 2f(l₂ − l₁). The antinode actually forms slightly ABOVE the tube mouth — the end correction e ≈ 0.3 × diameter — but because it shifts l₁ and l₂ equally, the subtraction wipes it out. That cancellation is the whole genius of the two-resonance method.',
                    },
                    {
                        'heading': 'Procedure: hunting the loud spots',
                        'body': 'Strike the fork on a rubber pad (never on the bench — it dents the prongs and changes f) and hold it horizontally just above the tube mouth. Lower the reservoir slowly; the hum swells to a maximum and fades. Bracket the loudest point from both directions and read the water level on the metre scale — that is l₁. Continue down to find l₂.\n\nA fork rings for only a few seconds, so re-strike often. Take each length twice (water falling and rising) and average. With f = 512 Hz at 25 °C expect l₁ ≈ 16 cm and l₂ ≈ 49 cm, giving v ≈ 343 m/s. The accepted value at temperature t °C is v = 331.4 + 0.6t, so always note the room temperature.',
                    },
                    {
                        'heading': 'Errors and precautions',
                        'body': 'Judging "loudest" by ear is the dominant random error — repeat and average. Temperature matters: sound travels about 0.6 m/s faster per degree, so a chilly morning lab and a warm afternoon lab disagree by several m/s. Humid air is slightly faster again.\n\nFurther precautions for the report: keep the fork\u2019s prongs vibrating in a vertical plane just above the mouth without touching the tube, avoid noisy surroundings, read the scale at eye level, and use l₂ − l₁ rather than l₁ alone so the end correction cancels. Examiners often ask: "Why is the second resonance fainter?" — because the column loses more energy at the larger length.',
                    },
                ],
                'fun_fact': 'Thunder lets you use the speed of sound for free: count seconds between lightning and thunder and divide by three to get the storm\u2019s distance in kilometres.',
                'quiz': [
                    {
                        'q': 'For a closed air column, resonance occurs when l equals:',
                        'options': ['λ/2, λ, 3λ/2…', 'λ/4, 3λ/4, 5λ/4…', 'Any multiple of λ', 'λ/3, 2λ/3…'],
                        'answer': 1,
                        'explain': 'A node at the water and an antinode at the open end require odd quarter-wavelengths.',
                    },
                    {
                        'q': 'With f = 512 Hz, l₁ = 16.0 cm and l₂ = 49.4 cm, v ≈ ?',
                        'options': ['327 m/s', '342 m/s', '512 m/s', '171 m/s'],
                        'answer': 1,
                        'explain': 'v = 2f(l₂ − l₁) = 2 × 512 × 0.334 ≈ 342 m/s.',
                    },
                    {
                        'q': 'The two-resonance method is preferred over using l₁ alone because:',
                        'options': ['It is louder', 'The end correction cancels in l₂ − l₁', 'It needs no tuning fork', 'Water level is easier to read'],
                        'answer': 1,
                        'explain': 'Both lengths are shifted by the same end correction e, so their difference is exactly λ/2 regardless of e.',
                    },
                ],
            },
            {
                'slug': 'sonometer-laws',
                'title': 'Sonometer: Laws of Vibrating Strings',
                'icon': 'music_note',
                'minutes': 16,
                'sim': 'nebphysics/sonometer',
                'sim_type': '3d',
                'summary': 'Slide the bridge and pile on weights until the paper rider leaps off the wire — resonance! — then verify that f×L stays constant for each fork.',
                'objectives': [
                    'State the laws of length and tension for vibrating strings',
                    'Use a paper rider to detect resonance between wire and fork',
                    'Verify fL = constant at fixed tension',
                    'Relate the sonometer equation f = (1/2L)√(T/μ) to the data',
                ],
                'knowledge': [
                    {
                        'heading': 'The vibrating string equation',
                        'body': 'A stretched wire of vibrating length L, tension T and mass per unit length μ has fundamental frequency f = (1/2L)√(T/μ). Three laws fall out: the law of length (f ∝ 1/L), the law of tension (f ∝ √T) and the law of mass (f ∝ 1/√μ). The sonometer — a wire over two movable bridges on a hollow sounding box — is built to test them.\n\nFor the law of length you keep the load fixed and find the resonant lengths for several forks: each product f × L should come out the same number. Doubling the frequency must exactly halve the length, like fretting a guitar string at its midpoint to jump an octave.',
                    },
                    {
                        'heading': 'The paper rider trick',
                        'body': 'The wire\u2019s vibration is far too small to see. The classic detector is a tiny inverted-V paper rider straddling the wire midway between the bridges. Strike the fork, press its stem on the sounding box, and adjust the bridge in millimetre steps. Off resonance the rider sits still; at resonance the wire suddenly vibrates with large amplitude and the rider dances and is flung off.\n\nWhy the midpoint? The fundamental mode has its antinode there, so the rider feels the maximum motion. Approach resonance from both sides and take the mean of the two bridge positions where the rider just jumps — that brackets the true resonant length.',
                    },
                    {
                        'heading': 'Tension, errors, precautions',
                        'body': 'The tension is supplied by a hanging load: T = Mg, and you must include the hanger\u2019s own mass. For the law of tension, fix one fork and find the resonant length at several loads — L should grow as √T, so a graph of L² against T is a straight line.\n\nError sources: friction at the pulley makes the true tension differ from Mg; the wire may be kinked or non-uniform (μ varies); the bridges must be knife-sharp so the vibrating length is well defined; and the fork loses frequency if struck violently. Precautions: strike gently on rubber, press the stem firmly on the box for good energy transfer, and keep the rider tiny so it does not load the wire.',
                    },
                ],
                'fun_fact': 'The sarangi and the sitar obey the same f = (1/2L)√(T/μ) — every tuning peg twist is a live "law of tension" experiment.',
                'quiz': [
                    {
                        'q': 'At fixed tension, a 256 Hz fork resonates at 60 cm. A 512 Hz fork will resonate at about:',
                        'options': ['120 cm', '60 cm', '30 cm', '15 cm'],
                        'answer': 2,
                        'explain': 'f ∝ 1/L at fixed T, so doubling f halves the resonant length to 30 cm.',
                    },
                    {
                        'q': 'To double a wire\u2019s fundamental frequency by changing tension alone, T must become:',
                        'options': ['2T', '4T', '√2 T', 'T/2'],
                        'answer': 1,
                        'explain': 'f ∝ √T, so doubling f needs four times the tension.',
                    },
                    {
                        'q': 'The paper rider is placed midway between the bridges because:',
                        'options': ['It balances better there', 'The fundamental\u2019s antinode (maximum amplitude) is at the middle', 'The wire is coolest there', 'The node is at the middle'],
                        'answer': 1,
                        'explain': 'The fundamental mode has nodes at the bridges and its single antinode at the centre, so the rider is thrown off most easily there.',
                    },
                ],
            },
            {
                'slug': 'ohms-law-resistivity',
                'title': "Ohm's Law & Resistivity",
                'icon': 'electric_bolt',
                'minutes': 16,
                'sim': 'nebphysics/ohms-law',
                'sim_type': '3d',
                'summary': 'Slide the rheostat, log ammeter-voltmeter pairs into a table, draw the V-I line and turn its slope into the resistivity of the wire on your bench.',
                'objectives': [
                    'Verify Ohm\u2019s law from a straight V-I graph',
                    'Wire ammeter in series and voltmeter in parallel correctly',
                    'Determine R from the slope and ρ = πd²R/4L from the wire\u2019s dimensions',
                    'Explain why heating of the wire must be avoided during readings',
                ],
                'knowledge': [
                    {
                        'heading': 'Ohm\u2019s law and what can break it',
                        'body': 'Ohm\u2019s law states that at constant temperature the current through a metallic conductor is proportional to the potential difference across it: V = IR. On a V-I graph the data should fall on a straight line through the origin whose slope is the resistance R.\n\nThe law is not universal — filament bulbs curve (they heat up), diodes conduct one way only. Even your test wire disobeys if the current heats it, which is why alloys like constantan and manganin, whose resistance barely changes with temperature, are the standard samples, and why you close the key only briefly for each reading.',
                    },
                    {
                        'heading': 'Circuit and procedure',
                        'body': 'The circuit: battery → plug key → rheostat → ammeter, all in SERIES with the test wire, and the voltmeter in PARALLEL across the wire alone. The ammeter has tiny resistance so it does not disturb the current; the voltmeter has very high resistance so it steals almost none.\n\nSlide the rheostat to set five or six well-spread currents, recording V and I each time. Plot V against I, draw the best-fit line and read R from the slope — more reliable than any single V/I ratio. Then measure the wire\u2019s length L with a metre scale and diameter d with a screw gauge (several places, two perpendicular directions), and compute ρ = RA/L = πd²R/4L.',
                    },
                    {
                        'heading': 'Why your ρ may be off',
                        'body': 'The diameter enters squared, so a 2% error in d becomes 4% in ρ — measure d most carefully of all. Connections add contact resistance; clean the wire ends. The voltmeter, if cheap, draws current and makes the ammeter read slightly high. And if you leave the key closed, Joule heating raises R as you watch.\n\nTypical values to expect: constantan ρ ≈ 49 × 10⁻⁸ Ω·m, nichrome ≈ 110 × 10⁻⁸ Ω·m, copper just 1.7 × 10⁻⁸ Ω·m (too small to measure well this way). Quoting your result with units and comparing against the accepted value is exactly what the examiner wants in the conclusion.',
                    },
                ],
                'fun_fact': 'Nepal\u2019s long rural transmission lines are aluminium, not copper — aluminium has higher resistivity but is so much lighter and cheaper per ohm that the economics win.',
                'quiz': [
                    {
                        'q': 'In the Ohm\u2019s law circuit, the voltmeter is connected:',
                        'options': ['In series with the wire', 'In parallel across the test wire', 'In series with the battery only', 'Across the ammeter'],
                        'answer': 1,
                        'explain': 'A voltmeter measures potential difference across an element, so it goes in parallel with the wire; its high resistance keeps it from diverting current.',
                    },
                    {
                        'q': 'A V-I graph through the origin has slope 4.0. The sample\u2019s resistance is:',
                        'options': ['0.25 Ω', '4.0 Ω', '16 Ω', 'Cannot tell'],
                        'answer': 1,
                        'explain': 'V = IR means slope ΔV/ΔI = R = 4.0 Ω.',
                    },
                    {
                        'q': 'A 2% error in measuring wire diameter d produces what error in ρ?',
                        'options': ['1%', '2%', 'About 4%', 'None'],
                        'answer': 2,
                        'explain': 'ρ = πd²R/4L depends on d², so fractional errors in d are doubled — measure the diameter with the screw gauge very carefully.',
                    },
                    {
                        'q': 'Why use constantan rather than copper for the test wire?',
                        'options': ['It is shinier', 'Its resistance is conveniently large and nearly independent of temperature', 'It is magnetic', 'It is cheaper than copper'],
                        'answer': 1,
                        'explain': 'Constantan\u2019s high resistivity gives a measurable R in a short wire, and its tiny temperature coefficient keeps R steady while current flows.',
                    },
                ],
            },
            {
                'slug': 'meter-bridge',
                'title': 'Meter Bridge: Unknown Resistance',
                'icon': 'balance',
                'minutes': 15,
                'sim': 'nebphysics/meter-bridge',
                'sim_type': '3d',
                'summary': 'Tap the jockey along a one-metre wire until the galvanometer sits dead on zero, then let X = R(100 − l)/l expose the unknown resistor.',
                'objectives': [
                    'Explain the Wheatstone bridge balance condition',
                    'Locate the null point with a jockey on the bridge wire',
                    'Calculate X = R(100 − l)/l from the balancing length',
                    'Use the interchange method to cancel end errors',
                ],
                'knowledge': [
                    {
                        'heading': 'A Wheatstone bridge made of wire',
                        'body': 'The meter bridge is a folded Wheatstone bridge: known resistance R in the left gap, unknown X in the right gap, and a uniform 1 m constantan wire as the other two arms. A jockey tapped at distance l from the left end splits the wire into resistances proportional to l and (100 − l).\n\nAt the null point the galvanometer reads zero — no current crosses the bridge — and the balance condition gives R/X = l/(100 − l), so X = R(100 − l)/l. No meter calibration matters at balance: the galvanometer only needs to show ZERO honestly, which is why bridge methods beat ammeter-voltmeter methods for precision.',
                    },
                    {
                        'heading': 'Procedure for a sharp null',
                        'body': 'Choose R from the resistance box so the balance lands near the middle of the wire (between 40 and 60 cm) — there the bridge is most sensitive and percentage errors in l are smallest. Tap the jockey briefly; never drag it, or you scrape the wire and change its cross-section.\n\nFind the deflection direction at both ends first (it must reverse — otherwise a connection is broken), then close in on zero. Record l, then INTERCHANGE R and X and balance again: the average of X from both positions cancels the small "end resistances" where the wire is soldered to the copper strips. Repeat for two or three different R values.',
                    },
                    {
                        'heading': 'Errors and standard viva questions',
                        'body': 'Sources of error: the wire may not be perfectly uniform (the biggest one), end/contact resistances at the copper strips, heating of the wire if current flows too long, and a blunt jockey contact. Precautions: use the key only while tapping, keep balance near 50 cm, interchange and average, and never press hard with the jockey.\n\nClassic viva questions: "Why is the galvanometer not damaged at balance?" (no current flows through it), "Why constantan wire?" (uniform, high resistivity, low temperature coefficient), and "Why is the method unsuitable for very low or very high resistances?" (end resistances and insensitivity dominate when X is far from R).',
                    },
                ],
                'fun_fact': 'Charles Wheatstone did not invent his bridge — Samuel Christie did in 1833 — but Wheatstone popularised it so well that even your NEB practical sheet carries his name.',
                'quiz': [
                    {
                        'q': 'Balance occurs at l = 40 cm with R = 6 Ω in the left gap. X = ?',
                        'options': ['4 Ω', '9 Ω', '6 Ω', '2.4 Ω'],
                        'answer': 1,
                        'explain': 'X = R(100 − l)/l = 6 × 60/40 = 9 Ω.',
                    },
                    {
                        'q': 'At the exact null point, the current through the galvanometer is:',
                        'options': ['Maximum', 'Half the total', 'Zero', 'Equal to the battery current'],
                        'answer': 2,
                        'explain': 'Balance means the two bridge points are at equal potential, so no current crosses the galvanometer branch.',
                    },
                    {
                        'q': 'Why should the balance point lie near the middle of the wire?',
                        'options': ['The wire is thicker there', 'Bridge sensitivity is highest and the percentage error in l is lowest', 'The galvanometer prefers it', 'It saves time'],
                        'answer': 1,
                        'explain': 'Near 50 cm a 1 mm uncertainty in l produces the smallest relative error in the ratio l/(100 − l).',
                    },
                ],
            },
            {
                'slug': 'potentiometer-emf',
                'title': 'Potentiometer: Comparing EMFs',
                'icon': 'settings_input_component',
                'minutes': 16,
                'sim': 'nebphysics/potentiometer',
                'sim_type': '3d',
                'summary': 'Balance two cells one after another on a four-metre wire and let E₁/E₂ = l₁/l₂ compare their EMFs — without drawing a single microamp from either.',
                'objectives': [
                    'Explain the principle of the potentiometer (potential drop ∝ length)',
                    'Find balancing lengths for two cells with a jockey',
                    'Compute E₁/E₂ = l₁/l₂ and explain why it measures true EMF',
                    'State why the driver-cell voltage must exceed both EMFs',
                ],
                'knowledge': [
                    {
                        'heading': 'Why a potentiometer beats a voltmeter',
                        'body': 'A voltmeter must draw a little current to deflect, and that current causes a drop across the cell\u2019s internal resistance — so a voltmeter always reads slightly LESS than the true EMF. The potentiometer dodges this completely: at balance, the cell drives zero current, so nothing is lost internally and the balancing length measures the genuine EMF.\n\nThe principle: a steady current from a driver cell flows down a long uniform wire, so potential falls linearly with distance — a constant gradient k volts per centimetre. A point l cm from the start sits at potential kl below the start.',
                    },
                    {
                        'heading': 'Procedure: two balances, one ratio',
                        'body': 'Connect the driver circuit (accumulator, key, rheostat) across the full wire. Connect cell 1 between the wire\u2019s start and the galvanometer-jockey, with like poles (both positives) at the same end — otherwise no balance exists anywhere. Slide the jockey until the galvanometer is null: that is l₁, where kl₁ = E₁. Switch the two-way key to cell 2 and find l₂.\n\nDividing kills the unknown gradient: E₁/E₂ = l₁/l₂. Everything depends on the driver current staying constant, so do NOT touch the rheostat between the two balances, and check l₁ again at the end — if it has drifted, the driver cell is sagging and the run must be repeated.',
                    },
                    {
                        'heading': 'Sensitivity, errors, precautions',
                        'body': 'A longer balancing length means a smaller percentage error, so adjust the rheostat to push balances toward the far end of the wire. The wire must be uniform — its non-uniformity is the chief systematic error. Contact must be gentle: dragging the jockey scrapes the wire thin.\n\nIf the galvanometer deflects the same way at both ends of the wire, either the driver voltage is below the cell\u2019s EMF (gradient too small — reduce the series rheostat) or a polarity is reversed. Standard viva: "Why is the potentiometer called an ideal voltmeter?" — because it draws no current at balance; effectively infinite resistance.',
                    },
                ],
                'fun_fact': 'Before digital meters, national standards labs kept the volt itself on potentiometers balanced against Weston standard cells — the same null method you are practising.',
                'quiz': [
                    {
                        'q': 'Cell 1 balances at 290 cm and cell 2 at 216 cm. E₁/E₂ = ?',
                        'options': ['0.74', '1.34', '1.45', '2.16'],
                        'answer': 1,
                        'explain': 'E₁/E₂ = l₁/l₂ = 290/216 ≈ 1.34.',
                    },
                    {
                        'q': 'The potentiometer measures TRUE EMF because at balance:',
                        'options': ['The wire has no resistance', 'The cell supplies zero current, so no internal drop occurs', 'The galvanometer amplifies the voltage', 'The driver cell is disconnected'],
                        'answer': 1,
                        'explain': 'Null deflection means no current through the cell branch; with I = 0 there is no Ir loss inside the cell and the wire segment matches the full EMF.',
                    },
                    {
                        'q': 'No balance can be found anywhere on the wire. A likely cause is:',
                        'options': ['The wire is too uniform', 'Driver potential across the wire is smaller than the cell\u2019s EMF', 'The galvanometer is too sensitive', 'The jockey is too light'],
                        'answer': 1,
                        'explain': 'If the total drop along the wire is less than E, the potential kl can never reach the cell\u2019s EMF — reduce the series resistance or use a stronger driver.',
                    },
                ],
            },
            {
                'slug': 'galvanometer-figure-of-merit',
                'title': 'Galvanometer: Figure of Merit',
                'icon': 'speed',
                'minutes': 14,
                'sim': 'nebphysics/galvanometer',
                'sim_type': '3d',
                'summary': 'Feed a galvanometer tiny known currents through a high-resistance box, read the deflection in divisions, and compute k = I/θ — the current behind each division.',
                'objectives': [
                    'Define figure of merit k = I/θ and current sensitivity',
                    'Vary the series resistance and record deflections',
                    'Compute k = E/(R + G)θ for each setting and average',
                    'Calculate the current Ig for full-scale deflection',
                ],
                'knowledge': [
                    {
                        'heading': 'What the figure of merit means',
                        'body': 'A moving-coil galvanometer deflects in proportion to the current through its coil: θ divisions for current I, with k = I/θ the figure of merit — the current needed per division of deflection. A typical school galvanometer has k around 10⁻⁵ A/div: a 30-division scale therefore reaches full deflection at Ig = 30k, well under a milliamp.\n\nKnowing k is the gateway to building real meters: converting the galvanometer to an ammeter needs a shunt resistance carrying everything beyond Ig, and converting to a voltmeter needs a high series resistance. Both calculations begin with the k you measure here.',
                    },
                    {
                        'heading': 'Circuit and calculation',
                        'body': 'Connect a cell of EMF E, a plug key, a high resistance box R and the galvanometer (resistance G) all in series. The current is I = E/(R + G), so the deflection obeys θ = E/[k(R + G)]. Choose R values (a few thousand ohms) that give deflections spread between about 5 and 29 divisions, and record (R, θ) pairs.\n\nFor each pair compute k = E/[(R + G)θ] and take the mean. Even better, plot 1/θ against R: the points form a straight line with slope k/E, giving k graphically and exposing any rogue reading. G itself is usually supplied, or measured separately by the half-deflection method.',
                    },
                    {
                        'heading': 'Precautions and the half-deflection idea',
                        'body': 'Never connect the galvanometer without the high resistance — full battery current would slam and possibly burn the coil. Start with the LARGEST R, close the key only briefly for each reading, and tap the case gently so the needle settles without sticking. Read at eye level to dodge parallax on the mirror scale.\n\nThe related half-deflection method finds G: with deflection θ at resistance R, add a shunt S across the galvanometer and adjust until deflection halves; then G = RS/(R − S) ≈ S when R is large. Examiners pair these two experiments constantly, so know both formulas.',
                    },
                ],
                'fun_fact': 'Early submarine telegraph operators read messages from a mirror galvanometer\u2019s light spot trembling across a wall — detecting microamps that crossed entire oceans.',
                'quiz': [
                    {
                        'q': 'E = 2 V, R = 4900 Ω, G = 100 Ω gives θ = 20 div. k = ?',
                        'options': ['2 × 10⁻⁵ A/div', '4 × 10⁻⁴ A/div', '10⁻⁴ A/div', '5 × 10⁻⁶ A/div'],
                        'answer': 0,
                        'explain': 'I = 2/5000 = 4 × 10⁻⁴ A; k = I/θ = 4 × 10⁻⁴/20 = 2 × 10⁻⁵ A per division.',
                    },
                    {
                        'q': 'With k = 2 × 10⁻⁵ A/div and a 30-division scale, full-scale current Ig = ?',
                        'options': ['0.6 mA', '6 mA', '60 mA', '0.06 mA'],
                        'answer': 0,
                        'explain': 'Ig = k × 30 = 6 × 10⁻⁴ A = 0.6 mA.',
                    },
                    {
                        'q': 'Why must a high resistance always be in series with the galvanometer here?',
                        'options': ['To increase deflection', 'To limit the current to microamp levels and protect the delicate coil', 'To heat the circuit', 'To charge the cell'],
                        'answer': 1,
                        'explain': 'The coil tolerates only tiny currents; without the resistance box the battery would drive far more than full-scale current and damage it.',
                    },
                ],
            },
            {
                'slug': 'focal-length-mirror-lens',
                'title': 'Focal Length of Mirrors & Lenses',
                'icon': 'center_focus_strong',
                'minutes': 17,
                'sim': 'nebphysics/focal-length',
                'sim_type': '3d',
                'summary': 'Slide pins along an optical bench, kill the parallax between pin and image, log u-v pairs and let both the formula and the 1/v-1/u graph reveal f.',
                'objectives': [
                    'Apply the mirror/lens formula through the u-v method',
                    'Remove parallax to locate a real image precisely',
                    'Compute f = uv/(u + v) and average over several pairs',
                    'Interpret the straight-line 1/v vs 1/u graph and its intercepts',
                ],
                'knowledge': [
                    {
                        'heading': 'The u-v method',
                        'body': 'For a concave mirror or convex lens forming a real image, object distance u and image distance v obey 1/f = 1/u + 1/v (using positive magnitudes for real objects and images). Measure several (u, v) pairs and each yields f = uv/(u + v); their mean is your result.\n\nEven better is the graph: plotting 1/v against 1/u gives a straight line of slope −1 whose intercepts on both axes equal 1/f. A quick rough start: aim the mirror at a distant window — parallel rays converge at the focus, giving an approximate f so you know where to place pins.',
                    },
                    {
                        'heading': 'Parallax: how you "see" an invisible image',
                        'body': 'A real aerial image floats in space with nothing on it to look at directly — so we use parallax. Place the image pin roughly where the image seems to be and move your eye side to side: if pin and image shift relative to each other, they are at different distances. Adjust the pin until they stay locked together from every angle: no parallax, and the pin tip now stands exactly at the image.\n\nKeep all pin tips, the lens centre (optical centre) and the mirror pole at the same height on the bench axis. Note also the index correction: the pin\u2019s position is read from the bench scale, but distances should be measured to the lens/mirror surface — subtract holder offsets.',
                    },
                    {
                        'heading': 'Choosing distances and avoiding bad data',
                        'body': 'Place the object BEYOND the focus, or no real image exists — inside f the image becomes virtual, upright and unreachable by the image pin. Avoid u ≈ f (image races off the bench, huge and dim) and u ≈ v ≈ 2f only as one of several points (it is the symmetric case where the image is the same size as the object).\n\nSpread your u values from just beyond f out to about 3f for a well-conditioned graph. Error sources: parallax judged carelessly, bench scale misread, thick lens treated as thin, and the pin not at the principal axis height. Quote f to a sensible precision (0.1 cm) with the mean and the graph value side by side.',
                    },
                ],
                'fun_fact': 'Your eye runs the same lens formula continuously: ciliary muscles retune the focal length every time your gaze jumps from your copy to the whiteboard.',
                'quiz': [
                    {
                        'q': 'For a convex lens, u = 30 cm gives a sharp real image at v = 30 cm. f = ?',
                        'options': ['30 cm', '60 cm', '15 cm', '7.5 cm'],
                        'answer': 2,
                        'explain': 'f = uv/(u + v) = 900/60 = 15 cm. u = v = 2f is the symmetric configuration.',
                    },
                    {
                        'q': '"No parallax" between image pin and image means:',
                        'options': ['They look equally bright', 'They do not shift relative to each other as the eye moves — same position in space', 'The pin is taller', 'The image vanishes'],
                        'answer': 1,
                        'explain': 'Zero relative shift with eye movement is the test that two things are at the same distance — the pin tip then marks the image location.',
                    },
                    {
                        'q': 'An object placed INSIDE the focal length of a convex lens gives:',
                        'options': ['A real inverted image', 'No image at all', 'A virtual, erect, magnified image that the image pin cannot locate', 'A real image at 2f'],
                        'answer': 2,
                        'explain': 'Inside f the rays diverge after the lens; the image is virtual and on the same side, so the u-v real-image method fails there.',
                    },
                    {
                        'q': 'The 1/v versus 1/u graph for this experiment is:',
                        'options': ['A parabola', 'A straight line with intercepts 1/f on both axes', 'A circle', 'A horizontal line'],
                        'answer': 1,
                        'explain': '1/v = −1/u + 1/f is linear with slope −1; setting either variable to zero gives intercept 1/f.',
                    },
                ],
            },
            {
                'slug': 'prism-minimum-deviation',
                'title': 'Prism: Angle of Minimum Deviation',
                'icon': 'change_history',
                'minutes': 17,
                'sim': 'nebphysics/prism-deviation',
                'sim_type': '3d',
                'summary': 'Sweep the incident ray across a 60° prism, watch the deviation dip through a minimum, and convert Dₘ into the refractive index of the glass.',
                'objectives': [
                    'Trace a ray through a prism using Snell\u2019s law at both faces',
                    'Record (i, D) pairs and plot the deviation curve',
                    'Locate the minimum deviation Dₘ and the symmetry i = e',
                    'Compute n = sin((A + Dₘ)/2) / sin(A/2)',
                ],
                'knowledge': [
                    {
                        'heading': 'Geometry of deviation',
                        'body': 'Light entering a prism refracts toward the normal at the first face, crosses the glass, and refracts away at the second face. Two relations carry the whole experiment: r₁ + r₂ = A (the refraction angles meet the apex angle) and D = i + e − A (total deviation is what is left of the entry and exit bends).\n\nAs you raise i from grazing values, D first decreases, reaches a single minimum Dₘ, then increases — a U-shaped curve. At the minimum the ray passes SYMMETRICALLY: i = e, r₁ = r₂ = A/2, and the ray inside runs parallel to the base. Symmetry is why the minimum is unique.',
                    },
                    {
                        'heading': 'From Dₘ to the refractive index',
                        'body': 'At minimum deviation, Snell\u2019s law at the first face reads sin i = n sin r₁ with i = (A + Dₘ)/2 and r₁ = A/2. Hence n = sin[(A + Dₘ)/2] / sin(A/2). For a 60° crown-glass prism, Dₘ ≈ 39° gives n ≈ 1.52.\n\nIn the pin-and-paper version of this practical you fix the prism on drawing paper, prick two pins along an incident ray and two along the emergent ray, then measure i and D with a protractor for many incidence angles. The simulation replaces the pins with a draggable ray but the data analysis — table, curve, minimum — is identical.',
                    },
                    {
                        'heading': 'Reading the minimum well, and TIR surprises',
                        'body': 'The curve is FLAT near its minimum, which is both a gift and a trap: a small error in i barely changes D (gift), but eyeballing the exact minimum from a couple of points is unreliable (trap). Take many points spaced a few degrees apart around the dip and read Dₘ from a smooth curve through them, never from a single measurement.\n\nAt small incidence angles you may find no emergent ray at all: r₂ exceeds the critical angle and the ray suffers total internal reflection inside the prism. Note it, then continue at larger i. Other precautions: pins (or rays) well separated for direction accuracy, sharp pencil prism outline, protractor read to half a degree, and the same prism face used as entry face throughout.',
                    },
                ],
                'fun_fact': 'A rainbow over the Kathmandu valley is millions of raindrop "prisms" each turning sunlight through its own minimum deviation — about 42° for red light, which fixes the rainbow\u2019s radius in the sky.',
                'quiz': [
                    {
                        'q': 'For a prism, the deviation D equals:',
                        'options': ['i + e − A', 'A − i − e', 'i − e + A', 'A/2'],
                        'answer': 0,
                        'explain': 'The ray bends (i − r₁) at entry and (e − r₂) at exit; adding them and using r₁ + r₂ = A gives D = i + e − A.',
                    },
                    {
                        'q': 'At minimum deviation through a prism:',
                        'options': ['i = 0', 'i = e and the internal ray is parallel to the base', 'e = 90°', 'r₁ = A'],
                        'answer': 1,
                        'explain': 'The minimum occurs at the symmetric passage: equal angles at both faces and the refracted ray parallel to the base.',
                    },
                    {
                        'q': 'A = 60° and Dₘ = 40°. n = ?',
                        'options': ['sin 50°/sin 30° ≈ 1.53', 'sin 40°/sin 60° ≈ 0.74', 'sin 100°/sin 60° ≈ 1.14', 'sin 20°/sin 30° ≈ 0.68'],
                        'answer': 0,
                        'explain': 'n = sin[(A + Dₘ)/2]/sin(A/2) = sin 50°/sin 30° ≈ 0.766/0.5 ≈ 1.53.',
                    },
                    {
                        'q': 'Why should Dₘ be read from a smooth curve through many points rather than one reading?',
                        'options': ['The protractor only works on curves', 'The D-i curve is flat near the minimum, so a single point cannot locate Dₘ reliably', 'D changes with time', 'The prism heats up'],
                        'answer': 1,
                        'explain': 'Near the minimum, widely different i values give nearly equal D; only a fitted curve through the dip pins down Dₘ precisely.',
                    },
                ],
            },
        ],
    },
]
