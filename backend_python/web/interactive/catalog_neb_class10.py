"""Interactive courses for NEB / SEE grade 9-10 (Basic Education Examination).

The grade 11-12 side of the hub ships the NEB practical labs in
``catalog_neb_physics`` / ``catalog_neb_chemistry``. This module is the same
idea one stage earlier: the practicals and the graph work a Class 10 student is
examined on in the SEE, each one as a working simulation rather than a static
diagram.

Every lesson here maps to a real unit of the CDC Class 10 curriculum, so a
teacher can send a student to exactly the experiment in today's lesson plan.
"""

COURSES = [
    {
        'slug': 'neb-science-10-lab',
        'title': 'NEB Science 10 — SEE Practical Lab',
        'category': 'neb10',
        'age_range': '15-16',
        'level': 'Intermediate',
        'icon': 'science',
        'color': '#0D9488',
        'tagline': 'The Class 10 science practicals you are examined on — mirrors, Ohm\'s law, indicators and food tests — as working virtual laboratories.',
        'description': 'Every SEE candidate sits a science practical examination, and every one of those practicals is a procedure you can rehearse here before you touch the real apparatus. Measure the focal length of a concave mirror and follow the rays; build a circuit, take voltage-current readings and get the resistance from the slope of your own graph; test a set of household substances with litmus, phenolphthalein and methyl orange; and run the iodine, Benedict\'s and Biuret tests that tell starch, sugar and protein apart. Readouts, observations and conclusions follow the format the marker expects in your practical answer sheet.',
        'skills': [
            'Measuring focal length and drawing ray diagrams for a concave mirror',
            'Taking voltage and current readings and plotting a V-I graph',
            'Finding the equivalent resistance of series and parallel combinations',
            'Using indicators to classify a solution as acidic, basic or neutral',
            'Running and interpreting iodine, Benedict\'s and Biuret food tests',
            'Recording observation, inference and conclusion in the practical format',
        ],
        'lessons': [
            {
                'slug': 'concave-mirror',
                'title': 'Focal Length of a Concave Mirror',
                'icon': 'flare',
                'minutes': 14,
                'sim': 'nebclass10/concave-mirror',
                'sim_type': 'lab3d',
                'summary': 'Move an object along the principal axis of a concave mirror and watch the image change — real, inverted and diminished far away, then magnified near the focus. Switch to the distant-object method to measure f the way the school lab does.',
                'objectives': [
                    'State the mirror formula 1/f = 1/v + 1/u and use it',
                    'Explain why parallel rays from a distant object converge at the focus',
                    'Describe the image when the object is beyond C, at C, between C and F, and between F and the pole',
                    'Compute the magnification m = −v/u and say what its sign means',
                    'Find the focal length of a concave mirror by the distant-object method',
                ],
                'knowledge': [
                    {
                        'heading': 'The mirror formula',
                        'body': 'A concave mirror is a piece of a sphere. Its centre of curvature C lies on the principal axis at a distance R from the pole, and the focus F lies halfway between the pole and C, so f = R/2.\n\nFor real, positive distances the mirror formula is 1/f = 1/v + 1/u, which rearranges to v = uf/(u − f). Distances are always measured from the pole of the mirror, on the axis. If v comes out positive the image is real and in front of the mirror; if it comes out negative the image is virtual and behind the mirror.\n\nMagnification is m = −v/u. A negative m means the image is inverted relative to the object.',
                    },
                    {
                        'heading': 'The distant-object method',
                        'body': 'If the object is very far away — a tree, a building, the sun on a screen — the rays reaching the mirror are effectively parallel. Parallel rays reflect through the focus, so the sharp image forms in the focal plane. That is the quickest way to measure f: hold the mirror facing a distant object, move a screen until the image is sharpest, and the pole-to-screen distance is f.\n\nIn the lab you do this three times, average the readings, and also do the u-v method for a check. The two answers should agree to within your reading error.',
                    },
                    {
                        'heading': 'Image for every object position',
                        'body': 'Object beyond C: image between F and C, real, inverted, diminished. Object at C: image at C, real, inverted, same size. Object between C and F: image beyond C, real, inverted, magnified. Object at F: image at infinity. Object between F and the pole: image behind the mirror, virtual, erect, magnified.\n\nA dentist\'s mirror and a shaving mirror both put the face between the pole and the focus, which is why they magnify. A torch reflector puts the bulb at the focus, so the reflected beam is parallel.',
                    },
                ],
                'fun_fact': 'A satellite dish and a radio telescope are the same idea turned around: a huge concave surface collects parallel rays and concentrates them at the focus, where the receiver sits.',
                'quiz': [
                    {
                        'q': 'The radius of curvature of a concave mirror is 30 cm. Its focal length is:',
                        'options': ['30 cm', '15 cm', '60 cm', '7.5 cm'],
                        'answer': 1,
                        'explain': 'For a spherical mirror f = R/2 = 30/2 = 15 cm.',
                    },
                    {
                        'q': 'An object is placed 20 cm from a concave mirror of focal length 10 cm. The image is:',
                        'options': ['At infinity', 'At 20 cm, real and inverted, same size', 'At 20 cm, virtual', 'At 10 cm, real'],
                        'answer': 1,
                        'explain': 'u = 20 cm and f = 10 cm, so the object is at C = 2f. v = uf/(u − f) = 200/10 = 20 cm and m = −1: real, inverted, same size.',
                    },
                    {
                        'q': 'A concave mirror forms a virtual image when the object lies:',
                        'options': ['Beyond C', 'At C', 'Between F and the pole', 'Between C and F'],
                        'answer': 2,
                        'explain': 'Only when the object is between the focus and the pole does the reflected light diverge, giving a virtual, erect, magnified image behind the mirror.',
                    },
                    {
                        'q': 'Why does the distant-object method give the focal length directly?',
                        'options': ['Because the object is bright', 'Because rays from a distant object are nearly parallel and focus in the focal plane', 'Because the mirror is concave', 'Because the image is inverted'],
                        'answer': 1,
                        'explain': 'Parallel rays reflect through F, so the sharp image forms at the focal plane, and the pole-to-image distance is f.',
                    },
                ],
            },
            {
                'slug': 'ohms-law',
                'title': 'Ohm\'s Law and Resistor Combinations',
                'icon': 'electrical_services',
                'minutes': 16,
                'sim': 'nebclass10/ohms-law',
                'sim_type': 'lab3d',
                'summary': 'Wire a cell, an ammeter and one or two resistors in series or parallel. Raise the voltage, record the current, and read the resistance off the slope of the V-I graph you built yourself.',
                'objectives': [
                    'State Ohm\'s law and the conditions under which it holds',
                    'Take a set of V and I readings and plot the V-I graph',
                    'Explain why the slope of the V-I graph is the reciprocal of the resistance',
                    'Compute the equivalent resistance in series (R = R1 + R2) and parallel (1/R = 1/R1 + 1/R2)',
                    'Explain why current is the same in series and voltage is the same in parallel',
                ],
                'knowledge': [
                    {
                        'heading': 'Ohm\'s law',
                        'body': 'Ohm\'s law says that, at constant temperature, the current through a conductor is directly proportional to the potential difference across it: V = IR, with V in volts, I in amperes and R in ohms.\n\nThat is why the V-I graph of a metal wire at a steady temperature is a straight line through the origin. Its slope is ΔI/ΔV, which is 1/R, so the resistance is the reciprocal of the slope. A steeper line means a smaller resistance.\n\nThe law fails when the temperature changes — a filament lamp heats up, its resistance rises, and the V-I graph bends.',
                    },
                    {
                        'heading': 'Series and parallel',
                        'body': 'In series the same current passes through every resistor, and the voltages add: R = R1 + R2 + … . Adding a resistor in series always increases the total resistance and reduces the current.\n\nIn parallel the voltage across every branch is the same, and the currents add: 1/R = 1/R1 + 1/R2 + … . Adding a branch in parallel always decreases the total resistance, because there is one more path for the charge.\n\nTwo resistors of 10 Ω and 20 Ω give 30 Ω in series but only 6.7 Ω in parallel — a fact worth checking against the readouts here.',
                    },
                    {
                        'heading': 'Doing the practical properly',
                        'body': 'Connect the cell, key, rheostat, ammeter in series and voltmeter in parallel with the resistor. The ammeter must be in series because it has a very low resistance, and the voltmeter in parallel because it has a very high resistance; swapping them gives a wrong reading and can damage the meter.\n\nTake at least five readings across the range, tabulate V and I, and plot V on the x-axis against I on the y-axis. Draw the best straight line, take two points far apart on the line (not two data points) for the slope, and compute R = 1/slope. State the temperature condition and mention that the wire heats up if the current is kept on too long.',
                    },
                ],
                'fun_fact': 'The ohm is named after Georg Simon Ohm, whose 1827 result was ignored for years. He was paid so little as a schoolteacher that he eventually resigned over it.',
                'quiz': [
                    {
                        'q': 'A 6 V battery drives a current of 0.5 A through a resistor. The resistance is:',
                        'options': ['3 Ω', '12 Ω', '0.083 Ω', '6.5 Ω'],
                        'answer': 1,
                        'explain': 'R = V/I = 6/0.5 = 12 Ω.',
                    },
                    {
                        'q': 'The V-I graph of a metallic conductor at constant temperature is:',
                        'options': ['A parabola through the origin', 'A straight line through the origin', 'A straight line not through the origin', 'A hyperbola'],
                        'answer': 1,
                        'explain': 'V ∝ I at constant temperature, so the graph is a straight line through the origin with slope 1/R.',
                    },
                    {
                        'q': 'Two resistors of 4 Ω and 6 Ω are joined in parallel. The equivalent resistance is:',
                        'options': ['10 Ω', '2.4 Ω', '5 Ω', '1.2 Ω'],
                        'answer': 1,
                        'explain': '1/R = 1/4 + 1/6 = 5/12, so R = 12/5 = 2.4 Ω. The parallel value is always smaller than the smaller resistor.',
                    },
                    {
                        'q': 'In a series circuit, which quantity is the same through every component?',
                        'options': ['Voltage', 'Current', 'Resistance', 'Power'],
                        'answer': 1,
                        'explain': 'Charge has only one path in series, so the same current flows through every component; the voltages add up to the supply voltage.',
                    },
                    {
                        'q': 'Why is the ammeter connected in series and not across the resistor?',
                        'options': ['It is cheaper', 'Because it has a very low resistance and would short the supply if placed in parallel', 'Because it measures voltage', 'Because the current is zero in parallel'],
                        'answer': 1,
                        'explain': 'An ideal ammeter has almost zero resistance. Connected in parallel it would carry a huge current and damage itself and the cell.',
                    },
                ],
            },
            {
                'slug': 'indicators',
                'title': 'Acids, Bases and Indicators',
                'icon': 'water_drop',
                'minutes': 13,
                'sim': 'nebclass10/indicators',
                'sim_type': 'lab3d',
                'summary': 'Test lemon juice, curd, lime water, soap, baking soda and a salt solution with litmus paper, phenolphthalein, methyl orange and universal indicator — and watch the colour change decide the answer.',
                'objectives': [
                    'Define an acid and a base and give everyday examples of each',
                    'Describe the colour change of litmus, phenolphthalein and methyl orange in acid, base and neutral solutions',
                    'Read a pH value and place a solution on the pH scale',
                    'Explain what a universal indicator is and why it is more useful than litmus',
                    'Predict the products of an acid-base (neutralisation) reaction',
                ],
                'knowledge': [
                    {
                        'heading': 'Acids and bases at home',
                        'body': 'An acid gives hydrogen ions (H⁺) in water and tastes sour: lemon juice (citric acid), vinegar, curd, tamarind, sour milk. A base gives hydroxide ions (OH⁻) in water, feels soapy and tastes bitter: soap, lime water, milk of magnesia, baking soda solution, ash water.\n\nSome substances are neutral, neither acidic nor basic — pure water, common salt solution and sugar solution. pH 7 is neutral; below 7 is acidic and above 7 is basic. Strong acids have pH near 1 and strong bases near 13.',
                    },
                    {
                        'heading': 'Indicators and their colours',
                        'body': 'An indicator is a substance that changes colour when it is put into an acid or a base.\n\nBlue litmus turns red in an acid; red litmus turns blue in a base. Phenolphthalein is colourless in acid and neutral solutions but pink in a base. Methyl orange is red-orange in an acid but yellow in a base. Universal indicator is a mixture and shows a whole range of colours, so it tells you roughly how strong the acid or base is, not only which one it is.\n\nThe colours are worth memorising in a table — a question that asks for "the colour of phenolphthalein in lime water" is a free mark if you know it, and a lost one if you guess.',
                    },
                    {
                        'heading': 'Neutralisation',
                        'body': 'When an acid reacts with a base they cancel each other out and form a salt and water: HCl + NaOH → NaCl + H₂O. Because the product is often neutral, the reaction is called neutralisation.\n\nThis is why lime water soothes an acid burn, and why an antacid tablet (a mild base) settles acidity in the stomach. In the lab you can follow the neutralisation by adding a drop of phenolphthalein: the pink colour of the base disappears exactly at the end point.',
                    },
                ],
                'fun_fact': 'Litmus comes from lichens — the same organism group you study in the classification chapter. It has been used as an indicator for more than 700 years, long before anyone knew what an acid was.',
                'quiz': [
                    {
                        'q': 'Blue litmus paper is dipped into lime water. It turns:',
                        'options': ['Red', 'Blue (no change)', 'Colourless', 'Yellow'],
                        'answer': 1,
                        'explain': 'Lime water is a base. Blue litmus stays blue in a base; it would only turn red in an acid.',
                    },
                    {
                        'q': 'Phenolphthalein in a dilute acid solution is:',
                        'options': ['Pink', 'Colourless', 'Yellow', 'Blue'],
                        'answer': 1,
                        'explain': 'Phenolphthalein is colourless in acidic and neutral solutions and turns pink only in a base.',
                    },
                    {
                        'q': 'A solution has pH 3. It is:',
                        'options': ['Strongly basic', 'Acidic', 'Neutral', 'Weakly basic'],
                        'answer': 1,
                        'explain': 'Any pH below 7 is acidic, and pH 3 is a fairly strong acid (vinegar is about pH 3).',
                    },
                    {
                        'q': 'Which indicator tells you both whether a solution is acidic or basic and roughly how strong it is?',
                        'options': ['Litmus', 'Phenolphthalein', 'Methyl orange', 'Universal indicator'],
                        'answer': 3,
                        'explain': 'Universal indicator is a mixture whose colour changes continuously across the pH scale, so it gives a rough pH value.',
                    },
                    {
                        'q': 'Acid + base → salt + water. This reaction is called:',
                        'options': ['Oxidation', 'Neutralisation', 'Displacement', 'Decomposition'],
                        'answer': 1,
                        'explain': 'The acid and the base neutralise each other, giving a salt and water.',
                    },
                ],
            },
            {
                'slug': 'food-tests',
                'title': 'Food Tests: Starch, Sugar and Protein',
                'icon': 'restaurant',
                'minutes': 13,
                'sim': 'nebclass10/food-tests',
                'sim_type': 'lab3d',
                'summary': 'Run the three food tests on rice, potato, bread, banana, milk, egg white, soybean and groundnut, and work out what each food contains from the colour change.',
                'objectives': [
                    'Describe the iodine test for starch and its blue-black colour',
                    'Describe Benedict\'s test for reducing sugar and the brick-red colour after heating',
                    'Describe the Biuret test for protein and its violet colour',
                    'Explain why Benedict\'s test needs heating and the other two do not',
                    'Name the food groups a balanced diet needs and give a local source of each',
                ],
                'knowledge': [
                    {
                        'heading': 'Why food tests matter',
                        'body': 'Carbohydrate, protein, fat, vitamin, mineral, roughage and water are the seven components of a balanced diet. Starch and sugar supply energy, protein builds and repairs the body, and fat stores energy and protects organs.\n\nYou cannot tell which food contains what by looking at it, so the body\'s building blocks are detected by simple colour tests. Each test is specific: iodine reacts only with starch, Benedict\'s solution only with reducing sugar, and Biuret reagent only with protein.',
                    },
                    {
                        'heading': 'The three tests',
                        'body': 'Iodine test for starch: add two or three drops of iodine solution. A blue-black colour means starch is present; a yellow-brown colour means it is absent. It works at room temperature — rice, potato and bread all turn blue-black.\n\nBenedict\'s test for reducing sugar: add Benedict\'s solution and heat the tube gently in a water bath. If reducing sugar is present the blue solution turns green, then yellow, then brick red. Banana, milk and sugar solution test positive. Heating is essential — no heating, no colour change.\n\nBiuret test for protein: add sodium hydroxide, then a few drops of copper sulphate solution. A violet colour means protein. Milk, egg white, soybean and groundnut test positive.',
                    },
                    {
                        'heading': 'Reading the result honestly',
                        'body': 'The test tells you presence or absence, not how much. A faint brick red means a little sugar; a deep brick red means a lot. Record the colour you actually saw rather than what the book says you should see.\n\nTwo mistakes cost marks in the practical: heating the tube in the open flame instead of a water bath (the solution boils over and spits), and adding iodine to a solid without a drop of water, so the colour is patchy. Also, always write the observation and the inference separately: "Observation — the solution turned blue-black. Inference — starch is present."',
                    },
                ],
                'fun_fact': 'The Biuret test is named after the compound biuret, which gives the same violet colour with copper ions. It detects the peptide bond itself, so it works for any protein — from egg white to soybean to your own hair.',
                'quiz': [
                    {
                        'q': 'Iodine solution is added to a boiled potato. The colour is:',
                        'options': ['Brick red', 'Blue-black', 'Violet', 'Yellow'],
                        'answer': 1,
                        'explain': 'Potato contains starch, and iodine gives a blue-black colour with starch.',
                    },
                    {
                        'q': 'Benedict\'s test gives a brick-red precipitate. The food contains:',
                        'options': ['Starch', 'Protein', 'Reducing sugar', 'Fat'],
                        'answer': 2,
                        'explain': 'The blue solution turning green, yellow and finally brick red on heating shows a reducing sugar.',
                    },
                    {
                        'q': 'Which test needs the tube to be heated in a water bath?',
                        'options': ['Iodine test', 'Biuret test', 'Benedict\'s test', 'None of them'],
                        'answer': 2,
                        'explain': 'Benedict\'s test only works on heating; the iodine and Biuret tests give their colour at room temperature.',
                    },
                    {
                        'q': 'Biuret reagent turns violet in a food. The food contains:',
                        'options': ['Protein', 'Starch', 'Sugar', 'Vitamin C'],
                        'answer': 0,
                        'explain': 'Biuret reagent reacts with the peptide bond, so a violet colour means protein.',
                    },
                    {
                        'q': 'A student writes "the solution turned violet, so sugar is present". What is wrong?',
                        'options': ['Nothing', 'Violet is the protein test, not the sugar test', 'The colour should be blue-black', 'The test needs heating'],
                        'answer': 1,
                        'explain': 'Violet is the Biuret result for protein. Sugar is shown by Benedict\'s solution turning brick red on heating.',
                    },
                ],
            },
        ],
    },
    {
        'slug': 'neb-maths-10-explorer',
        'title': 'NEB Mathematics 10 — Graph and Data Explorer',
        'category': 'neb10',
        'age_range': '15-16',
        'level': 'Intermediate',
        'icon': 'calculate',
        'color': '#2563EB',
        'tagline': 'Parabolas, data sets and trigonometric heights you can move with your hand — the three graph questions that appear in the SEE mathematics paper every year.',
        'description': 'In the SEE mathematics paper you must draw and read graphs: the parabola of a quadratic equation, the histogram and the measures of central tendency of a data set, and the height-and-distance figure in trigonometry. This course lets you change a, b and c and see the parabola move, type your own data and watch mean, median and mode shift, and raise and lower a theodolite to see the height come out of the tangent formula. Each lesson also tells you the exact marks-bearing steps of the written answer.',
        'skills': [
            'Sketching y = ax² + bx + c and reading off the vertex, axis and roots',
            'Using the discriminant to say how many real roots a quadratic has',
            'Computing mean, median, mode and range from raw data',
            'Drawing and interpreting a histogram with a chosen class width',
            'Solving height-and-distance problems with tan θ = height ⁄ distance',
        ],
        'lessons': [
            {
                'slug': 'quadratic-graph',
                'title': 'Graphs of Quadratic Equations',
                'icon': 'functions',
                'minutes': 15,
                'sim': 'nebclass10/quadratic-graph',
                'sim_type': '3d',
                'summary': 'Slide a, b and c and watch the parabola open, shift and turn. The vertex, the axis of symmetry, the discriminant and the roots are computed live, so you can test every case in the syllabus in a couple of minutes.',
                'objectives': [
                    'Draw the graph of y = ax² + bx + c from a table of values',
                    'State the shape of the graph and how the sign of a decides it',
                    'Find the vertex and the axis of symmetry using x = −b/2a',
                    'Use the discriminant D = b² − 4ac to count the real roots',
                    'Solve a quadratic equation graphically and check against the factorised form',
                ],
                'knowledge': [
                    {
                        'heading': 'Shape and opening',
                        'body': 'The graph of y = ax² + bx + c (a ≠ 0) is a parabola. If a is positive it opens upwards and has a minimum; if a is negative it opens downwards and has a maximum. The bigger |a| is, the narrower the parabola.\n\nThe y-intercept is simply c, because putting x = 0 leaves y = c. That fixes one point without any calculation, and it is a standard first step in the answer.',
                    },
                    {
                        'heading': 'Vertex, axis and roots',
                        'body': 'The parabola is symmetric about the vertical line x = −b/2a. That line is the axis of symmetry, and it passes through the vertex. Substituting that x back into the equation gives the y-coordinate of the vertex.\n\nThe roots are the x-intercepts, where y = 0. Solving ax² + bx + c = 0 with the formula x = (−b ± √(b² − 4ac))/2a gives them. The sign of D = b² − 4ac decides the case: D > 0 gives two distinct real roots and the parabola cuts the x-axis twice; D = 0 gives one repeated root and the parabola touches the axis, its vertex sitting exactly on it; D < 0 gives no real root and the parabola never meets the axis.',
                    },
                    {
                        'heading': 'Answering it for marks',
                        'body': 'A typical SEE question gives a quadratic, asks for a table of values and a graph, and then asks you to solve the equation from the graph. Take x values on both sides of the vertex, at least five of them. Plot the points accurately, join them with a smooth free-hand curve (never a ruler) and label the axis of symmetry and the vertex.\n\nTo solve graphically, read the x-values where the curve crosses the x-axis. If the question says "solve graphically", writing only the algebraic roots without the graph loses most of the marks — and the graph must actually pass through those values.',
                    },
                ],
                'fun_fact': 'Every water fountain jet, every thrown ball and every arch with a uniform load traces a parabola. Galileo was the first to prove that a projectile path is exactly a parabola, not just approximately one.',
                'quiz': [
                    {
                        'q': 'The graph of y = x² + 4 is a parabola with its vertex at:',
                        'options': ['(0, 4)', '(4, 0)', '(0, −4)', '(2, 2)'],
                        'answer': 0,
                        'explain': 'Here a = 1, b = 0, c = 4, so the vertex is at x = −b/2a = 0 and y = 0 + 0 + 4 = 4.',
                    },
                    {
                        'q': 'For which value of the discriminant does the parabola touch the x-axis at exactly one point?',
                        'options': ['D > 0', 'D = 0', 'D < 0', 'D = 1'],
                        'answer': 1,
                        'explain': 'When b² − 4ac = 0 the two roots coincide, so the vertex lies on the axis and the curve touches it at one point.',
                    },
                    {
                        'q': 'The axis of symmetry of y = x² − 6x + 9 is:',
                        'options': ['x = 3', 'x = −3', 'x = 6', 'x = 9'],
                        'answer': 0,
                        'explain': 'x = −b/2a = 6/2 = 3. In fact y = (x − 3)², so the vertex is (3, 0).',
                    },
                    {
                        'q': 'The roots of y = x² − 2x − 3 are:',
                        'options': ['3 and −1', '−3 and 1', '3 and 1', '2 and −3'],
                        'answer': 0,
                        'explain': 'Factorising: (x − 3)(x + 1) = 0 gives x = 3 and x = −1. The parabola cuts the axis at those two points.',
                    },
                    {
                        'q': 'The graph of y = −2x² + 4x − 5 opens:',
                        'options': ['Upwards', 'Downwards', 'Sideways', 'It is a straight line'],
                        'answer': 1,
                        'explain': 'The sign of a decides: a = −2 is negative, so the parabola opens downwards and has a maximum.',
                    },
                ],
            },
            {
                'slug': 'statistics-explorer',
                'title': 'Mean, Median, Mode and Histograms',
                'icon': 'bar_chart',
                'minutes': 14,
                'sim': 'nebclass10/statistics-explorer',
                'sim_type': '3d',
                'summary': 'Load the marks of a class, a year of rainfall or the heights of fifteen students, then watch the mean, median and mode move as the data changes. The histogram redraws itself with the class width you choose.',
                'objectives': [
                    'Compute the mean, median, mode and range of a raw data set',
                    'Explain what each average tells you and when it misleads',
                    'Group data into classes and draw a histogram',
                    'Read the modal class off a histogram',
                    'Decide which average is the right one for a given situation',
                ],
                'knowledge': [
                    {
                        'heading': 'The three averages',
                        'body': 'The mean is the sum of all the values divided by how many there are: x̄ = Σx/n. It uses every value, so a single extreme value drags it.\n\nThe median is the middle value when the data is arranged in order. With an even count it is the mean of the two middle values. The median is not affected by how extreme the extremes are, which is why house prices and exam marks are often reported as medians.\n\nThe mode is the value that appears most often. A data set can have no mode (nothing repeats) or several modes. The range is the largest value minus the smallest, and it measures how spread out the data is.',
                    },
                    {
                        'heading': 'Grouped data and the histogram',
                        'body': 'When there are many readings you group them into classes of equal width and count the frequency in each class. A histogram has the classes on the x-axis and the frequency on the y-axis, and the bars touch, because the classes are continuous.\n\nThe class with the tallest bar is the modal class, and it is the only kind of "mode" that exists for grouped data. For grouped data the mean is computed from the mid-values: x̄ = Σfm/Σf, where m is the mid-value of each class.\n\nThe choice of class width changes how the histogram looks but not the underlying data — that is worth saying in an answer that asks you to compare two groupings.',
                    },
                    {
                        'heading': 'Choosing the right average',
                        'body': 'Use the mean when the data is fairly even and you want to use every value: the average height of a class, the average rainfall of a month.\n\nUse the median when a few extreme values would distort the mean: the average income of a neighbourhood, the average waiting time at a hospital. Use the mode when the most common item is the point: the most common shoe size to stock, the most common score in a game.\n\nA question that gives you three averages and asks which to use is testing this judgement, not your arithmetic. Say which you choose and why in one sentence.',
                    },
                ],
                'fun_fact': 'A class can have the same mean as another class and be completely different: 40, 50, 60 and 0, 50, 100 both average 50, but the second set is far more spread out. That is exactly why the range (and, in higher classes, the standard deviation) is reported with the mean.',
                'quiz': [
                    {
                        'q': 'The mean of 8, 10, 12, 14 and 16 is:',
                        'options': ['10', '12', '14', '60'],
                        'answer': 1,
                        'explain': 'Sum = 60 and n = 5, so the mean = 60/5 = 12.',
                    },
                    {
                        'q': 'The median of 7, 3, 9, 4, 11 is:',
                        'options': ['4', '7', '9', '6.8'],
                        'answer': 1,
                        'explain': 'In order: 3, 4, 7, 9, 11. The middle value is 7.',
                    },
                    {
                        'q': 'The values 5, 6, 6, 7, 9, 9, 9, 12 have mode:',
                        'options': ['6', '9', '7.5', 'Two modes, 6 and 9'],
                        'answer': 1,
                        'explain': '9 appears three times, more often than any other value, so 9 is the mode.',
                    },
                    {
                        'q': 'For the data 2, 4, 6, 8, 100 the average that best describes a "typical" value is:',
                        'options': ['The mean, 24', 'The median, 6', 'The range, 98', 'The mode'],
                        'answer': 1,
                        'explain': 'The mean is dragged up to 24 by the single value 100; the median 6 describes the typical value far better.',
                    },
                    {
                        'q': 'In a histogram the bars touch because:',
                        'options': ['It looks better', 'The class intervals are continuous', 'The data is discrete', 'The frequency is the same'],
                        'answer': 1,
                        'explain': 'Each class runs up to the start of the next with no gap, so the bars are drawn touching; a bar chart for discrete values has gaps instead.',
                    },
                ],
            },
            {
                'slug': 'height-distance',
                'title': 'Height and Distance with a Theodolite',
                'icon': 'architecture',
                'minutes': 14,
                'sim': 'nebclass10/height-distance',
                'sim_type': '3d',
                'summary': 'Set the instrument a measured distance from a tower, read the angle of elevation, and get the height from tan θ. Change what is unknown and the same triangle solves the reverse problems.',
                'objectives': [
                    'Identify the angle of elevation and the angle of depression in a figure',
                    'Use tan θ = perpendicular ⁄ base to find a height or a distance',
                    'Solve problems in which the instrument has its own height above the ground',
                    'Draw a clean, labelled figure before substituting any numbers',
                    'Round the answer sensibly and state the unit',
                ],
                'knowledge': [
                    {
                        'heading': 'The two angles',
                        'body': 'The angle of elevation is the angle between the horizontal line through the observer\'s eye and the line of sight to an object above the horizontal. If you look up at the top of a tower, that is the angle of elevation.\n\nThe angle of depression is the angle between the horizontal through the observer and the line of sight to an object below. It is measured downwards. Because the two horizontal lines are parallel, the angle of depression from the top of a tower equals the angle of elevation from the foot — a fact that turns most "depression" problems into the same triangle.',
                    },
                    {
                        'heading': 'The working rule',
                        'body': 'In the right-angled triangle, tan θ = perpendicular ⁄ base. So height = distance × tan θ, and distance = height ⁄ tan θ.\n\nUse sin when the hypotenuse and the opposite side are involved, and cos when the hypotenuse and the adjacent side are involved — but in height-and-distance questions the known pair is almost always the base and the height, which means tan.\n\nIf the instrument is not at ground level, work in two steps: find the height above the instrument using tan, then add the instrument\'s own height. Forgetting that addition is the commonest lost mark in the whole question.',
                    },
                    {
                        'heading': 'Standard values to memorise',
                        'body': 'tan 30° = 1/√3 ≈ 0.5774, tan 45° = 1, tan 60° = √3 ≈ 1.7321. Also sin 30° = 1/2, sin 60° = √3/2, cos 30° = √3/2 and cos 60° = 1/2.\n\nSEE questions are written so that the arithmetic comes out clean with these values. If you find yourself reaching for a calculator for a 45° problem, you have probably set the triangle up wrongly. Always draw the figure first, mark the right angle and the angle of elevation, and write which side is known and which is wanted before substituting.',
                    },
                ],
                'fun_fact': 'Thales of Miletus measured the height of the Great Pyramid around 600 BC by waiting for the moment when his own shadow equalled his height — at that instant the pyramid\'s shadow equalled the pyramid\'s height. He had turned a 45° angle into a measuring tape.',
                'quiz': [
                    {
                        'q': 'The angle of elevation of the top of a tower from a point 30 m away is 45°. The height of the tower is:',
                        'options': ['15 m', '30 m', '30√3 m', '60 m'],
                        'answer': 1,
                        'explain': 'tan 45° = h/30 and tan 45° = 1, so h = 30 m.',
                    },
                    {
                        'q': 'A tower is 20 m high. From its top the angle of depression of a car is 30°. The distance of the car from the foot is:',
                        'options': ['20 m', '20√3 m', '40 m', '20/√3 m'],
                        'answer': 1,
                        'explain': 'tan 30° = 20/d, so d = 20/tan 30° = 20√3 ≈ 34.6 m. The angle of depression equals the angle of elevation from the car.',
                    },
                    {
                        'q': 'A theodolite 1.5 m high stands 40 m from a building and reads an angle of elevation of 30° to the roof. The height of the building is about:',
                        'options': ['23.1 m', '24.6 m', '21.6 m', '40 m'],
                        'answer': 1,
                        'explain': 'Height above the instrument = 40 tan 30° = 23.09 m; add the 1.5 m instrument height to get 24.59 ≈ 24.6 m.',
                    },
                    {
                        'q': 'Which ratio is used when the known sides are the base and the perpendicular?',
                        'options': ['sin θ', 'cos θ', 'tan θ', 'cosec θ'],
                        'answer': 2,
                        'explain': 'tan θ = perpendicular/base, which is exactly the pair given in a height-and-distance problem.',
                    },
                    {
                        'q': 'The angle of depression from the top of a cliff to a boat equals the angle of elevation from the boat to the top because:',
                        'options': ['The triangle is isosceles', 'The two horizontal lines are parallel, so the angles are alternate angles', 'Both angles are 45°', 'The cliff is vertical'],
                        'answer': 1,
                        'explain': 'The horizontal through the observer and the horizontal through the boat are parallel; the line of sight is a transversal, so the angles are alternate (Z) angles and equal.',
                    },
                ],
            },
        ],
    },
]
