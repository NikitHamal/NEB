---
subject: Science and Technology
grade: 10
unit: 13
title: Information and Communication Technology
hours: 0
area: Science and Technology
---

When you speak into a phone, record a voice note, watch DishHome satellite TV or send a message over the internet, physical quantities such as sound and light are converted into electrical **signals**, encoded into binary digits (`0` and `1`), modulated onto carrier waves, transmitted across a channel, and reconstructed at the receiver. This unit covers **analog and digital signals**, **bits, nibbles and bytes**, **components of a digital communication system**, **baseband and broadband transmission**, **positive and negative impacts of digital technology**, **netizenship, digital citizenship, online reputation and digital wellbeing**, and **creating and editing audio and audio-visual materials**.

::: key What SEE asks from this unit
Expect 1-mark and 2-mark questions on **analog vs digital signals**, **bit, nibble, byte and memory units**, **ADC and DAC**, the **exact order of the 9 blocks of digital signal transmission** (`Source → Input transducer → Encoder → Modulator → Channel → Demodulator → Decoder → Output transducer → Output signal`), **carrier, modulating and modulated signals**, **baseband vs broadband transmission**, **netizen and digital citizenship**, **online reputation management vs digital wellbeing**, **audio (`.mp3`, `.wav`, `.wma`) vs video (`.mp4`, `.3gp`, `.svi`, `.avi`, `.mov`) file formats**, and 4-mark questions on **steps to cut/trim or join a video clip** (for example shortening a 5-minute or 6-minute video to 3 or 4 minutes).
:::

## 13.1 Signals, analog-to-digital conversion and memory units

### What is a signal?

::: definition Signal
A **signal** is a time-varying electric current (wave) or electromagnetic wave that carries a message, data or information from one system or network (transmitter) to another (receiver). A signal can travel over both **wired media** (copper twisted-pair, coaxial cable, optical fibre) and **wireless media** (radio waves, microwaves, infrared, satellite links), and can be either **analog** or **digital**.
:::

### Evolution of television broadcasting

Television technology illustrates why modern communication moved from analog to digital signals:

1. **Antenna-connected (terrestrial analog) TV:** Electromagnetic waves transmitted from a broadcast station travel through the air to a rooftop antenna. As the waves travel long distances through the atmosphere, they lose energy (**attenuation**) and pick up atmospheric interference. Consequently, the potential difference induced in the antenna is very weak, producing a weak modulated electric current and poor audio-visual quality (snowy picture and noise).
2. **Cable TV:** Modulated signals are sent through coaxial or fibre cables from a cable headend to homes. To watch cable TV on a computer, a **cable modem** is used.
3. **Dish TV (Direct-to-Home satellite TV):** Digital signals are broadcast from a communication satellite in space to a small parabolic dish antenna at the user's home, giving clear high-definition audio and video across mountains and valleys.
4. **Internet TV (IPTV / streaming):** Audio-visual data travel as digital packets over broadband internet connections.

### Types of signals: Analog signal and Digital signal

Signals used in communication are classified into two types:

#### 1. Analog signal

::: definition Analog signal
An **analog signal** is a continuous signal whose value (amplitude, voltage, pressure or temperature) varies smoothly and continuously with time over an infinite number of possible values within a range.
:::

- **Waveform:** Represented by a smooth, continuous **sine wave**.
- **Examples:** Human voice/sound waves in air, the electrical output of a microphone, mercury thermometer readings, vehicle pointer speedometer, old landline telephone signals, and medium-wave (AM/FM) radio waves.
- **Limitation:** Because any small fluctuation in voltage changes the signal, analog signals are **easily distorted by external noise and interference**, and their quality degrades over long distances.

#### 2. Digital signal

::: definition Digital signal
A **digital signal** is a discrete (non-continuous) signal that represents information as a sequence of separate, fixed levels — in binary electronics, only two states: **LOW (`0`)** and **HIGH (`1`)**.
:::

- **Waveform:** Represented by a **square wave (rectangular pulses)** switching sharply between two voltage levels.
- **Switch ON/OFF circuit activity:** Connect a $5\ \text{V}$ source, a switch and a bulb in a circuit and record the voltage across the bulb over time:
  - When the **switch is ON (closed)**, the potential difference across the bulb is $5\ \text{V}$, representing a **HIGH signal (`1`)**.
  - When the **switch is OFF (open)**, the potential difference is $0\ \text{V}$, representing a **LOW signal (`0`)**.
- In computers and smartphones, millions of microscopic **transistors** act as ultra-fast electronic switches turning ON (`1`) and OFF (`0`) billions of times per second.

```figure caption="Comparison of (a) a continuous analog signal (sine wave) and (b) a discrete digital signal (square-wave pulses). In (b), points A and B are HIGH (5 V, switch ON, binary 1), while point C is LOW (0 V, switch OFF, binary 0)."
import numpy as np, matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.2, 2.35))
t = np.linspace(0, 4*np.pi, 400)
ax1.plot(t, 5*np.sin(t), color=ACCENT, lw=1.8)
ax1.axhline(0, color=MUTED, lw=0.8)
ax1.set_title("(a) Analog signal (continuous)", fontsize=8.5, color=INK, fontweight="bold")
ax1.set_xlabel("Time (t)", fontsize=8, color=INK); ax1.set_ylabel("Voltage (V)", fontsize=8, color=INK)
ax1.set_ylim(-6.2, 6.2); ax1.set_xticks([]); ax1.spines[['top','right']].set_visible(False)
ax1.text(1.6, 5.3, "Continuous wave", fontsize=7.5, color=ACCENT)

bits = [1, 0, 1, 1, 0, 1, 0]
tx = np.arange(0, len(bits)+1)
ty = bits + [bits[-1]]
ax2.step(tx, [b*5 for b in ty], where='post', color=SERIES[1], lw=1.9)
ax2.set_title("(b) Digital signal (discrete 0 and 1)", fontsize=8.5, color=INK, fontweight="bold")
ax2.set_xlabel("Time (t)", fontsize=8, color=INK); ax2.set_ylabel("Voltage (V)", fontsize=8, color=INK)
ax2.set_ylim(-1.2, 6.6); ax2.set_yticks([0, 5]); ax2.set_yticklabels(["0 V (0)", "5 V (1)"], fontsize=7.5)
ax2.set_xticks([])
ax2.spines[['top','right']].set_visible(False)
for i, b in enumerate(bits):
    ax2.text(i+0.5, 5.45 if b else 0.45, str(b), ha='center', fontsize=8, fontweight='bold', color=INK)
ax2.plot([0.5, 2.5, 4.5], [5, 5, 0], 'o', color=INK, ms=4)
ax2.annotate("A (ON)", xy=(0.5, 5), xytext=(0.15, 6.0), fontsize=7.2, color=INK)
ax2.annotate("B (ON)", xy=(2.5, 5), xytext=(2.15, 6.0), fontsize=7.2, color=INK)
ax2.annotate("C (OFF)", xy=(4.5, 0), xytext=(4.05, -1.05), fontsize=7.2, color=INK)
fig.tight_layout()
```

### Difference between Analog Signal and Digital Signal

| Basis | Analog Signal | Digital Signal |
|---|---|---|
| **Representation** | Represents information using continuous waveforms whose amplitude varies smoothly over time | Represents information using discrete values, typically in the form of binary code (`0`s and `1`s) |
| **Waveform & voltage example** | Represented by a continuous **sine wave** (for example, an alternating voltage signal varying continuously from $-12\ \text{V}$ to $+12\ \text{V}$ or $-5\ \text{V}$ to $+5\ \text{V}$) | Represented by a **square wave** (for example, a discrete voltage signal switching between two fixed levels such as $0\ \text{V}$ and $+5\ \text{V}$) |
| **Change with time** | Changes continuously with time across an infinite number of values within a range | Changes between two fixed discrete values (`0` = LOW/OFF and `1` = HIGH/ON) with time |
| **Effect of noise** | Easily disturbed by noise and interference, making the received information less accurate and less clear | Not easily disturbed by noise, keeping the transmitted information more accurate and clear |
| **Long-distance transmission** | Degrades over long distances (attenuation and noise accumulation), limiting its effective transmission range | Can be transmitted over long distances without significant degradation (easily regenerated, making it ideal for long-distance communication) |
| **Storage space** | Requires more storage space since it involves continuous variations of amplitude | Requires less storage space because it can be easily represented and compressed using binary code (`0` and `1`) |
| **Conversion device** | **ADC (Analog-to-Digital Converter)** converts an analog signal into a digital signal (e.g., a **temperature sensor** or microphone feeding a computer) | **DAC (Digital-to-Analog Converter)** converts a digital signal into an analog signal (e.g., **playing music on a computer** or phone through a loudspeaker) |
| **Examples** | Human speech in air, thermocouple/temperature sensor output, mercury thermometer, old landline telephone, AM/FM radio waves | Signals inside a computer, smartphone, smartwatch, optical fibre data, CD/DVD, USB cable |

### Analog-to-Digital Conversion (ADC) and Digital-to-Analog Conversion (DAC)

Because physical quantities in nature (voice, temperature, pressure, light intensity) are **analog** while computers and digital networks store and process **digital (`0` and `1`)** data, two converters bridge the two worlds:

- **ADC (Analog-to-Digital Converter):** An electronic circuit that samples a continuous analog signal and converts it into discrete binary digital code (`0`s and `1`s). *Examples:* A digital **temperature sensor** or digital thermometer converting continuous thermal voltage into a binary reading; a smartphone microphone converting analog sound waves into digital audio data.
- **DAC (Digital-to-Analog Converter):** An electronic circuit that converts binary digital data (`0`s and `1`s) back into a continuous analog electrical signal. *Examples:* **Playing music on a computer** or smartphone, where stored `.mp3`/`.wav` binary data are converted into analog audio currents to drive headphones or a loudspeaker.

### Binary combinations and Computer Memory Units

Digital devices use the **binary number system** (base 2), which has only two digits: `0` and `1`. With $n$ binary digits (bits), the number of possible combinations of `0` and `1` is $2^n$:

- **1 bit ($n = 1$):** $2^1 = 2$ combinations (`0`, `1`)
- **2 bits ($n = 2$):** $2^2 = 4$ combinations (`00`, `01`, `10`, `11`)
- **3 bits ($n = 3$):** $2^3 = 8$ combinations (`000`, `001`, `010`, `011`, `100`, `101`, `110`, `111`)
- **4 bits ($n = 4$):** $2^4 = 16$ combinations (called **1 nibble**)
- **8 bits ($n = 8$):** $2^8 = 256$ combinations (called **1 byte**, which represents one character such as `'A'` or `'7'`)

::: definition Bit, Nibble and Byte
- **Bit (Binary Digit):** The smallest unit of data in a computer memory, having a single binary value of either `0` or `1` (represented by lowercase `b`).
- **Nibble:** A group of **4 bits** (for example `1011` or `0000`). Two nibbles make one byte.
- **Byte:** A group of **8 bits** (for example `00000000` or `11010011`) treated as a single unit of data to store one character (represented by uppercase `B`).
:::

| Memory Unit | Relation | Equivalent in Bytes / Bits |
|---|---|---|
| **1 Bit (b)** | `0` or `1` | Smallest unit of computer memory |
| **1 Nibble** | $4\ \text{bits}$ | $\frac{1}{2}\ \text{Byte}$ |
| **1 Byte (B)** | $8\ \text{bits} = 2\ \text{nibbles}$ | $1\ \text{character}$ (e.g. `00000000`) |
| **1 Kilobyte (KB)** | $1024\ \text{Bytes}$ | $2^{10}\ \text{B} = 8192\ \text{bits}$ |
| **1 Megabyte (MB)** | $1024\ \text{Kilobytes (KB)}$ | $1024 \times 1024\ \text{B}$ |
| **1 Gigabyte (GB)** | $1024\ \text{Megabytes (MB)}$ | $1024^3\ \text{B}$ |
| **1 Terabyte (TB)** | $1024\ \text{Gigabytes (GB)}$ | $1024^4\ \text{B}$ |

::: example Binary combinations and switch states
**Problem.** (a) How many distinct binary combinations can be formed using $3$ bits and $4$ bits? (b) In a $5\ \text{V}$ digital circuit, what binary digits correspond to $0\ \text{V}$ (switch OFF) and $5\ \text{V}$ (switch ON)?

**Solution.** (a) With $n$ bits, the number of combinations is $2^n$. For $n = 3$, $2^3 = 8$ combinations (`000` to `111`). For $n = 4$ (one nibble), $2^4 = 16$ combinations.

(b) $0\ \text{V}$ (switch OFF) represents the LOW digital state **`0`**, and $5\ \text{V}$ (switch ON) represents the HIGH digital state **`1`**.
:::

::: example Memory unit conversion (SEE pattern)
**Problem.** (a) How many nibbles and bits are there in $4\ \text{Bytes}$? (b) A pen drive of $2\ \text{GB}$ stores audio recordings each of size $4\ \text{MB}$. How many recordings can it hold?

**Solution.** (a) Since $1\ \text{Byte} = 2\ \text{nibbles} = 8\ \text{bits}$:
$$\text{Nibbles} = 4 \times 2 = 8, \quad \text{Bits} = 4 \times 8 = 32$$
(b) Convert $2\ \text{GB}$ into $\text{MB}$: $2\ \text{GB} = 2 \times 1024\ \text{MB} = 2048\ \text{MB}$.
$$\text{Number of audio files} = \frac{2048\ \text{MB}}{4\ \text{MB}} = 512\ \text{recordings}$$
:::

## 13.2 Signal transmission and digital communication system

### Signal transmission: Analog vs Digital transmission

**Signal transmission** is the process of sending a signal from a transmitter to a receiver through a communication medium (channel) such as a copper wire, optical fibre or free space.

| Basis | Analog Signal Transmission | Digital Signal Transmission |
|---|---|---|
| **Form of signal** | Transmitted as a continuous wave | Transmitted as discrete binary pulses (`0` and `1`) |
| **Effect of distance** | Signal weakens and noise accumulates; amplifiers amplify both noise and signal | Repeaters regenerate clean `0` and `1` pulses, so quality stays constant over long distances |
| **Error detection** | Difficult to detect and correct errors | Error-detection and error-correction codes remove transmission errors |
| **Security** | Less secure; hard to encrypt | Highly secure; data can be encrypted and compressed easily |
| **Multiplexing** | Uses Frequency Division Multiplexing (FDM); lower capacity | Uses Time Division Multiplexing (TDM); carries voice, video and data together |
| **Examples** | Traditional AM/FM radio, old landline telephone | Optical-fibre internet, 4G/5G mobile calls, digital satellite TV |

### Components of a Digital Communication System

A digital communication system transmits an analog physical message (such as a speaker's voice) to a distant listener through **nine sequential stages**:

> **Source → Input Transducer → Encoder → Modulator → Channel → Demodulator → Decoder → Output Transducer → Output Signal**

```figure caption="Block diagram of a digital communication system. The transmitter side converts the physical source signal into a modulated wave for the channel; the receiver side demodulates, decodes and converts it back into the original physical output signal."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 2.7))
ax.set_xlim(0, 13); ax.set_ylim(0, 6.2); ax.axis("off")
def blk(x, y, w, h, title, sub, fc):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.18", fc=fc, ec=INK, lw=1.1))
    ax.text(x+w/2, y+h*0.64, title, ha="center", va="center", fontsize=7.3, fontweight="bold", color=INK)
    ax.text(x+w/2, y+h*0.26, sub, ha="center", va="center", fontsize=6.4, color=MUTED)
def arr(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
blk(0.1, 4.1, 2.2, 1.5, "1. Source", "Sound / voice", "#FFF1C9")
blk(2.7, 4.1, 2.5, 1.5, "2. Input Transducer", "Mic (sound → elec.)", "#E5ECF6")
blk(5.6, 4.1, 2.2, 1.5, "3. Encoder", "ADC + compress", "#E5ECF6")
blk(8.2, 4.1, 2.2, 1.5, "4. Modulator", "Carrier wave", "#E5ECF6")
blk(10.8, 2.3, 2.0, 1.5, "5. Channel", "Fibre / air / wire", "#D7EBDD")
blk(8.2, 0.5, 2.2, 1.5, "6. Demodulator", "Separates signal", "#F9D5D0")
blk(5.6, 0.5, 2.2, 1.5, "7. Decoder", "DAC + error fix", "#F9D5D0")
blk(2.7, 0.5, 2.5, 1.5, "8. Output Transducer", "Speaker (elec. → sound)", "#F9D5D0")
blk(0.1, 0.5, 2.2, 1.5, "9. Output Signal", "Heard sound", "#FFF1C9")
arr(2.3, 4.85, 2.7, 4.85); arr(5.2, 4.85, 5.6, 4.85); arr(7.8, 4.85, 8.2, 4.85)
arr(10.4, 4.85, 11.8, 3.8); arr(11.8, 2.3, 10.4, 1.25)
arr(8.2, 1.25, 7.8, 1.25); arr(5.6, 1.25, 5.2, 1.25); arr(2.7, 1.25, 2.3, 1.25)
fig.tight_layout()
```

1. **Source:** The origin of the message to be sent, usually an analog physical quantity such as human voice, music or an image.
2. **Input Transducer:** Converts the physical signal from the source into an analog electrical signal. *Example:* A **microphone** converts sound waves into electrical current; a camera sensor converts light into electrical signals.
3. **Encoder:** Converts the analog electrical signal into a digital binary sequence (`0`s and `1`s using an ADC) and compresses the data into the minimum number of bits for efficient bandwidth use.
4. **Modulator:** Superimposes (modulates) the digital data (the **modulating signal**) onto a high-frequency **carrier wave** to produce a **modulated signal** capable of travelling long distances through the transmission medium.
5. **Channel (Transmission Medium):** The physical path through which the signal travels from the transmitter to the receiver (such as twisted-pair wire, coaxial cable, optical fibre or radio/satellite waves in free space).
6. **Demodulator:** The first stage at the receiver; it separates the information-bearing digital signal from the high-frequency carrier wave.
7. **Decoder:** Re-digitizes and decodes the demodulated signal, checks and corrects transmission errors, and converts the digital code back into an analog electrical signal (using a DAC).
8. **Output Transducer:** Converts the decoded electrical signal back into its original physical form. *Example:* A **loudspeaker** converts electrical current into sound waves; a display screen converts it into light.
9. **Output Signal:** The final physical message (sound, picture or text) received by the user.

```figure caption="Modulation in signal transmission. (a) Low-frequency modulating signal (information), (b) high-frequency carrier signal, and (c) the resulting modulated signal sent into the channel."
import numpy as np, matplotlib.pyplot as plt
fig, axs = plt.subplots(3, 1, figsize=(4.8, 2.85), sharex=True)
t = np.linspace(0, 4*np.pi, 600)
m = 0.45*np.sin(t)
c = np.sin(12*t)
mod = (1 + m)*c
titles = ["(a) Modulating signal (low-frequency message / data)",
          "(b) Carrier signal (high-frequency wave)",
          "(c) Modulated signal (carrier + modulating signal)"]
cols = [ACCENT, MUTED, SERIES[1]]
for ax, y, ti, col in zip(axs, [m, c, mod], titles, cols):
    ax.plot(t, y, color=col, lw=1.35)
    ax.set_title(ti, fontsize=7.8, color=INK, loc="left", pad=2)
    ax.set_yticks([]); ax.set_xticks([])
    ax.spines[['top','right','bottom']].set_visible(False)
fig.tight_layout()
```

### Baseband Transmission and Broadband Transmission

Signals are sent through communication channels in two ways:

- **Baseband transmission:** Digital signals (`0` and `1` voltage pulses) are sent directly through a cable **without converting them into analog signals** (no modulation). A single signal uses the **entire bandwidth** of the medium at a time, and communication is bidirectional on the same channel over **short distances** (for example connecting computers in a school **Ethernet LAN** or via a USB cable).
- **Broadband transmission:** Digital signals are first **modulated into analog waves** (optical or electromagnetic waves of different frequencies) using **Frequency Division Multiplexing (FDM)**. The bandwidth of the medium is divided into **multiple independent channels** so many signals (internet data, voice, multiple TV channels) travel **simultaneously** over **long distances**. High-speed fibre/cable internet and cable television are broadband transmissions.

| Basis | Baseband Transmission | Broadband Transmission |
|---|---|---|
| **Signal form** | Transmits digital signals (`0` and `1` pulses) directly without modulation | Converts digital signals into modulated analog waves |
| **Bandwidth use** | A single signal occupies the entire bandwidth of the channel | Bandwidth is divided into multiple frequency channels (FDM) |
| **Simultaneous signals** | Only one signal is transmitted at a time | Multiple signals are transmitted simultaneously |
| **Direction** | Bidirectional on a single cable (sending and receiving share the wire) | Unidirectional per channel (uses two channels or two frequencies) |
| **Distance** | Suitable for short distances | Suitable for long-distance high-speed transmission |
| **Examples** | Ethernet LAN cable between computers | High-speed broadband internet, cable TV, optical-fibre trunk lines |

### Advantages of Digital Transmission

1. **High noise immunity:** Small electrical disturbances in the channel cannot easily flip a `0` into a `1`, so there is minimal distortion.
2. **Clean regeneration over long distances:** Repeaters reconstruct crisp `0` and `1` pulses without amplifying channel noise.
3. **Error detection and correction:** Extra check bits allow the decoder to find and fix bit errors automatically.
4. **High security:** Digital data can be **encrypted** and **compressed** before transmission.
5. **Efficient multiplexing:** Voice, video and text data from many users can share a single channel using Time Division Multiplexing (TDM).
6. **Reliable, low-cost hardware:** Digital integrated circuits (ICs) are smaller, cheaper, more reliable and easier to design than analog circuits, with less cross-talk.

## 13.3 Impact of digital technology in daily life

### Influence of digital technology on ICT

1. **Digital telecommunication:** Enables crystal-clear voice calls, 4G/5G mobile data, VoIP internet calls and thousands of simultaneous telephone conversations over a single optical fibre.
2. **Digital media:** Electronic devices and platforms (smartphones, computers, news portals, podcasts, social media) allow instant creation, storage and worldwide sharing of news, audio and video.
3. **Digital television (DTV):** Provides high-definition (HD/4K) pictures and clear sound through four delivery modes: **Terrestrial DTV** (local transmitter), **Cable DTV** (via cable headend), **Satellite DTV** (Dish TV via satellite dish), and **Mobile/Portable DMB** (Digital Multimedia Broadcasting to handheld devices and car systems).

### Digital technologies used in daily life and their impacts

Common digital devices in everyday Nepali life include the **digital and infrared thermometer**, **smartwatch**, **digital wallet (eSewa, Khalti, Fonepay QR)**, **online digital library**, **online newspapers (`gorkhapatraonline.com`)**, **digital camera**, **calculator** and **digital vehicle speedometer**.

| Positive Effects of Digital Technology | Negative Effects of Digital Technology |
|---|---|
| **1. Digital library:** Free access to digital books, reference materials and journals anytime, encouraging reading habits | **1. Social behaviour changes:** Excessive screen time leads to irritability, social isolation and weaker family interaction |
| **2. Online newspapers:** Instant access to national and global news on smartphones without waiting for print delivery | **2. Cybercrime:** Hacking, online fraud, phishing, identity theft and character assassination harm individuals and families |
| **3. Digital payment:** Cashless shopping, utility bill payment, tax payment and ticket booking via QR codes and mobile banking | **3. Lack of physical exercise:** Children spending hours on screens suffer from obesity, physical weakness and poor posture |
| **4. Online business:** Local producers and shops can promote and sell goods nationwide over the internet | **4. Harmful digital games:** Violent online games cause addiction, mental stress, sleep loss and aggressive behaviour |
| **5. Social networks:** Connects distant family members (such as relatives working abroad) and provides a platform for public expression | **5. Spread of misinformation:** Fake news, rumours and deepfakes spread rapidly on social media |
| **6. Entertainment and learning:** Educational videos, animations, music and interactive simulations make learning engaging | **6. Reduced physical consumption:** Decline of traditional print bookstores, postal services and physical retail businesses |

## 13.4 Digital citizenship, online reputation and digital wellbeing

### Netizen, Netizenship and Digital Citizenship

Digital communication has connected people across every continent into a single **global village**.

::: definition Netizen and Digital Citizenship
- **Netizen (Citizen of the Net):** A person who actively uses the internet and participates in online communities.
- **Digital citizenship (Netizenship):** The citizenship of a netizen in the virtual world of the internet — that is, the **responsible, ethical, safe and respectful use** of digital technology and online platforms.
:::

### Characteristics of a Good Netizen (Internet Etiquette / Netiquette)

1. **Polite and civilised communication:** Uses respectful, courteous language in emails, comments and online discussions.
2. **Respect for others and privacy:** Treats every online user with dignity, even when disagreeing, and never shares another person's private photos, messages or personal data without consent.
3. **Awareness of digital permanence:** Understands that anything posted online creates a permanent **digital footprint** that can be seen for years.
4. **Respect for intellectual property:** Never copies another person's articles, photos, music or videos without permission, and **cites the original source** whenever reference material is used.
5. **Verification before sharing:** Checks facts before forwarding news or posts so rumours and misinformation do not spread.

### Online Reputation and Digital Reputation Management

::: definition Online Reputation and Digital Reputation Management
- **Online reputation (Digital reputation):** The public perception or image of an individual or an institution formed from their online profile, posts, comments, shares and digital footprint.
- **Digital reputation management:** The continuous process of building, monitoring and protecting a positive, credible and trustworthy image of a person or organisation on the internet.
:::

- **Personal online reputation:** Built by using one's real name and authentic photo, keeping a consistent username across professional/social networks, posting knowledgeable and constructive content (for example sharing scientific discoveries or educational articles), and protecting accounts with strong privacy settings and passwords so impostors cannot post harmful material.
- **Institutional online reputation:** Websites and verified social-media pages of schools, hospitals, banks and government offices represent them officially. Their credibility is maintained by publishing accurate notices, maintaining presence on major platforms, and **responding promptly and politely to public queries, comments and complaints**.

### Digital Wellbeing (Digital Wellness / डिजिटल आरोग्यता)

Spending hours online without physical balance causes **physical problems** (eye strain, blurred vision, insomnia, headache, back/neck pain, obesity) and **mental/social problems** (anxiety, depression, irritability, low self-esteem, dishonesty, loneliness, social isolation and internet addiction).

::: definition Digital Wellbeing
**Digital wellbeing** (digital wellness) is the state of being physically, mentally, socially and emotionally healthy by maintaining a **healthy balance between online (screen) time and offline (real-world) activities**.
:::

#### Precautions and habits for Digital Wellbeing

1. **Separate and limit screen time:** Fix daily time limits for smartphones, games and social media, and take regular breaks (such as the 20-20-20 eye rule) and offline time with family and outdoor sports.
2. **Turn off unnecessary notifications:** Silence non-essential social-media notifications during study hours, work and before sleep.
3. **No screens before bedtime:** Stop using phones at least 30–60 minutes before sleeping to prevent insomnia.
4. **Use Digital Wellbeing applications:** Install screen-time monitoring tools such as **Digital Wellbeing**, **ActionDash**, **Digital Detox** or **Microsoft Launcher** to track and reduce excessive phone use.

### Difference between Digital Wellbeing, Digital Citizenship and Digital Reputation

| Basis | Digital Wellbeing | Digital Citizenship | Digital Reputation |
|---|---|---|---|
| **Meaning** | Maintaining physical, mental and social health by balancing online and offline life | Responsible, ethical and safe conduct as an active member of the online community | The public image or perception of a person or institution based on online activity |
| **Focus** | Internal — personal health, sleep, posture and screen-time balance | Behavioural — obeying cyber rules, netiquette, copyright and mutual respect | External — how others judge your credibility, expertise and trustworthiness online |
| **Key practice** | Setting screen-time limits, turning off notifications, taking digital detox breaks | Using polite language, citing sources, not spreading fake news or cyberbullying | Posting accurate, constructive content and resolving public feedback on time |

## 13.5 Creating and editing audio and audio-visual materials

### Audio recording, file formats and audio editing

- **Audio recording:** Sound is recorded using the **microphone** of a smartphone or computer, which acts as an input transducer converting sound waves into electrical signals that are encoded and saved as digital audio files.
- **Common audio file formats (extensions):** **`.MP3`** (MPEG-1 Audio Layer 3), **`.WAV`** (Waveform Audio), **`.WMA`** (Windows Media Audio), and **`.AAC`**.
- **Audio editing software:** Unwanted noise or pauses can be trimmed and clips can be mixed using free or commercial software such as **Audacity** (`audacityteam.org`), **MP3 Cutter**, **GarageBand** or **Adobe Audition**.

### Video (audio-visual) recording, file formats and video editing

- **Audio-visual recording:** Captures both sound and moving pictures simultaneously using a **smartphone camera, digital camera or webcam** with a microphone.
- **Common video file formats (extensions):** **`.MP4`**, **`.3GP`**, **`.AVI`**, **`.SVI`**, and **`.MOV`**.
- **Video editing:** Removing unwanted parts of a recorded video (**video cutting / trimming**) or combining two or more short clips into a single continuous video (**video joining / merging**).
- **Video editing software:** **Windows Video Editor** (built into Windows), **CapCut**, **InShot**, **Wondershare Filmora**, **Adobe Premiere Pro**, or the built-in **Gallery Edit** tool on a smartphone.

```figure caption="Workflow for (a) cutting/trimming a 5-minute video down to 3 minutes using start/end drag bars and (b) joining multiple clips into one exported MP4 video in a video editor."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
fig, ax = plt.subplots(figsize=(5.1, 2.35))
ax.set_xlim(0, 12); ax.set_ylim(0, 5.2); ax.axis("off")
ax.text(0.2, 4.7, "(a) Video Cutting / Trimming (5 min clip → 3 min clip)", fontsize=8.2, fontweight="bold", color=INK)
ax.add_patch(Rectangle((0.3, 3.2), 11.2, 1.0, fc="#eef2f8", ec=MUTED, lw=1.0))
ax.add_patch(Rectangle((2.2, 3.2), 6.8, 1.0, fc="#dbe4ff", ec=ACCENT, lw=1.6))
ax.plot([2.2, 2.2], [3.0, 4.4], color=ACCENT, lw=3); ax.plot([9.0, 9.0], [3.0, 4.4], color=ACCENT, lw=3)
ax.text(1.2, 3.7, "Cut out", ha="center", va="center", fontsize=7.2, color=MUTED)
ax.text(5.6, 3.7, "Selected 3 min segment kept (Start bar → End bar)", ha="center", va="center", fontsize=7.5, fontweight="bold", color=INK)
ax.text(10.2, 3.7, "Cut out", ha="center", va="center", fontsize=7.2, color=MUTED)

ax.text(0.2, 2.1, "(b) Video Joining (Combining clips into one final video)", fontsize=8.2, fontweight="bold", color=INK)
for x, lbl, fc in [(0.3, "Clip 1\n(Intro)", "#FFF1C9"), (3.1, "Clip 2\n(Experiment)", "#D7EBDD"), (5.9, "Clip 3\n(Summary)", "#E5ECF6")]:
    ax.add_patch(FancyBboxPatch((x, 0.4), 2.3, 1.2, boxstyle="round,pad=0.04,rounding_size=0.15", fc=fc, ec=INK, lw=1.1))
    ax.text(x+1.15, 1.0, lbl, ha="center", va="center", fontsize=7.4, color=INK)
ax.annotate("", xy=(9.2, 1.0), xytext=(8.4, 1.0), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4))
ax.add_patch(FancyBboxPatch((9.3, 0.4), 2.3, 1.2, boxstyle="round,pad=0.04,rounding_size=0.15", fc="#F9D5D0", ec=INK, lw=1.2))
ax.text(10.45, 1.0, "Finish Video\n& Export (.MP4)", ha="center", va="center", fontsize=7.4, fontweight="bold", color=INK)
fig.tight_layout()
```

#### (a) Steps for Video Cutting / Trimming (e.g. shortening a 5-minute or 6-minute video to 3 or 4 minutes)

1. **Open Video Editor and create a project:** Launch **Video Editor** on the computer, click **New video project**, enter a project name (for example *Class 10 Science ICT*), and click **OK**.
2. **Import and place on the storyboard:** Select the recorded video from the computer memory, add it to the **Project library**, and drag it down into the **Storyboard / Editing panel**.
3. **Open the Trim tool:** Select the video clip on the storyboard and click **Trim**.
4. **Set Start and End points:** Play the video to identify the unwanted sections, then drag the **two blue trim bars (start-time bar and end-time bar)** so that only the required duration (for example 3 minutes or 4 minutes) remains between them, and click **Done**.
5. **Export and save:** Click **Finish video** at the top right, choose the video quality, click **Export**, and save the shortened `.MP4` file in the desired folder.

#### (b) Steps for Video Joining (Combining multiple clips into one video)

1. Place all the video clips to be joined inside a folder on the computer.
2. Open **Video Editor**, start a **New video project**, and import the required clips into the **Project library**.
3. Select the clips and drag them in the desired sequence onto the **Storyboard / Editing panel**.
4. Tick/select all the clips on the storyboard and click **Finish video**.
5. Click **Export** and choose a location to save the combined single `.MP4` video file.

::: example Planning a 5-minute Science video and shortening it to 3 minutes
**Problem.** Prepare a plan to create a 5-minute audio-visual material on any topic of Class 10 Science, and write the steps to shorten that video to 3 minutes.

**Solution.**
- **Part 1 — Plan to create a 5-minute video (Topic: Information and Communication Technology):**
  1. *Scripting and storyboarding:* Divide the 5 minutes into clear segments: Minute 0–1 (Introduction to signals: analog vs digital with wave diagrams); Minute 1–2 (Block diagram of digital signal transmission); Minute 2–3 (Positive and negative impacts of digital technology); Minute 3–4 (Netizenship and Digital Wellbeing); Minute 4–5 (Summary and Online Reputation tips).
  2. *Recording:* Use a smartphone camera and microphone in a quiet room to record short video clips and voice-overs for each segment, and prepare clear diagrams.
  3. *Joining and exporting:* Open Video Editor → click **New video project** → import all recorded clips into the **Project library** → drag them in order onto the **Storyboard** → click **Finish video** → **Export** as a 5-minute `.MP4` file.
- **Part 2 — Steps to shorten the 5-minute video to 3 minutes (Video Trimming):**
  1. Open the 5-minute video project in **Video Editor** and place the video on the **Storyboard**.
  2. Click the **Trim** button to open the trimming window.
  3. Play the clip to spot pauses, repetitions or less essential examples totaling 2 minutes, and move the **start and end blue drag bars** to keep only the core 3-minute content; click **Done**.
  4. Click **Finish video** → **Export** and save the new 3-minute video file.
:::

## Chapter summary

- A **signal** is a time-varying physical quantity that carries information. **Analog signals** are continuous sine waves; **digital signals** are discrete binary pulses (`0` = LOW / switch OFF, `1` = HIGH / switch ON).
- An **ADC** converts analog signals into digital binary code; a **DAC** converts digital binary data back into analog signals for human perception.
- **Computer memory units:** $1\ \text{bit} = 0\text{ or }1$ (smallest unit); $1\ \text{nibble} = 4\ \text{bits}$; $1\ \text{Byte (B)} = 8\ \text{bits} = 2\ \text{nibbles}$ (e.g. `00000000`); $1\ \text{KB} = 1024\ \text{B}$; $1\ \text{MB} = 1024\ \text{KB}$; $1\ \text{GB} = 1024\ \text{MB}$; $1\ \text{TB} = 1024\ \text{GB}$. With $n$ bits, $2^n$ binary combinations are possible.
- **Stages of digital signal transmission (in order):** Source → Input Transducer → Encoder → Modulator → Channel → Demodulator → Decoder → Output Transducer → Output Signal.
- **Baseband transmission** sends digital signals directly without modulation over a single short-distance channel (Ethernet LAN). **Broadband transmission** modulates signals onto multiple carrier frequencies (FDM) to send many signals simultaneously over long distances (cable TV, high-speed internet).
- **Netizen** = an active user ("citizen") of the internet. **Digital citizenship** = responsible, ethical and safe participation online. **Online reputation management** builds and protects a person's or organisation's public image online.
- **Digital wellbeing** is maintaining physical, mental, social and emotional health by balancing online screen time with offline life.
- **Audio formats:** `.mp3`, `.wav`, `.wma`, `.aac` (edited in Audacity). **Video formats:** `.mp4`, `.3gp`, `.avi`, `.svi`, `.mov` (trimmed and joined in Windows Video Editor, Filmora or Premiere Pro).

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which of the following represents an analog signal? <span class="marks">[1]</span>
   (a) infrared thermometer (b) computer (c) smartwatch (d) medium-wave radio
2. Which binary sequence represents 1 byte of computer memory? <span class="marks">[1]</span>
   (a) 0000 (b) 00000000 (c) 100000 (d) 000001
3. Which is the correct relationship between a nibble and a byte? <span class="marks">[1]</span>
   (a) 1 nibble = 4 bytes (b) 2 nibbles = 1 byte (c) 4 nibbles = 1 byte (d) 8 nibbles = 1 byte
4. Which of the following shows the stages of digital signal transmission in the correct order? <span class="marks">[1]</span>
   (a) Source, input transducer, decoder, modulator, channel, demodulator, encoder, output transducer
   (b) Source, input transducer, encoder, modulator, channel, demodulator, decoder, output transducer
   (c) Source, input transducer, encoder, demodulator, channel, modulator, decoder, output transducer
   (d) Source, encoder, input transducer, modulator, channel, decoder, demodulator, output transducer
5. Which of the following is an audio file format? <span class="marks">[1]</span>
   (a) .SVI (b) .MP4 (c) .MP3 (d) .3GP
6. What are people who actively use the internet called? <span class="marks">[1]</span>
   (a) citizens (b) online managers (c) audio-video editors (d) netizens
7. What does the habit of regularly posting accurate information about new scientific discoveries on social media indicate? <span class="marks">[1]</span>
   (a) unsystematic use of social media (b) digital wellbeing skill (c) digital detox (d) digital reputation management

::: note Answers to Group A
**1.** (d) — a medium-wave radio uses continuous analog electromagnetic waves; the others are digital devices.
**2.** (b) — 1 byte equals 8 bits, and `00000000` has 8 bits (`0000` is 4 bits = 1 nibble).
**3.** (b) — 1 nibble = 4 bits and 1 byte = 8 bits, so 2 nibbles = 1 byte.
**4.** (b) — Source → Input transducer → Encoder → Modulator → Channel → Demodulator → Decoder → Output transducer.
**5.** (c) — `.MP3` (along with `.WAV` and `.WMA`) is an audio format; `.SVI`, `.MP4` and `.3GP` are video formats.
**6.** (d) — active users of the internet are called netizens (citizens of the net).
**7.** (d) — posting constructive, knowledgeable content builds a credible public image online, which is digital reputation management.
:::

**Group B — Short answer (2 marks each)**

1. Define a bit, a nibble and a byte. What is the purpose of a DAC in a computer system? <span class="marks">[2]</span>
2. Differentiate between an analog signal and a digital signal in any two points. <span class="marks">[2]</span>
3. Differentiate between baseband transmission and broadband transmission in two points. <span class="marks">[2]</span>
4. Define digital citizenship. Write any two characteristics of a good netizen. <span class="marks">[2]</span>
5. What is digital wellbeing? Mention any two precautions to maintain digital wellbeing. <span class="marks">[2]</span>
6. Differentiate between digital wellbeing and digital reputation in two points. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** A **bit** (`0` or `1`) is the smallest unit of computer memory; a **nibble** is a group of 4 bits; a **byte** is a group of 8 bits. A **DAC (Digital-to-Analog Converter)** converts digital binary data (`0`s and `1`s) into continuous analog signals so humans can hear or view the output.
**2.** (i) An **analog signal** is continuous and varies smoothly over time (sine wave), whereas a **digital signal** is discrete and takes only binary values `0` and `1` (square pulses). (ii) Analog signals are easily distorted by noise, whereas digital signals are highly immune to noise.
**3.** (i) **Baseband transmission** sends a single digital signal without modulation using the entire bandwidth over short distances (e.g. Ethernet LAN). (ii) **Broadband transmission** modulates signals into analog waves across multiple frequency channels to send many signals simultaneously over long distances (e.g. cable TV, high-speed internet).
**4.** **Digital citizenship** is the responsible, ethical and safe use of the internet by a netizen. Good netizen habits: (i) using polite, civilised language in emails and comments; (ii) respecting others' privacy and citing the source of intellectual property.
**5.** **Digital wellbeing** is the state of physical, mental, social and emotional health achieved by balancing online screen time with offline life. Precautions: (i) setting daily time limits on screen and social-media use; (ii) turning off non-essential notifications during study and before sleep.
**6.** (i) **Digital wellbeing** is internally focused on protecting one's personal physical and mental health from screen overuse, whereas **digital reputation** is externally focused on the public perception of an individual or organisation online. (ii) Digital wellbeing is practised by limiting screen time, whereas digital reputation is managed by posting authentic, constructive content.
:::

**Group C — Long answer (4 marks each)**

1. Draw the block diagram of a digital communication system and state the function of the input transducer, encoder, modulator and demodulator. <span class="marks">[4]</span>
2. Write any four advantages of digital signal transmission over analog transmission. Why is high-speed internet considered a broadband transmission? <span class="marks">[4]</span>
3. Write any two positive and two negative impacts of digital technology in daily life. What health problems are seen in a child who uses a mobile phone excessively for years? <span class="marks">[4]</span>
4. If you have to shorten a 6-minute video clip into a 4-minute video clip, write in order the four main steps you follow in a video editor. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Draw the 9-block diagram: `Source → Input Transducer → Encoder → Modulator → Channel → Demodulator → Decoder → Output Transducer → Output Signal`. Functions: (i) **Input transducer** (e.g. microphone) converts the physical signal into an electrical signal; (ii) **Encoder** compresses the signal and converts it into binary digits (`0` and `1`); (iii) **Modulator** superimposes the digital data onto a high-frequency carrier wave for transmission through the channel; (iv) **Demodulator** separates the transmitted signal from the carrier wave at the receiver.
**2.** Advantages: (i) highly immune to channel noise and interference; (ii) signals can be regenerated by repeaters over long distances without loss of quality; (iii) error-detection and correction codes prevent data corruption; (iv) easy to encrypt and compress for security. High-speed internet is **broadband transmission** because it divides a high-capacity medium (fibre or coaxial cable) into multiple frequency channels to carry voice, video and large data streams simultaneously over long distances.
**3.** Positive impacts: (i) cashless digital payments (QR/mobile wallets) and online banking save time; (ii) digital libraries and online classes make study materials accessible anywhere. Negative impacts: (i) cybercrime, phishing and online harassment harm personal security; (ii) excessive screen time causes social isolation and physical inactivity. Health problems in the child: **poor eyesight (vision strain), insomnia (lack of sleep), obesity, and lack of concentration in study**.
**4.** To trim a 6-minute video to 4 minutes: (i) Launch **Video Editor**, click **New video project**, name the project, import the 6-minute video into the **Project library**, and drag it onto the **Storyboard / Editing panel**. (ii) Select the video clip and click **Trim**. (iii) Play the video and drag the **start and end blue bars** so that 2 minutes of unwanted footage are excluded and the selected clip length is **4 minutes**, then click **Done**. (iv) Click **Finish video**, select **Export**, and save the 4-minute `.MP4` video file to the computer.
:::

