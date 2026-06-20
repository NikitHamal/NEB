from .catalog_neb_physics_12 import COURSES as _C12

COURSES = [
    {
        'slug': 'neb-physics-practical-11',
        'title': 'NEB Physics Practicals — Class 11',
        'category': 'physics',
        'age_range': '16-17',
        'level': 'Intermediate',
        'icon': 'straighten',
        'color': '#D97706',
        'tagline': 'Every Class 11 NEB physics practical as a realistic virtual lab — measure, record and compute like a real scientist.',
        'description': 'This course walks you through the complete NEB Class 11 physics practical syllabus with one working virtual instrument per experiment. You will read a real vernier scale, time a pendulum with your own reflexes, balance forces on a Gravesand board and find the specific heat of a metal — taking readings, filling tables and computing results exactly the way you will in the school lab and the board practical exam. Every formula, least count and source of error matches the standard NEB lab manual.',
        'skills': [
            'Reading vernier, screw gauge and spherometer scales',
            'Recording observations and tabulating data',
            'Plotting graphs and extracting slopes',
            'Estimating errors and writing precautions',
            'Verifying laws of mechanics and heat',
        ],
        'lessons': [
            {
                'slug': 'vernier-calipers',
                'title': 'Vernier Calipers',
                'icon': 'straighten',
                'minutes': 15,
                'sim': 'nebphysics/vernier-calipers',
                'sim_type': 'lab3d',
                'summary': 'Grip a sphere, cylinder or beaker in virtual vernier jaws, find the coincident division on the magnified scale and compute the reading — with random zero errors to keep you honest.',
                'objectives': [
                    'State and compute the least count of a vernier calipers',
                    'Take a reading by combining main scale and vernier coincidence',
                    'Identify positive and negative zero error and apply the correction',
                    'Measure diameter, length and internal depth of regular objects',
                    'List precautions that reduce errors with vernier instruments',
                ],
                'knowledge': [
                    {
                        'heading': 'Why a vernier beats a plain ruler',
                        'body': 'A metre ruler can read to 1 mm at best — your eye simply cannot split a millimetre reliably. The vernier calipers adds a small sliding scale whose 10 divisions span only 9 main-scale millimetres. Because each vernier division is 0.9 mm, exactly one vernier line will coincide with a main-scale line, and which one it is tells you the fraction of a millimetre.\n\nLeast count = 1 MSD − 1 VSD = 1 mm − 0.9 mm = 0.1 mm = 0.01 cm. Total reading = main scale reading (the mark just before the vernier zero) + coincident division × least count. With this trick a Rs 300 instrument measures to a hundredth of a centimetre.',
                    },
                    {
                        'heading': 'Procedure and zero error',
                        'body': 'Close the jaws gently on the object — sphere or cylinder between the outside jaws, a beaker depth with the depth rod or inside jaws. Note the main scale reading just left of the vernier zero, then scan the vernier for the line that exactly coincides with a main-scale line. Repeat at different orientations of a sphere and average, because real spheres are never perfectly round.\n\nBefore measuring, close the jaws fully with nothing inside. If the vernier zero sits right of the main zero the error is positive and must be subtracted from every reading; if it sits left, the error is negative and is added. Corrected reading = observed reading − zero error (with its sign). NEB examiners love asking this correction rule.',
                    },
                    {
                        'heading': 'Sources of error and precautions',
                        'body': 'The biggest error is over-tightening: squeeze a soft object and you measure the squashed size, not the true one. Hold the calipers square to the object — a tilted jaw reads long. Parallax while spotting the coincident line is another classic mistake; view the scales perpendicularly.\n\nPrecautions to write in your report: check and record zero error first, grip gently without pressure, take at least three readings at different places and average, and keep your eye directly above the coincidence. Mentioning instrument wear (loose jaws on an old calipers) earns extra credit as a source of systematic error.',
                    },
                ],
                'fun_fact': 'The vernier scale was invented in 1631 by French mathematician Pierre Vernier — almost 400 years later, students in Kathmandu and Karachi alike still read his scale exactly the same way.',
                'quiz': [
                    {
                        'q': 'A vernier calipers has 10 vernier divisions equal to 9 mm. Its least count is:',
                        'options': ['1 mm', '0.1 mm', '0.01 mm', '0.9 mm'],
                        'answer': 1,
                        'explain': 'LC = 1 MSD − 1 VSD = 1 mm − 0.9 mm = 0.1 mm = 0.01 cm. That is the smallest length it can resolve.',
                    },
                    {
                        'q': 'Main scale reads 2.3 cm, the 7th vernier division coincides. The observed reading is:',
                        'options': ['2.37 cm', '2.307 cm', '2.377 cm', '3.0 cm'],
                        'answer': 0,
                        'explain': 'Reading = MSR + n × LC = 2.3 + 7 × 0.01 = 2.37 cm.',
                    },
                    {
                        'q': 'With jaws fully closed, the vernier zero lies to the RIGHT of the main scale zero. The zero error is:',
                        'options': ['Negative, so add the correction', 'Positive, so subtract it from readings', 'Zero', 'Impossible to correct'],
                        'answer': 1,
                        'explain': 'Vernier zero ahead of main zero means every reading comes out too large — a positive zero error that must be subtracted.',
                    },
                    {
                        'q': 'Why do we measure a sphere\u2019s diameter at several orientations?',
                        'options': ['To wear in the jaws', 'Because spheres are never perfectly round, so we average', 'To change the least count', 'It is not necessary'],
                        'answer': 1,
                        'explain': 'Real objects have slight irregularities; averaging several mutually perpendicular diameters reduces random error.',
                    },
                ],
            },
            {
                'slug': 'screw-gauge',
                'title': 'Micrometer Screw Gauge',
                'icon': 'cyclone',
                'minutes': 14,
                'sim': 'nebphysics/screw-gauge',
                'sim_type': 'lab3d',
                'summary': 'Rotate the thimble until the ratchet clicks on a wire, sheet or even a human hair, then combine the linear and circular scales to read down to 0.01 mm.',
                'objectives': [
                    'Relate pitch and number of circular divisions to least count',
                    'Close the spindle correctly using the ratchet',
                    'Combine main scale and circular scale into one reading',
                    'Correct readings for positive and negative zero error',
                ],
                'knowledge': [
                    {
                        'heading': 'Pitch, least count and the magic of screws',
                        'body': 'A screw converts big rotations into tiny advances. If one full turn of the thimble moves the spindle 1 mm (the pitch) and the thimble edge carries 100 divisions, then rotating by just one division advances the spindle 1/100 mm. Least count = pitch / number of circular divisions = 1 mm / 100 = 0.01 mm.\n\nThat is ten times finer than vernier calipers, which is why the screw gauge is the right tool for wire diameters, paper thickness and hair. Total reading = linear (main) scale reading + circular scale division on the reference line × least count.',
                    },
                    {
                        'heading': 'Using the ratchet and reading the scales',
                        'body': 'Place the wire between the stud and spindle and turn using the ratchet cap, never the bare thimble. The ratchet slips at a fixed gentle pressure, so every student squeezes the wire identically — this kills the over-tightening error that plagues beginners.\n\nRead the last fully visible millimetre mark on the sleeve, then the circular division aligned with the reference line. For a wire, take readings in two perpendicular directions at three places along the length, because drawn wires are slightly oval and tapered. Average everything.',
                    },
                    {
                        'heading': 'Zero error and backlash',
                        'body': 'Close the gap fully with nothing inside: if the circular zero stops below the reference line, the error is positive (subtract); above it, negative (add). For example, if division 96 sits on the line with 100 divisions on the thimble, zero error = −4 × 0.01 = −0.04 mm and the correction is +0.04 mm.\n\nThe second hidden enemy is backlash: worn screws have slack, so the spindle lags when you reverse direction. Always approach the final position rotating the same way. Write both of these in the error analysis section of your practical copy — they are standard NEB viva questions.',
                    },
                ],
                'fun_fact': 'A human hair is only 0.05-0.1 mm thick — a screw gauge measures it in seconds, and quality-control engineers use the very same instrument to check ball bearings in aircraft engines.',
                'quiz': [
                    {
                        'q': 'Pitch 1 mm, 100 circular divisions. Least count = ?',
                        'options': ['0.01 cm', '0.1 mm', '0.01 mm', '1 mm'],
                        'answer': 2,
                        'explain': 'LC = pitch / circular divisions = 1/100 mm = 0.01 mm.',
                    },
                    {
                        'q': 'Why must you turn the ratchet, not the thimble, when closing on a wire?',
                        'options': ['It is faster', 'The ratchet applies a fixed gentle pressure so the wire is not squashed', 'The thimble is fragile', 'It changes the pitch'],
                        'answer': 1,
                        'explain': 'The ratchet slips at a set torque, giving every measurement the same contact pressure and preventing deformation of the object.',
                    },
                    {
                        'q': 'Linear scale shows 2 mm, circular scale division 37 is on the reference line, zero error +0.03 mm. Corrected diameter = ?',
                        'options': ['2.37 mm', '2.34 mm', '2.40 mm', '2.07 mm'],
                        'answer': 1,
                        'explain': 'Observed = 2 + 37 × 0.01 = 2.37 mm; corrected = 2.37 − (+0.03) = 2.34 mm.',
                    },
                ],
            },
            {
                'slug': 'spherometer',
                'title': 'Spherometer: Radius of Curvature',
                'icon': 'lens_blur',
                'minutes': 15,
                'sim': 'nebphysics/spherometer',
                'sim_type': 'lab3d',
                'summary': 'Lower the central screw till it kisses a plane glass, then a watch glass, read the sagitta h on the disc scale and compute R = l²/6h + h/2.',
                'objectives': [
                    'Explain how a spherometer measures tiny vertical heights',
                    'Take zero and surface readings to find the sagitta h',
                    'Apply R = l²/6h + h/2 with the leg separation l',
                    'Judge when the tip "just touches" and avoid over-driving the screw',
                ],
                'knowledge': [
                    {
                        'heading': 'Three legs and a screw',
                        'body': 'A spherometer stands on three legs forming an equilateral triangle of side l, with a micrometer screw at the exact centre. On a flat surface the tip and the legs all touch at the same level. On a convex watch glass, the centre bulges up by a tiny height h — the sagitta — and the screw must be raised by exactly h to touch.\n\nGeometry of a circle through the three leg points gives the elegant result R = l²/6h + h/2, where R is the radius of the sphere the surface belongs to. A bump of half a millimetre on a 4 cm triangle reveals a radius of half a metre — small heights decode huge curvatures.',
                    },
                    {
                        'heading': 'Procedure: difference of two readings',
                        'body': 'First place the instrument on plane glass and turn the screw down until the tip just touches; note reading a from the pitch scale (mm) and disc scale (100 divisions, LC = 0.01 mm). Then move to the watch glass and repeat for reading b. The sagitta is simply h = b − a.\n\nMeasure l by pressing the legs on paper and measuring the three pin-prick separations with a ruler or vernier, then averaging. In the simulation the touch is shown by a green glow; in the real lab you watch the gap and the reflection of the tip, or listen for the faint scratch as you slide the instrument.',
                    },
                    {
                        'heading': 'Errors: the "just touches" problem',
                        'body': 'The whole experiment hangs on judging contact. Drive the screw too far and you lift the legs, reading h too large; stop early and h is too small. Approach the surface slowly from above, and always rotate in one direction to dodge backlash error in the screw.\n\nOther error sources for your report: the legs may not form a perfect equilateral triangle (measure all three sides), the glass may flex under pressure, and temperature changes alter the screw. Since h appears in the denominator, a 10% error in a tiny h becomes a 10% error in R — h is the quantity to measure most carefully.',
                    },
                ],
                'fun_fact': 'Opticians in Nepal and everywhere else still use spherometers to check the curvature of spectacle lenses — the same R = l²/6h + h/2 your practical exam asks for.',
                'quiz': [
                    {
                        'q': 'A spherometer measures the radius of curvature using:',
                        'options': ['The weight of the glass', 'The central height (sagitta) above three fixed legs', 'Light reflection angles', 'The diameter of the glass'],
                        'answer': 1,
                        'explain': 'The screw measures how much the surface centre rises above the plane of the three legs; geometry converts that h into R.',
                    },
                    {
                        'q': 'With l = 4 cm and h = 0.05 cm, R ≈ ?',
                        'options': ['16 cm', '53.4 cm', '8.2 cm', '160 cm'],
                        'answer': 1,
                        'explain': 'R = l²/6h + h/2 = 16/(0.3) + 0.025 ≈ 53.4 cm.',
                    },
                    {
                        'q': 'Why must the screw always be rotated in the same direction near contact?',
                        'options': ['To polish the glass', 'To avoid backlash (slack) error in the screw threads', 'To increase the pitch', 'It looks professional'],
                        'answer': 1,
                        'explain': 'Reversing direction lets the screw move within its thread slack, so the scale turns without the tip moving — a systematic error called backlash.',
                    },
                ],
            },
            {
                'slug': 'simple-pendulum-g',
                'title': 'Simple Pendulum: Measuring g',
                'icon': 'timer',
                'minutes': 18,
                'sim': 'nebphysics/pendulum-g',
                'sim_type': 'lab3d',
                'summary': 'Time 20 oscillations with a stopwatch that obeys YOUR reflexes, tabulate L and T², plot the graph and pull g out of the slope.',
                'objectives': [
                    'Use T = 2π√(L/g) to design a measurement of g',
                    'Time 20 oscillations and compute the period accurately',
                    'Plot L versus T² and extract g from the slope',
                    'Explain why timing many oscillations beats timing one',
                    'Identify human reaction time as the dominant random error',
                ],
                'knowledge': [
                    {
                        'heading': 'The physics: a clock made of string',
                        'body': 'For small swings (under about 10°), a simple pendulum is a harmonic oscillator with period T = 2π√(L/g), where L is measured from the support to the CENTRE of the bob. Squaring gives T² = (4π²/g)L — so a graph of T² against L is a straight line through the origin with slope 4π²/g.\n\nThat graph is the heart of the experiment: g = 4π²/slope. Using the slope of several points instead of a single reading cancels random errors and exposes any systematic offset (a line that misses the origin hints you measured L to the top of the bob, not its centre).',
                    },
                    {
                        'heading': 'Procedure: why 20 oscillations?',
                        'body': 'Your thumb on the stopwatch is good to about ±0.2 s. If you time a single 1.8 s oscillation, that is an 11% error — useless. Time 20 oscillations (≈36 s) and the same ±0.2 s shrinks to 0.5%: the trick is dividing one reaction error across many periods, T = t/20.\n\nStart counting as the bob passes the LOWEST point — it moves fastest there, so your judgement of the crossing is sharpest. Count "zero" when you start the watch (a classic blunder is counting "one"). Repeat for five or six lengths between 40 cm and 120 cm and record everything in a table before graphing.',
                    },
                    {
                        'heading': 'Errors and precautions',
                        'body': 'Keep the amplitude small: at 15° the period is already about 0.4% longer than the small-angle formula, and the error grows with angle. Use an inextensible thread and a heavy, small bob so air drag and thread stretch stay negligible. Measure L with a metre ruler to the bob centre — add the bob radius to the thread length.\n\nIn Kathmandu g ≈ 9.79-9.81 m/s² depending on altitude. If your value lands within a few percent of that, your technique is sound. For the report: reaction time at start and stop, amplitude too large, fan or wind disturbing the bob, and support not rigid are the four standard sources of error.',
                    },
                ],
                'fun_fact': 'Until the 1930s, the official value of g for whole countries was set by pendulum surveys — and gravity really is measurably weaker atop high Himalayan stations than in the Terai.',
                'quiz': [
                    {
                        'q': 'Why time 20 oscillations instead of 1?',
                        'options': ['The pendulum slows down after one swing', 'Your fixed reaction error is divided across 20 periods, shrinking its effect', 'The formula only works for 20', 'To make the lab longer'],
                        'answer': 1,
                        'explain': 'Reaction error (~0.2 s) is roughly constant per press; spreading it over 20 periods cuts the percentage error in T twenty-fold.',
                    },
                    {
                        'q': 'The slope of a T² vs L graph is 4.0 s²/m. g = ?',
                        'options': ['4.0 m/s²', '9.87 m/s²', '2π m/s²', '39.5 m/s²'],
                        'answer': 1,
                        'explain': 'slope = 4π²/g, so g = 4π²/4.0 = 9.87 m/s².',
                    },
                    {
                        'q': 'L should be measured from the support to:',
                        'options': ['The top of the bob', 'The centre of the bob', 'The bottom of the bob', 'Anywhere on the thread'],
                        'answer': 1,
                        'explain': 'The effective length of a simple pendulum runs to the centre of mass of the bob: thread length + bob radius.',
                    },
                    {
                        'q': 'Doubling the bob\u2019s mass while keeping L fixed makes the period:',
                        'options': ['Double', 'Halve', 'Stay the same', '√2 times larger'],
                        'answer': 2,
                        'explain': 'T = 2π√(L/g) contains no mass — a heavier bob swings with exactly the same period.',
                    },
                ],
            },
            {
                'slug': 'parallelogram-of-forces',
                'title': 'Parallelogram Law of Forces',
                'icon': 'open_with',
                'minutes': 15,
                'sim': 'nebphysics/parallelogram-forces',
                'sim_type': 'lab3d',
                'summary': 'Load three hangers on a Gravesand apparatus, watch the knot settle into equilibrium, and check that the parallelogram of P and Q really balances R.',
                'objectives': [
                    'State the parallelogram law of vector addition',
                    'Set up equilibrium of three concurrent forces on Gravesand\u2019s apparatus',
                    'Compute the resultant √(P² + Q² + 2PQcosγ) and compare it with R',
                    'Explain when three given forces cannot balance (triangle rule)',
                ],
                'knowledge': [
                    {
                        'heading': 'The law being tested',
                        'body': 'If two forces acting at a point are drawn as the adjacent sides of a parallelogram, their resultant is the diagonal from that point — in magnitude AND direction. Numerically the diagonal is R = √(P² + Q² + 2PQcosγ), where γ is the angle between the forces.\n\nGravesand\u2019s apparatus tests this physically: strings over two frictionless pulleys carry weights P and Q, while a third weight R hangs straight down from the same knot. The knot drifts until the three pulls cancel. At equilibrium the resultant of P and Q must be exactly equal and opposite to R — vertical, with magnitude R.',
                    },
                    {
                        'heading': 'Procedure on the board',
                        'body': 'Hang known slotted weights on all three hangers and let the junction settle. Put a mirror-backed paper behind the strings and mark each string\u2019s direction by sighting dots with no parallax, then remove the paper and draw the lines to a scale such as 1 cm = 50 g-wt.\n\nConstruct the parallelogram on P and Q, measure its diagonal, and compare with the weight R (don\u2019t forget hanger weights!). Agreement within 2-3% verifies the law. In the simulation, drag the knot away and release it — watching it return to the same spot shows that equilibrium is genuine, not an accident of friction.',
                    },
                    {
                        'heading': 'Why some weights can never balance',
                        'body': 'Three forces at a point can only balance if each one is smaller than the sum of the other two — the same rule as triangle sides, because balanced forces drawn head-to-tail must close into a triangle. Load R = 400 g against P = Q = 100 g and the knot simply crashes into the pulleys: no geometry can make 200 g of pull hold up 400 g.\n\nError sources for your report: pulley friction (tap the board so strings settle to their true directions), stretching strings, hanger weights forgotten in P, Q, R, and parallax while marking string directions. NEB examiners often ask: "Why must the board be vertical?" — because only then do the weights act parallel to the board\u2019s plane.',
                    },
                ],
                'fun_fact': 'Suspension bridges across Nepali rivers are giant parallelogram-law demonstrations — every tower and anchor cable carries the vector sum of the deck\u2019s pull, computed exactly like your P and Q.',
                'quiz': [
                    {
                        'q': 'P = Q = 100 g-wt with 120° between them. Their resultant is:',
                        'options': ['200 g-wt', '141 g-wt', '100 g-wt', '50 g-wt'],
                        'answer': 2,
                        'explain': 'R = √(100² + 100² + 2·100·100·cos120°) = √(10000) = 100 g-wt. At 120°, two equal forces have a resultant equal to either.',
                    },
                    {
                        'q': 'At equilibrium, the resultant of P and Q must be:',
                        'options': ['Zero', 'Equal and opposite to R', 'Horizontal', 'Larger than R'],
                        'answer': 1,
                        'explain': 'The knot is in equilibrium, so P + Q + R (vectors) = 0; hence the resultant of P and Q is exactly −R: vertical, upward, magnitude R.',
                    },
                    {
                        'q': 'Which set of weights CANNOT be in equilibrium at a point?',
                        'options': ['100, 100, 150 g', '100, 200, 250 g', '100, 100, 250 g', '150, 200, 300 g'],
                        'answer': 2,
                        'explain': '250 > 100 + 100, breaking the triangle rule — the third force exceeds the maximum possible resultant of the other two.',
                    },
                ],
            },
            {
                'slug': 'coefficient-of-friction',
                'title': 'Coefficient of Friction',
                'icon': 'sledding',
                'minutes': 14,
                'sim': 'nebphysics/friction-incline',
                'sim_type': 'lab3d',
                'summary': 'Tilt an incline until the block just slips to capture the angle of repose, then switch to a spring-balance pull and confirm μ two independent ways.',
                'objectives': [
                    'Define static and kinetic coefficients of friction',
                    'Measure the angle of repose and use μₛ = tan θᵣ',
                    'Find μ from a horizontal pull with a spring balance',
                    'Show that friction depends on the surfaces, not the contact area',
                ],
                'knowledge': [
                    {
                        'heading': 'Static vs kinetic friction',
                        'body': 'Friction is the contact force opposing relative sliding. While the block is still, static friction matches your push exactly, up to a maximum fₛ(max) = μₛN. Once sliding starts, kinetic friction takes over with the slightly smaller value f = μₖN — which is why a block "breaks free" and then accelerates.\n\nBoth coefficients depend only on the pair of surfaces (wood on wood ≈ 0.3-0.5, rubber on concrete ≈ 0.7, ice ≈ 0.05) and, surprisingly, not on the apparent contact area. Flip a brick onto its small face and it slides at the same angle.',
                    },
                    {
                        'heading': 'Method 1: angle of repose',
                        'body': 'Tilt the plane slowly. Gravity\u2019s component along the slope is mg sinθ while the maximum static friction is μₛ mg cosθ. The block slips at the instant mg sinθ exceeds μₛ mg cosθ, i.e. at tanθᵣ = μₛ. Measure the angle of repose θᵣ and the coefficient drops out with no force measurement at all — the mass even cancels.\n\nRaise the angle in tiny steps near the slipping point, and repeat several times taking the mean. The "just slips" moment is genuinely fuzzy on real surfaces (dust, humidity), which is the main random error in this method.',
                    },
                    {
                        'heading': 'Method 2: horizontal pull, and precautions',
                        'body': 'On a horizontal table, pull the block through a spring balance. The reading when the block JUST starts to move equals μₛN = μₛmg; while it slides steadily at constant speed the reading equals μₖmg. Keep the string horizontal — an angled pull lifts the block and reduces N, faking a smaller μ.\n\nPrecautions: clean and dust the surfaces, pull smoothly without jerks, read the balance at eye level, and add weights to repeat with different normal forces — the graph of limiting friction vs N is a straight line through the origin whose slope is μ. Report tanθᵣ and the pull method side by side and discuss why they differ slightly.',
                    },
                ],
                'fun_fact': 'Trekking-boot soles are rubber lugs precisely because rubber on rock has μ near 1.0 — more than triple the grip of leather soles that older Himalayan expeditions used.',
                'quiz': [
                    {
                        'q': 'A block just begins to slide when the incline reaches 30°. μₛ = ?',
                        'options': ['0.5', '0.58', '0.87', '30'],
                        'answer': 1,
                        'explain': 'μₛ = tan θᵣ = tan 30° ≈ 0.58.',
                    },
                    {
                        'q': 'Doubling the block\u2019s mass changes the angle of repose how?',
                        'options': ['It doubles', 'It halves', 'It stays the same', 'It becomes 45°'],
                        'answer': 2,
                        'explain': 'tan θᵣ = μₛ contains no mass — both the driving force and friction scale with mg, so the slip angle is unchanged.',
                    },
                    {
                        'q': 'A 2 kg block needs 8 N to keep sliding at constant speed. μₖ ≈ ? (g = 9.8)',
                        'options': ['0.25', '0.41', '0.8', '4'],
                        'answer': 1,
                        'explain': 'Constant speed means pull = kinetic friction: μₖ = F/mg = 8/(2×9.8) ≈ 0.41.',
                    },
                ],
            },
            {
                'slug': 'hookes-law-spring',
                'title': "Hooke's Law & Spring Constant",
                'icon': 'waves',
                'minutes': 15,
                'sim': 'nebphysics/hookes-law',
                'sim_type': 'lab3d',
                'summary': 'Load a spring 50 g at a time, read the pointer on a mm scale, plot F against x and read k off the slope — then test series and parallel combinations.',
                'objectives': [
                    'State Hooke\u2019s law and its limit of proportionality',
                    'Measure extension with a pointer and scale for increasing loads',
                    'Determine k from the slope of an F-x graph',
                    'Predict and verify k for springs in series and parallel',
                ],
                'knowledge': [
                    {
                        'heading': 'F = kx, within limits',
                        'body': 'Hooke\u2019s law says the restoring force of a spring is proportional to its extension: F = kx. The spring constant k (N/m) is the stiffness — how many newtons stretch it one metre. The law holds only up to the elastic limit; stretch a spring too far and it deforms permanently, and your graph bends over.\n\nWhen a mass m hangs in equilibrium, the spring force balances gravity, so kx = mg. Each 50 g (0.49 N) you add stretches our k = 25 N/m spring by about 2 cm — comfortably readable on a mm scale.',
                    },
                    {
                        'heading': 'Procedure: load, settle, read',
                        'body': 'Note the pointer\u2019s zero reading with no load. Add slotted masses one at a time, let the oscillation die out, and read the pointer against the mm scale at eye level. Extension x = reading − zero reading. Take readings while loading AND unloading: if the two disagree, the spring passed its elastic limit and the run must be repeated with smaller loads.\n\nPlot F = mg on the y-axis versus x on the x-axis. A best-fit straight line through the origin confirms Hooke\u2019s law, and its slope is k. Using the graph instead of one reading averages out small reading errors — the same trick as the pendulum experiment.',
                    },
                    {
                        'heading': 'Series and parallel springs',
                        'body': 'Two springs in SERIES share the same force but add extensions, so 1/k = 1/k₁ + 1/k₂ — the combination is softer than either spring. Two springs in PARALLEL share the load at the same extension, so k = k₁ + k₂ — stiffer. With k₁ = 25 and k₂ = 40 N/m you get 15.4 N/m in series and 65 N/m in parallel; the simulation lets you verify both numbers.\n\nError sources: pointer parallax (read square-on), the spring oscillating when you read, zero drift if the spring sags permanently, and forgetting that the hanger itself has mass. These exact points are the expected "precautions" list in the NEB practical copy.',
                    },
                ],
                'fun_fact': 'A car\u2019s suspension uses four stiff springs in parallel with shock absorbers — and weighing machines from vegetable markets in Asan to airport baggage belts are just calibrated Hooke\u2019s-law springs.',
                'quiz': [
                    {
                        'q': 'A 200 g mass stretches a spring 8 cm. k ≈ ? (g = 9.8)',
                        'options': ['2.5 N/m', '24.5 N/m', '0.245 N/m', '245 N/m'],
                        'answer': 1,
                        'explain': 'k = F/x = (0.2 × 9.8)/0.08 = 1.96/0.08 ≈ 24.5 N/m.',
                    },
                    {
                        'q': 'Two identical springs of constant k are connected in series. The combination\u2019s constant is:',
                        'options': ['2k', 'k', 'k/2', 'k²'],
                        'answer': 2,
                        'explain': 'Series springs add extensions under the same force: 1/k_eff = 1/k + 1/k, so k_eff = k/2 — twice as soft.',
                    },
                    {
                        'q': 'Your F-x graph is straight at first but curves at large loads. The curve marks:',
                        'options': ['The elastic limit being exceeded', 'A wrong value of g', 'The spring getting heavier', 'Parallax error'],
                        'answer': 0,
                        'explain': 'Beyond the limit of proportionality the spring no longer obeys F = kx and may be permanently deformed.',
                    },
                ],
            },
            {
                'slug': 'specific-heat-mixtures',
                'title': 'Specific Heat by Method of Mixtures',
                'icon': 'thermostat',
                'minutes': 18,
                'sim': 'nebphysics/specific-heat',
                'sim_type': 'lab3d',
                'summary': 'Heat a metal piece to 100 °C, drop it into a calorimeter and chase the thermometer to its peak — then balance the heat equation to identify the metal.',
                'objectives': [
                    'State the principle of calorimetry (heat lost = heat gained)',
                    'Carry out the method of mixtures with correct readings θ₁, θ₂, θ',
                    'Include the calorimeter\u2019s water equivalent in the calculation',
                    'Explain how heat loss to the room biases the result and how to reduce it',
                ],
                'knowledge': [
                    {
                        'heading': 'The principle of calorimetry',
                        'body': 'When a hot solid meets cold water in an insulated vessel, heat flows until both reach a common temperature θ. If no heat escapes, heat lost by the solid equals heat gained by the water AND the calorimeter: mₛcₛ(θ₂ − θ) = (m_w c_w + m_c c_c)(θ − θ₁).\n\nEverything except cₛ is measurable — masses on a balance, temperatures on a thermometer — so the solid\u2019s specific heat follows from one equation. Water\u2019s huge specific heat (4186 J/kg·K, about ten times copper\u2019s) is why a small metal block barely warms the water by a few degrees.',
                    },
                    {
                        'heading': 'Procedure, step by step',
                        'body': 'Weigh the dry copper calorimeter (m_c), add water and weigh again (giving m_w), and record the initial water temperature θ₁. Meanwhile heat the weighed solid in boiling water or a steam heater for ten minutes so it is uniformly at θ₂ ≈ 100 °C (check with a thermometer in the heater).\n\nTransfer the solid QUICKLY — every second in the air sheds heat — and stir gently. The thermometer rises, peaks, then begins a slow fall as the room steals heat. The mixture temperature θ is the PEAK reading. Then compute cₛ = (m_w c_w + m_c c_c)(θ − θ₁) / mₛ(θ₂ − θ) and compare with standard values (copper 385, iron 450, aluminium 900 J/kg·K) to identify your metal.',
                    },
                    {
                        'heading': 'Heat loss: the experiment\u2019s great enemy',
                        'body': 'Real calorimeters leak heat by conduction, convection, radiation and evaporation, so your θ is always a little low and the computed cₛ comes out wrong. Defences: polish the calorimeter (shiny surfaces radiate less), sit it inside a padded wooden box, use a lid, start with water slightly BELOW room temperature so it first gains heat from the room and then loses — the two leaks partly cancel (a trick known as Rumford\u2019s correction).\n\nOther errors: water splashing during the drop, solid touching the calorimeter wall, thermometer not stirred to the true mixture temperature, and droplets of boiling water carried over with the solid. Toggle "heat loss" in the simulation and watch the computed value drift — that is precisely the systematic error your report must discuss.',
                    },
                ],
                'fun_fact': 'Water\u2019s enormous specific heat is why Phewa Lake softens Pokhara\u2019s climate — the lake absorbs a whole afternoon of sunshine while warming barely a degree.',
                'quiz': [
                    {
                        'q': 'The method of mixtures rests on the assumption that:',
                        'options': ['All metals have equal specific heat', 'Heat lost by the hot body equals heat gained by water and calorimeter', 'Temperature always rises', 'The calorimeter absorbs no heat'],
                        'answer': 1,
                        'explain': 'With good insulation, energy is conserved between the contents: heat lost = heat gained, including the calorimeter\u2019s share.',
                    },
                    {
                        'q': 'Why must the hot solid be moved to the calorimeter quickly?',
                        'options': ['So it stays shiny', 'It loses heat to the air during transfer, lowering θ₂ below the assumed value', 'Water evaporates otherwise', 'The stopwatch is running'],
                        'answer': 1,
                        'explain': 'During transfer the solid cools below the temperature you recorded in the heater, making the heat-balance equation slightly wrong.',
                    },
                    {
                        'q': '100 g of metal at 100 °C warms 200 g of water (+ negligible calorimeter) from 20.0 to 24.0 °C. cₛ ≈ ?',
                        'options': ['385 J/kg·K', '441 J/kg·K', '900 J/kg·K', '4186 J/kg·K'],
                        'answer': 1,
                        'explain': 'cₛ = m_w c_w Δθ_w / (mₛ Δθₛ) = 0.2×4186×4 / (0.1×76) ≈ 441 J/kg·K — close to iron.',
                    },
                    {
                        'q': 'Starting with water slightly below room temperature helps because:',
                        'options': ['Water boils faster later', 'Heat gained from the room before the peak partly cancels heat lost after it', 'The thermometer reads better when cold', 'It increases the specific heat of water'],
                        'answer': 1,
                        'explain': 'This is Rumford\u2019s compensation: the calorimeter first absorbs heat from the surroundings, then releases it, so the net exchange roughly cancels.',
                    },
                ],
            },
        ],
    },
] + _C12
