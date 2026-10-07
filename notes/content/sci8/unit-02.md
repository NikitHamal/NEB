---
subject: Science and Technology
grade: 8
unit: 2
title: Information and Communication Technology
hours: 0
area: Science and Technology
---

Information and communication technology (ICT) includes the devices and systems people use to create, store, find and share information. A phone, radio, computer or school network can help people learn and communicate, but each tool also needs careful use. Understanding how data moves through a device helps us choose suitable tools and protect people and information.

::: key Use technology with purpose
A device is useful when it helps complete a real task safely and accurately. Before sharing, ask: Is the information correct? Do I have permission? Could the post reveal private information or hurt someone?
:::

## 2.1 Devices, data, information, hardware and software

A **digital device** represents information using coded values that electronic circuits can process. **Data** are raw facts such as numbers, words, pictures or sound samples. **Information** is data organised so that it is meaningful. A list of daily temperatures is data; a graph showing a weekly warming trend is information.

**Hardware** is the physical part of a device: screen, keyboard, camera, processor, memory, speakers and storage. **Software** is the set of instructions that tells the hardware what to do. An operating system manages common tasks and helps applications run. A drawing program, calculator and web browser are examples of applications. A device needs both working hardware and appropriate software to perform useful tasks.

```figure caption="A digital device accepts input, processes data, stores it and presents an output."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8, 2.5))
ax.set_xlim(0, 12); ax.set_ylim(0, 5); ax.axis("off")
labels=[("Input",0.5),("Process",3.0),("Storage",5.5),("Output",8.0),("People",10.2)]
for label,x in labels:
    ax.add_patch(FancyBboxPatch((x,1.9),1.55,0.9,boxstyle="round,pad=0.06",fc="#eef3fb",ec=ACCENT,lw=1.0))
    ax.text(x+0.775,2.35,label,ha="center",va="center",fontsize=7.5,color=INK)
for (_,x1),(_,x2) in zip(labels,labels[1:]):
    ax.annotate("",xy=(x2-0.12,2.35),xytext=(x1+1.63,2.35),arrowprops=dict(arrowstyle="->",color=MUTED,lw=1.0))
ax.text(6,0.85,"A task may use only some of these stages.",ha="center",fontsize=7,color=MUTED)
fig.tight_layout()
```

::: example Classify a computer part
**Problem.** A student types a report, saves it and prints a copy. Name the input, storage and output devices or parts.

**Solution.** The **keyboard** is input because it sends typed characters to the computer. A drive or other storage holds the saved file. The **printer** is an output device because it produces a paper copy. The word-processing application is software, not hardware.
:::

## 2.2 Input, processing, storage, output, files and networks

An **input** enters data into a system; examples include a keyboard, microphone, camera or sensor. The processor follows instructions to **process** it. **Storage** keeps data for later use, either temporarily in working memory or for longer in a drive or memory card. **Output** presents results through a screen, speaker, printer or indicator. One device can perform more than one role: a touchscreen displays information and also accepts touch input.

A **file** is a named collection of information, such as a document, image or audio recording. A folder helps organise files. Use clear names, save work regularly and keep an additional copy of important school files where permitted. File extensions such as `.jpg` or `.pdf` often indicate a format; they do not guarantee that a file is safe or trustworthy.

A **network** connects devices so they can exchange data and share services. A local network may connect computers in a school; the internet links many networks around the world. A router helps direct data between networks. Network access does not mean every connected device or message is safe. Use only accounts and networks you are allowed to use.

::: example Make a sensible file name
**Problem.** A student has three science reports from the same year. Suggest a file name that is more useful than `newfile2`.

**Solution.** A clear name could be `science_water_cycle_2026-06-12.docx`. It gives the subject, topic and date without using private details. If the school requires a different format, follow that rule. Store the document in the correct class folder and keep a backup in an approved location.
:::

## 2.3 Internet use, search, privacy, security and communication

A search engine matches words in a query to pages it has indexed. Use specific search words, compare more than one reliable source and check who published the information and when. A result near the top is not automatically correct. For health, safety or current events, prefer a relevant official or expert source and ask a teacher or trusted adult when unsure.

**Privacy** means having control over personal information. A full name combined with a home address, phone number, school timetable or live location can expose a person to harm. Ask permission before posting another person's photo, message or work. Check an app's audience and sharing settings, and do not publish passwords, verification codes or private documents. A digital post can be copied or forwarded even after it is deleted from the original page.

Use a long, unique passphrase for each important account, keep it private and enable an additional sign-in check when available. Do not open unexpected links or attachments, and do not install software from unknown sources. Sign out on shared devices. If an account or device seems compromised, tell a trusted adult or school administrator promptly; do not retaliate or try to break into another account.

Responsible communication is respectful, clear and lawful. Pause before sending an angry message; do not bully, threaten or spread unverified claims. Credit creators when reusing their work and follow copyright or licence conditions. Report harmful content through an appropriate trusted channel rather than resharing it.

```figure caption="A careful search checks the source, date and evidence before information is shared."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.7, 2.7))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
steps=[("Search",(1.2,4.5)),("Check source",(5.4,4.5)),("Compare evidence",(5.4,1.3)),("Share carefully",(1.2,1.3))]
for label,(x,y) in steps:
    ax.add_patch(FancyBboxPatch((x,y),2.4,0.8,boxstyle="round,pad=0.08",fc="#eef3fb",ec=ACCENT,lw=1.0))
    ax.text(x+1.2,y+0.4,label,ha="center",va="center",fontsize=8,color=INK)
for a,b in [((3.7,4.9),(5.2,4.9)),((6.6,4.4),(6.6,2.2)),((5.2,1.7),(3.7,1.7))]:
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle="->",color=MUTED,lw=1.1))
ax.annotate("revise the search if evidence is weak",xy=(1.7,4.35),xytext=(2.4,2.2),ha="center",fontsize=6.8,color=MUTED,arrowprops=dict(arrowstyle="->",color=SERIES[2],connectionstyle="arc3,rad=-0.4"))
fig.tight_layout()
```

::: example Check a search result
**Problem.** A webpage says that a household mixture cures every illness. What should a student check before believing or sharing it?

**Solution.** Check who wrote and published the page, its date, the evidence it provides and whether relevant health authorities support the claim. Compare with reliable sources and ask a trusted adult or health professional. Do not try an unknown treatment or forward the claim merely because many people have shared it.
:::

::: example Respond to a suspicious message
**Problem.** A message says, “Your school account will close today—send your password and code to this link.” What should you do?

**Solution.** Do not click the link or share the password or code. Verify the message using the school's known official contact or website, and report it to a teacher or administrator. A real support worker should not need a student's password or one-time sign-in code.
:::

::: caution A password is not a secret to share with a friend
Even a trusted friend can lose a device or forward a message by mistake. Keep passwords and sign-in codes private, and ask a teacher or guardian for help through an approved process if access is lost.
:::

## Chapter summary

- Data are raw facts; information is data organised to be meaningful.
- Hardware is physical equipment; software is the instructions and applications that use it.
- Digital tasks may use input, processing, storage and output; files and folders help organise work.
- Networks connect devices, but an internet result or link is not automatically safe or accurate.
- Check source, date and evidence; protect private information and use unique passwords.
- Communicate respectfully, ask permission before sharing another person's information and credit reused work.

## Practice questions

1. Which is software? (a) keyboard (b) monitor (c) word processor (d) speaker
2. What is one example of an output device?
3. Give one difference between data and information.
4. Why should a search result's source and date be checked?

::: note Answers to questions 1–4
**1.** (c) — a word processor is an application program.
**2.** A screen, speaker, printer or indicator can present output.
**3.** Data are raw facts; information is data organised to be meaningful.
**4.** The result may be outdated, inaccurate or published by a source without suitable evidence.
:::

5. Explain the roles of input and storage in saving a photograph on a phone.
6. A classmate asks for your sign-in code to “help with homework.” What is a safer response?
7. List three checks for deciding whether a web page is a useful source.
8. Why should you ask permission before posting a photograph of another student?

::: note Answers to questions 5–8
**5.** The camera captures input; the device processes the image and stores it as a file in memory or other approved storage.
**6.** Do not share the code. Offer to help in another way and ask a teacher or guardian if the account needs support.
**7.** Check author or publisher, publication date, evidence and agreement with other reliable sources; any three are acceptable.
**8.** The photograph is personal information. Permission respects the person's privacy and helps prevent unwanted copying or sharing.
:::
