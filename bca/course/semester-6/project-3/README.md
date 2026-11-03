# Project III — BCA 356

Semester VI · 3 credits · a project course. TU does not publish a unit-wise syllabus for it, so this book is a **companion handbook**. Project I (BCA 256) built a stand-alone program and Project II (BCA 306) built a networked web system. Project III adds the **physical world and data**: sensors measure something real, a small device sends the readings, a server stores and analyses them, and a phone app turns the numbers into a decision. The running example is **KhetSense**, a soil-moisture and weather monitor for a hill-farm cooperative that tells farmers when to irrigate.

| Unit | Title |
|---|---|
| 1 | From Web to IoT: Scope, Architecture and Hardware Choice |
| 2 | Sensors, Calibration, Noise and Messaging |
| 3 | Storing and Analysing Sensor Data: Cleaning, Anomalies and a Forecast |
| 4 | The Mobile Client: Offline-first Sync, Screens and Testing |
| 5 | Field Test, Report, Demo and Viva for Project III |

## Verification

Every program in this book was run and the printed output pasted from the real run (Python 3 standard library plus NumPy: `random` with fixed seeds, `sqlite3`, `json`, `statistics`). No real sensor was connected: sensor values are produced by a documented simulator with a fixed seed so that every number can be reproduced. Hardware code for the ESP32 is shown as MicroPython but is **not executed** here.

## Source and honesty

**The unit structure is reconstructed.** BCA 356 has no published topic list; colleges set their own proposal and report format. **Always follow your own college's project guidelines and your supervisor's instructions first**; where they differ from this book, they win. KhetSense is an invented teaching example, not a real cooperative's system; every farm, name, price and reading in it is made up. Component prices are rough orders of magnitude, not quotes. Nothing here has had a subject-teacher review.
