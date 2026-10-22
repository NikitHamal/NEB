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
