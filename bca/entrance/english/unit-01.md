---
subject: English
grade: BCA
unit: 1
title: Synonyms, Antonyms and One-Word Substitution
hours: 6
area: Vocabulary
---

Vocabulary is worth about 6 of the 40 English marks and is the part that cannot be crammed in a week. The Dean's Office model sets one-word substitutions ("that which cannot be divided" → *indivisible*), synonyms, and meanings of phrases. The method is the same for all of them: learn word families, not isolated words, and use prefixes and roots to guess unknown words.

::: key What the paper asks from this chapter
- **Synonyms and antonyms** of common academic words (abundant, benevolent, candid, frugal).
- **One word for a group of words** (bilingual, philanthropist, regicide, pedestrian, indivisible).
- **Confusable words**: affect/effect, accept/except, principal/principle.
:::

## 1.1 Synonyms and antonyms

| Word | Synonym | Antonym |
|---|---|---|
| abundant | plentiful, ample | scarce, meagre |
| ancient | old, antique | modern |
| benevolent | kind, charitable | malevolent, cruel |
| brave | courageous, bold | timid, cowardly |
| candid | frank, honest | secretive, evasive |
| conceal | hide | reveal, expose |
| diligent | hardworking | lazy, idle |
| expand | grow, enlarge | contract, shrink |
| fragile | delicate, brittle | sturdy |
| frugal | thrifty | extravagant, wasteful |
| generous | liberal | stingy, miserly |
| lucid | clear | obscure, vague |
| permanent | lasting | temporary |
| rapid | swift, quick | slow |
| transparent | clear | opaque |
| verbose | wordy | concise, terse |
| ephemeral | short-lived | eternal, lasting |
| commence | begin, start | conclude, finish |

::: tip Prefix clues
*un-, in-, im-, dis-, non-* usually reverse meaning (indivisible, disagree). *mal-/mis-* means bad (malevolent), *bene-* means good (benevolent), *-cide* means killing (regicide, suicide), *-phobia* means fear.
:::

```photogrid label="1.1" cols="2" ratio="1.25" caption="Two people who made English vocabulary easier to organise. (a) Samuel Johnson (1709-1784), painted by Joshua Reynolds, whose Dictionary of the English Language (1755) was the first great dictionary of English. (b) Peter Mark Roget (1779-1869), a doctor who published his Thesaurus in 1852, a book that groups words by meaning, so that you find synonyms and antonyms side by side (Fig 1.1)."
@ photo id="bcaeng/johnson" cap="Samuel Johnson: the Dictionary, 1755"
focus 0.5 0.3
@ photo id="bcaeng/roget" cap="Roget: the Thesaurus, 1852"
focus 0.5 0.3
```

```svgfig label="1.1" caption="Words sit on a scale, not in a box. Each line puts synonyms and antonyms of one idea on a scale from less to more. On the quantity scale scarce and meagre are antonyms of ample, plentiful and abundant; on the attitude scale cruel and malevolent are the opposite of charitable and benevolent; on the clarity scale obscure and vague are the opposite of clear and lucid. Words in the same colour group are synonyms, but the stronger word is further along the scale (abundant is more than ample). Learn the direction of the word, then the shade."
f = Fig(780, 330)
scales = [("Quantity", "less", "more", [("scarce", .08), ("meagre", .24), ("ample", .62), ("plentiful", .78), ("abundant", .93)], .42),
          ("Attitude", "unkind", "kind", [("cruel", .08), ("malevolent", .27), ("charitable", .68), ("benevolent", .90)], .47),
          ("Clarity", "unclear", "clear", [("obscure", .09), ("vague", .30), ("clear", .66), ("lucid", .88)], .48)]
assert sum(len(s[3]) for s in scales) == 13
for i, (nm, lo, hi, ws, cut) in enumerate(scales):
    y = 70 + i * 100
    f.text(20, y - 30, nm, size=12, color=NAVY, anchor="start", bold=True)
    f.arrow([(60, y + 26), (730, y + 26)], color=SLATE, sw=1.6, both=True)
    f.text(60, y + 44, lo, size=10.5, color=RED, anchor="start", bold=True); f.text(730, y + 44, hi, size=10.5, color=TEAL, anchor="end", bold=True)
    for w, p in ws:
        x = 60 + p * 670; wd = len(w) * 7.2 + 20; neg = p < cut
        f.box(x - wd / 2, y - 12, wd, 28, w, fill=(ROSE if neg else MINT), stroke=(RED if neg else TEAL), color=(RED if neg else TEAL), size=11, bold=True)
        f.line(x, y + 16, x, y + 26, color=SLATE, sw=1.2)
```

## 1.2 One word for a group of words

| Group of words | One word |
|---|---|
| that which cannot be divided | indivisible |
| that which cannot be erased | indelible |
| that which cannot be dissolved | insoluble |
| a person who speaks two languages | bilingual |
| a person who loves mankind | philanthropist |
| a person who hates mankind | misanthrope |
| a person who does not believe in God | atheist |
| a person who walks on foot | pedestrian |
| a person new to a profession | novice |
| a government by the people | democracy |
| killing of a king | regicide |
| killing of oneself | suicide |
| a place where birds are kept | aviary |
| a place where bees are kept | apiary |
| life story written by oneself / by another | autobiography / biography |
| a doctor who treats children | paediatrician |
| fear of heights / closed spaces | acrophobia / claustrophobia |

```photogrid label="1.2" cols="2" ratio="1.3" caption="Two real places for two one-word substitutions. (a) An apiary is a place where bees are kept: this is a bee house on a bee trail in Germany. (b) An aviary is a place where birds are kept, here a glass aviary in a garden. The prefixes api- (bee) and avi- (bird) with the ending -ary (a place) build both words (Fig 1.2)."
@ photo id="bcaeng/apiary" cap="Apiary: a place for bees"
focus 0.5 0.6
@ photo id="bcaeng/aviary" cap="Aviary: a place for birds"
focus 0.5 0.5
```

```svgfig label="1.2" caption="One-word substitutions are built from parts, and the cell joins each pair of parts and checks the result: bi + lingual, phil + anthropist, mis + anthrope, a + theist, regi + cide, sui + cide, api + ary, avi + ary, in + divisible. Once you know that -cide means killing and -ary means a place for something, a word you have never met (like sororicide, the killing of a sister) can be guessed."
rows = [("bi", "lingual", "bilingual", "two + language"), ("phil", "anthropist", "philanthropist", "love + human being"), ("mis", "anthrope", "misanthrope", "hate + human being"),
        ("a", "theist", "atheist", "without + god"), ("regi", "cide", "regicide", "king + killing"), ("sui", "cide", "suicide", "self + killing"),
        ("api", "ary", "apiary", "bee + place for"), ("avi", "ary", "aviary", "bird + place for"), ("in", "divisible", "indivisible", "not + able to be divided")]
assert all(a + b == c for a, b, c, d in rows) and len(rows) == 9
f = Fig(780, 330)
for i, (a, b, c, d) in enumerate(rows):
    y = 14 + i * 34
    f.box(20, y, 80, 26, a, fill=SAND, stroke=AMBER, color=AMBER, size=11, bold=True)
    f.text(112, y + 18, "+", size=13, color=SLATE, bold=True)
    f.box(126, y, 130, 26, b, fill=BLUE, stroke=NAVY, color=NAVY, size=11, bold=True)
    f.text(272, y + 18, "=", size=13, color=SLATE, bold=True)
    f.box(290, y, 150, 26, c, fill=MINT, stroke=TEAL, color=TEAL, size=11, bold=True)
    f.text(456, y + 18, d, size=10.5, color=SLATE, anchor="start")
f.text(690, 40, "prefix", size=10.5, color=AMBER, bold=True); f.text(690, 60, "root / ending", size=10.5, color=NAVY, bold=True); f.text(690, 80, "whole word", size=10.5, color=TEAL, bold=True)
```

## 1.3 Words often confused

| Pair | Meaning and use |
|---|---|
| affect / effect | *affect* (verb) = influence; *effect* (noun) = result |
| accept / except | accept = receive; except = apart from |
| principal / principle | principal = head, main; principle = rule |
| stationary / stationery | not moving / writing material |
| advice / advise | noun / verb |
| lose / loose | misplace / not tight |
| complement / compliment | completes / praise |

```svgfig label="1.3" caption="Four confusable pairs with a memory hook for each. Affect is the action (verb) and effect is the end result (noun); principal means head or main and principle means rule (both principle and rule end in -le); stationary means standing still, while stationery is writing material (paper and envelope have an e); advice is the noun and advise is the verb. Use the hook in the exam, not the rule from memory."
f = Fig(780, 330)
cards = [("affect / effect", ["affect (verb): floods affect farmers", "effect (noun): the effect of the flood", "A = Action, E = End result"]),
         ("principal / principle", ["principal: head or main (the college principal)", "principle: a rule (a principle of honesty)", "principle and rule both end in -le"]),
         ("stationary / stationery", ["stationary: not moving (a stationary bus)", "stationery: paper, pens, envelopes", "stationEry = paper, envElope"]),
         ("advice / advise", ["advice (noun): give good advice", "advise (verb): I advise you to study", "c as in ice = noun; s = verb"])]
for i, (t, ls) in enumerate(cards):
    x = 14 + (i % 2) * 390; y = 14 + (i // 2) * 160
    f.box(x, y, 372, 146, "", fill=SOFT, stroke="#cbd5e1", r=4)
    f.text(x + 186, y + 26, t, size=13, color=NAVY, bold=True)
    for j, s in enumerate(ls):
        f.text(x + 14, y + 62 + j * 28, s, size=11, color=(RED if j == 2 else SLATE), anchor="start", bold=(j == 2))
```

## 1.4 Eight traps in vocabulary

Vocabulary marks are lost to small shades of meaning. These eight traps explain most of the wrong options in the model paper.

1. **Choose the shade, not just the topic.** *Frugal* and *stingy* both describe a person who spends little, but *frugal* is praise and *stingy* is blame (Fig 1.1). If the sentence is positive, choose the positive word. Ask whether the word shows approval or disapproval before you look at the options.
2. **Not every word with *in-* is a negative.** *Indivisible* means not able to be divided, but *invaluable* means extremely valuable, not worthless. *Inflammable* means it burns easily, the same as *flammable*. Check the root before you trust the prefix.
3. **Learn the strong endings.** *-cide* means killing (regicide, suicide), *-phobia* means fear (acrophobia), *-ary* means a place for something (apiary, aviary), and *-ology* means study of. These endings let you build one-word substitutions you have never seen (Fig 1.2).
4. **Do not mix the two "man" words.** A *philanthropist* loves mankind and gives to people in need, while a *misanthrope* hates mankind. *Phil-* means love and *mis-* means hate. Bilingual (two languages) is different from monolingual (one) and polyglot (many).
5. **Apiary is bees, aviary is birds.** The two words differ by one letter, so students swap them under time pressure. Remember *api* from *apiculture* (bee keeping) and *avi* from *aviation* (flight, as birds fly). Do the same with *autobiography* (written by oneself) and *biography* (by another).
6. **Affect is the verb, effect is the noun.** "Load-shedding can *affect* a student" uses a verb; "the *effect* of load-shedding" uses a noun (Fig 1.3). The exception, *effect* as a verb meaning to bring about, is rare in this paper. Use the hook: A for Action, E for End result.
7. **Principal and principle sound the same.** The *principal* of a campus is a person or the main thing; a *principle* is a rule. If you can replace the word with *rule*, use *principle*. The same two-letter habit separates *stationary* (still) from *stationery* (paper).
8. **Use the sentence, not the single word.** Many words have two meanings, so *close*, *bank* and *fine* change with the sentence. In an antonym question read the whole sentence and replace the word with each option. The one that changes the meaning to its opposite is correct.

### 1.4.1 Worked checks

**Q. Give one word for "the killing of a king".**

**Answer.** *Regi-* means king and *-cide* means killing, so the word is **regicide** (Fig 1.2). *Suicide* is killing of oneself.

**Q. Choose the antonym of *benevolent*.**

**Answer.** *Benevolent* means kind and wishing good (bene = good). Its opposite is **malevolent** (mal = bad), and *cruel* is also an antonym (Fig 1.1).

**Q. Fill in the blank: "The new rule will not ____ the exam date." (affect / effect)**

**Answer.** A verb is needed, so use **affect** (to influence): "The new rule will not affect the exam date." *Effect* would be a noun, as in "the effect of the rule".

**Q. Name a place where bees are kept and a place where birds are kept.**

**Answer.** A place for bees is an **apiary** (api- = bee) and a place for birds is an **aviary** (avi- = bird), both with the ending *-ary* for a place (Fig 1.2).

## Formula and fact sheet

| Prefix / suffix | Meaning | Example |
|---|---|---|
| bene- / mal- | good / bad | benevolent / malevolent |
| -cide | killing | regicide |
| -phobia | fear | acrophobia |
| in-, un- | not | indelible, unkind |
| bi- | two | bilingual |

## Chapter summary

- Learn words in pairs (word, opposite) rather than singly.
- Use prefixes and roots to decode unfamiliar words.
- One-word substitutions are tested from a limited list; learn the table above.
- Affect is usually a verb; effect is usually a noun.
- Principal (person, main), principle (rule).

## Practice questions

**Set A — Recall (20 questions)**

1. The synonym of "abundant" is
   (a) scarce (b) tiny (c) weak (d) plentiful
2. The antonym of "generous" is
   (a) kind (b) stingy (c) rich (d) noble
3. The synonym of "brave" is
   (a) courageous (b) timid (c) lazy (d) rude
4. The antonym of "ancient" is
   (a) old (b) antique (c) modern (d) historic
5. The synonym of "rapid" is
   (a) swift (b) slow (c) steady (d) heavy
6. One word for "a person who can speak two languages":
   (a) linguist (b) polyglot (c) interpreter (d) bilingual
7. One word for "that which cannot be divided":
   (a) indelible (b) insoluble (c) indivisible (d) indefensible
8. The antonym of "victory" is
   (a) triumph (b) defeat (c) success (d) win
9. One word for "a person who loves mankind":
   (a) misanthrope (b) pessimist (c) optimist (d) philanthropist
10. The synonym of "huge" is
    (a) enormous (b) tiny (c) narrow (d) modest
11. The antonym of "expand" is
    (a) grow (b) stretch (c) contract (d) swell
12. One word for "a person who walks on foot":
    (a) passenger (b) pedestrian (c) traveller (d) cyclist
13. The synonym of "begin" is
    (a) commence (b) conclude (c) finish (d) cease
14. One word for "government by the people":
    (a) autocracy (b) aristocracy (c) democracy (d) bureaucracy
15. The antonym of "transparent" is
    (a) clear (b) thin (c) bright (d) opaque
16. The synonym of "conceal" is
    (a) reveal (b) hide (c) show (d) expose
17. One word for "a person who does not believe in God":
    (a) theist (b) pagan (c) atheist (d) agnostic
18. The synonym of "fragile" is
    (a) delicate (b) sturdy (c) solid (d) firm
19. The antonym of "optimistic" is
    (a) hopeful (b) pessimistic (c) cheerful (d) confident
20. One word for "a place where birds are kept":
    (a) kennel (b) stable (c) apiary (d) aviary

::: note Answers and explanations — Set A
**1.** (d) — abundant means more than enough.
**2.** (b) — stingy is the opposite of generous.
**3.** (a) — courageous means brave.
**4.** (c) — modern is the opposite of ancient.
**5.** (a) — swift means fast.
**6.** (d) — bilingual (two); a polyglot speaks many.
**7.** (c) — indivisible; indelible means cannot be erased.
**8.** (b) — defeat is the opposite of victory.
**9.** (d) — philanthropist; a misanthrope hates people.
**10.** (a) — enormous means very big.
**11.** (c) — contract means to shrink.
**12.** (b) — pedestrian.
**13.** (a) — commence means start.
**14.** (c) — democracy; autocracy is rule by one.
**15.** (d) — opaque lets no light through.
**16.** (b) — conceal means hide.
**17.** (c) — atheist; an agnostic is unsure.
**18.** (a) — delicate means easily broken.
**19.** (b) — pessimistic expects the worst.
**20.** (d) — aviary; an apiary is for bees.
:::

**Set B — Understanding (12 questions)**

1. The synonym of "benevolent" is
   (a) cruel (b) greedy (c) kind (d) lazy
2. The antonym of "diligent" is
   (a) lazy (b) careful (c) hardworking (d) quick
3. The synonym of "candid" is
   (a) secretive (b) rude (c) shy (d) frank
4. The antonym of "scarce" is
   (a) rare (b) plentiful (c) little (d) limited
5. One word for "a doctor who treats children":
   (a) physician (b) surgeon (c) paediatrician (d) cardiologist
6. One word for "the life story of a person written by another":
   (a) biography (b) autobiography (c) diary (d) memoir
7. The synonym of "meagre" is
   (a) rich (b) ample (c) plentiful (d) scanty
8. One word for "the killing of a king":
   (a) homicide (b) regicide (c) suicide (d) genocide
9. The antonym of "permanent" is
   (a) temporary (b) lasting (c) eternal (d) fixed
10. Choose the correct word: "The new tax will ___ every family."
    (a) effect (b) afflict (c) affect (d) infect
11. Choose the correct word: "The medicine had a good ___ on him."
    (a) affect (b) affects (c) affected (d) effect
12. Choose the correct word: "Everyone ___ Ravi came to the class."
    (a) accept (b) except (c) expect (d) excerpt

::: note Answers and explanations — Set B
**1.** (c) — bene- means good; benevolent is kind.
**2.** (a) — diligent is hardworking, so lazy is opposite.
**3.** (d) — candid means frank.
**4.** (b) — scarce is in short supply; plentiful is the opposite.
**5.** (c) — paediatrician.
**6.** (a) — a biography is written by another; an autobiography by oneself.
**7.** (d) — meagre means small in amount, scanty.
**8.** (b) — regicide; -cide means killing.
**9.** (a) — temporary.
**10.** (c) — affect is the verb for influence.
**11.** (d) — effect, a noun, after "a good".
**12.** (b) — except means apart from.
:::

**Set C — Application (8 questions)**

1. The synonym of "verbose" is
   (a) brief (b) wordy (c) silent (d) rude
2. The antonym of "obscure" is
   (a) hidden (b) vague (c) dark (d) clear
3. One word for "fear of heights":
   (a) acrophobia (b) claustrophobia (c) hydrophobia (d) xenophobia
4. One word for "a person who is new to a profession":
   (a) expert (b) veteran (c) novice (d) master
5. The synonym of "ephemeral" is
   (a) eternal (b) lasting (c) solid (d) short-lived
6. The antonym of "frugal" is
   (a) extravagant (b) thrifty (c) careful (d) economical
7. Choose the correct word: "The ___ of the school is very strict."
   (a) principle (b) prince (c) principal (d) principally
8. The synonym of "lucid" is
   (a) confusing (b) clear (c) dull (d) heavy

::: note Answers and explanations — Set C
**1.** (b) — verbose means using too many words.
**2.** (d) — obscure means unclear; clear is the opposite.
**3.** (a) — acro- means high; claustrophobia is fear of closed spaces.
**4.** (c) — novice means beginner.
**5.** (d) — ephemeral lasts a very short time.
**6.** (a) — frugal means thrifty; extravagant is opposite.
**7.** (c) — principal is the head of a school.
**8.** (b) — lucid means clear.
:::
