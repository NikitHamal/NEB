# Internet of Things - BCA 454 (Semester VIII, Elective IV, 3 credits)

Study notes for the TU Internet of Things elective (course code CACS460 in the TU outline, Year IV / Semester VIII, 5 hours a week: 3 theory and 2 practical). Six units follow the outline, its topic order and its hours (8, 18, 6, 10, 3 and 3).

| Unit | Title | Hours | Outline topics covered |
|---|---|---|---|
| 1 | Introduction to IoT | 8 | definition and characteristics, physical design, logical design (functional blocks, communication models, APIs), enabling technologies, IoT levels, IoT and M2M (SDN, NFV, SNMP, NETCONF-YANG), nine domain-specific IoTs |
| 2 | Sensors, Actuators and Interfacing | 18 | roles of sensors and actuators; active/passive, analog/digital, contact/no-contact, absolute/relative; position, occupancy and motion, velocity and acceleration, force, pressure, flow, acoustic, humidity, light, radiation, temperature, chemical, biosensor, camera; actuators and PWM; Arduino and Raspberry Pi installation, interfacing and Python programming; laboratory plan |
| 3 | IoT Platform Design Methodology | 6 | the ten steps worked through the weather monitoring system case study (level 6) with a runnable service |
| 4 | Data and Analytics for IoT | 10 | introduction, machine learning, big data analytics tools and technology, edge streaming analytics, network analytics |
| 5 | IoT Physical Servers and Cloud Offering | 3 | cloud storage models and communication APIs (REST, WebSocket, MQTT, CoAP), platforms |
| 6 | Securing IoT Systems | 3 | IoT security challenges and security practices, real incidents, standards |

## Verification

Every Python block is executed by `bca/tools/fill_script_outputs.py` and its real output is inserted (standard library and NumPy only, fixed seeds). Blocks marked `# noexec` need hardware or an account (gpiozero, the DHT22 driver, ThingSpeak) and are shown without output; Arduino C++ sketches are not run (no board in the sandbox) and are marked as such. Hand calculations (ADC steps, LM35 and NTC conversions, ultrasonic distance, barometric altitude, data volumes, HDFS blocks, regression, z-scores, bills and storage budgets) were recomputed in Python; the worked cases in Units 1 to 6 reuse the same programs. The runnable miniature in Unit 3 starts a real local HTTP server on a free port and talks to it with `urllib`.

## Source and honesty

Units, topics and hours follow the TU CACS460 outline as reproduced at notebahadur.com; the reference books it lists are Bahga and Madisetti, *Internet of Things: A Hands-on Approach* (the ten-step methodology, IoT levels and the weather monitoring case); Hanes et al., *IoT Fundamentals* (Cisco Press; Unit 4 follows its data and analytics chapter); Raj Kamal; Gary Smart, *Practical Python Programming for IoT*; and Gaston Hillar, *Internet of Things with Python*. The revised-curriculum elective list names Internet of Things among the Elective IV options, so this book is registered as BCA 454; each college runs a subset of electives. Hardware specifications (Arduino Uno, Raspberry Pi, sensor data-sheet values) are typical published figures; check the data sheet of the exact part. Incident figures (Target, Jeep, Mirai) differ slightly between sources and are quoted as "about"; the UK product-security law and the OWASP and ETSI lists are summarised from public text, so check the current versions. Cloud prices in the examples are illustrative. Nothing here has had a subject-teacher review.
