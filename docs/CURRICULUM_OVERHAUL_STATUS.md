# NEBians Official CDC/NEB Curriculum & Content Overhaul Status

## 1. Root-Cause Diagnosis (Why Students Found Discrepancies)

A systematic audit of all 36 school books (`cs8`..`qbank12`), 5 question banks, and entrance tracks revealed the exact root cause of the student-reported syllabus mismatch:

1. **Class 10 Science and Technology (`sci10`) & `qbank10` (Units 2–4)**:
   - While the 19 **unit titles** of `sci10` matched the 2080 BS CDC textbook (*Science and Technology, Grade 10*), the **sub-topic bullets** in `notes/curriculum/sci10.md` were originally drafted as a generic topic guide using pre-2080 SLC/SEE topics rather than the 2080 BS CDC textbook sections.
   - Because chapter authors followed `notes/curriculum/sci10.md` strictly, multiple chapters of `sci10` (and the corresponding Science sections of `qbank10`) taught outdated or off-syllabus topics:
     - **Unit 13 (Information and Communication Technology)**: Taught generic computer fundamentals (CPU, ALU, RAM/ROM, LAN/MAN/WAN topologies, B2B/B2C e-commerce) instead of the official CDC Grade 10 Unit 13 curriculum: **Signals (Analog & Digital), ADC/DAC, Bit/Nibble/Byte, Digital Signal Transmission (Source -> Input Transducer -> Encoder -> Modulator -> Channel -> Demodulator -> Decoder -> Output Transducer -> Output Signal), Baseband vs Broadband Transmission, Positive/Negative Impacts of Digital Technology, Netizen & Digital Citizenship, Online Reputation Management, Digital Wellbeing, and Audio/Video Recording & Editing (`.mp3`, `.wav`, `.mp4`, `.3gp`, `.svi`, trimming/joining steps)**.
     - **Unit 1 (Scientific Learning)**: Taught Vernier callipers and screw gauges (Grade 11 Physics) while omitting **Independent, Dependent & Controlled Variables** and **Unit-wise Equation / Homogeneity Analysis** ($v^2 = u^2 + 2as$, $s = ut + \frac{1}{2}at^2$, $P = hdg$, $F = ma$), which are examined in every SEE paper.
     - **Unit 4 (Heredity)**: Omitted **Mitosis and Meiosis cell division**, **DNA vs RNA structure**, and **Selective Breeding / Crossbreeding (mule, pomato), Artificial Insemination, IVF, and DNA Testing**.
     - **Unit 5 (Physiological Structure and Life Process)**: Covered 4 old systems (Nervous, Endocrine, Reproduction, Excretion) removed in 2080 BS, while missing the 2080 focus on **Human Blood Circulatory System, Blood Pressure, Diabetes, Uric Acid (Gout), Heart Attack, Angiogram, and Open-Heart Surgery**.
     - **Unit 6 (Nature and Environment)**: Omitted **Medicinal Plants of Nepal** (Tulsi, Neem, Gurjo, Ghodtapre, Bojho, Ghiukumari, Yarsagumba, Jatamasi, Sarpagandha, Panchaule) and **Endangered Plants & Animals of Nepal** alongside Climate Change, Greenhouse Effect, and Acid Rain.
     - **Unit 7 (Motion and Force)**: Included Grade 9 Newton's Laws of Motion & Momentum alongside Grade 10 **Gravitation, Gravity, Variation of $g$, Feather-Coin Experiment, Mass/Weight, Free Fall, and Weightlessness**.
     - **Unit 9 (Heat)**: Included Grade 9 latent heat/heat transfer while needing **Anomalous Expansion of Water ($0^\circ\text{C}$ to $4^\circ\text{C}$), Hope's Apparatus, Specific Heat Capacity applications, Calorimetry, and Thermometer Calibration**.
     - **Unit 10 (Wave)**: Included Grade 9 Wave Motion & Sound while missing **Total Internal Reflection, Critical Angle, Optical Fibre/Endoscopy, Dispersion of Light & Rainbow Formation, and Human Eye / Corneal Transplantation / Cataract / Vision Defects**.
     - **Unit 11 (Electricity and Magnetism)**: Included Grade 9 Ohm's Law & Resistance instead of **DC vs AC ($50\text{ Hz}$), Magnetic Field of Straight Wire & Solenoid (Right-Hand Thumb & Grip Rules), Magnetic Flux, Motor Effect, Faraday's Laws of Electromagnetic Induction, AC Generator/Dynamo, and Transformer**.
     - **Unit 12 (Universe)**: Omitted **Importance of Gravitational Force in the Universe, Hubble's Law ($v = Hd$), Critical Density, Open/Flat/Closed Universe, and Big Crunch**.
     - **Unit 15 (Chemical Reaction)**: Included Grade 8/9 Acids, Bases & Salts instead of **Types of Reactions (Combination, Thermal/Electrolytic/Photochemical Decomposition, Single/Double Displacement, Neutralisation, Exothermic/Endothermic) and Rate of Reaction (Temperature, Pressure, Surface Area, Light, Positive & Negative Catalysts)**.
     - **Unit 16 (Gases)**: Taught Boyle's/Charles' laws (Grade 11) and Hydrogen/Oxygen (Grade 9) while completely omitting **Ammonia Gas ($NH_3$ — lab preparation, Haber's process, fountain experiment, properties, uses)** alongside **Carbon Dioxide ($CO_2$), Greenhouse Effect, and Acid Rain**.
     - **Unit 17 (Metal and Non-metals)**: Omitted the specific **Ores of Iron, Aluminium, Copper, Silver, and Gold** and the **5 Steps of Metallurgy (Mining/Grinding, Concentration, Oxidation: Roasting vs Calcination, Reduction/Smelting, Refining)**.
     - **Unit 18 (Hydrocarbon and its Compounds)**: Taught Carboxylic Acids instead of **Monohydric/Dihydric/Trihydric Alcohols and the three required compounds: Methanol ($CH_3OH$), Ethanol ($C_2H_5OH$), and Glycerol / Propane-1,2,3-triol ($C_3H_5(OH)_3$)** alongside Methane, Ethane, Propane, and Butane.
     - **Unit 19 (Chemicals used in Daily Life)**: Taught old syllabus Cement, Glass, Plastics, and Fertilisers instead of **Food Preservatives (Natural vs Chemical), Artificial Fruit Ripening (Calcium Carbide vs Ethylene/Ethephon), Cleaning Agents (Soap Saponification Lab Process, Detergent, Natural Cleansers), and Chemical vs Biological Pesticides (Insecticides, Herbicides, Fungicides, Rodenticides, Pesticides Management Act 2076, Chemical Pollution)**.

2. **Class 8 Question Bank (`qbank8` Units 23–25)**:
   - While `cs8` Unit 20 was updated from QBASIC to Python, `qbank8` Units 23, 24, and 25 still tested QBASIC (`CLS`, `PRINT`, `INPUT`, `MID$`, `WEND`).

3. **Other School Books (`cs10`, `acc10`, `eco10`, `math10`, `omath10`, `soc10`, `nep10`, `eng10`, `sci8`, `math8`, `eng8`, `nep8`, `soc8`, `health8`, `phy11/12`, `chem11/12`, `bio11/12`, `math11/12`, `cs11/12`, `eng11/12`, `nep11/12`)**:
   - Verified against official CDC 2076–2083 curricula/textbooks (`cs10` already uses the 2081/2082 Python curriculum; `acc10` and `eco10` use official 2080/2083 specification grids; `sci8` uses the 2080 CDC textbook including Robotics/AI/Cloud in Unit 2).

---

## 2. Overhaul Tracker (Do Not Duplicate — Pick Up Next `OPEN` Item)

| Target | Scope | Status |
|---|---|---|
| `sci10` Unit 13 | Complete rewrite for official CDC Grade 10 ICT (Signals, ADC/DAC, Nibble/Byte, Digital Communication 9-block chain, Baseband/Broadband, Netizen/Digital Citizenship, Online Reputation, Digital Wellbeing, Audio/Video Editing) | **IN PROGRESS** |
| `sci10` Unit 16 | Rewrite for official CDC Some Gases ($CO_2$ lab prep/properties/uses, $NH_3$ lab prep/Haber's process/fountain experiment/properties/uses, Greenhouse Effect & Acid Rain) | **IN PROGRESS** |
| `sci10` Unit 19 | Rewrite for official CDC Chemicals Used in Daily Life (Food Preservatives, Fruit Ripening, Soap Saponification & Detergents, Chemical vs Biological Pesticides & Pollution) | **IN PROGRESS** |
| `sci10` Unit 5 | Rewrite for official CDC Human Blood Circulatory System, Blood Groups, Blood Pressure, Diabetes, Uric Acid, Heart Attack, Angiogram & Open-Heart Surgery | **IN PROGRESS** |
| `sci10` Unit 12 | Update for official CDC Universe (Gravitational importance, Big Bang, Hubble's Law $v=Hd$, Critical Density, Open/Flat/Closed Universe & Big Crunch) | **IN PROGRESS** |
| `sci10` Unit 1, 4, 6, 7, 9, 10, 11, 15, 17, 18 | Align all remaining `sci10` units with official 2080 CDC textbook sections & SEE 2080/2081 questions | **IN PROGRESS** |
| `qbank10` Units 2, 3, 4 | Update SEE Science Objective, Subjective & Model Question Sets to match 2080 CDC Science syllabus | **OPEN** |
| `qbank8` Units 23, 24, 25 | Replace QBASIC questions/programs with Python to match `cs8` Unit 20 | **OPEN** |
| Export & Rebuild | Run `export_syllabus.py`, `export_study.py`, `build_pdf.py`, and deploy to backend | **IN PROGRESS** |
