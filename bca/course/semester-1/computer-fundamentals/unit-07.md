---
subject: Computer Fundamentals and Applications
grade: BCA Semester 1
unit: 7
title: Contemporary Technologies
hours: 13
area: BCA 101 · Computer Fundamentals and Applications · Unit 7
---

Computing keeps changing. This unit surveys the technologies that shape work and study today (e-commerce, e-governance, multimedia, artificial intelligence, the Internet of Things, big data, cloud computing, blockchain, virtual and augmented reality, robotics and mobile networks) and the ethical issues they raise. For each, you get a definition, how it works, what it is used for, and its limits.

::: key What this unit gives you
- E-commerce and e-governance models, with Nepali examples.
- Multimedia: how text, images, audio and video are digitised, with size calculations.
- AI and machine learning, IoT, big data, cloud, blockchain, VR/AR, robotics, 5G.
- Green computing, e-waste, and cyber ethics.
:::

## 7.1 E-commerce, e-business and digital payments

**E-commerce** is buying and selling goods or services over electronic networks; **e-business** is the wider use of the Internet to run all business processes (supply, accounting, customer care).

| Model | Parties | Example |
|---|---|---|
| B2C | business → consumer | Daraz, an airline's online booking |
| B2B | business → business | supplier ordering through a portal |
| C2C | consumer → consumer | Facebook Marketplace, Hamrobazar |
| C2B | consumer → business | freelancers selling services |
| G2C / G2B | government with citizens / businesses | online tax filing |

**Benefits:** 24×7 reach, lower overheads, wider choice, easy price comparison. **Limits:** payment fraud, trust and delivery problems, limited Internet access in remote areas, returns and logistics.

**Digital payments in Nepal:** bank cards and mobile banking, **QR payments** interoperable through Fonepay, and digital wallets such as eSewa, Khalti and IME Pay. A payment gateway links shop, bank and customer; the shop never sees the card secret, and the transaction is authorised, then settled. Nepal Rastra Bank licenses payment service providers.

```svgfig label="7.2" caption="Digital signature: the sender hashes the document and encrypts the hash with the private key; the receiver decrypts with the public key and compares hashes."
f = Fig(760, 290)
f.text(190, 14, "SENDER (Sita)", size=12, color=NAVY, bold=True); f.text(570, 14, "RECEIVER (Ram)", size=12, color=TEAL, bold=True)
f.box(20, 36, 110, 44, "Document", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(20, 120, 110, 44, "Hash (digest)\nSHA-256", fill=SOFT, stroke=SLATE, size=10, bold=True)
f.box(180, 120, 130, 44, "Encrypt hash with\nSita's PRIVATE key", fill=SAND, stroke=AMBER, size=9.5, bold=True)
f.box(180, 200, 130, 40, "Digital signature", fill=SAND, stroke=AMBER, size=11, bold=True)
f.arrow([(75, 80), (75, 120)]); f.arrow([(130, 142), (180, 142)]); f.arrow([(245, 164), (245, 200)], color=AMBER)
f.arrow([(310, 220), (440, 220)], color=SLATE, label="doc + sign + cert", lpos=(375, 210), lsize=9)
f.box(440, 36, 110, 44, "Document\n(received)", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(440, 120, 110, 44, "New hash\nH2", fill=SOFT, stroke=SLATE, size=10.5, bold=True)
f.box(600, 120, 140, 44, "Decrypt signature with\nSita's PUBLIC key = H1", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.box(600, 200, 140, 40, "H1 = H2 ?  valid : reject", fill=ROSE, stroke=RED, size=10, bold=True)
f.arrow([(495, 80), (495, 120)]); f.arrow([(660, 164), (660, 200)], color=TEAL); f.arrow([(550, 142), (600, 142)], color=SLATE, dash=True)
f.arrow([(495, 164), (495, 220), (600, 220)], color=SLATE)
f.text(380, 270, "A valid match proves integrity (not altered) and authenticity (signed by Sita); the certificate from a CA (Nepal: Office of the Controller of Certification) binds the public key to Sita.", size=8.5, color=SLATE)
```

## 7.2 E-governance

**E-governance** uses ICT to deliver government services and to make administration transparent and efficient. Four interaction types: **G2C** (citizens: passport and licence applications, online tax filing), **G2B** (businesses: company registration, customs), **G2G** (between agencies: shared databases) and **G2E** (employees: payroll, leave). Examples in Nepal include the online filing of income tax with the Inland Revenue Department, company registration, the national ID (NID) programme, online driving licence and passport booking, and the Government Integrated Data Centre.

Benefits: less corruption through less face-to-face handling, 24×7 service, lower cost and faster work. Barriers: the **digital divide** (unequal access and skill), electricity and connectivity, security and privacy of citizen data, legacy paper processes, resistance to change.

```svgfig label="7.3" caption="E-governance interaction models: the government (centre) serves citizens (G2C), businesses (G2B), other agencies (G2G) and employees (G2E)."
f = Fig(760, 290)
f.box(250, 108, 260, 74, "GOVERNMENT service platform\n(data centre, NID,\ndigital signature)", fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
M = [(20, 20, "G2C  Citizen", "Nagarik App, online\nPAN / passport form", AMBER, SAND), (540, 20, "G2B  Business", "Customs ASYCUDA,\ncompany registration", TEAL, MINT), (20, 205, "G2G  Agency", "shared NID data,\nIRD with banks", NAVY, BLUE), (540, 205, "G2E  Employee", "online leave, payroll,\nSutra system", RED, ROSE)]
for x, y, t, e, c, bg in M:
    f.box(x, y, 200, 66, t + "\n" + e, fill=bg, stroke=c, size=10, bold=False)
f.arrow([(220, 60), (290, 125)], color=AMBER, both=True); f.arrow([(540, 60), (470, 125)], color=TEAL, both=True)
f.arrow([(220, 235), (290, 165)], color=NAVY, both=True); f.arrow([(540, 235), (470, 165)], color=RED, both=True)
```

## 7.3 Multimedia

**Multimedia** combines text, images, audio, video and animation, usually with interactivity. Everything is digitised: sampled, quantised and stored as bits.

- **Image**: a grid of **pixels**; size = width × height × bits per pixel / 8. **Raster** formats: JPEG (lossy photos), PNG (lossless, transparency), GIF (256 colours, animation); **vector** formats (SVG) store shapes and scale without blur.
- **Audio**: **sampling rate** × **bit depth** × channels. CD audio: 44,100 samples/s × 16 bits × 2 channels.
- **Video**: a sequence of frames (24–60 per second); compressed by codecs such as H.264 and H.265, which exploit similarity between frames.
- **Compression**: *lossless* (ZIP, PNG; exact recovery) versus *lossy* (JPEG, MP3, H.264; discards detail people barely notice).

::: example Worked example: raw sizes
**Image** 1920 × 1080 at 24 bits per pixel: 1920 × 1080 × 3 bytes = 6,220,800 bytes ≈ **5.93 MiB** uncompressed.

**Audio**, 1 minute of CD quality: 44,100 × 16 × 2 = 1,411,200 bits per second = 176,400 bytes per second; × 60 = 10,584,000 bytes ≈ **10.1 MiB**. MP3 at 128 kbps needs 128,000 × 60 / 8 = 960,000 bytes ≈ **0.92 MiB**, about 11 times smaller.

**Video**, 1 second of uncompressed 1080p at 30 fps, 24-bit colour: 6,220,800 × 30 ≈ 187 MB. This is why compression is unavoidable.
:::

Applications: education, entertainment, advertising, simulation, games, digital libraries. **Authoring tools:** Photoshop/GIMP (images), Audacity (audio), DaVinci Resolve/Premiere (video), Blender (3D and animation).

```photogrid label="7.1" cols="4" ratio="1.2" caption="Contemporary technologies as real devices: (a) a VR headset, (b) a Raspberry Pi single-board computer that runs IoT projects, (c) a PIR motion sensor used in IoT nodes, (d) a 3D printer building an object layer by layer."
@ photo id="bca101/vr" cap="VR headset: display + lenses + head tracking"
@ photo id="bca101/rpi" cap="Raspberry Pi 4: a small Linux computer for IoT gateways"
@ photo id="bca101/pir" cap="PIR sensor: detects motion by infrared change"
@ photo id="bca101/print3d" cap="3D printing: additive manufacturing"
```

## 7.4 Artificial intelligence and machine learning

**Artificial intelligence (AI)** is the study of machines doing tasks that normally need human intelligence: perceiving, reasoning, learning, deciding. **Machine learning (ML)** is the branch where a system *learns patterns from data* rather than being told explicit rules; **deep learning** uses many-layered neural networks.

| ML type | Learns from | Example |
|---|---|---|
| Supervised | labelled examples | spam filter, house-price prediction, exam-result classification |
| Unsupervised | unlabelled data | grouping customers by behaviour |
| Reinforcement | rewards through trial and error | game-playing agents, robot control |

Applications: speech recognition, translation, face and image recognition, recommendation systems, medical imaging, chatbots and large language models, self-driving research, fraud detection.

**Limits and issues:** AI needs large quantities of good data; it can inherit **bias** from that data; it can be confidently wrong; its decisions may be hard to explain; privacy, copyright and job-displacement concerns follow. AI is a tool whose output needs human checking. The Semester V subject *Artificial Intelligence* is a full course.

**Expert systems** (rules from human experts, e.g. medical diagnosis aids) and **natural language processing** (NLP) are classical AI areas still in use.

## 7.5 Internet of Things (IoT)

IoT is a network of physical objects with **sensors**, small processors and connectivity that collect and exchange data without human intervention. An IoT system has four layers: sensing devices, connectivity (Wi-Fi, Bluetooth, LoRa, 4G/5G), a cloud platform that stores and analyses data, and an application that shows or acts on the result.

Examples: smart home (lights, thermostat), smart agriculture (soil-moisture sensors that trigger irrigation), health wearables, smart meters, vehicle tracking, industrial monitoring. Common hardware: **Arduino**, **ESP32**, **Raspberry Pi**.

Issues: security of cheap devices (default passwords make botnets), privacy of data collected at home, interoperability, power and connectivity.

## 7.6 Big data

**Big data** is data too large, fast or varied for ordinary tools. The classic description is the **3 Vs**: **Volume** (terabytes to petabytes), **Velocity** (generated and processed in real time) and **Variety** (structured tables, semi-structured JSON, unstructured text, images, video); **Veracity** (data quality) and **Value** are often added.

Technologies: distributed storage and processing (**Hadoop**, **Spark**), NoSQL stores, data warehouses and lakes. Uses: recommendation, fraud detection, traffic and weather prediction, health analytics. Issues: privacy, security, storage cost, and the risk of wrong conclusions from poor data. The BCA electives *Data Mining and Data Warehouse* and *Business Intelligence* extend this.

## 7.7 Cloud computing

**Cloud computing** delivers computing resources (servers, storage, databases, software) over the Internet on demand, billed by use, instead of owning them.

| Service model | You manage | Provider manages | Example |
|---|---|---|---|
| **IaaS** | OS, apps, data | servers, storage, network | AWS EC2, Azure VMs |
| **PaaS** | apps, data | OS, runtime, infrastructure | Google App Engine, Heroku |
| **SaaS** | just use it | everything | Gmail, Google Docs, Microsoft 365 |

**Deployment models:** *public* (shared, run by a provider), *private* (one organisation), *hybrid* (both), *community*. **Features:** on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service. **Benefits:** no upfront hardware cost, scale up and down, global access, built-in backup. **Concerns:** dependence on connectivity, data privacy and jurisdiction, vendor lock-in, outages. **Virtualisation** (many virtual machines on one physical server) underlies it; **edge computing** processes data near its source to reduce delay. (Semester VIII: *Cloud Computing*.)

```svgfig label="7.1" caption="Cloud service models as a stack: what the provider manages (shaded) and what the customer manages, for IaaS, PaaS and SaaS."
f = Fig(760, 300)
layers = ["Application", "Data", "Runtime / middleware", "Operating system", "Virtualisation, servers", "Storage and network"]
cols = [("On-premises", 10), ("IaaS", 200), ("PaaS", 390), ("SaaS", 580)]
cust = {"On-premises": 6, "IaaS": 4, "PaaS": 2, "SaaS": 0}
ex = {"On-premises": "own server room", "IaaS": "AWS EC2, Azure VM", "PaaS": "Google App Engine, Heroku", "SaaS": "Gmail, Google Docs, eSewa web"}
for name, x in cols:
    f.text(x + 85, 14, name, size=12.5, color=NAVY, bold=True)
    for i, l in enumerate(layers):
        mine = i < cust[name]
        f.box(x, 28 + i * 34, 170, 30, l, fill=SAND if mine else MINT, stroke=AMBER if mine else TEAL, size=9.5, bold=mine)
    f.text(x + 85, 248, ex[name], size=9.5, color=SLATE, italic=True)
f.box(200, 268, 14, 14, "", fill=SAND, stroke=AMBER); f.text(222, 275, "customer manages", size=9.5, anchor="start")
f.box(360, 268, 14, 14, "", fill=MINT, stroke=TEAL); f.text(382, 275, "provider manages", size=9.5, anchor="start")
```

## 7.8 Blockchain and cryptocurrency

A **blockchain** is a shared, append-only ledger kept by many computers. Transactions are grouped into **blocks**; each block stores a **hash** (a fixed-size fingerprint) of the previous block, so altering any old block changes every later hash and is detected. A **consensus** rule (proof of work or proof of stake) decides who adds the next block, so no single authority is needed.

Uses: cryptocurrencies (Bitcoin, Ethereum), supply-chain tracing, land and academic-record verification, smart contracts. Issues: energy use (proof of work), volatility and fraud in crypto markets, slow throughput, irreversible mistakes. In Nepal, **Nepal Rastra Bank has declared cryptocurrency trading illegal** (2017 notice, reaffirmed since); learn the technology but follow the law.

## 7.9 Virtual, augmented and mixed reality; robotics; 5G

- **Virtual reality (VR)** immerses the user in a computer-generated world through a headset and motion tracking (training simulators, games, virtual field trips). **Augmented reality (AR)** overlays digital content on the real view (Pokémon Go, furniture preview in a phone camera, navigation arrows). **Mixed reality** lets virtual objects interact with the real ones.
- **Robotics** combines sensors, actuators and control software: industrial arms, surgical robots, drones, warehouse robots, agricultural robots. A robot senses → decides → acts.
- **Drones (UAVs)** are used for photography, surveying and delivery.
- **5G** is the fifth cellular generation: higher speed (up to Gbps), very low latency (about 1 to 10 ms) and capacity for many devices. It enables remote surgery trials, IoT at scale and cloud gaming.
- **3D printing** builds objects layer by layer from a digital model; **quantum computing** uses qubits that can be in superposition and may one day solve special problems (factoring, simulation) far faster; it is still experimental.

## 7.10 Green computing, e-waste and cyber ethics

**Green computing** is designing and using computers with less environmental harm: energy-efficient hardware, power management and sleep modes, virtualisation, cloud consolidation, recycling. **E-waste**: discarded devices contain lead, mercury and cadmium; they must be recycled or refurbished, not burned or dumped. Extending a device's life is the greenest option.

**Cyber ethics** is acting responsibly online: respect for privacy, copyright and licences; no hacking or piracy; no cyberbullying or hate speech; honesty (no plagiarism, no fake news); protecting other people's data. The **digital footprint** you leave (posts, searches, locations) is permanent in practice, so think before posting. **Digital divide**: the gap between those who have access and skill and those who do not; closing it is a national task in Nepal (rural connectivity, community learning centres).

## Formula and fact sheet

- Image bytes = W × H × bits per pixel / 8. Audio rate = sample rate × bit depth × channels.
- 3 Vs of big data: volume, velocity, variety.
- IaaS / PaaS / SaaS; public / private / hybrid cloud.
- Supervised (labelled), unsupervised (unlabelled), reinforcement (rewards).
- E-commerce models B2C, B2B, C2C, C2B; e-governance G2C, G2B, G2G, G2E.
- Blockchain = linked blocks with hashes + consensus. Cryptocurrency trading is illegal in Nepal.
- IoT = sensors + connectivity + cloud + application. 5G = speed, low latency, many devices.

## Chapter summary

- E-commerce and e-governance move trade and public service online; Nepali payment wallets and QR have made small payments digital.
- Multimedia is digitised media; compression (lossless or lossy) makes it practical.
- AI and ML learn from data; IoT collects data; big data and the cloud store and process it at scale.
- Blockchain provides a tamper-evident shared ledger; VR/AR, robotics and 5G extend where computing reaches.
- Every technology brings ethical and environmental responsibilities.

## Practice

**A. Short questions**

1. Define e-commerce. List its models with an example each.
2. What is e-governance? Give four examples from Nepal.
3. Differentiate lossy and lossless compression.
4. Define AI, ML and deep learning.
5. What is IoT? Name its four layers.
6. What are the 3 Vs of big data?
7. Differentiate IaaS, PaaS and SaaS.
8. What is a blockchain?
9. Differentiate VR and AR.
10. What is e-waste? How can it be reduced?

**B. Numerical problems**

11. Find the uncompressed size in MiB of a 1280 × 720 image with 24-bit colour.
12. How many bytes does 3 minutes of mono audio at 44.1 kHz, 16-bit need?
13. An MP3 is 4 MiB and plays for 4 minutes. Find its average bit rate in kbps.

**C. Long questions**

14. Explain cloud computing with its service and deployment models.
15. Discuss the benefits and challenges of e-governance in Nepal.
16. Explain how machine learning differs from conventional programming, with examples of its three types.

::: note Answers and worked solutions
**1.** E-commerce is trading through electronic networks. B2C (Daraz), B2B (supplier portal), C2C (Hamrobazar), C2B (freelancing).
**2.** Use of ICT in government services. Online income-tax filing, company registration, passport/licence appointments, national ID.
**3.** Lossless recovers the original exactly (ZIP, PNG); lossy discards less-noticeable detail for smaller files (JPEG, MP3).
**4.** AI: machines performing tasks needing intelligence; ML: learning patterns from data; deep learning: ML with multi-layer neural networks.
**5.** Network of sensor-equipped connected objects. Layers: sensing devices, connectivity, cloud/analytics, application.
**6.** Volume, velocity, variety.
**7.** IaaS rents infrastructure (virtual servers); PaaS gives a platform to run your applications; SaaS provides ready software over the web.
**8.** A distributed, append-only ledger of blocks linked by hashes and maintained by consensus, making tampering evident.
**9.** VR replaces the real world with a virtual one; AR adds virtual content to the real world.
**10.** Discarded electronics containing toxic metals. Reduce by repair, reuse, refurbishing and certified recycling.
**11.** 1280 × 720 × 3 = 2,764,800 bytes ≈ **2.64 MiB**.
**12.** 44,100 × 2 bytes × 180 s = **15,876,000 bytes** ≈ 15.1 MiB.
**13.** 4 MiB = 4 × 1,048,576 × 8 = 33,554,432 bits; over 240 s = 139,810 bps ≈ **140 kbps**.
**14.** Definition, five features, IaaS/PaaS/SaaS table, deployment models, benefits and concerns (§7.7).
**15.** Use §7.2: benefits (transparency, speed, cost, 24×7) and barriers (digital divide, security, infrastructure, skills).
**16.** Conventional programming: rules + data → answers. ML: data + answers → rules (a model). Supervised: spam filter; unsupervised: customer clustering; reinforcement: game agent.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

### Medium question (5 marks)

**Q10. Explain the Internet of Things (IoT) with its layers and applications. (5 marks)**

The **Internet of Things** is a network of physical objects with sensors, small processors and network connections that collect and exchange data without human typing (Plate 7.1).

1. **Sensing layer:** sensors and actuators (temperature, motion, soil moisture, GPS) such as the PIR sensor in Plate 7.1.
2. **Network layer:** Wi-Fi, Bluetooth, LoRa, 4G/5G or Ethernet carries the readings.
3. **Gateway/edge:** a small computer such as a Raspberry Pi filters data and forwards it.
4. **Cloud/data layer:** servers store and analyse the data.
5. **Application layer:** dashboards, mobile apps and automatic actions.

| Domain | Nepali example |
|---|---|
| Agriculture | soil-moisture sensors that control irrigation in Terai farms |
| Smart home | motion light, smart meter of the electricity authority |
| Health | wearable heart-rate bands |
| Transport | GPS tracking of buses and ambulances |
| Environment | air-quality monitors in Kathmandu Valley |

**Challenges.** Weak device security, privacy, battery life, poor connectivity and standards. **Example.** A farmer's sensor sends moisture data through a gateway to the cloud, and the app starts the pump when the soil is dry.

### Long question (10 marks)

**Q14. Explain cloud computing with its service and deployment models. (10 marks)**

**Introduction.** **Cloud computing** is the delivery of computing resources (servers, storage, databases, software) over the Internet on demand, usually paid by use. NIST lists five characteristics: on-demand self-service, broad network access, resource pooling, rapid elasticity and measured service.

**Service models** (Figure 7.1)

1. **IaaS (Infrastructure as a Service):** the provider gives virtual machines, storage and networks; the customer installs the OS and applications. *Example:* AWS EC2, Azure VM.
2. **PaaS (Platform as a Service):** the provider gives the OS and runtime; the customer deploys only code and data. *Example:* Google App Engine, Heroku.
3. **SaaS (Software as a Service):** ready-made software used through a browser. *Example:* Gmail, Google Docs, Microsoft 365.

**Deployment models**

4. **Public cloud:** shared infrastructure owned by a provider (AWS, Azure, Google Cloud). Cheap and scalable.
5. **Private cloud:** used by one organisation, in its own or hired data centre. More control and security, higher cost.
6. **Hybrid cloud:** public and private clouds joined together; sensitive data stays private while peak load goes public.
7. **Community cloud:** shared by organisations with common needs, such as several banks or universities.

| Model | Customer manages | Example |
|---|---|---|
| IaaS | OS, runtime, data, app | virtual server |
| PaaS | data and app | app platform |
| SaaS | only own data and settings | webmail |

**Benefits.** Low start-up cost, elasticity, access from anywhere, automatic backup and updates. **Challenges.** Internet dependence, data privacy and legal location of data, vendor lock-in and security responsibility.

**Nepali example.** A college hosts its results portal on a cloud VM (IaaS), uses Google Workspace for email (SaaS), and scales servers up during results week.

**Conclusion.** Cloud computing turns computing into a utility. The service model decides how much work the customer keeps, and the deployment model decides who shares the infrastructure.

**Q15. Discuss the benefits and challenges of e-governance in Nepal. (10 marks)**

**Introduction.** **E-governance** is the use of ICT by government to deliver services, share information and involve citizens. Its models are G2C, G2B, G2G and G2E (Figure 7.3). Nepal's Digital Nepal Framework, the National ID project, the Nagarik App and the Electronic Transactions Act 2063 support it.

**Benefits**

1. **Transparency:** online records and tracking reduce hidden decisions and bribery.
2. **Saves time and cost:** a citizen applies for a PAN or driving-licence service online instead of travelling to several offices.
3. **Efficiency:** shared data (G2G) avoids repeated forms and speeds up approvals.
4. **Wider access:** remote districts can use services through mobile phones and common service centres.
5. **Accountability:** every action is logged and signed with a digital signature (Figure 7.2).
6. **Revenue:** online tax filing and customs systems increase collection.

**Challenges**

7. **Digital divide:** low internet access, cost and digital literacy in rural areas.
8. **Security and privacy:** large national databases attract hackers and need strong law and encryption.
9. **Infrastructure and power:** unreliable electricity and network links.
10. **Legacy processes and resistance:** paper rules, staff skills and lack of interoperability between offices.

| Aspect | Benefit | Challenge |
|---|---|---|
| Citizens | fast, cheap service | no device or skill |
| Government | efficiency, revenue | cost, staff training |
| Data | one source of truth | privacy and breaches |

**Examples in Nepal.** Online vehicle tax, Nagarik App documents, Inland Revenue return filing, customs clearance, and the Sutra payroll system.

**Conclusion.** E-governance makes services faster and more transparent. Its success in Nepal depends on connectivity, training, privacy law and trust.

**Q16. Explain how machine learning differs from conventional programming, with examples of its three types. (10 marks)**

**Introduction.** In **conventional programming** a human writes the rules; the program applies the rules to data and gives answers. In **machine learning (ML)** the computer receives data and answers, and it finds the rules itself. The learned rules are called a **model**.

| Basis | Conventional programming | Machine learning |
|---|---|---|
| Input | data and rules | data and expected answers |
| Output | answers | rules (model) |
| Rules written by | programmer | algorithm from examples |
| Suitable for | clear fixed logic (payroll) | patterns too complex to write (faces, speech) |
| Changes | edit the code | retrain with new data |
| Example | tax calculator | spam filter |

**Three types of machine learning**

1. **Supervised learning:** learns from **labelled** examples. *Classification* predicts a category (spam or not spam, pass or fail); *regression* predicts a number (house price). *Example:* predicting whether a student will pass from attendance and marks.
2. **Unsupervised learning:** finds structure in **unlabelled** data. *Clustering* groups similar items; *association* finds items bought together. *Example:* grouping customers of a Kathmandu supermarket by buying habits.
3. **Reinforcement learning:** an agent acts in an environment and receives **rewards or penalties**, learning the best policy by trial and error. *Example:* a robot learning to walk, or a game-playing program.

**Workflow.** Collect data, clean it, split into training and test sets, train a model, evaluate accuracy, deploy and monitor. A model that memorises the training data is **overfitted** and fails on new data.

**Applications.** Nepali-language speech recognition, crop-disease detection from photographs, credit scoring and fraud detection in banks, and recommendations on video sites.

**Conclusion.** Machine learning replaces hand-written rules by rules learned from data. Supervised, unsupervised and reinforcement learning cover prediction, discovery and decision-making, and all depend on good-quality data.
