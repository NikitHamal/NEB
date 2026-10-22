# Class 12 Mathematics lesson scripts

Shared helpers live in `_m.py`, which reuses the Biology helpers (`Captions`, `table`, `reveal_table`, `example_head`,
`neby_in/out`) and adds `worked` (a problem read aloud, then one written line per narrated sentence, answer in amber),
counting props (`slots`, `num_in`, `tile`, `word`, `person`, `round_table`, `pascal`) and layout helpers (`head`,
`bullets`, `reveal_list`). Minutes are narration length; `python3 tools/lessons/ttskeys.py <script>` lists the narration
cache files a unit uses, so each unit is pushed with only its own audio. Each pushed unit has been checked part by part
with frames.py.

| Unit | Title | Narration | Parts |
|---|---|---|---|
| 1 | Permutation and Combination | 14.2 min | cold open (a Bagmati number plate: does order matter?), 6 parts (AND multiplies / OR adds on a Kathmandu–Pokhara–Jomsom route map, factorials and why 0! = 1, filling boxes with and without repetition; ⁿPᵣ built box by box, ⁿP₄ = 20·ⁿP₂, TRIANGLE with the vowels as one block and in the gaps, 'no two together' vs 'not all together'; AAB with tagged A₁A₂ collapsing 3!/2!, KATHMANDU, MISSISSIPPI with the I's in the gaps; a round table rotating into one arrangement, (n−1)! and garlands (n−1)!/2, eight friends, 5 letters into 3 boxes = 3⁵ not 5³, the formula table; four selections × 3! orders = ⁴P₃, ⁿCᵣ, the 7-men-4-women committee with complements, 12 points with 5 collinear; five properties with their counting reasons, Pascal's triangle with row sums 2ⁿ, n = 9 r = 3 from 36/84/126, ²ⁿC₃ : ⁿC₂ = 44 : 3), 6 worked examples, 3 quizzes, recap |
| 2 | Binomial Theorem | 12.0 min | cold open (the cube root of 127 to four places, without a calculator), 6 parts ((a + b)¹…⁴ beside Pascal's rows, the theorem, why a³b² appears ⁵C₂ = 10 times (choosing b from 2 of 5 brackets), the induction proof via Pascal's rule, (2x + 3/x)⁵, (√3 + 1)⁵ − (√3 − 1)⁵ = 152; T₍ᵣ₊₁₎, middle terms, term independent of x in (x² − 2/x)⁹, coefficient of x³² in (x⁴ − 1/x³)¹⁵, sums of coefficients, 45/120/210 → n = 10; any index with |x| < 1 and partial sums of (1 − x)⁻¹ converging inside the band and flying off outside it, √(1 − 2x) and 1/√(4 + x); (1.02)^⅓, ∛127 = 5.0265, √102, (1.02)¹⁰; e from compound interest, the 1/r! terms stacking up on a number line to e, 2 < e < 3; eˣ, aˣ, log(1 + x) and log((1 + x)/(1 − x)), Σ n/n! = e, cosh 1, log 2 = 0.6931), 11 worked examples, 2 quizzes, recap |
