---
subject: Question Bank
grade: 11
unit: 16
title: "Computer Science: Model Question Sets and Predicted Questions"
hours: 0
area: Computer Science
---

This chapter does three jobs. It sets out the grid of the Grade 11 Computer Science paper and what it implies for study; it gives **two complete model papers** with full solutions, each to the exact pattern of 2 hours and 50 marks; and it ends with a **ranked list of predicted questions**, each with the reason for its rank.

::: caution What "predicted" means here
Nobody outside the examination board knows next year's paper. The ranking below rests on two things only: the **grid**, which fixes how many questions of each kind are asked, and the **syllabus**, which fixes what can be asked. It is not a claim that any question will come, and none of the model questions is a copy of a past paper. If a topic is ranked low, that means it is less likely, never that it is safe to skip.
:::

::: key The grid (50 marks, 2 hours)
| Group | Questions | Marks | Skill |
|---|---|---|---|
| A | 9 MCQs | 9 x 1 = 9 | recall and short output |
| B | 5 short questions, most with an "or" choice | 5 x 5 = 25 | define, differentiate, explain, short program, short HTML |
| C | 2 long questions, with an "or" choice | 2 x 8 = 16 | longer program or HTML page, or an explanation with a diagram |
:::

## 16.1 Pattern analysis

### 16.1.1 What the grid implies

- Written answers carry 41 of the 50 marks. A student who only revises MCQs cannot pass comfortably.
- With an "or" choice in most written questions, you must be strong in **one of the two options of each question**, not both.
- Eight units share 80 teaching hours. Dividing the 50 marks in proportion to teaching hours gives the expected weight in the table below.

| Unit | Hours | Expected marks (hours/80 x 50) | Typical vehicle |
|---|---|---|---|
| 1 Computer System | 20 | 12.5 | MCQs, a differentiate table, short notes |
| 2 Number System and Boolean Logic | 11 | 6.9 | conversion, complement subtraction, truth-table proof |
| 3 Software and Operating System | 12 | 7.5 | OS functions, differentiate, Linux |
| 4 Application Package | 5 | 3.1 | short notes, one MCQ |
| 5 Programming Concepts and Logics | 8 | 5.0 | C programs in Group B and Group C |
| 6 Web Technology I | 8 | 5.0 | HTML code, CSS types |
| 7 Multimedia | 6 | 3.8 | components, applications |
| 8 Information Security and Cyber Law | 10 | 6.3 | cybercrime, malware, IPR, cyber law |

```figure caption="Expected weight of each unit if the 50 marks follow teaching hours. Programming usually earns more than this share, because the 8-mark long questions are most often programs."
import numpy as np, matplotlib.pyplot as plt
units = ["1 System", "2 Number/Logic", "3 Software/OS", "4 Packages", "5 Programming", "6 Web I", "7 Multimedia", "8 Security"]
hrs = np.array([20, 11, 12, 5, 8, 8, 6, 10])
marks = hrs / 80 * 50
y = np.arange(len(units))[::-1]
fig, ax = plt.subplots(figsize=(4.8, 2.9))
ax.barh(y, marks, height=0.6, color=ACCENT)
for yi, m in zip(y, marks):
    ax.text(m + 0.2, yi, f"{m:.1f}", va="center", ha="left", fontsize=8, color=INK)
ax.set_yticks(y); ax.set_yticklabels(units, fontsize=8)
ax.set_xlim(0, 15)
ax.set_xlabel("Expected marks out of 50", fontsize=8)
ax.tick_params(labelsize=8, length=0)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.xaxis.grid(True, color=GRID, lw=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
```

### 16.1.2 Question types that keep returning

| Type | Why it returns |
|---|---|
| C program using a loop or an array | The syllabus names control structures, arrays and strings, and a program is the only fair way to test them |
| Number conversion and complement subtraction | A bounded, calculable topic with a single right answer |
| Truth-table verification of a Boolean law | The syllabus says "statement and verification of laws using truth table" |
| "Differentiate between" with a table | Easy to mark; five contrasts, five marks |
| HTML code for a described page | Syllabus is a long list of tags and forms |
| Cybercrime, malware and protection | A whole unit of 10 hours with plenty to write |

## 16.2 Model Set 1

### 16.2.1 Question paper

**Computer Science, Grade XI, Model Set 1**  
Time: 2 hours  Full marks: 50  Pass marks: 20  
*Candidates are required to give their answers in their own words as far as practicable. The figures in the margin indicate full marks. Attempt all questions.*

**Group A: Multiple choice questions** (9 x 1 = 9)  
*Rewrite the correct option of each question in your answer sheet.*

1. Transistors were used as the main switching device in which generation of computers? <span class="marks">[1]</span>
   (a) first (b) second (c) third (d) fourth
2. How many megabytes are there in 1 GB? <span class="marks">[1]</span>
   (a) 1024 (b) 1000 (c) 1048 (d) 512
3. The binary equivalent of the decimal number 13 is <span class="marks">[1]</span>
   (a) 1011 (b) 1110 (c) 1101 (d) 1001
4. The operating system function of allocating CPU time to different programs is <span class="marks">[1]</span>
   (a) process management (b) file management (c) security management (d) device management
5. What is the output of `int x = 9; printf("%d", x / 2 + x % 2);`? <span class="marks">[1]</span>
   (a) 4 (b) 5 (c) 6 (d) 1
6. How many times does the body of `for (i = 0; i < 5; i += 2)` execute? <span class="marks">[1]</span>
   (a) 2 (b) 3 (c) 4 (d) 5
7. Which attribute of the `<img>` tag gives the file name of the picture? <span class="marks">[1]</span>
   (a) href (b) src (c) alt (d) link
8. WAV and MP3 are file formats of which multimedia component? <span class="marks">[1]</span>
   (a) text (b) graphics (c) audio (d) animation
9. Malicious software that secretly records the keys pressed by a user is a type of <span class="marks">[1]</span>
   (a) spyware (b) firewall (c) compiler (d) utility

**Group B: Short answer questions** (5 x 5 = 25)

10. (a) Differentiate between primary memory and secondary memory. <span class="marks">[5]</span>  
    **Or** (b) What is a bus? Explain the data bus, address bus and control bus. *(1+4)* <span class="marks">[5]</span>
11. (a) Convert $(225)_{10}$ into binary, octal and hexadecimal. <span class="marks">[5]</span>  
    **Or** (b) State and verify the identity $A + A'B = A + B$ using a truth table. <span class="marks">[5]</span>
12. (a) Write a C program to read a number and find the sum of its digits. <span class="marks">[5]</span>  
    **Or** (b) Write a C program to read ten numbers in an array and count how many are even and how many are odd. <span class="marks">[5]</span>
13. (a) Write HTML code to display the heading "Welcome to Nepal" in red, centred, followed by a picture with alternative text and an unordered list of three cities. <span class="marks">[5]</span>  
    **Or** (b) Differentiate between tag and attribute. Explain the HTML5 `audio` and `video` elements. *(2+3)* <span class="marks">[5]</span>
14. (a) What is cybercrime? Explain phishing, hacking and ransomware. *(1+4)* <span class="marks">[5]</span>  
    **Or** (b) What is a digital signature? Explain copyright and trademark. *(2+3)* <span class="marks">[5]</span>

**Group C: Long answer questions** (2 x 8 = 16)

15. (a) Write a C program to read the marks of five students in an array and display the total, the highest, the lowest and the average. <span class="marks">[8]</span>  
    **Or** (b) Write a C program to read a word, count the number of vowels in it and display the word in reverse. <span class="marks">[8]</span>
16. (a) Explain the components of a computer system with a block diagram. *(3+5)* <span class="marks">[8]</span>  
    **Or** (b) What is multimedia? Explain its components and any four applications. *(2+3+3)* <span class="marks">[8]</span>

### 16.2.2 Solutions to Model Set 1

::: note Group A
**1.** (b) — second generation (1956 to 1963) used transistors.
**2.** (a) — 1 GB = 1024 MB.
**3.** (c) — $13 = 8 + 4 + 1 = 1101$.
**4.** (a) — scheduling the CPU is process management.
**5.** (b) — $9/2 = 4$ in integers and $9 \% 2 = 1$, so $4 + 1 = 5$.
**6.** (b) — $i$ takes the values 0, 2 and 4; at 6 the condition $i < 5$ fails.
**7.** (b) — `src` names the image file; `alt` gives the replacement text.
**8.** (c) — both are audio formats.
**9.** (a) — a keylogger is a kind of spyware.
:::

**10.** (a)

| Primary memory | Secondary memory |
|---|---|
| Directly accessed by the CPU | Accessed through the I/O system after loading into primary memory |
| Fast | Slower |
| Smaller capacity, costlier per byte | Large capacity, cheaper per byte |
| RAM is volatile; ROM and cache are part of it | Non-volatile, keeps data permanently |
| RAM, ROM, cache | Hard disk, flash drive, DVD |

**Or (b)** A bus is a set of parallel wires that carries data, addresses and signals between the components of a computer.
- **Data bus**: carries data and instructions between CPU, memory and I/O; it is bidirectional, and its width equals the word length.
- **Address bus**: carries the address of the memory location or device to be accessed, one way from CPU to memory; $n$ address lines can address $2^n$ locations.
- **Control bus**: carries control signals such as memory read, memory write, clock and interrupt; it is bidirectional.

**11.** (a) Binary: $225 \div 2 = 112$ r 1; $112 \div 2 = 56$ r 0; $56 \div 2 = 28$ r 0; $28 \div 2 = 14$ r 0; $14 \div 2 = 7$ r 0; $7 \div 2 = 3$ r 1; $3 \div 2 = 1$ r 1; $1 \div 2 = 0$ r 1. Reading upward, $(225)_{10} = (11100001)_2$.

Octal: group in threes from the right: 011 100 001 gives 3, 4, 1, so $(341)_8$.

Hexadecimal: group in fours: 1110 0001 gives E and 1, so $(E1)_{16}$. Check: $14 \times 16 + 1 = 225$.

**Or (b)** The identity $A + A'B = A + B$.

| A | B | A' | A'B | A + A'B | A + B |
|---|---|---|---|---|---|
| 0 | 0 | 1 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 | 1 | 1 |
| 1 | 0 | 0 | 0 | 1 | 1 |
| 1 | 1 | 0 | 0 | 1 | 1 |

The columns $A + A'B$ and $A + B$ are the same in all four rows, so the identity is verified.

**12.** (a)

```
#include <stdio.h>
int main() {
    int n, sum = 0;
    printf("Enter a number: ");
    scanf("%d", &n);
    while (n > 0) {
        sum = sum + n % 10;
        n = n / 10;
    }
    printf("Sum of digits = %d\n", sum);
    return 0;
}
```

Sample run: input 4825 gives `Sum of digits = 19` (4 + 8 + 2 + 5). The loop takes the last digit with `% 10`, adds it, and removes it with `/ 10`.

**Or (b)**

```
#include <stdio.h>
int main() {
    int a[10], i, even = 0, odd = 0;
    printf("Enter 10 numbers: ");
    for (i = 0; i < 10; i++) {
        scanf("%d", &a[i]);
        if (a[i] % 2 == 0)
            even++;
        else
            odd++;
    }
    printf("Even = %d, Odd = %d\n", even, odd);
    return 0;
}
```

Sample run: input 1 to 10 gives `Even = 5, Odd = 5`.

**13.** (a)

```
<html>
<head>
  <title>Nepal</title>
</head>
<body>
  <h1 align="center"><font color="red">Welcome to Nepal</font></h1>
  <img src="everest.jpg" alt="Mount Everest" width="300">
  <ul>
    <li>Kathmandu</li>
    <li>Pokhara</li>
    <li>Lumbini</li>
  </ul>
</body>
</html>
```

**Or (b)** A tag is a keyword in angle brackets that defines an HTML element, such as `<p>`; an attribute gives extra information to a tag as name="value" inside the opening tag, such as `align="center"`.
- The `<audio>` element plays sound without a plug-in: `<audio src="song.mp3" controls></audio>`; the `controls` attribute shows play and volume buttons.
- The `<video>` element plays video: `<video src="lesson.mp4" width="320" height="240" controls></video>`. Several formats can be offered with `<source>` elements inside either tag, and `<track>` adds subtitles to a video.

**14.** (a) Cybercrime is a crime committed using a computer or network, or aimed at them.
- **Phishing**: fake emails, messages or websites that look genuine are used to trick people into giving passwords, card numbers or bank details.
- **Hacking**: gaining access to a computer or network without permission, to steal, change or destroy data.
- **Ransomware**: malware that locks or encrypts a victim's files and demands payment for the key.

**Or (b)** A digital signature is an electronic code made with the sender's private key and attached to a document; the receiver checks it with the public key. It proves the sender's identity (authentication), shows that the message was not altered (integrity), and stops the sender from denying it (non-repudiation).

Copyright is the legal right of the creator of an original work, such as a book, song or program, to copy, distribute and adapt it, and to stop others doing so without permission. A trademark is a name, logo or sign registered to identify the goods of one business and distinguish them from those of others.

**15.** (a)

```
#include <stdio.h>
int main() {
    int m[5], i, total = 0, max, min;
    printf("Enter marks of 5 students: ");
    for (i = 0; i < 5; i++) {
        scanf("%d", &m[i]);
        total = total + m[i];
    }
    max = min = m[0];
    for (i = 1; i < 5; i++) {
        if (m[i] > max)
            max = m[i];
        if (m[i] < min)
            min = m[i];
    }
    printf("Total = %d\n", total);
    printf("Highest = %d\n", max);
    printf("Lowest = %d\n", min);
    printf("Average = %.2f\n", total / 5.0);
    return 0;
}
```

Sample run: input `56 78 34 90 62` gives Total = 320, Highest = 90, Lowest = 34, Average = 64.00. Dividing by `5.0` and not `5` keeps the fractional part.

**Or (b)**

```
#include <stdio.h>
#include <string.h>
int main() {
    char s[50];
    int i, v = 0;
    printf("Enter a word: ");
    scanf("%s", s);
    for (i = 0; i < strlen(s); i++) {
        switch (s[i]) {
            case 'a': case 'e': case 'i': case 'o': case 'u':
            case 'A': case 'E': case 'I': case 'O': case 'U':
                v++;
        }
    }
    printf("Vowels = %d\n", v);
    printf("Reverse = ");
    for (i = strlen(s) - 1; i >= 0; i--)
        printf("%c", s[i]);
    printf("\n");
    return 0;
}
```

Sample run: input `Education` gives `Vowels = 5` and `Reverse = noitacudE`.

**16.** (a) Diagram:

```
            +---------------------- CPU -----------------------+
 Input ---> |  Control Unit  <--->  ALU      (registers inside) | ---> Output
 devices    +----------------------^----------------------------+      devices
                                    |
                          Primary memory (RAM, ROM, cache)
                                    |
                          Secondary storage (disk, flash, DVD)
```

- **Input unit**: accepts data and instructions and converts them into binary signals (keyboard, mouse, scanner).
- **CPU**: the control unit fetches and decodes instructions and directs all units; the ALU performs arithmetic and logic; registers hold values being processed.
- **Primary memory**: RAM holds programs and data in use, ROM holds start-up programs, cache holds frequently used data close to the CPU.
- **Secondary storage**: permanent, large storage such as hard disk and flash drive.
- **Output unit**: converts results to a human form (monitor, printer, speaker).

**Or (b)** Multimedia is the integrated use of text, graphics, audio, video and animation in a computer-based product. Components: text (words), graphics (still images), audio (sound and music), video (moving pictures) and animation (pictures in sequence giving motion). Applications: education (e-learning, virtual classes), entertainment (games, films), business (advertisements, presentations), and medicine (simulations and 3D body models).

## 16.3 Model Set 2

### 16.3.1 Question paper

**Computer Science, Grade XI, Model Set 2**  
Time: 2 hours  Full marks: 50  Pass marks: 20  
*Candidates are required to give their answers in their own words as far as practicable. The figures in the margin indicate full marks. Attempt all questions.*

**Group A: Multiple choice questions** (9 x 1 = 9)  
*Rewrite the correct option of each question in your answer sheet.*

1. Which of the following is an output device? <span class="marks">[1]</span>
   (a) scanner (b) mouse (c) speaker (d) light pen
2. The sum of $(1010)_2$ and $(0111)_2$ is <span class="marks">[1]</span>
   (a) $(10001)_2$ (b) $(10000)_2$ (c) $(1111)_2$ (d) $(10011)_2$
3. What is the output of a NAND gate when both of its inputs are 1? <span class="marks">[1]</span>
   (a) 0 (b) 1 (c) 2 (d) undefined
4. Which of the following is a Linux distribution? <span class="marks">[1]</span>
   (a) Windows 10 (b) Fedora (c) iOS (d) Android
5. What is the output of `int a = 5, b = 3; printf("%d", a > b ? a - b : b - a);`? <span class="marks">[1]</span>
   (a) 2 (b) 8 (c) -2 (d) 3
6. What is the output of `char s[] = "COMPUTER"; printf("%d", strlen(s));`? <span class="marks">[1]</span>
   (a) 7 (b) 8 (c) 9 (d) 0
7. Which tag defines the title shown on the browser tab? <span class="marks">[1]</span>
   (a) `<head>` (b) `<title>` (c) `<body>` (d) `<header>`
8. Which of the following is a graphics file format? <span class="marks">[1]</span>
   (a) MP3 (b) JPEG (c) AVI (d) TXT
9. A person who illegally breaks into computer systems is called a <span class="marks">[1]</span>
   (a) hacker (b) programmer (c) operator (d) analyst

**Group B: Short answer questions** (5 x 5 = 25)

10. (a) Write short notes on cache memory and buffer. *(2.5+2.5)* <span class="marks">[5]</span>  
    **Or** (b) Differentiate between impact and non-impact printers with examples. <span class="marks">[5]</span>
11. (a) Subtract $(101101)_2$ from $(110010)_2$ using 2's complement, using 6 bits. <span class="marks">[5]</span>  
    **Or** (b) State and verify De Morgan's theorem $(AB)' = A' + B'$ using a truth table. <span class="marks">[5]</span>
12. (a) Write a C program to read a number and check whether it is an Armstrong number (for example 153). <span class="marks">[5]</span>  
    **Or** (b) Write a C program to find the simple interest and the amount for a given principal, time and rate. <span class="marks">[5]</span>
13. (a) Differentiate between Windows and Linux. <span class="marks">[5]</span>  
    **Or** (b) What is a mobile operating system? Name any two types and explain two features of each. *(1+4)* <span class="marks">[5]</span>
14. (a) What is malware? Explain virus, worm and Trojan horse. *(1+4)* <span class="marks">[5]</span>  
    **Or** (b) Write short notes on the Electronic Transactions Act, 2063 of Nepal. <span class="marks">[5]</span>

**Group C: Long answer questions** (2 x 8 = 16)

15. (a) Write a C program to read two matrices of order 2 x 3 and display their difference. <span class="marks">[8]</span>  
    **Or** (b) Write a C program to display the pattern below using nested loops. <span class="marks">[8]</span>

```
   *
  * *
 * * *
* * * *
```

16. (a) Write HTML code to create a web page with the title "My School", a light blue background, a centred level-1 heading, a paragraph in which the school name is bold, an ordered list of three subjects and a table of three students with roll number, name and marks. <span class="marks">[8]</span>  
    **Or** (b) What is computer ethics? Explain the ICT policy of Nepal. *(3+5)* <span class="marks">[8]</span>

### 16.3.2 Solutions to Model Set 2

::: note Group A
**1.** (c) — a speaker produces sound; the others are input devices.
**2.** (a) — $10 + 7 = 17 = (10001)_2$.
**3.** (a) — NAND is the inverse of AND; AND(1, 1) = 1, so NAND = 0.
**4.** (b) — Fedora is a Linux distribution; Android is a mobile OS built on a Linux kernel but is not called a distribution.
**5.** (a) — $5 > 3$ is true, so the value is $5 - 3 = 2$.
**6.** (b) — COMPUTER has 8 letters.
**7.** (b) — the text in `<title>` is shown on the tab.
**8.** (b) — JPEG is an image format.
**9.** (a) — unauthorised intruders are hackers.
:::

**10.** (a) **Cache memory** is a small, very fast memory between the CPU and RAM that keeps copies of frequently used data and instructions, so the CPU does not wait for the slower RAM; it is made of SRAM and is costly. **Buffer** is a temporary storage area that holds data while it is moved between two devices of different speeds, for example between the CPU and a printer; it prevents the faster device from waiting and is released when the transfer ends.

**Or (b)**

| Impact printer | Non-impact printer |
|---|---|
| Strikes an ink ribbon against the paper | Prints with ink spray, toner or heat, without striking |
| Noisy | Quiet |
| Can print carbon copies | Cannot |
| Lower quality, slower | Better quality, faster |
| Dot matrix printer | Inkjet and laser printers |

**11.** (a) 6-bit numbers: $50 - 45$ in binary is $110010 - 101101$.
- 1's complement of 101101 = 010010.
- Add 1 for the 2's complement: $010010 + 1 = 010011$.
- Add to 110010: $110010 + 010011 = 1\,000101$.
- Discard the carry out of the sixth bit. The answer is $(000101)_2 = 5$, which agrees with $50 - 45 = 5$.

**Or (b)** The theorem states that the complement of a product equals the sum of the complements.

| A | B | AB | (AB)' | A' | B' | A' + B' |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 1 | 1 | 1 | 1 |
| 0 | 1 | 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 | 1 | 1 |
| 1 | 1 | 1 | 0 | 0 | 0 | 0 |

The columns $(AB)'$ and $A' + B'$ are identical, so the theorem is verified.

**12.** (a)

```
#include <stdio.h>
int main() {
    int n, orig, rem, sum = 0;
    printf("Enter a number: ");
    scanf("%d", &n);
    orig = n;
    while (n > 0) {
        rem = n % 10;
        sum = sum + rem * rem * rem;
        n = n / 10;
    }
    if (sum == orig)
        printf("%d is an Armstrong number\n", orig);
    else
        printf("%d is not an Armstrong number\n", orig);
    return 0;
}
```

Sample runs: 153 gives `153 is an Armstrong number` ($1^3 + 5^3 + 3^3 = 153$); 154 gives `154 is not an Armstrong number`. This program is for three-digit numbers.

**Or (b)**

```
#include <stdio.h>
int main() {
    float p, t, r, si;
    printf("Enter principal, time and rate: ");
    scanf("%f %f %f", &p, &t, &r);
    si = p * t * r / 100;
    printf("Simple interest = %.2f\n", si);
    printf("Amount = %.2f\n", p + si);
    return 0;
}
```

Sample run: Rs 10000 for 2 years at 8 percent gives `Simple interest = 1600.00` and `Amount = 11600.00`.

**13.** (a)

| Windows | Linux |
|---|---|
| Proprietary software of Microsoft | Open-source, free software |
| Needs a paid licence | Free to use and distribute |
| Source code is not available | Source code is available and can be modified |
| Mostly used on desktops | Used on servers, desktops, phones and embedded devices |
| Often attacked by viruses | Few attacks; strong file permissions |

**Or (b)** A mobile operating system manages the hardware, touch screen, sensors, network and apps of a smartphone or tablet.
- **Android**: developed by Google on the Linux kernel, open source, used by many manufacturers; features the Play Store and a customisable home screen.
- **iOS**: developed by Apple for its own devices only, closed source; features the App Store and tight integration with Apple hardware and services.

**14.** (a) Malware is malicious software designed to damage, disrupt or gain unauthorised access to a computer system.
- **Virus**: attaches to a host file and spreads when the file is run or shared; it can corrupt files.
- **Worm**: a stand-alone program that copies itself across networks, using bandwidth and slowing systems.
- **Trojan horse**: appears to be a useful program but contains hidden harmful code; it does not replicate itself and works by trick.

**Or (b)** The Electronic Transactions Act, 2063 is Nepal's main cyber law. It gives legal recognition to electronic records and digital signatures, provides for certifying authorities, allows government offices to work and take payments electronically, and defines offences such as pirating or altering source code, unauthorised access, damaging a computer system and publishing illegal material in electronic form. The penalty is a fine, imprisonment or both. Cases are heard by the Information Technology Tribunal, and the complaint must be filed within 35 days of learning of the offence.

**15.** (a)

```
#include <stdio.h>
int main() {
    int a[2][3], b[2][3], d[2][3], i, j;
    printf("Enter first matrix (2x3): ");
    for (i = 0; i < 2; i++)
        for (j = 0; j < 3; j++)
            scanf("%d", &a[i][j]);
    printf("Enter second matrix (2x3): ");
    for (i = 0; i < 2; i++)
        for (j = 0; j < 3; j++)
            scanf("%d", &b[i][j]);
    for (i = 0; i < 2; i++)
        for (j = 0; j < 3; j++)
            d[i][j] = a[i][j] - b[i][j];
    printf("Difference:\n");
    for (i = 0; i < 2; i++) {
        for (j = 0; j < 3; j++)
            printf("%4d", d[i][j]);
        printf("\n");
    }
    return 0;
}
```

Sample run: first matrix 9 8 7 / 6 5 4 and second 1 2 3 / 4 5 6 give 8 6 4 / 2 0 -2.

**Or (b)**

```
#include <stdio.h>
int main() {
    int i, j;
    for (i = 1; i <= 4; i++) {
        for (j = 1; j <= 4 - i; j++)
            printf(" ");
        for (j = 1; j <= i; j++)
            printf("* ");
        printf("\n");
    }
    return 0;
}
```

In row $i$ the first inner loop prints $4 - i$ spaces and the second prints $i$ stars each followed by a space, so the stars are aligned to the right.

**16.** (a)

```
<html>
<head>
  <title>My School</title>
</head>
<body bgcolor="lightblue">
  <h1 align="center">Welcome</h1>
  <p>You are reading about <b>Shree Janapriya School</b>.</p>
  <ol>
    <li>Physics</li>
    <li>Chemistry</li>
    <li>Computer Science</li>
  </ol>
  <table border="1">
    <tr>
      <th>Roll</th>
      <th>Name</th>
      <th>Marks</th>
    </tr>
    <tr>
      <td>1</td>
      <td>Sita</td>
      <td>82</td>
    </tr>
    <tr>
      <td>2</td>
      <td>Ram</td>
      <td>76</td>
    </tr>
    <tr>
      <td>3</td>
      <td>Hari</td>
      <td>69</td>
    </tr>
  </table>
</body>
</html>
```

Marks go for the structure, the title, `bgcolor` on `<body>`, the centred `<h1>`, `<b>` inside the paragraph, the `<ol>` with `<li>`, and the table with header and three data rows.

**Or (b)** Computer ethics is the set of moral principles that guide the use of computers and the internet. Its rules include not using another person's account, not copying or selling pirated software, not spreading viruses or false information, respecting the privacy of others and acknowledging sources.

The National ICT Policy, 2015 aims to make Nepal an information and knowledge-based society and economy: affordable broadband for all, ICT in every school, services of the government online (e-government), growth of the IT industry, safety of networks and data, and a smaller digital divide. The Digital Nepal Framework puts the policy into practice in sectors such as education, health, agriculture and finance.

## 16.4 Predicted questions

::: caution How this list is ranked
Tier A items are those whose **slot is certain** and whose type returns because the syllabus makes it the natural question. Tier B are certain slots where the type is likelier to be rotated. Tier C are legitimate syllabus topics less likely to appear as written questions. A rank is a reason, not a promise.
:::

### Tier A: practise first

| Rank | Question | Reason |
|---|---|---|
| 1 | A C program using a loop: factorial, sum of digits, reverse, prime, Fibonacci, table | Unit 5 states `for`, `while`, `do-while` and a program is the standard test of them; programs fill both the 5-mark and the 8-mark slot |
| 2 | A C program using a one-dimensional array: largest, sum, average, sort | The syllabus names arrays, and the "or" choice in Group C often offers an array question |
| 3 | Matrix addition or subtraction using a two-dimensional array | The syllabus says "matrix addition and subtraction" explicitly |
| 4 | Number conversion among decimal, binary, octal and hexadecimal | The first bullet of Unit 2; always calculable |
| 5 | Binary subtraction by 1's and 2's complement | Named in the syllabus; a clean five-mark working question |
| 6 | Truth table and verification of a Boolean law (De Morgan, distributive, absorption) | The syllabus asks for "verification using truth table" |
| 7 | HTML code for a page with a table, list and form | Unit 6 has 16 bullets; code questions are the natural test |
| 8 | Differentiate between compiler and interpreter; RAM and ROM; Windows and Linux | Tables of contrast are easy for the examiner to mark and fit a five-mark slot |

### Tier B: strong second line

| Rank | Question | Reason |
|---|---|---|
| 9 | Cybercrime and its types; protection from cybercrime | Unit 8 carries ten hours; long answer material |
| 10 | Virus, worm and Trojan horse; malicious software and spam | Frequently posed as a "differentiate" |
| 11 | Operating system functions; multiprogramming, multitasking, multiprocessing, distributed | Core of Unit 3; fits "define and explain" |
| 12 | Generations of computers | Unit 1; a table answer with five rows |
| 13 | Data bus, address bus, control bus | One bullet that matches a five-mark answer |
| 14 | Logic gates with truth table and symbol | A classic question and a calculable answer |
| 15 | Inline, embedded and external CSS | Last bullet of Unit 6; short and exact |
| 16 | Electronic Transactions Act and ICT policy of Nepal | Local content that needs written points |
| 17 | A C program using a string function or a switch | Named in Unit 5 bullets for strings and selection |

### Tier C: still in the syllabus

| Rank | Question | Reason |
|---|---|---|
| 18 | Types of computer by size; mobile computing | Often asked as an MCQ rather than a written question |
| 19 | OMR, OCR, BCR, MICR and other input devices | Equally likely as a "short notes" question |
| 20 | Components and applications of multimedia | Six hours; a straightforward theory answer |
| 21 | Mobile OS and open-source OS | Short; may appear as an "or" option |
| 22 | HTML5 audio, video, canvas and svg | Newer bullets; ask for a short description or code |
| 23 | Domain name, web hosting, CMS | Definition-type questions |
| 24 | Digital signature, copyright, patent and trademark | Good MCQ material as well as short notes |
| 25 | Domain-specific tools: payroll, inventory, hotel | The unit has only 5 hours; likely to be an MCQ or short note |

::: tip Using this list in the last week
- Day 1 to 2: ranks 1 to 3. Write each program out by hand, then compile it.
- Day 3: ranks 4 to 6. Redo every conversion and proof without looking.
- Day 4: rank 7, then ranks 8 and 15. Write HTML on paper, tag by tag.
- Day 5 to 6: ranks 9 to 14 and 16 to 17.
- Day 7: one full model set in 2 hours, marked against the solutions.
:::

## Chapter summary

- The paper is 9 + 25 + 16 = 50 marks in 2 hours; written answers are 41 marks, and most written questions give an "or" choice.
- Two programs are almost always asked: pick a loop program and an array program and learn them well enough to write without a book.
- Conversions and complements: division by 2 for binary, groups of 3 and 4 bits for octal and hexadecimal; invert and add 1 for 2's complement, discard the final carry.
- A truth-table proof needs all rows and a closing statement that the two columns are equal.
- HTML code is marked on structure: nesting, closed tags, attributes in quotes, shared `name` for radio buttons.
- Security answers need named examples (phishing, ransomware, virus, worm, Trojan) and Nepal's Electronic Transactions Act, 2063.
- Rankings in this chapter follow the grid and the syllabus; they are guidance for effort, not a prediction of the paper.

## Practice questions

**Group A: Multiple choice (1 mark each)**

1. Which of the following is the fastest storage in a computer? <span class="marks">[1]</span>
   (a) cache (b) RAM (c) hard disk (d) DVD
2. The 2's complement of $0011$ (4 bits) is <span class="marks">[1]</span>
   (a) 1100 (b) 1101 (c) 1011 (d) 0100
3. What is the output of `int i, s = 0; for (i = 2; i <= 6; i += 2) s += i; printf("%d", s);`? <span class="marks">[1]</span>
   (a) 12 (b) 10 (c) 8 (d) 6
4. Which HTML tag makes a hyperlink? <span class="marks">[1]</span>
   (a) `<a>` (b) `<link>` (c) `<href>` (d) `<url>`

::: note Answers to Group A
**1.** (a) — cache sits closest to the CPU.
**2.** (b) — 1's complement of 0011 is 1100; adding 1 gives 1101.
**3.** (a) — $2 + 4 + 6 = 12$.
**4.** (a) — the anchor tag.
:::

**Group B: Short answer (5 marks each)**

1. Write a C program to print the sum of the even numbers from 1 to n and count them. <span class="marks">[5]</span>
2. Explain why NAND is called a universal gate. <span class="marks">[5]</span>
3. Write any five differences between a virus and a worm. <span class="marks">[5]</span>

::: note Answers to Group B
**1.**

```
#include <stdio.h>
int main() {
    int n, i, sum = 0, count = 0;
    printf("Enter n: ");
    scanf("%d", &n);
    for (i = 1; i <= n; i++) {
        if (i % 2 == 0) {
            sum = sum + i;
            count++;
        }
    }
    printf("Sum of even numbers up to %d = %d\n", n, sum);
    printf("Count = %d\n", count);
    return 0;
}
```

For n = 9 the output is a sum of 20 and a count of 4 (2 + 4 + 6 + 8).

**2.** A gate is universal if every other gate can be made from it alone. With NAND: NOT is a NAND with both inputs joined ($A \cdot A$ complemented gives $A'$); AND is a NAND followed by a NOT; OR is a NAND of the two inverted inputs, since $(A' B')' = A + B$ by De Morgan. Because NOT, AND and OR can form any logic function, NAND alone is enough. NOR is universal in the same way.

**3.** A virus needs a host file; a worm is stand-alone. A virus spreads when a user runs or shares the infected file; a worm spreads by itself through network weaknesses. A virus mainly corrupts or deletes files; a worm mainly consumes bandwidth and memory. A virus is activated by human action; a worm needs none. Removing a virus means cleaning the host file; removing a worm means closing the hole it used and deleting the copies.
:::

**Group C: Long answer (8 marks each)**

1. Write a C program to read a 2 x 2 matrix and display the sum of its diagonal elements. <span class="marks">[8]</span>

::: note Answer to Group C
**1.** Program:

```
#include <stdio.h>
int main() {
    int a[2][2], i, j, sum = 0;
    printf("Enter 4 elements: ");
    for (i = 0; i < 2; i++)
        for (j = 0; j < 2; j++)
            scanf("%d", &a[i][j]);
    for (i = 0; i < 2; i++)
        sum = sum + a[i][i];
    printf("Sum of diagonal = %d\n", sum);
    return 0;
}
```

For the elements 1 2 3 4 the diagonal elements are `a[0][0]` and `a[1][1]`, 1 and 4, so the output is `Sum of diagonal = 5`. Marks go for declaring the array, the nested input loops, the single loop on `a[i][i]` and the output.
:::
